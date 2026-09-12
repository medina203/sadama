-- Sadama - Estructura PostgreSQL en espanol
-- Regla: 4 primeras letras de tabla + _ + campo
-- Generado 2026-09-11 - compatible con Django 6.0.6 + psycopg 3.2

-- Tabla: usuario
-- db_table = usuario
CREATE TABLE "usuario" (
    "usua_id" bigserial PRIMARY KEY,
    "usua_usuario" varchar(150) NOT NULL UNIQUE,
    "usua_nombre" varchar(150) NOT NULL DEFAULT '''',
    "usua_apellido" varchar(150) NOT NULL DEFAULT '''',
    "usua_correo" varchar(254) NOT NULL DEFAULT '''',
    "usua_contrasena" varchar(128) NOT NULL,
    "usua_es_superusuario" boolean NOT NULL DEFAULT false,
    "usua_es_staff" boolean NOT NULL DEFAULT false,
    "usua_esta_activo" boolean NOT NULL DEFAULT true,
    "usua_ultimo_acceso" timestamptz NULL,
    "usua_fecha_ingreso" timestamptz NOT NULL DEFAULT now(),
    "usua_rol" varchar(10) NOT NULL CHECK ("usua_rol" IN (''admin'',''owner'',''seller'')),
    "usua_telefono" varchar(20) NOT NULL DEFAULT ''''
);
CREATE TABLE "usuario_groups" ("id" bigserial PRIMARY KEY, "user_id" bigint NOT NULL REFERENCES "usuario"("usua_id") DEFERRABLE INITIALLY DEFERRED, "group_id" integer NOT NULL REFERENCES "auth_group"("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE "usuario_user_permissions" ("id" bigserial PRIMARY KEY, "user_id" bigint NOT NULL REFERENCES "usuario"("usua_id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission"("id") DEFERRABLE INITIALLY DEFERRED);

-- Tabla: categoria 
CREATE TABLE "categoria" (
    "cate_id" bigserial PRIMARY KEY,
    "cate_nombre" varchar(100) NOT NULL UNIQUE,
    "cate_descripcion" text NOT NULL DEFAULT ''''
);

-- Tabla: producto 
CREATE TABLE "producto" (
    "prod_id" bigserial PRIMARY KEY,
    "prod_nombre" varchar(200) NOT NULL,
    "prod_descripcion" text NOT NULL DEFAULT '''',
    "prod_precio" numeric(10,2) NOT NULL CHECK ("prod_precio" >= 0),
    "prod_stock" integer NOT NULL CHECK ("prod_stock" >= 0) DEFAULT 0,
    "prod_imagen" varchar(100) NULL,
    "prod_qr" varchar(100) NOT NULL DEFAULT '''',
    "prod_activo" boolean NOT NULL DEFAULT true,
    "prod_creado" timestamptz NOT NULL DEFAULT now(),
    "prod_actualizado" timestamptz NOT NULL DEFAULT now(),
    "prod_categoria_id" bigint REFERENCES "categoria"("cate_id") ON DELETE SET NULL,
    "prod_propietario_id" bigint NOT NULL REFERENCES "usuario"("usua_id") ON DELETE CASCADE
);
CREATE INDEX "producto_prod_categoria_id_idx" ON "producto"("prod_categoria_id");
CREATE INDEX "producto_prod_propietario_id_idx" ON "producto"("prod_propietario_id");

-- Tabla: venta 
CREATE TABLE "venta" (
    "vent_id" bigserial PRIMARY KEY,
    "vent_fecha" timestamptz NOT NULL DEFAULT now(),
    "vent_total" numeric(12,2) NOT NULL DEFAULT 0 CHECK ("vent_total" >= 0),
    "vent_cliente" varchar(200) NOT NULL DEFAULT '''',
    "vent_metodo_pago" varchar(10) NOT NULL CHECK ("vent_metodo_pago" IN (''cash'',''card'',''transfer'')) DEFAULT ''cash'',
    "vent_anulada" boolean NOT NULL DEFAULT false,
    "vent_vendedor_id" bigint NOT NULL REFERENCES "usuario"("usua_id") ON DELETE PROTECT
);
CREATE INDEX "venta_vent_vendedor_id_idx" ON "venta"("vent_vendedor_id");
CREATE INDEX "venta_vent_fecha_idx" ON "venta"("vent_fecha");

-- Tabla: detalle_venta 
CREATE TABLE "detalle_venta" (
    "deta_id" bigserial PRIMARY KEY,
    "deta_venta_id" bigint NOT NULL REFERENCES "venta"("vent_id") ON DELETE CASCADE,
    "deta_producto_id" bigint NOT NULL REFERENCES "producto"("prod_id") ON DELETE PROTECT,
    "deta_cantidad" integer NOT NULL CHECK ("deta_cantidad" >= 1),
    "deta_precio_unitario" numeric(10,2) NOT NULL CHECK ("deta_precio_unitario" >= 0),
    "deta_descuento" numeric(10,2) NOT NULL DEFAULT 0 CHECK ("deta_descuento" >= 0),
    "deta_subtotal" numeric(12,2) NOT NULL CHECK ("deta_subtotal" >= 0)
);
CREATE INDEX "detalle_venta_deta_venta_id_idx" ON "detalle_venta"("deta_venta_id");
CREATE INDEX "detalle_venta_deta_producto_id_idx" ON "detalle_venta"("deta_producto_id");
