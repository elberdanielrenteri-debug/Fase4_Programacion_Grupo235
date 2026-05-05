# excepciones.py
# En este archivo se definen las excepciones personalizadas del sistema.
# Estas excepciones ayudan a identificar errores específicos de forma clara.

class ErrorAplicacion(Exception):
    """Excepción base para todos los errores del sistema."""
    pass


class ClienteInvalidoError(ErrorAplicacion):
    """Se genera cuando un cliente tiene datos inválidos."""
    pass


class ServicioNoValidoError(ErrorAplicacion):
    """Se genera cuando un servicio tiene información incorrecta."""
    pass


class ServicioNoDisponibleError(ErrorAplicacion):
    """Se genera cuando se intenta usar un servicio no disponible."""
    pass


class ReservaError(ErrorAplicacion):
    """Se genera cuando ocurre un problema al crear, procesar o cancelar una reserva."""
    pass