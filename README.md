# Copa Mundial 2027 — App con Python (Flask) + MongoDB Atlas

Aplicacion con las 17 pantallas que definiste, conectada a una base de datos
real en MongoDB Atlas, con un script que crea las colecciones y las llena con
toda la informacion del torneo (anfitriones, sedes, grupos, selecciones,
jugadores, partidos, etc.).

## Estructura de la carpeta

```
CopaMundial2027/
├── app/
│   ├── __init__.py         -> crea la app de Flask (app factory)
│   ├── config.py           -> lee las variables del .env
│   ├── database.py         -> conexion reutilizable a MongoDB Atlas
│   ├── routes/
│   │   ├── auth.py         -> pantallas 1, 2, 3 (login, registro, recuperar)
│   │   ├── main.py         -> pantalla 4 (inicio)
│   │   ├── content.py      -> pantallas 5-13 y 15
│   │   └── extras.py       -> pantallas 14, 16, 17 (quiz, ajustes, zona +18)
│   ├── templates/          -> un .html por cada una de las 17 pantallas
│   └── static/css/style.css -> estilo oscuro/azul igual al mockup
├── database/
│   ├── seed_data.py            -> TODOS los datos del torneo en Python
│   └── create_collections.py   -> script que crea y llena las colecciones en Atlas
├── requirements.txt
├── .env.example
├── run.py                  -> arranca el servidor
└── README.md
```

## Pasos para correrla en Visual Studio Code

### 1. Abre la carpeta en VS Code
`Archivo -> Abrir carpeta... -> CopaMundial2027`

### 2. Crea el entorno virtual
En la terminal integrada de VS Code (Terminal -> Nueva terminal):

```
python -m venv venv
```

Activalo:
- Windows: `venv\Scripts\activate`
- Mac/Linux: `source venv/bin/activate`

### 3. Instala las dependencias

```
pip install -r requirements.txt
```

### 4. Configura tu conexion a MongoDB Atlas
1. Entra a https://cloud.mongodb.com, crea un cluster gratuito (M0) si no
   tienes uno.
2. En **Network Access**, agrega tu IP (o "Allow access from anywhere" para
   pruebas).
3. En **Database Access**, crea un usuario con contraseña.
4. En tu cluster: **Connect -> Drivers -> Python**, copia la cadena de
   conexion (empieza con `mongodb+srv://...`).
5. En la carpeta del proyecto, copia `.env.example` y renombralo a `.env`.
6. Pega tu cadena en `MONGO_URI` dentro de `.env`.

### 5. Crea y llena las colecciones (esto es lo que pediste)
Con el entorno virtual activado, corre:

```
python database/create_collections.py
```

Esto se conecta a tu cluster de Atlas y crea automaticamente las colecciones:
`anfitriones, ciudades_sede, estadios, selecciones, grupos, jugadores,
partidos, historia_mundial, noticias, quiz_preguntas, datos_generales,
usuarios` — ya cargadas con la informacion del torneo. Puedes correrlo las
veces que quieras: siempre borra y vuelve a cargar los datos, sin duplicar.

Tambien puedes darle clic derecho al archivo en VS Code -> "Run Python File
in Terminal".

### 6. Arranca la aplicacion

```
python run.py
```

Abre tu navegador en **http://127.0.0.1:5000**

## Notas importantes

- **Contraseñas**: nunca se guardan en texto plano; se guardan con hash
  (`werkzeug.security`).
- **Zona +18**: pide verificar edad y, si iniciaste sesion, muestra tu
  Quiniela (predicciones + puntos + insignias). No tiene ninguna funcion de
  apuestas con dinero real, tal como pediste — solo puntos dentro de la app.
- **Quiniela**: la gente pronostica el marcador de los partidos (desde la
  pantalla de Partidos) y gana puntos e insignias cuando el partido termina.
  Reglas en `database/seed_data.py` (`PUNTOS_MARCADOR_EXACTO`,
  `PUNTOS_RESULTADO_CORRECTO`, `INSIGNIAS`).
- **Jugadores**: la coleccion trae 66 jugadores reales (al menos uno por
  cada una de las 48 selecciones, con extras en las selecciones mas
  populares), con nombre, seleccion, posicion, numero y edad. El campo
  `foto_url` viene vacio a proposito — no se insertan fotografias reales de
  personas por derechos de imagen. Mientras tanto la app dibuja un avatar
  con la inicial de cada jugador; si mas adelante subes fotos tuyas (a tu
  propio servidor, Cloudinary, etc.), solo pon la URL en `foto_url` dentro
  de `database/seed_data.py`, vuelve a correr `create_collections.py`, y la
  plantilla la mostrara automaticamente en vez del avatar.
- **Partidos**: el script carga una muestra inicial (6 partidos de ejemplo).
  La coleccion esta lista para que agregues el resto (hasta 104) editando
  `database/seed_data.py` y volviendo a correr `create_collections.py`.
- **Selecciones**: las 48 ya estan completas, cada una con su bandera
  (emoji), grupo y confederacion — no falta nada ahi.
- Si `create_collections.py` marca error de conexion, revisa: (1) que tu
  `.env` tenga la cadena correcta, (2) que tu IP este permitida en Atlas
  (Network Access), (3) que el usuario/contraseña de la base sean correctos.

## Que sigue (para cuando quieras ampliarla)

- Agregar mas partidos y jugadores en `seed_data.py`.
- Subir imagenes/logos reales a `app/static/img/` y usarlas en las plantillas.
- Proteger las rutas internas para que solo se pueda entrar si hay sesion
  iniciada (ahora mismo el login guarda la sesion pero las demas pantallas no
  la exigen, para que puedas navegar libremente mientras pruebas).
