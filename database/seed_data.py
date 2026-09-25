# -*- coding: utf-8 -*-
"""
Datos oficiales del torneo, tal como los definiste, listos para insertarse
en MongoDB Atlas. Cada variable de aqui se convierte en UNA coleccion.
"""

# ---------------------------------------------------------------------------
# 1. PAISES ANFITRIONES
# ---------------------------------------------------------------------------
ANFITRIONES = [
    {"pais": "Canada", "codigo": "CA", "bandera": "🇨🇦", "bandera_url": "https://flagcdn.com/w80/ca.png",
     "ciudades_sede": ["Toronto", "Vancouver"]},
    {"pais": "Mexico", "codigo": "MX", "bandera": "🇲🇽", "bandera_url": "https://flagcdn.com/w80/mx.png",
     "ciudades_sede": ["Ciudad de Mexico", "Guadalajara", "Monterrey"]},
    {"pais": "Estados Unidos", "codigo": "US", "bandera": "🇺🇸", "bandera_url": "https://flagcdn.com/w80/us.png",
     "ciudades_sede": ["Atlanta", "Boston", "Dallas", "Houston", "Kansas City",
                        "Los Angeles", "Miami", "Nueva York/Nueva Jersey",
                        "Filadelfia", "Bahia de San Francisco", "Seattle"]},
]

# ---------------------------------------------------------------------------
# 2. CIUDADES SEDE + ESTADIOS (16 en total)
# ---------------------------------------------------------------------------
CIUDADES_SEDE = [
    {"num": 1,  "pais": "Canada",          "ciudad": "Toronto",                    "estadio": "Toronto Stadium",             "capacidad": None},
    {"num": 2,  "pais": "Canada",          "ciudad": "Vancouver",                  "estadio": "BC Place Vancouver",          "capacidad": 54500},
    {"num": 3,  "pais": "Mexico",          "ciudad": "Ciudad de Mexico",           "estadio": "Estadio Ciudad de Mexico",    "capacidad": 80824},
    {"num": 4,  "pais": "Mexico",          "ciudad": "Guadalajara",                "estadio": "Estadio Guadalajara",         "capacidad": 45664},
    {"num": 5,  "pais": "Mexico",          "ciudad": "Monterrey",                  "estadio": "Estadio Monterrey",           "capacidad": 51243},
    {"num": 6,  "pais": "Estados Unidos",  "ciudad": "Atlanta",                    "estadio": "Atlanta Stadium",             "capacidad": None},
    {"num": 7,  "pais": "Estados Unidos",  "ciudad": "Boston",                     "estadio": "Boston Stadium",              "capacidad": None},
    {"num": 8,  "pais": "Estados Unidos",  "ciudad": "Dallas",                     "estadio": "Dallas Stadium",              "capacidad": None},
    {"num": 9,  "pais": "Estados Unidos",  "ciudad": "Houston",                    "estadio": "Houston Stadium",             "capacidad": None},
    {"num": 10, "pais": "Estados Unidos",  "ciudad": "Kansas City",                "estadio": "Kansas City Stadium",         "capacidad": None},
    {"num": 11, "pais": "Estados Unidos",  "ciudad": "Los Angeles",                "estadio": "SoFi Stadium",                "capacidad": 70240},
    {"num": 12, "pais": "Estados Unidos",  "ciudad": "Miami",                      "estadio": "Miami Stadium",               "capacidad": None},
    {"num": 13, "pais": "Estados Unidos",  "ciudad": "Nueva York/Nueva Jersey",    "estadio": "MetLife Stadium",             "capacidad": 82500},
    {"num": 14, "pais": "Estados Unidos",  "ciudad": "Filadelfia",                 "estadio": "Philadelphia Stadium",        "capacidad": None},
    {"num": 15, "pais": "Estados Unidos",  "ciudad": "Bahia de San Francisco",     "estadio": "San Francisco Bay Area Stadium", "capacidad": None},
    {"num": 16, "pais": "Estados Unidos",  "ciudad": "Seattle",                    "estadio": "Seattle Stadium",             "capacidad": None},
]

# Lista de estadios "plana" para su propia coleccion (mismo contenido, otra forma)
ESTADIOS = [
    {"nombre": c["estadio"], "ciudad": c["ciudad"], "pais": c["pais"], "capacidad": c["capacidad"]}
    for c in CIUDADES_SEDE
]

