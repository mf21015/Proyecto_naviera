
CREATE TABLE public.auth_group (
  id integer GENERATED ALWAYS AS IDENTITY NOT NULL,
  name character varying NOT NULL UNIQUE,
  CONSTRAINT auth_group_pkey PRIMARY KEY (id)
);
CREATE TABLE public.auth_permission (
  id integer GENERATED ALWAYS AS IDENTITY NOT NULL,
  name character varying NOT NULL,
  content_type_id integer NOT NULL,
  codename character varying NOT NULL,
  CONSTRAINT auth_permission_pkey PRIMARY KEY (id)
);
CREATE TABLE public.auth_group_permissions (
  id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  group_id integer NOT NULL,
  permission_id integer NOT NULL,
  CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id)
);
CREATE TABLE public.django_content_type (
  id integer GENERATED ALWAYS AS IDENTITY NOT NULL,
  app_label character varying NOT NULL,
  model character varying NOT NULL,
  CONSTRAINT django_content_type_pkey PRIMARY KEY (id)
);
CREATE TABLE public.django_admin_log (
  id integer GENERATED ALWAYS AS IDENTITY NOT NULL,
  action_time timestamp with time zone NOT NULL,
  object_id text,
  object_repr character varying NOT NULL,
  action_flag smallint NOT NULL CHECK (action_flag >= 0),
  change_message text NOT NULL,
  content_type_id integer,
  user_id bigint NOT NULL,
  CONSTRAINT django_admin_log_pkey PRIMARY KEY (id)
);
CREATE TABLE public.django_migrations (
  id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  app character varying NOT NULL,
  name character varying NOT NULL,
  applied timestamp with time zone NOT NULL,
  CONSTRAINT django_migrations_pkey PRIMARY KEY (id)
);
CREATE TABLE public.django_session (
  session_key character varying NOT NULL,
  session_data text NOT NULL,
  expire_date timestamp with time zone NOT NULL,
  CONSTRAINT django_session_pkey PRIMARY KEY (session_key)
);
CREATE TABLE public.gestion_puerto (
  id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  nombre character varying NOT NULL,
  pais character varying NOT NULL,
  CONSTRAINT gestion_puerto_pkey PRIMARY KEY (id)
);
CREATE TABLE public.gestion_customuser (
  id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  password character varying NOT NULL,
  last_login timestamp with time zone,
  is_superuser boolean NOT NULL,
  username character varying NOT NULL UNIQUE,
  first_name character varying NOT NULL,
  last_name character varying NOT NULL,
  email character varying NOT NULL,
  is_staff boolean NOT NULL,
  is_active boolean NOT NULL,
  date_joined timestamp with time zone NOT NULL,
  rol character varying NOT NULL,
  puerto_id bigint,
  CONSTRAINT gestion_customuser_pkey PRIMARY KEY (id)
);
CREATE TABLE public.gestion_customuser_groups (
  id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  customuser_id bigint NOT NULL,
  group_id integer NOT NULL,
  CONSTRAINT gestion_customuser_groups_pkey PRIMARY KEY (id)
);
CREATE TABLE public.gestion_customuser_user_permissions (
  id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  customuser_id bigint NOT NULL,
  permission_id integer NOT NULL,
  CONSTRAINT gestion_customuser_user_permissions_pkey PRIMARY KEY (id)
);
CREATE TABLE public.gestion_ruta (
  id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  nombre character varying NOT NULL,
  CONSTRAINT gestion_ruta_pkey PRIMARY KEY (id)
);
CREATE TABLE public.gestion_rutapuerto (
  id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  orden integer NOT NULL,
  puerto_id bigint NOT NULL,
  ruta_id bigint NOT NULL,
  CONSTRAINT gestion_rutapuerto_pkey PRIMARY KEY (id)
);
CREATE TABLE public.gestion_importado (
  id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  numero_importador character varying NOT NULL,
  nombre_importador character varying NOT NULL,
  actividad_economica character varying,
  tipo_persona character varying,
  direccion_importador character varying,
  telefono_importador character varying,
  correo_importador character varying,
  fecha_registro date NOT NULL,
  usuario_id bigint,
  CONSTRAINT gestion_importado_pkey PRIMARY KEY (id)
);
CREATE TABLE public.gestion_embarque (
  id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  numero_contenedor character varying NOT NULL,
  descripcion_carga text,
  fecha_salida date NOT NULL,
  ubicacion_salida character varying,
  ubicacion_llegada character varying,
  monto_embarque numeric,
  buque_embarque character varying,
  peso_embarque numeric,
  usuario_id bigint NOT NULL,
  importador_id bigint NOT NULL,
  CONSTRAINT gestion_embarque_pkey PRIMARY KEY (id)
);
CREATE TABLE public.gestion_documento (
  id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  tipo character varying NOT NULL,
  descripcion text NOT NULL,
  fecha_emision timestamp with time zone NOT NULL,
  archivo_pdf character varying NOT NULL,
  ruta_puerto_id bigint NOT NULL,
  es_valido boolean,
  observacion text,
  creado_por_id bigint,
  embarque_id bigint,
  CONSTRAINT gestion_documento_pkey PRIMARY KEY (id)
);
CREATE TABLE public.gestion_seguimiento (
  id bigint GENERATED ALWAYS AS IDENTITY NOT NULL,
  fecha_seguimiento date NOT NULL,
  ubicacion_seguimiento character varying,
  status_seguimiento character varying,
  embarque_id bigint NOT NULL,
  usuario_id bigint NOT NULL,
  CONSTRAINT gestion_seguimiento_pkey PRIMARY KEY (id)
);


