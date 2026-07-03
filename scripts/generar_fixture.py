"""
Genera 3 fixtures separados por app con 6 meses de operaciones simuladas.
"""
import json, random, os
from datetime import datetime, timedelta

random.seed(42)

# ── Config ──────────────────────────────────────────────────
BASE = os.path.dirname(os.path.dirname(__file__))
OUTPUT_USERS    = os.path.join(BASE, "apps", "users",    "fixtures", "datos_usuarios.json")
OUTPUT_PRODUCTS = os.path.join(BASE, "apps", "products", "fixtures", "datos_productos.json")
OUTPUT_SALES    = os.path.join(BASE, "apps", "sales",    "fixtures", "datos_ventas.json")

# ── Datos base ──────────────────────────────────────────────

USERS = [
    {"pk": 1, "username": "admin",  "password": "pbkdf2_sha256$1200000$3UFeaca60sg3dszyvvgGqN$H747GNXPI6HvuaaO8dg1tdJmtXJaFfYBckAp/Yrvft4=", "plain": "admin123", "first": "Admin",   "last": "Principal", "email": "admin@sadama.com",     "role": "admin",  "phone": "555-0000"},
    {"pk": 2, "username": "carmen", "password": "pbkdf2_sha256$1200000$fufVRjwJFxtNlHaOa2X0WO$ABNG2KkBRhEV9hWNTRh5T6q4Mlykpel3ORp9RNMWf4Q=", "plain": "owner123","first": "Carmen",  "last": "López",     "email": "carmen@artesanias.com","role": "owner",  "phone": "555-0101"},
    {"pk": 3, "username": "luis",   "password": "pbkdf2_sha256$1200000$07pFLin9e61nk5BtzbsBru$Viswua+w96vGEBn3XiGWibUOzTsKtnNNYQoCtXl51M0=", "plain": "seller123","first": "Luis",    "last": "Martínez",  "email": "luis@artesanias.com",  "role": "seller", "phone": "555-0202"},
    {"pk": 4, "username": "maria",   "password": "pbkdf2_sha256$1200000$3UFeaca60sg3dszyvvgGqN$H747GNXPI6HvuaaO8dg1tdJmtXJaFfYBckAp/Yrvft4=", "plain": "admin123","first": "María",   "last": "García",    "email": "maria@artesanias.com", "role": "owner",  "phone": "555-0303"},
    {"pk": 5, "username": "ana",     "password": "pbkdf2_sha256$1200000$07pFLin9e61nk5BtzbsBru$Viswua+w96vGEBn3XiGWibUOzTsKtnNNYQoCtXl51M0=", "plain": "seller123","first": "Ana",     "last": "Ramírez",   "email": "ana@artesanias.com",   "role": "seller", "phone": "555-0404"},
    {"pk": 6, "username": "pepe",    "password": "pbkdf2_sha256$1200000$3UFeaca60sg3dszyvvgGqN$H747GNXPI6HvuaaO8dg1tdJmtXJaFfYBckAp/Yrvft4=", "plain": "admin123","first": "José",    "last": "Hernández", "email": "pepe@artesanias.com",   "role": "owner",  "phone": "555-0505"},
]

CATEGORIES = [
    {"pk": 1, "name": "Artesanías", "desc": "Artesanías tradicionales colombianas"},
    {"pk": 2, "name": "Textiles",   "desc": "Textiles y tejidos artesanales"},
    {"pk": 3, "name": "Cerámica",   "desc": "Cerámica y barro vidriado"},
    {"pk": 4, "name": "Joyería",    "desc": "Joyería artesanal"},
]

