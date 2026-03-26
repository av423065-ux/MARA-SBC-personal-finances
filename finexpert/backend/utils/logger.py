"""Configuración centralizada de logging para MARA."""
import logging
import sys


def setup_logger(name: str = "mara", level: str = "INFO") -> logging.Logger:
    """Crea y configura un logger con formato estándar para el proyecto."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger  # ya configurado, evitar duplicados

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter(
            fmt="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )
    logger.addHandler(handler)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    return logger


# Logger raíz del proyecto — importar desde aquí cuando se necesite
log = setup_logger("mara")