# ---------------------------------------------------------------------------
# 3. GRUPOS Y SELECCIONES (definitivo: 12 grupos de 4 = 48 selecciones)
# ---------------------------------------------------------------------------
GRUPOS = {
    "A": ["Mexico", "Sudafrica", "Corea del Sur", "Chequia"],
    "B": ["Canada", "Bosnia y Herzegovina", "Catar", "Suiza"],
    "C": ["Brasil", "Marruecos", "Haiti", "Escocia"],
    "D": ["Estados Unidos", "Paraguay", "Australia", "Turquia"],
    "E": ["Alemania", "Curazao", "Costa de Marfil", "Ecuador"],
    "F": ["Paises Bajos", "Japon", "Suecia", "Tunez"],
    "G": ["Belgica", "Egipto", "Iran", "Nueva Zelanda"],
    "H": ["Espana", "Cabo Verde", "Arabia Saudita", "Uruguay"],
    "I": ["Francia", "Senegal", "Irak", "Noruega"],
    "J": ["Argentina", "Argelia", "Austria", "Jordania"],
    "K": ["Portugal", "RD Congo", "Uzbekistan", "Colombia"],
    "L": ["Inglaterra", "Croacia", "Ghana", "Panama"],
}

BANDERAS = {
    "Mexico": "🇲🇽", "Sudafrica": "🇿🇦", "Corea del Sur": "🇰🇷", "Chequia": "🇨🇿",
    "Canada": "🇨🇦", "Bosnia y Herzegovina": "🇧🇦", "Catar": "🇶🇦", "Suiza": "🇨🇭",
    "Brasil": "🇧🇷", "Marruecos": "🇲🇦", "Haiti": "🇭🇹", "Escocia": "🏴",
    "Estados Unidos": "🇺🇸", "Paraguay": "🇵🇾", "Australia": "🇦🇺", "Turquia": "🇹🇷",
    "Alemania": "🇩🇪", "Curazao": "🇨🇼", "Costa de Marfil": "🇨🇮", "Ecuador": "🇪🇨",
    "Paises Bajos": "🇳🇱", "Japon": "🇯🇵", "Suecia": "🇸🇪", "Tunez": "🇹🇳",
    "Belgica": "🇧🇪", "Egipto": "🇪🇬", "Iran": "🇮🇷", "Nueva Zelanda": "🇳🇿",
    "Espana": "🇪🇸", "Cabo Verde": "🇨🇻", "Arabia Saudita": "🇸🇦", "Uruguay": "🇺🇾",
    "Francia": "🇫🇷", "Senegal": "🇸🇳", "Irak": "🇮🇶", "Noruega": "🇳🇴",
    "Argentina": "🇦🇷", "Argelia": "🇩🇿", "Austria": "🇦🇹", "Jordania": "🇯🇴",
    "Portugal": "🇵🇹", "RD Congo": "🇨🇩", "Uzbekistan": "🇺🇿", "Colombia": "🇨🇴",
    "Inglaterra": "🏴", "Croacia": "🇭🇷", "Ghana": "🇬🇭", "Panama": "🇵🇦",
}

# Codigo ISO 3166-1 alpha-2 de cada seleccion (Inglaterra y Escocia usan los
# codigos de subdivision de Reino Unido, que tambien soporta el servicio de
# banderas). Con esto armamos la URL de la imagen real de cada bandera.
CODIGOS_ISO = {
    "Mexico": "mx", "Sudafrica": "za", "Corea del Sur": "kr", "Chequia": "cz",
    "Canada": "ca", "Bosnia y Herzegovina": "ba", "Catar": "qa", "Suiza": "ch",
    "Brasil": "br", "Marruecos": "ma", "Haiti": "ht", "Escocia": "gb-sct",
    "Estados Unidos": "us", "Paraguay": "py", "Australia": "au", "Turquia": "tr",
    "Alemania": "de", "Curazao": "cw", "Costa de Marfil": "ci", "Ecuador": "ec",
    "Paises Bajos": "nl", "Japon": "jp", "Suecia": "se", "Tunez": "tn",
    "Belgica": "be", "Egipto": "eg", "Iran": "ir", "Nueva Zelanda": "nz",
    "Espana": "es", "Cabo Verde": "cv", "Arabia Saudita": "sa", "Uruguay": "uy",
    "Francia": "fr", "Senegal": "sn", "Irak": "iq", "Noruega": "no",
    "Argentina": "ar", "Argelia": "dz", "Austria": "at", "Jordania": "jo",
    "Portugal": "pt", "RD Congo": "cd", "Uzbekistan": "uz", "Colombia": "co",
    "Inglaterra": "gb-eng", "Croacia": "hr", "Ghana": "gh", "Panama": "pa",
    # Extra (para paises anfitriones / historial que no estan en GRUPOS)
    "Italia": "it",
}


