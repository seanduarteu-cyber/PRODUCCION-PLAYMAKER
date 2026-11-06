-- SQL 19B · base de FICHAS (jvgifibnoigpicwklasw) · SQL Editor → New query → pegar todo → Run
-- La E02 es sin mangas, así que su código termina en 03: RB-HOMUCC02 → RB-HOMUCC03
-- (la E01 sigue siendo RB-HOMUCC02: manga raglán con costados).
-- También pasa al código nuevo la E02 en las fichas que ya la tienen (ficha técnica y montajes), para que no pierdan su molde.
-- No cambia números ni otros moldes. Se puede volver a correr sin problema.

begin;

update public.moldes set codigo = 'RB-HOMUCC03', updated_at = now()
 where numero = 102 and codigo = 'RB-HOMUCC02';

update public.fichas_tallas
   set specs = replace(replace(specs::text, 'RB-HOMUCC02|102', 'RB-HOMUCC03|102'), 'E02 · RB-HOMUCC02', 'E02 · RB-HOMUCC03')::jsonb,
       imagenes = replace(imagenes::text, 'RB-HOMUCC02|102', 'RB-HOMUCC03|102')::jsonb
 where specs::text like '%RB-HOMUCC02|102%' or specs::text like '%E02 · RB-HOMUCC02%' or imagenes::text like '%RB-HOMUCC02|102%';

commit;

notify pgrst, 'reload schema';

-- Revisión: E01 = RB-HOMUCC02 (raglán) y E02 = RB-HOMUCC03 (sin mangas); y cuántas fichas quedan con la E02 antigua (debe ser 0)
select case when numero = 101 then 'E01' else 'E02' end as molde, codigo, descripcion,
       (select count(*) from public.fichas_tallas where specs::text like '%RB-HOMUCC02|102%' or imagenes::text like '%RB-HOMUCC02|102%') as fichas_con_e02_antigua,
       (select count(*) from public.fichas_tallas where specs::text like '%RB-HOMUCC03|102%') as fichas_con_e02
  from public.moldes where numero in (101, 102) order by numero;