PRODUCTS = [
    # (pk, name, desc, price, stock_after_sales, owner_pk, cat_pk, freq_weight)
    # freq_weight: higher = sells more often
    # Prices in COP (Colombian Pesos) — multiplied ~230x from MXN estimates
    (1,  "Jarrón de barro",       "Jarrón decorativo pintado a mano con esmaltes naturales.",                    80500, 14, 2, 3, 8),
    (2,  "Tapete de lana",        "Tapete tejido en telar de cintura con lana teñida con tintes naturales.",     133400, 8,  2, 2, 4),
    (3,  "Máscara de madera",     "Máscara tallada en cedro con decoración tradicional del Cauca.",              96600, 10, 2, 1, 5),
    (4,  "Ruana artesanal",       "Ruana tejida a mano en telar de pedal con lana de ovejo.",                    172500, 6,  4, 2, 3),
    (5,  "Collar de chaquira",    "Collar con chaquira fina en diseño wayúu.",                                   64400, 18, 4, 4, 9),
    (6,  "Plato de barro",        "Plato decorativo de barro vidriado. Apto para uso ligero.",                   41400, 25, 2, 3, 10),
    (7,  "Mochila wayúu",         "Mochila tejida a mano por la comunidad wayúu con fibras naturales.",          50600, 14, 4, 2, 7),
    (8,  "Figura tallada",        "Figura tallada en tagua. Pieza coleccionable única.",                         204700, 4,  2, 1, 2),
    (9,  "Pulsera de plata",      "Pulsera artesanal de plata 950 con diseño de hojas.",                        276000, 7,  4, 4, 3),
    (10, "Cazuela de barro",      "Cazuela de barro natural para guisos tradicionales.",                         71300, 9,  2, 3, 6),
    (11, "Aretes de chaquira",    "Aretes artesanales de chaquira con diseños geométricos.",                     34500, 22, 4, 4, 9),
    (12, "Servilleta bordada",    "Servilleta de manta bordada a mano con hilos de colores.",                    29900, 20, 4, 2, 7),
    (13, "Taza de barro",         "Taza de barro vidriado, ideal para café o decoración.",                       21850, 30, 2, 3, 10),
    (14, "Alpargatas",            "Alpargatas artesanales de fique con suela de caucho reciclado.",              103500, 10, 6, 1, 4),
    (15, "Sombrero vueltiao",     "Sombrero vueltiao tejido en fibra de caña flecha.",                           73600, 12, 6, 1, 5),
    (16, "Bolso de cuero",        "Bolso artesanal de cuero curtido con hebilla de metal.",                      156400, 6,  6, 1, 3),
    (17, "Pulsera de semillas",   "Pulsera tejida con semillas naturales y mostacilla.",                         19550, 35, 4, 4, 8),
    (18, "Adorno navideño",       "Adorno artesanal de barro pintado. Temporada navideña.",                      27600, 15, 2, 3, 1),
    (19, "Báscula de madera",     "Báscula decorativa tallada en madera de pino.",                               57500, 12, 6, 1, 5),
    (20, "Cobija de lana",        "Cobija gruesa de lana de ovejo tejida en telar rústico.",                     98900, 8,  4, 2, 4),
    (21, "Tazón de barro",        "Tazón hondo de barro vidriado, ideal para servir.",                           25300, 28, 2, 3, 9),
    (22, "Espejo artesanal",      "Espejo con marco tallado en madera y pintura decorativa.",                    119600, 7,  6, 1, 3),
    (23, "Monedero de cuero",     "Monedero artesanal de cuero con cierre metálico.",                            21850, 30, 6, 1, 7),
    (24, "Camino de mesa",        "Camino de mesa tejido en algodón con flecos.",                                59800, 10, 4, 2, 4),
    (25, "Set de 6 tazas",        "Set de 6 tazas de barro vidriado con diseño tradicional.",                    80500, 8,  2, 3, 6),
    (26, "Collar de plata",       "Collar de plata 950 con dije de hoja de orquídea.",                           195500, 6,  4, 4, 3),
    (27, "Cesta de palma",        "Cesta tejida en palma de iraca con asa de cuero.",                            43700, 15, 6, 1, 6),
    (28, "Tapete pequeño",        "Tapete decorativo pequeño tejido en telar de cintura.",                       64400, 12, 2, 2, 5),
    (29, "Jarra de barro",        "Jarra de barro vidriado para agua o decoración.",                             52900, 15, 2, 3, 7),
    (30, "Llavero artesanal",     "Llavero de chaquira con diseños de animales.",                                10350, 50, 4, 4, 8),
    (31, "Cojín bordado",         "Cojín de manta con bordado tradicional de flores.",                           41400, 18, 4, 2, 6),
    (32, "Cenicero de barro",     "Cenicero decorativo de barro vidriado con esmalte verde.",                    18400, 25, 2, 3, 5),
]