def url_bandera(nombre_pais, ancho=40):
    """
    Devuelve la URL de una imagen PNG real de la bandera de un pais,
    usando flagcdn.com (gratis, sin necesidad de API key). Se usa en vez
    de los emojis de bandera porque Windows no los dibuja como banderas
    (muestra solo el codigo de 2 letras en una cajita).
    """
    codigo = CODIGOS_ISO.get(nombre_pais)
    if not codigo:
        return None
    return f"https://flagcdn.com/w{ancho}/{codigo}.png"


# Confederacion aproximada, solo para poder filtrar "Por confederacion" en la pantalla de Selecciones
CONFEDERACIONES = {
    "Mexico": "CONCACAF", "Canada": "CONCACAF", "Estados Unidos": "CONCACAF",
    "Curazao": "CONCACAF", "Haiti": "CONCACAF", "Panama": "CONCACAF", "Jamaica": "CONCACAF",
    "Brasil": "CONMEBOL", "Argentina": "CONMEBOL", "Colombia": "CONMEBOL",
    "Ecuador": "CONMEBOL", "Paraguay": "CONMEBOL", "Uruguay": "CONMEBOL",
    "Sudafrica": "CAF", "Marruecos": "CAF", "Egipto": "CAF", "Tunez": "CAF",
    "Costa de Marfil": "CAF", "Ghana": "CAF", "Senegal": "CAF", "Argelia": "CAF",
    "Cabo Verde": "CAF", "RD Congo": "CAF",
    "Corea del Sur": "AFC", "Catar": "AFC", "Japon": "AFC", "Iran": "AFC",
    "Arabia Saudita": "AFC", "Irak": "AFC", "Jordania": "AFC", "Uzbekistan": "AFC",
    "Australia": "AFC",
    "Chequia": "UEFA", "Bosnia y Herzegovina": "UEFA", "Suiza": "UEFA",
    "Escocia": "UEFA", "Turquia": "UEFA", "Alemania": "UEFA", "Paises Bajos": "UEFA",
    "Suecia": "UEFA", "Belgica": "UEFA", "Espana": "UEFA", "Francia": "UEFA",
    "Noruega": "UEFA", "Austria": "UEFA", "Portugal": "UEFA", "Inglaterra": "UEFA",
    "Croacia": "UEFA",
    "Nueva Zelanda": "OFC",
}


def construir_selecciones():
    """Arma la coleccion 'selecciones' a partir de GRUPOS."""
    selecciones = []
    for grupo, equipos in GRUPOS.items():
        for equipo in equipos:
            selecciones.append({
                "nombre": equipo,
                "bandera": BANDERAS.get(equipo, "🏳️"),
                "bandera_url": url_bandera(equipo),
                "grupo": grupo,
                "confederacion": CONFEDERACIONES.get(equipo, "N/D"),
                "favorito": False,
            })
    return selecciones


def construir_grupos():
    """Arma la coleccion 'grupos', con tabla de posiciones inicial en cero."""
    grupos_doc = []
    for grupo, equipos in GRUPOS.items():
        tabla = []
        for pos, equipo in enumerate(equipos, start=1):
            tabla.append({
                "posicion": pos, "seleccion": equipo, "bandera": BANDERAS.get(equipo, "🏳️"),
                "bandera_url": url_bandera(equipo),
                "pj": 0, "pg": 0, "pe": 0, "pp": 0, "gf": 0, "gc": 0, "pts": 0,
            })
        grupos_doc.append({"grupo": grupo, "equipos": equipos, "tabla": tabla})
    return grupos_doc


