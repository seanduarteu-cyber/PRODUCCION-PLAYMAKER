-- SQL 18B · base de FICHAS (jvgifibnoigpicwklasw) · SQL Editor → New query → pegar todo → Run
-- Error al guardar fichas grandes: «new row for relation "fichas_tallas" violates check constraint …».
-- La tabla fichas_tallas tenía topes de tamaño muy chicos: la ficha técnica (specs) y los montajes (imagenes) hasta
-- 4.000 caracteres y las prendas (items) hasta 2.000. Una ficha con muchos diseños (ej: COT-2608, 19 diseños con su
-- despiece y su montaje) los supera. Esto amplía los tres topes (se mantienen, pero holgados).
-- No borra ni cambia ninguna ficha. Se puede volver a correr sin problema.

begin;

alter table public.fichas_tallas drop constraint if exists chk_fic_specs;
alter table public.fichas_tallas add constraint chk_fic_specs check (char_length(specs::text) <= 200000);

alter table public.fichas_tallas drop constraint if exists chk_fic_imagenes;
alter table public.fichas_tallas add constraint chk_fic_imagenes check (char_length(imagenes::text) <= 200000);

alter table public.fichas_tallas drop constraint if exists chk_fic_items;
alter table public.fichas_tallas add constraint chk_fic_items check (char_length(items::text) <= 20000);

commit;

notify pgrst, 'reload schema';

-- Revisión: chk_fic_specs y chk_fic_imagenes deben decir 200000, y chk_fic_items 20000
select conname as regla, pg_get_constraintdef(oid) as detalle
  from pg_constraint
 where conrelid = 'public.fichas_tallas'::regclass and contype = 'c'
 order by conname;
