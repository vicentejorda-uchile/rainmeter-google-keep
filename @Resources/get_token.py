"""
Obtiene el master token de tu cuenta de Google (se hace UNA sola vez).

Antes:
 1. Abre https://accounts.google.com/EmbeddedSetup (ojalá en ventana de incógnito)
 2. Inicia sesión y acepta ("I agree"). La página se queda cargando: es normal.
 3. F12 -> pestaña Application (Aplicación) -> Cookies -> accounts.google.com
 4. Copia el valor de la cookie 'oauth_token' (empieza con 'oauth2_4/...')
    Ojo: dura poco y sirve una sola vez; úsalo enseguida.

Requiere:  pip install gpsoauth
"""
import secrets

import gpsoauth

email = input("Email de Google: ").strip()
oauth_token = input("Valor de la cookie oauth_token: ").strip()
android_id = secrets.token_hex(8)  # cualquier ID de 16 caracteres hex sirve

res = gpsoauth.exchange_token(email, oauth_token, android_id)
print()
if "Token" in res:
    print("MASTER TOKEN (guárdalo en config.json, no lo compartas):")
    print(res["Token"])
else:
    print("No salió el token. Respuesta de Google:")
    print(res)
