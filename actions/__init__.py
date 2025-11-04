"""Acciones personalizadas del bot bíblico.

Este paquete importa explícitamente los módulos de acciones para que el
servidor de acciones de Rasa los descubra al iniciar.
"""

# Importar módulos de acciones (descubrimiento por efectos secundarios)
from . import actions  # noqa: F401
from . import action_srs  # noqa: F401
from . import action_trivia  # noqa: F401
from . import action_missions  # noqa: F401
from . import action_bingo  # noqa: F401