# ---------------------------------------------------------------------------
# 4. JUGADORES (al menos uno por cada una de las 48 selecciones, + estrellas
#    extra en las selecciones mas populares para pasar de 50 en total).
#    "foto_url" queda vacio a proposito: no se insertan fotografias reales de
#    personas (son contenido con derechos de imagen). Mientras tanto, la app
#    dibuja un avatar con la inicial del jugador; si mas adelante subes fotos
#    reales (por ejemplo a Cloudinary/S3/tu propio servidor), solo pon aqui la
#    URL de cada quien y la plantilla la usara automaticamente.
# ---------------------------------------------------------------------------
JUGADORES_DESTACADOS = [
    # --- Argentina ---
    {"nombre": "Lionel Messi",        "seleccion": "Argentina",       "posicion": "Delantero",       "numero": 10, "edad": 39, "destacado": True,  "foto_url": ""},
    {"nombre": "Julian Alvarez",      "seleccion": "Argentina",       "posicion": "Delantero",       "numero": 9,  "edad": 26, "destacado": False, "foto_url": ""},
    # --- Francia ---
    {"nombre": "Kylian Mbappe",       "seleccion": "Francia",         "posicion": "Delantero",       "numero": 10, "edad": 27, "destacado": True,  "foto_url": ""},
    {"nombre": "Ousmane Dembele",     "seleccion": "Francia",         "posicion": "Delantero",       "numero": 11, "edad": 29, "destacado": False, "foto_url": ""},
    # --- Portugal ---
    {"nombre": "Cristiano Ronaldo",   "seleccion": "Portugal",        "posicion": "Delantero",       "numero": 7,  "edad": 41, "destacado": True,  "foto_url": ""},
    {"nombre": "Bruno Fernandes",     "seleccion": "Portugal",        "posicion": "Mediocampista",   "numero": 8,  "edad": 32, "destacado": False, "foto_url": ""},
    # --- Inglaterra ---
    {"nombre": "Jude Bellingham",     "seleccion": "Inglaterra",      "posicion": "Mediocampista",   "numero": 10, "edad": 23, "destacado": True,  "foto_url": ""},
    {"nombre": "Harry Kane",          "seleccion": "Inglaterra",      "posicion": "Delantero",       "numero": 9,  "edad": 33, "destacado": False, "foto_url": ""},
    {"nombre": "Phil Foden",          "seleccion": "Inglaterra",      "posicion": "Mediocampista",   "numero": 11, "edad": 26, "destacado": False, "foto_url": ""},
    # --- Noruega ---
    {"nombre": "Erling Haaland",      "seleccion": "Noruega",         "posicion": "Delantero",       "numero": 9,  "edad": 26, "destacado": True,  "foto_url": ""},
    {"nombre": "Martin Odegaard",     "seleccion": "Noruega",         "posicion": "Mediocampista",   "numero": 8,  "edad": 27, "destacado": False, "foto_url": ""},
    # --- Brasil ---
    {"nombre": "Vinicius Junior",     "seleccion": "Brasil",          "posicion": "Delantero",       "numero": 7,  "edad": 26, "destacado": True,  "foto_url": ""},
    {"nombre": "Rodrygo",             "seleccion": "Brasil",          "posicion": "Delantero",       "numero": 11, "edad": 25, "destacado": False, "foto_url": ""},
    {"nombre": "Neymar Jr",           "seleccion": "Brasil",          "posicion": "Delantero",       "numero": 10, "edad": 34, "destacado": True,  "foto_url": ""},
    # --- España ---
    {"nombre": "Lamine Yamal",        "seleccion": "Espana",          "posicion": "Delantero",       "numero": 19, "edad": 19, "destacado": True,  "foto_url": ""},
    {"nombre": "Pedri",               "seleccion": "Espana",          "posicion": "Mediocampista",   "numero": 8,  "edad": 24, "destacado": False, "foto_url": ""},
    {"nombre": "Rodri",               "seleccion": "Espana",          "posicion": "Mediocampista",   "numero": 16, "edad": 30, "destacado": False, "foto_url": ""},
    # --- Alemania ---
    {"nombre": "Jamal Musiala",       "seleccion": "Alemania",        "posicion": "Mediocampista",   "numero": 10, "edad": 23, "destacado": True,  "foto_url": ""},
    {"nombre": "Florian Wirtz",       "seleccion": "Alemania",        "posicion": "Mediocampista",   "numero": 17, "edad": 23, "destacado": False, "foto_url": ""},
    # --- Países Bajos ---
    {"nombre": "Xavi Simons",         "seleccion": "Paises Bajos",    "posicion": "Mediocampista",   "numero": 7,  "edad": 23, "destacado": False, "foto_url": ""},
    {"nombre": "Cody Gakpo",          "seleccion": "Paises Bajos",    "posicion": "Delantero",       "numero": 11, "edad": 27, "destacado": False, "foto_url": ""},
    # --- Bélgica ---
    {"nombre": "Kevin De Bruyne",     "seleccion": "Belgica",         "posicion": "Mediocampista",   "numero": 7,  "edad": 35, "destacado": True,  "foto_url": ""},
    {"nombre": "Romelu Lukaku",       "seleccion": "Belgica",         "posicion": "Delantero",       "numero": 9,  "edad": 33, "destacado": False, "foto_url": ""},
    # --- Croacia ---
    {"nombre": "Luka Modric",         "seleccion": "Croacia",         "posicion": "Mediocampista",   "numero": 10, "edad": 41, "destacado": True,  "foto_url": ""},
    # --- Uruguay ---
    {"nombre": "Federico Valverde",   "seleccion": "Uruguay",         "posicion": "Mediocampista",   "numero": 15, "edad": 28, "destacado": False, "foto_url": ""},
    {"nombre": "Darwin Nunez",        "seleccion": "Uruguay",         "posicion": "Delantero",       "numero": 9,  "edad": 27, "destacado": False, "foto_url": ""},
    # --- Colombia ---
    {"nombre": "James Rodriguez",     "seleccion": "Colombia",        "posicion": "Mediocampista",   "numero": 10, "edad": 35, "destacado": True,  "foto_url": ""},
    {"nombre": "Luis Diaz",           "seleccion": "Colombia",        "posicion": "Delantero",       "numero": 7,  "edad": 29, "destacado": False, "foto_url": ""},
    # --- Marruecos ---
    {"nombre": "Achraf Hakimi",       "seleccion": "Marruecos",       "posicion": "Defensa",         "numero": 2,  "edad": 27, "destacado": True,  "foto_url": ""},
    # --- Senegal ---
    {"nombre": "Sadio Mane",          "seleccion": "Senegal",         "posicion": "Delantero",       "numero": 10, "edad": 34, "destacado": False, "foto_url": ""},
    # --- Egipto ---
    {"nombre": "Mohamed Salah",       "seleccion": "Egipto",          "posicion": "Delantero",       "numero": 10, "edad": 34, "destacado": True,  "foto_url": ""},
    # --- Ghana ---
    {"nombre": "Mohammed Kudus",      "seleccion": "Ghana",           "posicion": "Mediocampista",   "numero": 20, "edad": 25, "destacado": False, "foto_url": ""},
    # --- Argelia ---
    {"nombre": "Riyad Mahrez",        "seleccion": "Argelia",         "posicion": "Delantero",       "numero": 7,  "edad": 35, "destacado": False, "foto_url": ""},
    # --- Costa de Marfil ---
    {"nombre": "Sebastien Haller",    "seleccion": "Costa de Marfil", "posicion": "Delantero",       "numero": 11, "edad": 31, "destacado": False, "foto_url": ""},
    # --- Túnez ---
    {"nombre": "Youssef Msakni",      "seleccion": "Tunez",           "posicion": "Delantero",       "numero": 8,  "edad": 35, "destacado": False, "foto_url": ""},
    # --- Cabo Verde ---
    {"nombre": "Ryan Mendes",         "seleccion": "Cabo Verde",      "posicion": "Delantero",       "numero": 11, "edad": 34, "destacado": False, "foto_url": ""},
    # --- RD Congo ---
    {"nombre": "Cedric Bakambu",      "seleccion": "RD Congo",        "posicion": "Delantero",       "numero": 19, "edad": 34, "destacado": False, "foto_url": ""},
    # --- Sudáfrica ---
    {"nombre": "Percy Tau",           "seleccion": "Sudafrica",       "posicion": "Delantero",       "numero": 7,  "edad": 31, "destacado": False, "foto_url": ""},
    # --- México ---
    {"nombre": "Santiago Gimenez",    "seleccion": "Mexico",          "posicion": "Delantero",       "numero": 20, "edad": 24, "destacado": True,  "foto_url": ""},
    {"nombre": "Edson Alvarez",       "seleccion": "Mexico",          "posicion": "Mediocampista",   "numero": 4,  "edad": 27, "destacado": False, "foto_url": ""},
    # --- Canadá ---
    {"nombre": "Alphonso Davies",     "seleccion": "Canada",          "posicion": "Defensa",         "numero": 19, "edad": 24, "destacado": True,  "foto_url": ""},
    {"nombre": "Jonathan David",      "seleccion": "Canada",          "posicion": "Delantero",       "numero": 20, "edad": 25, "destacado": False, "foto_url": ""},
    # --- Estados Unidos ---
    {"nombre": "Christian Pulisic",   "seleccion": "Estados Unidos",  "posicion": "Delantero",       "numero": 10, "edad": 27, "destacado": True,  "foto_url": ""},
    {"nombre": "Weston McKennie",     "seleccion": "Estados Unidos",  "posicion": "Mediocampista",   "numero": 8,  "edad": 27, "destacado": False, "foto_url": ""},
    # --- Paraguay ---
    {"nombre": "Miguel Almiron",      "seleccion": "Paraguay",        "posicion": "Mediocampista",   "numero": 21, "edad": 32, "destacado": False, "foto_url": ""},
    # --- Ecuador ---
    {"nombre": "Moises Caicedo",      "seleccion": "Ecuador",         "posicion": "Mediocampista",   "numero": 23, "edad": 24, "destacado": False, "foto_url": ""},
    # --- Panamá ---
    {"nombre": "Cecilio Waterman",    "seleccion": "Panama",          "posicion": "Delantero",       "numero": 9,  "edad": 30, "destacado": False, "foto_url": ""},
    # --- Haití ---
    {"nombre": "Duckens Nazon",       "seleccion": "Haiti",           "posicion": "Delantero",       "numero": 20, "edad": 30, "destacado": False, "foto_url": ""},
    # --- Curazao ---
    {"nombre": "Leandro Bacuna",      "seleccion": "Curazao",         "posicion": "Mediocampista",   "numero": 6,  "edad": 34, "destacado": False, "foto_url": ""},
    # --- Japón ---
    {"nombre": "Takefusa Kubo",       "seleccion": "Japon",           "posicion": "Delantero",       "numero": 7,  "edad": 25, "destacado": False, "foto_url": ""},
    # --- Corea del Sur ---
    {"nombre": "Son Heung-min",       "seleccion": "Corea del Sur",   "posicion": "Delantero",       "numero": 7,  "edad": 33, "destacado": True,  "foto_url": ""},
    # --- Arabia Saudita ---
    {"nombre": "Salem Al-Dawsari",    "seleccion": "Arabia Saudita",  "posicion": "Delantero",       "numero": 10, "edad": 35, "destacado": False, "foto_url": ""},
    # --- Catar ---
    {"nombre": "Akram Afif",          "seleccion": "Catar",           "posicion": "Delantero",       "numero": 11, "edad": 29, "destacado": False, "foto_url": ""},
    # --- Irán ---
    {"nombre": "Mehdi Taremi",        "seleccion": "Iran",            "posicion": "Delantero",       "numero": 9,  "edad": 33, "destacado": False, "foto_url": ""},
    # --- Irak ---
    {"nombre": "Ayman Hussein",       "seleccion": "Irak",            "posicion": "Delantero",       "numero": 19, "edad": 29, "destacado": False, "foto_url": ""},
    # --- Jordania ---
    {"nombre": "Musa Al-Taamari",     "seleccion": "Jordania",        "posicion": "Delantero",       "numero": 17, "edad": 28, "destacado": False, "foto_url": ""},
    # --- Uzbekistán ---
    {"nombre": "Eldor Shomurodov",    "seleccion": "Uzbekistan",      "posicion": "Delantero",       "numero": 9,  "edad": 30, "destacado": False, "foto_url": ""},
    # --- Australia ---
    {"nombre": "Craig Goodwin",       "seleccion": "Australia",       "posicion": "Delantero",       "numero": 11, "edad": 33, "destacado": False, "foto_url": ""},
    # --- Nueva Zelanda ---
    {"nombre": "Chris Wood",          "seleccion": "Nueva Zelanda",   "posicion": "Delantero",       "numero": 9,  "edad": 34, "destacado": False, "foto_url": ""},
    # --- Chequia ---
    {"nombre": "Patrik Schick",       "seleccion": "Chequia",         "posicion": "Delantero",       "numero": 9,  "edad": 30, "destacado": False, "foto_url": ""},
    # --- Bosnia y Herzegovina ---
    {"nombre": "Edin Dzeko",          "seleccion": "Bosnia y Herzegovina", "posicion": "Delantero",  "numero": 9,  "edad": 40, "destacado": False, "foto_url": ""},
    # --- Suiza ---
    {"nombre": "Granit Xhaka",        "seleccion": "Suiza",           "posicion": "Mediocampista",   "numero": 10, "edad": 33, "destacado": False, "foto_url": ""},
    # --- Escocia ---
    {"nombre": "Andy Robertson",      "seleccion": "Escocia",         "posicion": "Defensa",         "numero": 3,  "edad": 32, "destacado": False, "foto_url": ""},
    # --- Turquía ---
    {"nombre": "Arda Guler",          "seleccion": "Turquia",         "posicion": "Mediocampista",   "numero": 8,  "edad": 21, "destacado": False, "foto_url": ""},
    # --- Suecia ---
    {"nombre": "Alexander Isak",      "seleccion": "Suecia",          "posicion": "Delantero",       "numero": 9,  "edad": 26, "destacado": False, "foto_url": ""},
    # --- Austria ---
    {"nombre": "David Alaba",         "seleccion": "Austria",         "posicion": "Defensa",         "numero": 4,  "edad": 34, "destacado": False, "foto_url": ""},
]