-- Foreign keys
ALTER TABLE auth_group_permissions ADD FOREIGN KEY (permission_id) REFERENCES auth_permission(id);
ALTER TABLE auth_group_permissions ADD FOREIGN KEY (group_id) REFERENCES auth_group(id);
ALTER TABLE auth_permission ADD FOREIGN KEY (content_type_id) REFERENCES django_content_type(id);
ALTER TABLE django_admin_log ADD FOREIGN KEY (content_type_id) REFERENCES django_content_type(id);
ALTER TABLE django_admin_log ADD FOREIGN KEY (user_id) REFERENCES gestion_customuser(id);
ALTER TABLE gestion_customuser ADD FOREIGN KEY (puerto_id) REFERENCES gestion_puerto(id);
ALTER TABLE gestion_customuser_groups ADD FOREIGN KEY (customuser_id) REFERENCES gestion_customuser(id);
ALTER TABLE gestion_customuser_groups ADD FOREIGN KEY (group_id) REFERENCES auth_group(id);
ALTER TABLE gestion_customuser_user_permissions ADD FOREIGN KEY (customuser_id) REFERENCES gestion_customuser(id);
ALTER TABLE gestion_customuser_user_permissions ADD FOREIGN KEY (permission_id) REFERENCES auth_permission(id);
ALTER TABLE gestion_rutapuerto ADD FOREIGN KEY (puerto_id) REFERENCES gestion_puerto(id);
ALTER TABLE gestion_rutapuerto ADD FOREIGN KEY (ruta_id) REFERENCES gestion_ruta(id);
ALTER TABLE gestion_importado ADD FOREIGN KEY (usuario_id) REFERENCES gestion_customuser(id);
ALTER TABLE gestion_embarque ADD FOREIGN KEY (usuario_id) REFERENCES gestion_customuser(id);
ALTER TABLE gestion_embarque ADD FOREIGN KEY (importador_id) REFERENCES gestion_importado(id);
ALTER TABLE gestion_documento ADD FOREIGN KEY (creado_por_id) REFERENCES gestion_customuser(id);
ALTER TABLE gestion_documento ADD FOREIGN KEY (embarque_id) REFERENCES gestion_embarque(id);
ALTER TABLE gestion_documento ADD FOREIGN KEY (ruta_puerto_id) REFERENCES gestion_rutapuerto(id);
ALTER TABLE gestion_seguimiento ADD FOREIGN KEY (embarque_id) REFERENCES gestion_embarque(id);
ALTER TABLE gestion_seguimiento ADD FOREIGN KEY (usuario_id) REFERENCES gestion_customuser(id);

