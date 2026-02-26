# Car Seller Agent - Setup Guide

¡Todo el código backend está listo! 🎉

Para que este agente funcione, necesitas conectar tu código con los servicios externos (Meta, Google, OpenAI). Sigue estos pasos:

## 1. Configurar Inteligencia Artificial (OpenAI)
1. Ve a [platform.openai.com](https://platform.openai.com/) y crea una cuenta.
2. Genera una **API Key**.
3. Abre el archivo `.env` en la carpeta `car_seller_agent` y pega tu clave en `OPENAI_API_KEY`.
4. Abre `services/ai.py` y edita el **SYSTEM_PROMPT** para poner la marca de tu auto, año, kilometraje, precio mínimo y fotos.

## 2. Configurar WhatsApp (Meta for Developers)
1. Ve a [developers.facebook.com](https://developers.facebook.com/) y crea una App tipo "Business".
2. Añade el producto **WhatsApp** a tu app.
3. Meta te dará un **Número de prueba** y un **Token de acceso temporal**.
4. Pega el Token en `WHATSAPP_TOKEN` y el ID del número en `PHONE_NUMBER_ID` dentro de tu archivo `.env`.

## 3. Configurar Webhooks con Railway (Hosting)
Para que Meta pueda enviarte los mensajes, el agente debe estar online 24/7. Lo subiremos a Railway conectándolo con tu repositorio de GitHub.

1. Entra a [Railway.app](https://railway.app/) e inicia sesión con GitHub.
2. Haz clic en **"New Project"** -> **"Deploy from GitHub repo"**.
3. Selecciona tu repositorio `AutomatizacionWSP`.
4. Railway detectará automáticamente el archivo `Procfile` y comenzará a construir (build) la aplicación.
5. **Variables de Entorno**: Ve a la pestaña "Variables" en tu proyecto de Railway y haz clic en "Raw Editor". Copia y pega allí todo el contenido de tu archivo `.env`. (O agrégalas una por una).
6. **Generar Dominio**: Ve a la pestaña "Settings" -> "Networking" y dale clic a **Generate Domain**. Railway te dará una URL pública gratuita (ej. `mi-agente-railway.app`).
7. **Conectar a Meta**: Ve a Meta Developers -> WhatsApp -> Configuración -> Webhooks.
8. En *URL de Callback*, pega tu URL de Railway y añádele `/webhook` (ej. `https://mi-agente-railway.app/webhook`).
9. En *Token de Verificación*, pon: `mi_token_secreto_personalizado`
10. Suscríbete a los eventos `messages`.

## 4. Google Sheets (Opcional por ahora)
Si quieres que guarde los leads:
1. Ve a Google Cloud Console, crea un proyecto y activa la "Google Sheets API".
2. Descarga el archivo JSON de la Service Account y guárdalo como `credentials.json` en la carpeta del proyecto.
3. Copia la URL de tu hoja de cálculo y ponla en `GOOGLE_SHEET_URL` en tu archivo `.env`.

## 5. ¡Pruébalo!
1. Envía un mensaje de WhatsApp al número de prueba de Meta.
2. Abre en tu navegador `http://localhost:8000/dashboard`.
3. ¡Revisa la sugerencia de la IA y haz clic en "✓ Send Reply"!
