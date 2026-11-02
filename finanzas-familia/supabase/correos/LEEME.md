# Correo con el código para entrar

La app entra **sin contraseña**: la persona escribe su correo, recibe un código de 6 dígitos y lo
escribe en la app. Supabase usa dos plantillas para eso (cuenta nueva y cuenta existente), y las
dos llevan el mismo contenido.

En Supabase › **Authentication › Emails › Templates**, en **Confirm signup** y en **Magic Link**:

- **Subject:** `{{ .Token }} es tu código para Finanzas Familia`
- **Message body:** el contenido de [`codigo.html`](codigo.html)

Guarda cada una con **Save changes**.