# Clientes: algunos recurrentes, otros one-time
RECURRENTES = [
    ("Ana Torres",      10),   # (nombre, veces que compra)
    ("Roberto Díaz",    7),
    ("Sofía Ramírez",   8),
    ("Pedro Hernández", 5),
    ("Laura Mendoza",   9),
    ("Carlos Ruiz",     4),
    ("Mónica Vargas",   6),
    ("Jorge Castillo",  5),
    ("Guadalupe Rico",  6),
    ("Francisco Trejo", 4),
    ("Tania Aguilar",   5),
    ("Rafael Cuevas",   3),
]

ONE_TIME = [
    "Gabriela Luna", "Fernando Soto", "Diana Paredes", "Hugo Rivas",
    "Patricia Vega", "Alberto Campos", "Elena Nava", "Raúl Ortiz",
    "Silvia Delgado", "Ignacio Flores", "Rosa Mejía", "Daniel Ponce",
    "Verónica León", "Oscar Ávila", "Claudia Serra", "Marco Galván",
    "Liliana Ríos", "Felipe Cruz", "Adriana Mora", "Tomás Ibarra",
    "Brenda Ayala", "Saúl Cuevas", "Natalia Ferrer", "Emilio Rocha",
    "Ximena Peña", "Iván Duarte", "Regina Solís", "Alan Trejo",
    "Paulina Larios", "Esteban Correa", "Beatriz Nava", "Ramiro Pacheco",
    "Celia Rentería", "Vicente Zavala", "Yolanda Quintana", "Leonel Anguiano",
    "Maribel Tovar", "Salvador Cárdenas", "Jimena Arriaga", "Benjamín Orozco",
    "Lourdes Gazca", "Edgar Montero", "Alejandra Villa", "Rogelio Cuevas",
    "Teresa Lozano", "Humberto Padilla", "Renata Suárez", "Efraín Galindo",
    "Conchita Vela", "Adolfo Bautista", "Susana Olivera", "Mauro Pineda",
    "Gloria Escalante", "Noé Valenzuela", "Fabiola Cisneros", "Rigoberto Alcalá",
    "Miriam Pantoja", "Héctor Ceja", "Luz María Haro", "Abel Tapia",
    "Ruth Zúñiga", "Julián Espinoza", "Elisa Becerra", "Anselmo Partida",
    "Margarita Villalobos", "Neftalí Rangel", "Araceli Preciado", "Josafat Godínez",
    "Dulce Cepeda", "Ezequiel Escamilla", "Leticia Ballesteros", "Fidel Zaragoza",
    "Aurora Santillán", "Adán Villarreal", "Katia Alanís", "Celso Zúñiga",
    "Maricela Ledezma", "Teodoro Ruelas", "Rocío Ornelas", "Ambrosio Curiel",
    "Esmeralda Tostado", "Aarón Gaytán", "Hilda Manríquez", "Valente Carvajal",
    "Lorena Banderas", "César Godínez", "Paola Gaytán", "Dimas Pelayo",
    "Alma Delia Rea", "Uriel Cardona", "Nayeli Cornejo", "Eligio Alanís",
    "Ofelia Anguiano", "Lázaro Camarillo", "Yesenia Rosas", "Moisés Rendón",
    "Cristina Ledezma", "Ismael Maya", "Magdalena Rentería", "Timoteo Mena",
    "Soledad Córdova", "Arnulfo Pedroza", "July Valencia", "Feliciano Bretón",
    "Griselda Arce", "Arturo Cisneros", "Eva Manríquez", "Néstor Haro",
    "Cynthia Zamarripa", "Job Partida", "Erika Corral", "Isidro Orellana",
    "Lizbeth Godínez", "Damián Quintana", "Karen Curiel", "Eliseo Padilla",
    "Irene Santoyo", "Renato Viera", "Amalia Rivas", "Pablo Nájera",
    "Leonor Pastrana", "Tadeo Treviño", "Manuela Zamora", "Flavio Rascón",
    "Jimena Esquivel", "Adrián Villanueva", "Sara Godínez", "Reynaldo Bernal",
    "Angélica Ocampo", "Elías Noriega", "Martina Candelaria", "Homero Valdés",
    "Itzel Lomelí", "Lucio Márquez", "Pilar Casillas", "Gilberto Enríquez",
    "Lupita Alarcón", "Eduardo Razo", "Estela Noriega", "Salomón Maya",
    "Agustina Gaytán", "Josué Hernández", "Clara Manzo", "Iker Viera",
    "Minerva Esqueda", "Gael Cervantes", "Reyna Ortega", "Cristóbal Limón",
    "Coral Betancourt", "Bernardo Maya", "Azucena Samano", "Erick Pantoja",
    "Jazmín Zepeda", "Maximiliano Ríos",
]