# ---------------------------------------------------------------------------
# 5. PARTIDOS (muestra inicial con fechas reales del calendario; se pueden
#    seguir agregando hasta completar los 104)
# ---------------------------------------------------------------------------
_PARTIDOS_BASE = [
    {"fecha": "2026-06-11", "hora": "16:00", "fase": "Grupo D", "local": "Estados Unidos", "visitante": "Japon", "estadio": "Estadio Sofi - Los Angeles", "marcador": "2-1"},
    {"fecha": "2026-06-11", "hora": "16:00", "fase": "Grupo A", "local": "Mexico", "visitante": "Sudafrica", "estadio": "Estadio Ciudad de Mexico", "marcador": None},
    {"fecha": "2026-06-12", "hora": "16:00", "fase": "Grupo B", "local": "Mexico", "visitante": "Canada", "estadio": "Estadio Azteca - COMX", "marcador": None},
    {"fecha": "2026-06-12", "hora": "22:00", "fase": "Grupo I", "local": "Francia", "visitante": "Senegal", "estadio": "Estadio de la Luz - Toronto", "marcador": None},
    {"fecha": "2026-06-13", "hora": "13:00", "fase": "Grupo J", "local": "Argentina", "visitante": "Arabia Saudita", "estadio": "Estadio Lusail - Doha", "marcador": None},
    {"fecha": "2026-06-13", "hora": "16:00", "fase": "Grupo E", "local": "Alemania", "visitante": "Escocia", "estadio": "MetLife Stadium - Nueva York", "marcador": None},
]


