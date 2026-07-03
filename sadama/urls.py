from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.decorators import login_not_required
from django.contrib.auth.views import LoginView, LogoutView

from apps.users.views import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='dashboard'),
    path('login/', login_not_required(LoginView.as_view()), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('productos/', include('apps.products.urls')),
    path('usuarios/', include('apps.users.urls')),
    path('ventas/', include('apps.sales.urls')),
    path('reportes/', include('apps.reports.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