# Vendedores
SELLERS = [1, 3, 5]  # admin, luis, ana

# ── Generación ──────────────────────────────────────────────

TODAY = datetime.now().replace(hour=19, minute=0, second=0, microsecond=0)
DAYS = 181
START = TODAY - timedelta(days=DAYS - 1)
START = START.replace(hour=9, minute=0)
END   = TODAY

# Build lookup maps
product_freq = {p[0]: p[7] for p in PRODUCTS}  # pk -> weight (index 7 = freq_weight)
product_data = {p[0]: p for p in PRODUCTS}

# Generate one-time customer visits
random.shuffle(ONE_TIME)
one_time_visits = []
for i, name in enumerate(ONE_TIME):
    # Spread across 6 months
    day_offset = int((i / len(ONE_TIME)) * DAYS) + random.randint(-15, 15)
    day_offset = max(0, min(DAYS-1, day_offset))
    visit_date = START + timedelta(days=day_offset)
    visit_date = visit_date.replace(hour=random.randint(9, 18), minute=random.randint(0, 59))
    one_time_visits.append((name, visit_date))

# Generate recurring customer visits
recurrent_visits = []
for name, times in RECURRENTES:
    # Spread their visits evenly across 6 months
    for i in range(times):
        day_offset = int((i / times) * DAYS) + random.randint(-10, 10)
        day_offset = max(0, min(DAYS-1, day_offset))
        visit_date = START + timedelta(days=day_offset)
        visit_date = visit_date.replace(hour=random.randint(9, 18), minute=random.randint(0, 59))
        recurrent_visits.append((name, visit_date))

all_visits = one_time_visits + recurrent_visits
all_visits.sort(key=lambda x: x[1])

# ── Build fixtures ──────────────────────────────────────────
fixture_users    = []
fixture_products = []
fixture_sales    = []

now_str = TODAY.isoformat()

# ── 1. Users ──
for u in USERS:
    fixture_users.append({
        "model": "users.user",
        "pk": u["pk"],
        "fields": {
            "password": u["password"],
            "last_login": now_str if u["role"] == "admin" else None,
            "is_superuser": u["role"] == "admin",
            "username": u["username"],
            "first_name": u["first"],
            "last_name": u["last"],
            "email": u["email"],
            "is_staff": u["role"] == "admin",
            "is_active": True,
            "date_joined": (TODAY - timedelta(days=200)).strftime("%Y-%m-%dT12:00:00Z"),
            "role": u["role"],
            "phone": u["phone"],
            "groups": [],
            "user_permissions": [],
        }
    })

# ── 2. Categories + Products ──
for c in CATEGORIES:
    fixture_products.append({
        "model": "products.category",
        "pk": c["pk"],
        "fields": {
            "name": c["name"],
            "description": c["desc"],
        }
    })

product_initial_stock = {}
for p in PRODUCTS:
    pk, name, desc, price, final_stock, owner, cat, _ = p
    product_initial_stock[pk] = final_stock
    fixture_products.append({
        "model": "products.product",
        "pk": pk,
        "fields": {
            "name": name,
            "description": desc,
            "price": f"{price:.2f}",
            "stock": final_stock,
            "image": "",
            "qr_code": "",
            "owner": owner,
            "category": cat,
            "active": True,
            "created_at": (TODAY - timedelta(days=200)).strftime("%Y-%m-%dT12:00:00Z"),
            "updated_at": TODAY.strftime("%Y-%m-%dT12:00:00Z"),
        }
    })

# Track stock deductions and sale total
# We'll track current stock to ensure we don't oversell
# Actually, we set final stock directly, so we don't deduct. But we need to
# know the stock at the time of each sale. Let's set initial stock higher
# and deduct as we generate sales.

