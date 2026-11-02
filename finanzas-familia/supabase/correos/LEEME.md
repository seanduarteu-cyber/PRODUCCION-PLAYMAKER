# Correos en español con código

En Supabase › **Authentication › Emails › Templates**:

| Plantilla | Asunto (Subject) | Contenido (Message body) |
|---|---|---|
| **Confirm signup** | `Tu código para Finanzas Familia` | pega `confirmar-cuenta.html` |
| **Reset password** | `Recupera tu contraseña de Finanzas Familia` | pega `recuperar-contrasena.html` |

Guarda cada una con **Save changes**.

`{{ .Token }}` es el código de 6 dígitos que la persona escribe en la app. Así la confirmación
funciona aunque el correo se abra en otro dispositivo o un filtro de correo de empresa abra el
enlace antes que la persona.
