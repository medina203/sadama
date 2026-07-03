from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory

from apps.products.models import Product

from .models import Sale, SaleItem


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ["client_name", "seller", "payment_method"]
        widgets = {
            "client_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej: Turista"}),
            "seller": forms.Select(attrs={"class": "form-select"}),
            "payment_method": forms.Select(attrs={"class": "form-select"}),
        }


class SaleItemForm(forms.ModelForm):
    class Meta:
        model = SaleItem
        fields = ["product", "quantity", "discount"]
        widgets = {
            "product": forms.Select(attrs={"class": "form-select"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "discount": forms.NumberInput(attrs={"class": "form-control", "min": 0, "step": "0.01", "placeholder": "$0"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["product"].queryset = Product.objects.filter(active=True)


class BaseSaleItemFormSet(forms.BaseInlineFormSet):
    def clean(self):
        if any(self.errors):
            return
        totals = {}
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get("DELETE", False):
                product = form.cleaned_data.get("product")
                quantity = form.cleaned_data.get("quantity")
                if product and quantity:
                    totals.setdefault(product.pk, {"product": product, "qty": 0})
                    totals[product.pk]["qty"] += quantity
        for pk, data in totals.items():
            if data["qty"] > data["product"].stock:
                raise ValidationError(
                    f"Stock insuficiente para '{data['product'].name}'. "
                    f"Disponible: {data['product'].stock}, solicitado total: {data['qty']}"
                )


SaleItemFormSet = inlineformset_factory(
    Sale, SaleItem, form=SaleItemForm, formset=BaseSaleItemFormSet, extra=2, can_delete=True
)
