"""Configuración global de MARA leída desde variables de entorno con valores por defecto."""
import os
import pathlib

# Directorio base del backend
BASE_DIR = pathlib.Path(__file__).parent

# Flask
FLASK_HOST  = os.getenv("FLASK_HOST", "0.0.0.0")
FLASK_PORT  = int(os.getenv("FLASK_PORT", "5000"))
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"

# Rutas de conocimiento
RULES_DIR  = BASE_DIR / "knowledge" / "rules"
FACTS_FILE = BASE_DIR / "knowledge" / "ontology" / "umbrales_financieros.json"

# Motor de inferencia
MAX_INFERENCE_CYCLES = int(os.getenv("MAX_CYCLES", "200"))

# CORS: orígenes permitidos (separados por coma en la variable de entorno)
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

# Nivel de log
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