def _construir_partidos():
    """Agrega la bandera (emoji + imagen real) de cada equipo a cada partido."""
    partidos = []
    for p in _PARTIDOS_BASE:
        p = dict(p)
        p["bandera_local"] = BANDERAS.get(p["local"], "🏳️")
        p["bandera_visitante"] = BANDERAS.get(p["visitante"], "🏳️")
        p["bandera_local_url"] = url_bandera(p["local"])
        p["bandera_visitante_url"] = url_bandera(p["visitante"])
        partidos.append(p)
    return partidos


PARTIDOS = _construir_partidos()

# ---------------------------------------------------------------------------
# 6. HISTORIA DEL MUNDIAL (campeones recientes, para la pantalla 13)
# ---------------------------------------------------------------------------
HISTORIA_MUNDIAL = [
    {"anio": 2022, "campeon": "Argentina", "bandera": "🇦🇷", "bandera_url": url_bandera("Argentina")},
    {"anio": 2018, "campeon": "Francia", "bandera": "🇫🇷", "bandera_url": url_bandera("Francia")},
    {"anio": 2014, "campeon": "Alemania", "bandera": "🇩🇪", "bandera_url": url_bandera("Alemania")},
    {"anio": 2010, "campeon": "Espana", "bandera": "🇪🇸", "bandera_url": url_bandera("Espana")},
    {"anio": 2006, "campeon": "Italia", "bandera": "🇮🇹", "bandera_url": url_bandera("Italia")},
    {"anio": 2002, "campeon": "Brasil", "bandera": "🇧🇷", "bandera_url": url_bandera("Brasil")},
]

