# Finanzas Familia

App para **registrar a diario los gastos, boletas, deudas y pagos en cuotas** de la familia, compartida entre los miembros (por ejemplo, tú y tu pareja) y con **descarga en Excel o PDF**. Funciona en **Android y iPhone** como aplicación instalable (PWA), sin pasar por las tiendas.

Cada familia es un **centro de costos separado y privado**: cualquier persona se registra con su propia cuenta, crea su familia e invita a los suyos. Nadie fuera de la familia puede ver sus datos, **ni siquiera quien administra la app** (ver [Privacidad](#privacidad)).

La lógica de cálculo replica la planilla `PRESUPUESTO_CASA` (hojas Presupuesto, Registro, Boletas y Deudas), y la app puede **importar esa planilla** para no partir de cero.

---

## Qué hace

| Pantalla | Para qué sirve |
|---|---|
| **Resumen** | Saldo proyectado a fin de mes, ya pagado, por pagar, saldo hoy, estado del mes (superávit / ajustado / déficit), distribución Esencial-Deudas-Prescindible-Ahorro contra metas, avance por categoría, ingresos del mes y alertas de boletas vencidas o cuotas pendientes. |
| **Gastos** | Registro diario: monto, categoría, descripción, fecha, medio de pago y foto de la boleta. Muestra quién registró cada gasto. Búsqueda y filtros por categoría o persona. **"Pagar en cuotas"** convierte una compra con tarjeta en un plan de cuotas futuras. |
| **Boletas** | Cuentas por pagar (luz, agua, gas, colegio…). Pagos parciales, boletas vencidas ("VENCIDA hace N días: pedir monto actualizado"), traspasadas (convenio / boleta nueva). Lo no pagado se arrastra a los meses siguientes. |
| **Cuotas** | Deudas, convenios, préstamos y compras en cuotas. Cuotas del mes con botón "Pagar", deuda restante, % del ingreso (alerta sobre 30%), prioridad por tasa (estrategia avalancha) y **proyección de 12 meses**. Admite cuotas variables por mes y cierre anticipado. |
| **Más** | Presupuesto por categoría, ingresos fijos, metas; familia y miembros (invitar, roles); **Excel y PDF** del mes, del año o de un rango; **importar planilla**; privacidad. |

Además: funciona **sin conexión** (se sincroniza al volver internet), **modo oscuro**, montos en pesos chilenos y botón "atrás" de Android.

---

## Privacidad

1. **Familias aisladas.** Las [reglas de Firestore](firestore.rules) solo permiten leer o escribir a los miembros de cada familia. No se pueden listar familias ni invitaciones. Las invitaciones son de **un solo uso** y vencen a los 7 días.
2. **Cifrado de extremo a extremo.** Al crear la familia se genera en el teléfono una **clave de la familia** (ej. `K7PD-3MXQ-9TRW-HZ2B-6NVC`). Con ella se cifra (AES-256-GCM) todo el contenido —montos, descripciones, categorías, presupuesto, boletas, deudas y fotos— **antes de subirlo**. La clave nunca llega al servidor: viaja en la invitación (en la parte `#` del enlace, que el navegador no envía) y queda guardada en cada teléfono.
3. **Qué ve el administrador del proyecto Firebase:** correos y nombres de las cuentas, nombre de cada familia, quién es miembro, y el mes y la fecha de creación de cada registro. **No** ve ningún monto ni descripción: solo texto cifrado.

> ⚠️ Guarda la clave de la familia (foto, nota o papel). Si se pierde en todos los teléfonos, los datos no se pueden recuperar. Los archivos Excel/PDF descargados no van cifrados.

---

## Probarla ya (modo demostración)

Sin configurar nada, la app funciona en **modo demostración**: los datos quedan solo en ese navegador.

```bash
cd finanzas-familia
npm install
npm run dev
```

Abre la dirección que aparece (ej. `http://localhost:5173`).

---

## Publicarla para tu familia (≈ 15 minutos, gratis)

Se usa **Firebase** (de Google), con el plan gratuito *Spark*, que alcanza de sobra para varias familias.

### 1. Crear el proyecto

1. Entra a <https://console.firebase.google.com> y crea un proyecto (ej. `finanzas-familia-dy`). Google Analytics no es necesario.
2. **Authentication** → *Comenzar* → en *Método de acceso* habilita **Correo electrónico/contraseña** y **Google**.
3. **Firestore Database** → *Crear base de datos* → edición **Standard**, ubicación **`southamerica-west1` (Santiago)** → modo **producción**.
4. **Configuración del proyecto** (engranaje) → *Tus apps* → ícono **Web `</>`** → registra la app (no hace falta marcar Hosting aquí) → copia los valores de `firebaseConfig`.

### 2. Configurar y publicar

```bash
cd finanzas-familia
cp .env.example .env.local
```

Pega en `.env.local` los valores copiados (`apiKey`, `authDomain`, `projectId`, etc.). Luego:

```bash
cp .firebaserc.example .firebaserc
```

Cambia `TU-ID-DE-PROYECTO` por el ID de tu proyecto, y publica:

```bash
npx -y firebase-tools@15 login
```

```bash
npm install
```

```bash
npm run deploy
```

`npm run deploy` compila la app y sube **la app (Hosting)**, **las reglas de seguridad** y **los índices**. Al terminar muestra la dirección, por ejemplo `https://finanzas-familia-dy.web.app`.

> Si cambias algo en la app, vuelve a ejecutar `npm run deploy`. Los teléfonos se actualizan solos.

### 3. Instalar en los teléfonos

- **Android (Chrome):** abre la dirección → menú ⋮ → **Instalar app** (o *Agregar a pantalla principal*).
- **iPhone (Safari):** abre la dirección → botón **Compartir** → **Agregar a inicio**.

Queda un ícono como cualquier app, abre a pantalla completa y funciona sin conexión.

### 4. Empezar a usarla

1. Crea tu cuenta → **Crear mi familia** (ej. "Casa DY") → **guarda la clave** que aparece.
2. *(Opcional)* **Más › Descargar Excel o PDF › Importar mi planilla**: sube `PRESUPUESTO_CASA_DY_2026-27.xlsx` y se cargan categorías, presupuesto, ingresos, gastos, boletas y la proyección de deudas.
3. Revisa **Más › Presupuesto** (montos por categoría e ingresos fijos).
4. **Más › Familia › Invitar a mi pareja** → *Enviar por WhatsApp*. Ella abre el enlace, crea su cuenta y entra directo a la misma familia. Ambos registran gastos y los ven al instante.

### 5. Compartirla con otras familias

Envíales la dirección de la app (ej. `https://finanzas-familia-dy.web.app`). Cada una crea su cuenta y **su propia familia**, con su propia clave. Sus datos quedan separados y cifrados: tú no puedes verlos.

---

## Excel y PDF

En **Más › Descargar Excel o PDF** eliges un mes, un año o un rango:

- **Excel (.xlsx)**: hoja *Presupuesto* (o *Resumen por mes* + una hoja por mes), *Registro*, *Ingresos*, *Boletas* y *Deudas* con la proyección de cuotas, con el mismo formato que la planilla.
- **PDF**: informe con resumen, categorías, distribución, ingresos, gastos, boletas por pagar y proyección de cuotas.

En el teléfono puedes **Descargar** o **Compartir** (WhatsApp, correo, Archivos/Drive).

---

## Para desarrolladores

```text
finanzas-familia/
├── src/
│   ├── lib/          cálculos (calc.ts), cifrado (crypto.ts), Excel/PDF, importador, formatos
│   ├── data/         backend Firebase / local (demo), acciones, estado (store.tsx)
│   ├── screens/      pantallas
│   └── components/   componentes de interfaz
├── tests/            pruebas (cálculos, cifrado, importador, reglas de Firestore)
├── firestore.rules   reglas de seguridad
└── firebase.json     Hosting + Firestore
```

| Comando | Qué hace |
|---|---|
| `npm run dev` | Servidor de desarrollo |
| `npm test` | Pruebas de cálculos (iguales a la planilla), cifrado e importación |
| `npm run test:reglas` | Pruebas de las reglas de seguridad en el emulador de Firestore (requiere Java) |
| `npm run emuladores` | Emuladores de Auth + Firestore. Compila con `VITE_FIREBASE_EMULADOR=1` para usarlos |
| `npm run build` | Compila la app en `dist/` |
| `npm run deploy` | Compila y publica en Firebase |

**Tecnología:** React 19 + TypeScript + Vite, PWA (vite-plugin-pwa), Firebase Auth + Firestore (con caché sin conexión), Web Crypto (AES-GCM + PBKDF2), ExcelJS, jsPDF.

### ¿Y en Play Store / App Store?

No es necesario, porque la PWA se instala desde el navegador. Si más adelante quieres publicarla en las tiendas, se puede empaquetar la misma app con [PWABuilder](https://www.pwabuilder.com) (Android) o [Capacitor](https://capacitorjs.com) (Android/iPhone; para iPhone se requiere una cuenta de Apple Developer).
