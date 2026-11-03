-- 16C · FICHAS (Supabase de Fichas) · El nombre de la persona puede ir vacío, pero sigue con tope de 80 caracteres
-- (la regla anterior, chk_det_nombre, exigía al menos 1 carácter y como máximo 80; se quitó en el 16B)
alter table public.fichas_detalle
  add constraint chk_det_nombre check (nombre is null or char_length(nombre) <= 80);
notify pgrst, 'reload schema';
select 'ok' as resultado;
