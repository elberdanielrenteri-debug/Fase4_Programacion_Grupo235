# modelos.py
# Aquí están las clases principales del sistema.
# Se implementan abstracción, herencia, polimorfismo, encapsulación
# y manejo de excepciones personalizadas.

from abc import ABC, abstractmethod
from excepciones import (
    ClienteInvalidoError,
    ServicioNoValidoError,
    ServicioNoDisponibleError,
    ReservaError,
)
from logger import registrar_evento


class Entidad(ABC):
    """
    Clase abstracta base.
    Representa cualquier entidad general del sistema.
    """

    def __init__(self, identificador: str):
        # Se valida que el identificador no esté vacío.
        if not str(identificador).strip():
            raise ValueError("El identificador no puede estar vacío.")

        self._identificador = str(identificador).strip()

    @property
    def identificador(self):
        """Permite consultar el identificador sin modificarlo directamente."""
        return self._identificador

    @abstractmethod
    def describir(self) -> str:
        """
        Método abstracto que obliga a las subclases a definir su propia descripción.
        """
        pass


class Cliente(Entidad):
    """
    Representa un cliente del sistema.
    Usa encapsulación mediante propiedades.
    """

    def __init__(self, identificador: str, nombre: str, documento: str, email: str):
        super().__init__(identificador)

        # Cada asignación pasa por su respectivo setter para validar datos.
        self.nombre = nombre
        self.documento = documento
        self.email = email

    @property
    def nombre(self):
        """Devuelve el nombre del cliente."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        """
        Valida que el nombre tenga al menos 2 caracteres.
        """
        try:
            valor = str(valor).strip()
            if len(valor) < 2:
                raise ClienteInvalidoError(
                    "El nombre del cliente debe tener al menos 2 caracteres."
                )
            self._nombre = valor
        except Exception as e:
            # Se encadena la excepción para conservar el error original.
            raise ClienteInvalidoError("No fue posible asignar el nombre del cliente.") from e

    @property
    def documento(self):
        """Devuelve el documento del cliente."""
        return self._documento

    @documento.setter
    def documento(self, valor):
        """
        Valida que el documento tenga solo números y tenga una longitud mínima.
        """
        try:
            valor = str(valor).strip()
            if not valor.isdigit():
                raise ClienteInvalidoError("El documento debe contener solo números.")
            if len(valor) < 5:
                raise ClienteInvalidoError("El documento debe tener al menos 5 dígitos.")
            self._documento = valor
        except Exception as e:
            raise ClienteInvalidoError("No fue posible asignar el documento del cliente.") from e

    @property
    def email(self):
        """Devuelve el correo electrónico del cliente."""
        return self._email

    @email.setter
    def email(self, valor):
        """
        Valida que el correo tenga un formato mínimo correcto.
        """
        try:
            valor = str(valor).strip()
            if "@" not in valor or "." not in valor:
                raise ClienteInvalidoError("El correo electrónico no tiene un formato válido.")
            self._email = valor
        except Exception as e:
            raise ClienteInvalidoError("No fue posible asignar el email del cliente.") from e

    def describir(self) -> str:
        # Método concreto que describe al cliente.
        return f"Cliente {self.nombre} | Documento: {self.documento} | Email: {self.email}"

    def __str__(self):
        return self.describir()


class Servicio(ABC):
    """
    Clase abstracta base para los servicios.
    Cada servicio especializado debe calcular su costo y describirse.
    """

    def __init__(self, codigo: str, nombre: str, tarifa_base: float, disponible: bool = True):
        try:
            codigo = str(codigo).strip()
            nombre = str(nombre).strip()

            if not codigo:
                raise ServicioNoValidoError("El código del servicio no puede estar vacío.")
            if len(nombre) < 3:
                raise ServicioNoValidoError("El nombre del servicio debe tener al menos 3 caracteres.")
            if tarifa_base < 0:
                raise ServicioNoValidoError("La tarifa base no puede ser negativa.")

            self._codigo = codigo
            self._nombre = nombre
            self._tarifa_base = float(tarifa_base)
            self._disponible = disponible

        except Exception as e:
            raise ServicioNoValidoError("No fue posible crear el servicio.") from e

    @property
    def codigo(self):
        return self._codigo

    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa_base(self):
        return self._tarifa_base

    @property
    def disponible(self):
        return self._disponible

    @disponible.setter
    def disponible(self, valor: bool):
        # Se guarda el valor convertido a booleano.
        self._disponible = bool(valor)

    @abstractmethod
    def calcular_costo(self, cantidad: int = 1, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        """
        Cada servicio debe calcular su costo de manera propia.
        """
        pass

    @abstractmethod
    def describir(self) -> str:
        """
        Cada servicio debe definir su propia descripción.
        """
        pass


class ServicioSala(Servicio):
    """
    Servicio especializado para reserva de salas.
    """

    def __init__(self, codigo: str, nombre: str, tarifa_base: float, capacidad_maxima: int):
        super().__init__(codigo, nombre, tarifa_base)

        if capacidad_maxima <= 0:
            raise ServicioNoValidoError("La capacidad máxima debe ser mayor que cero.")

        self.capacidad_maxima = capacidad_maxima

    def calcular_costo(self, cantidad: int = 1, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        """
        Calcula el costo de una sala según la cantidad de horas.
        """
        if cantidad <= 0:
            raise ServicioNoValidoError("La cantidad de horas debe ser mayor que cero.")

        subtotal = self.tarifa_base * cantidad
        total = subtotal + (subtotal * impuesto) - descuento

        # Evita que el total quede negativo por un descuento excesivo.
        return round(max(total, 0), 2)

    def describir(self) -> str:
        return f"Sala | Nombre: {self.nombre} | Tarifa: {self.tarifa_base} | Capacidad: {self.capacidad_maxima}"

    def __str__(self):
        return self.describir()


class ServicioEquipo(Servicio):
    """
    Servicio especializado para alquiler de equipos.
    """

    def __init__(self, codigo: str, nombre: str, tarifa_base: float, stock: int):
        super().__init__(codigo, nombre, tarifa_base)

        if stock < 0:
            raise ServicioNoValidoError("El stock no puede ser negativo.")

        self.stock = stock

    def calcular_costo(self, cantidad: int = 1, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        """
        Calcula el costo del alquiler de equipos.
        También verifica que haya stock suficiente.
        """
        if cantidad <= 0:
            raise ServicioNoValidoError("La cantidad de equipos debe ser mayor que cero.")

        if cantidad > self.stock:
            raise ServicioNoDisponibleError(
                f"No hay suficiente stock. Disponible: {self.stock}, solicitado: {cantidad}."
            )

        subtotal = self.tarifa_base * cantidad
        total = subtotal + (subtotal * impuesto) - descuento
        return round(max(total, 0), 2)

    def describir(self) -> str:
        return f"Equipo | Nombre: {self.nombre} | Tarifa: {self.tarifa_base} | Stock: {self.stock}"

    def __str__(self):
        return self.describir()


class ServicioAsesoria(Servicio):
    """
    Servicio especializado para asesorías.
    """

    def __init__(self, codigo: str, nombre: str, tarifa_base: float, area: str):
        super().__init__(codigo, nombre, tarifa_base)

        area = str(area).strip()
        if len(area) < 3:
            raise ServicioNoValidoError("El área de asesoría debe tener al menos 3 caracteres.")

        self.area = area

    def calcular_costo(self, cantidad: int = 1, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        """
        Calcula el costo de una asesoría según la cantidad de sesiones.
        """
        if cantidad <= 0:
            raise ServicioNoValidoError("La cantidad de sesiones debe ser mayor que cero.")

        subtotal = self.tarifa_base * cantidad
        total = subtotal + (subtotal * impuesto) - descuento
        return round(max(total, 0), 2)

    def describir(self) -> str:
        return f"Asesoría | Nombre: {self.nombre} | Área: {self.area} | Tarifa: {self.tarifa_base}"

    def __str__(self):
        return self.describir()


class Reserva(Entidad):
    """
    Representa una reserva hecha por un cliente sobre un servicio.
    Guarda el estado, el costo y permite procesar o cancelar.
    """

    def __init__(self, identificador: str, cliente: Cliente, servicio: Servicio, cantidad: int):
        super().__init__(identificador)

        # Se valida que los objetos recibidos sean del tipo correcto.
        if not isinstance(cliente, Cliente):
            raise ReservaError("El cliente asociado a la reserva no es válido.")
        if not isinstance(servicio, Servicio):
            raise ReservaError("El servicio asociado a la reserva no es válido.")
        if cantidad <= 0:
            raise ReservaError("La cantidad de la reserva debe ser mayor que cero.")

        self.cliente = cliente
        self.servicio = servicio
        self.cantidad = cantidad
        self.estado = "Pendiente"
        self.costo_total = 0.0

        registrar_evento(
            "INFO",
            f"Se creó la reserva {self.identificador} para el cliente {self.cliente.nombre}."
        )

    def procesar(self, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        """
        Procesa la reserva y calcula el valor total.
        Aquí se usa try/except/else/finally para cumplir con la guía.
        """
        try:
            # Primero se verifica la disponibilidad del servicio.
            if not self.servicio.disponible:
                raise ServicioNoDisponibleError(
                    f"El servicio {self.servicio.nombre} no está disponible."
                )

            # Luego se calcula el costo.
            self.costo_total = self.servicio.calcular_costo(
                cantidad=self.cantidad,
                impuesto=impuesto,
                descuento=descuento
            )
            self.estado = "Confirmada"

        except Exception as e:
            # Si algo falla, se registra y se vuelve a lanzar el error.
            registrar_evento("ERROR", f"Error al procesar la reserva {self.identificador}: {e}")
            raise

        else:
            # Solo entra aquí si no ocurrió ningún error.
            registrar_evento(
                "INFO",
                f"Reserva {self.identificador} confirmada correctamente con costo {self.costo_total}."
            )
            return self.costo_total

        finally:
            # Este bloque siempre se ejecuta, ocurra o no un error.
            registrar_evento("INFO", f"Finalizó el intento de procesamiento de la reserva {self.identificador}.")

    def cancelar(self) -> None:
        """
        Cancela una reserva si todavía no había sido cancelada.
        """
        try:
            if self.estado == "Cancelada":
                raise ReservaError("La reserva ya estaba cancelada.")

            self.estado = "Cancelada"
            registrar_evento("INFO", f"Reserva {self.identificador} cancelada correctamente.")

        except Exception as e:
            registrar_evento("ERROR", f"Error al cancelar la reserva {self.identificador}: {e}")
            raise

    def describir(self) -> str:
        return (
            f"Reserva {self.identificador} | Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | Cantidad: {self.cantidad} | "
            f"Estado: {self.estado} | Costo: {self.costo_total}"
        )

    def __str__(self):
        return self.describir()