# ---------------------------------------------------------------------------
# 7. NOTICIAS (muestra inicial para la pantalla 15)
# ---------------------------------------------------------------------------
NOTICIAS = [
    {"titulo": "FIFA anuncia el balon oficial del Mundial 2026", "categoria": "Mundial", "horas": 2},
    {"titulo": "Mexico ya tiene su lista preliminar de convocados", "categoria": "Mexico", "horas": 5},
    {"titulo": "Asi se veran los estadios del Mundial 2026", "categoria": "Mundial", "horas": 6},
    {"titulo": "La emocion del Mundial ya se vive en todo el mundo", "categoria": "Mundial", "horas": 12},
]

# ---------------------------------------------------------------------------
# 8. QUIZ (preguntas de ejemplo para la pantalla 14)
# ---------------------------------------------------------------------------
QUIZ_PREGUNTAS = [
    {"pregunta": "¿Cuantos paises seran anfitriones del Mundial 2026?", "opciones": ["2", "3", "4"], "respuesta": "3"},
    {"pregunta": "¿Cuantas selecciones participan en total?", "opciones": ["32", "40", "48"], "respuesta": "48"},
    {"pregunta": "¿Cuantos estadios se usaran en total?", "opciones": ["12", "16", "20"], "respuesta": "16"},
    {"pregunta": "¿Cuantos grupos hay en la fase de grupos?", "opciones": ["8", "12", "16"], "respuesta": "12"},
    {"pregunta": "¿Cuantos partidos se jugaran en total?", "opciones": ["64", "80", "104"], "respuesta": "104"},
]