# Set initial stock (before any sales)
initial_stock = product_data.copy()
# Compute how many units we need to have sold
total_sold = {}
for pk in product_data:
    total_sold[pk] = 0

# First pass: determine what sells in each visit
visit_items = []  # list of (name, datetime, [(prod_pk, qty, discount), ...])
for name, dt in all_visits:
    # How many products in this sale? (1-4 typically)
    num_items = random.choices([1, 2, 3, 4], weights=[30, 35, 25, 10])[0]
    # Pick products weighted by frequency
    candidates = list(product_data.keys())
    weights = [product_freq[pk] for pk in candidates]
    selected = random.choices(candidates, weights=weights, k=num_items)
    # Deduplicate but keep order
    seen = set()
    items = []
    for pk in selected:
        if pk not in seen:
            seen.add(pk)
            qty = random.choices([1, 2, 3], weights=[60, 30, 10])[0]
            discount = random.choices([0, 10, 20, 50], weights=[80, 10, 7, 3])[0]
            items.append((pk, qty, discount))
            total_sold[pk] = total_sold.get(pk, 0) + qty
    visit_items.append((name, dt, items))

# Set initial stock so that after all sales, we have final_stock
for p in PRODUCTS:
    pk = p[0]
    needed = total_sold[pk] + p[4]  # sold + final
    # Ensure at least some initial stock
    product_initial_stock[pk] = needed

# Second pass: create sales with stock at time of sale
# Track stock over time
current_stock = dict(product_initial_stock)
sale_pk = 0
item_pk = 0
sales_output = []

for name, dt, items in visit_items:
    sale_pk += 1
    seller = random.choice(SELLERS)
    payment = random.choices(["cash", "card", "transfer"], weights=[50, 35, 15])[0]
    cancelled = False  # No cancelled sales for demo
    
    items_out = []
    total = 0
    for prod_pk, qty, discount in items:
        # Check stock
        if current_stock[prod_pk] < qty:
            continue  # Skip if insufficient stock (should not happen with our setup)
        prod = product_data[prod_pk]
        unit_price = prod[3]
        subtotal = unit_price * qty - discount
        if subtotal < 0:
            subtotal = 0
        total += subtotal
        current_stock[prod_pk] -= qty
        
        item_pk += 1
        items_out.append({
            "model": "sales.saleitem",
            "pk": item_pk,
            "fields": {
                "sale": sale_pk,
                "product": prod_pk,
                "quantity": qty,
                "unit_price": f"{unit_price:.2f}",
                "discount": f"{discount:.2f}",
                "subtotal": f"{subtotal:.2f}",
            }
        })
    
    if not items_out:
        sale_pk -= 1
        continue  # Skip empty sales
    
    sales_output.append({
        "model": "sales.sale",
        "pk": sale_pk,
        "fields": {
            "date": dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "total": f"{total:.2f}",
            "client_name": name,
            "seller": seller,
            "payment_method": payment,
            "cancelled": cancelled,
        }
    })
    sales_output.extend(items_out)

# Fix product stock to final_stock
for entry in fixture_products:
    if entry["model"] == "products.product":
        pk = entry["pk"]
        for p in PRODUCTS:
            if p[0] == pk:
                entry["fields"]["stock"] = p[4]
                break

# ── Write ──────────────────────────────────────────────────
def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

write_json(OUTPUT_USERS,    fixture_users)
write_json(OUTPUT_PRODUCTS, fixture_products)
write_json(OUTPUT_SALES,    sales_output)

print(f"✓ Fixtures generados:")
print(f"  {OUTPUT_USERS}    ({len(fixture_users)} objetos)")
print(f"  {OUTPUT_PRODUCTS} ({len(fixture_products)} objetos)")
print(f"  {OUTPUT_SALES}    ({len(sales_output)} objetos)")
print()
print(f"  Usuarios: {len(USERS)}")
print(f"  Categorías: {len(CATEGORIES)}")
print(f"  Productos: {len(PRODUCTS)}")
print(f"  Ventas: {sale_pk}")
print(f"  Items de venta: {item_pk}")
print(f"  Clientes recurrentes: {len(RECURRENTES)}")
print(f"  Clientes one-time: {len(ONE_TIME)}")
print(f"  Total visitas: {len(all_visits)}")
