# DEPLOYMENT STATUS

**Fecha:** 2026-06-26
**Status:** Demo NO funciona end-to-end. Backend en Railway corre codigo viejo.

---

## El problema

El backend deployado en Railway (`rag-pdf-qa-demo-production.up.railway.app`) corre una version de codigo que:
- No tiene el fix completo de CORS
- No tiene auto-fallback a HuggingFace
- Devuelve 500 en `/ingest` por env vars incorrectas (`EMBEDDING_PROVIDER=openai` sin `OPENAI_API_KEY`)

**Causa raiz:** los pushes al repo no triggerean rebuilds en Railway (auto-deploy parece desactivado).

---

## Lo que SI funciona

- **Frontend (Vercel):** https://rag-pdf-qa-demo.vercel.app (UI completa, sin errores)
- **Backend (Railway) - endpoints parciales:**
  - `GET /` -> 200 OK
  - `GET /health` -> 200 OK
  - `OPTIONS /ingest` y `OPTIONS /query` (CORS preflight) -> 200 OK con headers correctos
  - `POST /query` -> 200 OK con citations (si hay datos)
- **CORS:** `access-control-allow-origin: https://rag-pdf-qa-demo.vercel.app` correcto
- **Supabase pgvector:** funcionando
- **Groq API key:** funcionando
- **HuggingFace embeddings:** configurado en codigo, auto-fallback si OpenAI falla

---

## Lo que NO funciona

- **POST /ingest** -> 500 Internal Server Error
- **Flujo end-to-end** (subir PDF -> pregunta -> respuesta) -> falla en el primer paso

---

## Accion 1 (rapida, 2 min): Forzar redeploy en Railway

1. https://railway.app/dashboard -> click en `rag-pdf-qa-demo`
2. Tab **Deployments** -> click en el ultimo deploy
3. Menu (3 puntos) -> **Redeploy**
4. Espera 3-5 min
5. Verifica: `curl https://rag-pdf-qa-demo-production.up.railway.app/`
   - Debe mostrar `"version": "0.3.0"` y `"env_check"` con los booleanos de las keys

---

## Accion 2 (si Railway no responde): Verificar env vars

1. **Railway -> tab Variables** del servicio `rag-pdf-qa-demo`
2. Verifica las 9 variables (ver `CREDENTIALS.md` local para los valores exactos)
3. Variables publicas: LLM_PROVIDER, LLM_MODEL, EMBEDDING_PROVIDER, EMBEDDING_MODEL, EMBEDDING_DIM, CORS_ORIGINS
4. Variables secretas: GROQ_API_KEY, SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY (valores en `CREDENTIALS.md`)
5. Si alguna esta mal, corrigela y haz Save
6. Railway redepleara automaticamente

---

## Accion 3 (plan B, 10 min): Deploy a Render con 1-click

Si Railway sigue sin responder, haz deploy del backend a **Render** usando `render.yaml`:

1. https://render.com -> Sign up con GitHub (gratis)
2. Click **"New +"** -> **"Blueprint"**
3. Conecta el repo `marcelovh10/rag-pdf-qa-demo`
4. Render detecta `render.yaml` automaticamente
5. Click **"Apply"** -> 5 min de build
6. Render te dara una URL tipo `https://rag-pdf-qa-api.onrender.com`
7. **Actualiza Vercel env var** `NEXT_PUBLIC_API_URL` = nueva URL
8. Redeploy Vercel

Las 3 variables secretas (GROQ_API_KEY, SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY) se deben agregar manualmente en el dashboard de Render.

---

## Verificacion final

Despues de aplicar cualquier accion, ejecuta desde PowerShell:

```powershell
cd D:\proyectos\monetizacion-online\rag-demo\backend
.\.venv\Scripts\python.exe test_e2e_real.py
```

**Esperado:** todas las pruebas en verde.

---

## Resumen ejecutivo

| Componente | Status | Accion |
|---|---|---|
| Frontend (Vercel) | OK | Ninguna |
| Backend (Railway) | Codigo viejo | Accion 1: redeploy manual |
| CORS | OK | Railway debe rebuildear |
| Supabase | OK | Ninguna |
| Plan B (Render) | Listo | Accion 3 si Railway no responde |
