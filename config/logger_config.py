import os
import sys

from dotenv import load_dotenv
from loguru import logger

load_dotenv()

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURACION LOGGER
# ═══════════════════════════════════════════════════════════════════════════════

class LoggerConfig:
    _initialized = False

    @classmethod
    def init(cls):
        """
        Inicializa el logger si aún no ha sido configurado.
        """
        if not cls._initialized:
            try:
                log_level = os.getenv("LOG_LEVEL", "INFO")

                logger.remove()
                logger.add(
                    sys.stderr,
                    format=(
                        "<cyan>{time:YYYY-MM-DD HH:mm:ss}</cyan> | "
                        "<level>{level: <8}</level> | "
                        "<cyan>{file.name: <10}</cyan> | "
                        "<cyan>{function: <10}:{line: <4}</cyan> | "
                        "<white>{message}</white>"
                    ),
                    level=log_level,
                    colorize=True,
                    backtrace=True,
                    diagnose=True
                )

                # Configurar colores personalizados para cada nivel
                logger.level("TRACE", color="<magenta>")
                logger.level("DEBUG", color="<blue>")
                logger.level("INFO", color="<green>")
                logger.level("SUCCESS", color="<bold><green>")
                logger.level("WARNING", color="<yellow>")
                logger.level("ERROR", color="<red>")
                logger.level("CRITICAL", color="<bold><red>")

                logger.trace(f"Logger inicializado con nivel: {log_level}")
                cls._initialized = True

            except Exception as e:
                logger.remove()
                logger.add(sys.stderr, level="INFO")
                logger.error(f"Error inicializando logger: {e}")

    @classmethod
    def get(cls):
        """
        Retorna el logger global ya inicializado.
        """
        if not cls._initialized:
            cls.init()
        return logger


# Alias global para usar en todo el proyecto
log = LoggerConfig.get()
LoggerConfig.init()


# ═══════════════════════════════════════════════════════════════════════════════
# NIVELES DE LOG DISPONIBLES (Loguru)
# ═══════════════════════════════════════════════════════════════════════════════
# TRACE (5)    → Nivel más detallado, imprime absolutamente todo.
#                Útil para depuración muy fina (valores internos, pasos ocultos).
#
# DEBUG (10)   → Información técnica útil para desarrolladores.
#                Ej: parámetros de funciones, consultas SQL, tiempos de ejecución.
#
# INFO (20)    → Flujo normal de la aplicación.
#                Ej: inicio de procesos, eventos importantes esperados.
#
# SUCCESS (25) → Nivel exclusivo de Loguru para resaltar éxitos.
#                Ej: “Proceso completado con éxito”, “Archivo guardado correctamente”.
#
# WARNING (30) → Algo inesperado ocurrió, pero no detiene la ejecución.
#                Ej: valores por defecto, datos nulos encontrados, reintentos.
#
# ERROR (40)   → Fallo en la ejecución que requiere atención.
#                Ej: “No se pudo conectar a la base de datos”.
#
# CRITICAL (50)→ Error grave que compromete el funcionamiento total.
#                Ej: caída de servicios principales, pérdida de datos.
#
# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTANTE SOBRE LOG_LEVEL
# ═══════════════════════════════════════════════════════════════════════════════
# El nivel de logs se controla con la variable de entorno LOG_LEVEL.
# Ejemplos de comportamiento:
#
#   LOG_LEVEL=TRACE   → imprime absolutamente todos los niveles.
#   LOG_LEVEL=DEBUG   → imprime DEBUG en adelante (DEBUG, INFO, SUCCESS, WARNING...).
#   LOG_LEVEL=INFO    → imprime INFO en adelante (INFO, SUCCESS, WARNING...).
#   LOG_LEVEL=WARNING → imprime solo WARNING, ERROR, CRITICAL.
#   LOG_LEVEL=ERROR   → imprime solo ERROR y CRITICAL.
#
# ═══════════════════════════════════════════════════════════════════════════════
# EJEMPLOS DE USO
# ═══════════════════════════════════════════════════════════════════════════════
#log.trace("Valor interno del loop: {}", "x")
#log.debug("Consulta SQL ejecutada: {}", "query")
#log.info("Servicio iniciado en el puerto {}", "port")
#log.success("Archivo procesado con éxito: {}", "filename")
#log.warning("Campo vacío detectado, usando valor por defecto")
#log.error("Fallo al conectar con el servidor: {}", "error")
#log.critical("Servicio caído: abortando ejecución")
# ═══════════════════════════════════════════════════════════════════════════════