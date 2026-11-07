# Rainmeter + Google Keep

Muestra una nota o lista de Google Keep como widget en el escritorio de Windows, usando [Rainmeter](https://www.rainmeter.net/).

![Ejemplo: lista de Keep como widget](screenshot.png)

> Agrega tu propia captura como `screenshot.png`, o borra la línea de arriba.

## Cómo funciona

Rainmeter no puede hablar con Google directamente, así que el proyecto funciona en dos partes:

1. `keep_sync.py` se conecta a Keep, descarga la nota que elijas y la guarda como `nota.txt`. Las listas se escriben con ☐ (pendiente) y ☑ (hecho).
2. La skin `KeepNota.ini` lee `nota.txt` cada 30 segundos y lo dibuja en el escritorio.

Una tarea programada de Windows ejecuta el script cada pocos minutos, así el widget se mantiene al día solo.

El widget es **solo de lectura**: los cambios se hacen en Keep, y aparecen en el widget después de unos minutos.

## Aviso importante

- Keep no tiene API oficial para cuentas personales. Este proyecto usa [gkeepapi](https://github.com/kiwiz/gkeepapi), una librería **no oficial** que Google no respalda, y que podría dejar de funcionar si Google cambia algo.
- Se autentica con un **master token**, que da **acceso completo a tu cuenta de Google**. Trátalo como una contraseña: nunca lo subas a GitHub ni lo compartas. El `.gitignore` de este repo ya excluye `config.json`, pero revisa siempre antes de hacer un commit.
- Se probó en Windows. No hay garantía en otros sistemas.

## Requisitos

- Windows
- [Rainmeter](https://www.rainmeter.net/)
- [Python 3](https://www.python.org/downloads/) (marca "Add Python to PATH" al instalarlo)

## Instalación

### 1. Descargar el proyecto

Clónalo directamente en la carpeta de skins de Rainmeter:

```
git clone https://github.com/TU_USUARIO/rainmeter-google-keep "%USERPROFILE%\Documents\Rainmeter\Skins\KeepNota"
```

También puedes descargar el ZIP y descomprimirlo en `Documentos\Rainmeter\Skins\KeepNota`. La estructura debe quedar así:

```
Skins\KeepNota\
├── KeepNota.ini
└── @Resources\
    ├── keep_sync.py
    ├── get_token.py
    ├── run_sync.vbs
    └── config.example.json
```

### 2. Instalar las dependencias

```
pip install -r requirements.txt
```

### 3. Obtener el master token (una sola vez)

La cookie dura poco y sirve una sola vez, así que prepara todo antes.

1. Abre el CMD dentro de la carpeta `@Resources` (en el Explorador, escribe `cmd` en la barra de direcciones y presiona Enter).
2. Escribe `python get_token.py`, pero **no presiones Enter todavía**.
3. En el navegador (mejor en ventana de incógnito) entra a `https://accounts.google.com/EmbeddedSetup`, inicia sesión y acepta. La página se queda cargando: es normal.
4. Presiona F12, ve a *Application* → *Cookies* → `accounts.google.com` y copia el valor de la cookie `oauth_token` (empieza con `oauth2_4/`).
5. Vuelve al CMD, presiona Enter, escribe tu correo y pega la cookie cuando la pida.
6. Si funciona, imprime un texto largo que empieza con `aas_et/`. Ese es tu master token.

### 4. Configurar

En `@Resources`, copia `config.example.json` como `config.json` y rellénalo:

```json
{
  "email": "tu_correo@gmail.com",
  "master_token": "aas_et/...",
  "note_title": "Título exacto de tu nota en Keep",
  "show_checked": true
}
```

- `note_title` es el título que aparece arriba de la nota en Keep (no el link). No distingue mayúsculas, pero el resto debe coincidir. La nota **debe tener título**.
- `show_checked`: `false` oculta los ítems ya completados.

### 5. Probar el script

```
python keep_sync.py
```

Deberían aparecer `nota.txt` y `sync.log` en `@Resources`. Si algo falla, el motivo queda escrito en `sync.log` (si no encuentra la nota, ahí aparece la lista de títulos que sí vio).

### 6. Cargar la skin

Clic derecho en el ícono de Rainmeter → *Refresh all* → *Skins* → `KeepNota` → `KeepNota.ini`.

Título, tamaño y colores se cambian en la sección `[Variables]` de `KeepNota.ini`.

### 7. Actualización automática

Crea una tarea programada que ejecute el lanzador `run_sync.vbs` (corre sin abrir ventanas). Cambia `TU_USUARIO` por tu usuario de Windows:

```
schtasks /create /tn "KeepRainmeter" /sc minute /mo 2 /f /tr "wscript.exe C:\Users\TU_USUARIO\Documents\Rainmeter\Skins\KeepNota\@Resources\run_sync.vbs"
```

Si usas un notebook, Windows puede no ejecutar la tarea a batería. Para permitirlo:

```
powershell -Command "Set-ScheduledTask -TaskName 'KeepRainmeter' -Settings (New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries)"
```

Para comprobar que funciona, mira `sync.log`: debería agregar una línea nueva cada 2 minutos.

Para pausarla o reactivarla:

```
schtasks /change /tn "KeepRainmeter" /disable
schtasks /change /tn "KeepRainmeter" /enable
```

## Dejar el widget pegado al escritorio

Clic derecho sobre el widget → *Posición* → **En el escritorio** (*On desktop*) para que quede detrás de las ventanas. Para traerlo al frente, elige **Más arriba** (*Topmost*).

## Solución de problemas

| Problema | Qué revisar |
|---|---|
| `python` no se reconoce | Reinstala Python marcando "Add Python to PATH" |
| `sync.log` dice que no encontró la nota | El título en `config.json` debe ser igual al de Keep; el log lista los títulos que vio |
| No se actualiza solo | Revisa `schtasks /query /tn "KeepRainmeter" /v /fo list`: `Last Result` debe ser `0`, y `Task To Run` no debe tener `TU_USUARIO` |
| Error al obtener el token | La cookie caduca rápido: saca una nueva y ejecuta `get_token.py` enseguida |
| El cambio tarda en verse | Keep tarda en subir los cambios a Google; con el intervalo de 2 minutos suele verse en unos 5 minutos |

## Si filtras tu master token por error

Si subiste `config.json` a GitHub, asume que el token quedó expuesto: cambia la contraseña de tu cuenta de Google, genera uno nuevo y elimina el commit del historial del repositorio.

## Licencia

MIT. Ver [LICENSE](LICENSE).