# ---------------------------------------------------------------------------
# 9. DATOS GENERALES (para la tarjeta de resumen en Inicio)
# ---------------------------------------------------------------------------
DATOS_GENERALES = {
    "paises_anfitriones": 3,
    "ciudades_sede": 16,
    "estadios": 16,
    "selecciones_participantes": 48,
    "jugadores": 1248,
    "grupos": 12,
    "partidos": 104,
    "jugadores_por_seleccion": 26,
}


# ---------------------------------------------------------------------------
# 10. QUINIELA (predicciones con puntos e insignias, SIN dinero real)
# ---------------------------------------------------------------------------
# Reglas de puntos:
#   - Marcador exacto acertado:        3 puntos
#   - Acertaste quien gana / empate, pero no el marcador exacto: 1 punto
#   - Fallaste por completo:           0 puntos
PUNTOS_MARCADOR_EXACTO = 3
PUNTOS_RESULTADO_CORRECTO = 1

# Insignias que se otorgan segun los puntos totales acumulados por el usuario
INSIGNIAS = [
    {"clave": "primera_prediccion", "nombre": "Primer Pronostico", "icono": "🔮", "requisito_puntos": 0, "requisito_predicciones": 1},
    {"clave": "profeta", "nombre": "Profeta del Mundial", "icono": "🎯", "requisito_puntos": 9, "requisito_predicciones": 0},
    {"clave": "fiel_aficionado", "nombre": "Fiel Aficionado", "icono": "❤️", "requisito_puntos": 0, "requisito_predicciones": 10},
    {"clave": "leyenda", "nombre": "Leyenda de la Quiniela", "icono": "🏆", "requisito_puntos": 30, "requisito_predicciones": 0},
]
