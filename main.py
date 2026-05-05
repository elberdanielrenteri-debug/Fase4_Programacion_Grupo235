# main.py
# Este es el archivo principal del sistema.
# Aquí se crean objetos, se ejecutan pruebas y se muestra un menú básico.

from modelos import (
    Cliente,
    ServicioSala,
    ServicioEquipo,
    ServicioAsesoria,
    Reserva,
)
from excepciones import (
    ClienteInvalidoError,
    ServicioNoValidoError,
    ServicioNoDisponibleError,
    ReservaError,
)
from logger import registrar_evento


# Listas donde se guardan los objetos creados.
clientes = []
servicios = []
reservas = []


def linea():
    """Imprime una línea separadora en pantalla."""
    print("-" * 75)


def ejecutar(nombre_operacion, funcion):
    """
    Ejecuta una operación y controla errores sin detener el programa.
    Esto permite que el sistema siga funcionando aunque ocurra un fallo.
    """
    print(f"\nOPERACIÓN: {nombre_operacion}")
    try:
        resultado = funcion()

        if resultado is not None:
            print("Resultado:", resultado)

        print("Estado: operación exitosa")

    except (ClienteInvalidoError, ServicioNoValidoError, ServicioNoDisponibleError, ReservaError, ValueError) as error:
        print("Error controlado:", error)
        registrar_evento("ERROR", f"{nombre_operacion}: {error}")


def crear_datos_iniciales():
    """
    Crea datos de ejemplo para poder probar el sistema.
    Se usan tanto casos válidos como inválidos.
    """
    global clientes, servicios, reservas

    # CLIENTES
    ejecutar("Crear cliente válido 1", lambda: clientes.append(Cliente("C001", "Juan Pérez", "12345678", "juan@gmail.com")))
    ejecutar("Crear cliente válido 2", lambda: clientes.append(Cliente("C002", "María López", "87654321", "maria@gmail.com")))
    ejecutar("Crear cliente inválido", lambda: clientes.append(Cliente("C003", "A", "12", "correo-mal")))

    # SERVICIOS
    ejecutar("Crear servicio sala", lambda: servicios.append(ServicioSala("S001", "Sala de juntas", 50000, 12)))
    ejecutar("Crear servicio equipo", lambda: servicios.append(ServicioEquipo("E001", "Videobeam", 30000, 5)))
    ejecutar("Crear servicio asesoría", lambda: servicios.append(ServicioAsesoria("A001", "Asesoría Python", 80000, "Programación")))

    # RESERVAS
    if len(clientes) >= 2 and len(servicios) >= 3:
        cliente1 = clientes[0]
        cliente2 = clientes[1]
        sala = servicios[0]
        equipo = servicios[1]
        asesoria = servicios[2]

        ejecutar(
            "Crear y procesar reserva de sala",
            lambda: reservas.append(Reserva("R001", cliente1, sala, 3))
        )
        if reservas:
            ejecutar("Procesar reserva R001", lambda: reservas[0].procesar(impuesto=0.19, descuento=5000))

        ejecutar(
            "Crear y procesar reserva de equipo",
            lambda: reservas.append(Reserva("R002", cliente2, equipo, 2))
        )
        if len(reservas) >= 2:
            ejecutar("Procesar reserva R002", lambda: reservas[1].procesar(impuesto=0.19, descuento=2000))

        ejecutar(
            "Crear y procesar reserva de asesoría",
            lambda: reservas.append(Reserva("R003", cliente1, asesoria, 1))
        )
        if len(reservas) >= 3:
            ejecutar("Procesar reserva R003", lambda: reservas[2].procesar(impuesto=0.19, descuento=0))

        # Casos inválidos para demostrar manejo de errores
        ejecutar("Crear reserva con cantidad inválida", lambda: Reserva("R004", cliente1, sala, 0))

        # Se desactiva la sala para probar un error de disponibilidad
        sala.disponible = False
        ejecutar("Procesar reserva con servicio no disponible", lambda: Reserva("R005", cliente2, sala, 1).procesar())
        sala.disponible = True

        # Cancelación de una reserva
        if len(reservas) >= 2:
            ejecutar("Cancelar reserva R002", lambda: reservas[1].cancelar())
            ejecutar("Cancelar nuevamente la reserva R002", lambda: reservas[1].cancelar())


def mostrar_resumen():
    """
    Muestra al final un resumen de los objetos creados.
    """
    linea()
    print("RESUMEN FINAL DEL SISTEMA")
    linea()

    print("\nCLIENTES REGISTRADOS:")
    for cliente in clientes:
        print(cliente)

    print("\nSERVICIOS REGISTRADOS:")
    for servicio in servicios:
        print(servicio)

    print("\nRESERVAS REGISTRADAS:")
    for reserva in reservas:
        print(reserva)


def menu():
    """
    Menú básico para interactuar con el sistema.
    Este menú es simple, pero sirve para mostrar funcionamiento real.
    """
    while True:
        linea()
        print("SISTEMA DE GESTIÓN DE CLIENTES, SERVICIOS Y RESERVAS")
        linea()
        print("1. Ver clientes")
        print("2. Ver servicios")
        print("3. Ver reservas")
        print("4. Ejecutar demostración automática")
        print("5. Salir")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            linea()
            print("CLIENTES")
            if not clientes:
                print("No hay clientes registrados.")
            else:
                for cliente in clientes:
                    print(cliente)

        elif opcion == "2":
            linea()
            print("SERVICIOS")
            if not servicios:
                print("No hay servicios registrados.")
            else:
                for servicio in servicios:
                    print(servicio)

        elif opcion == "3":
            linea()
            print("RESERVAS")
            if not reservas:
                print("No hay reservas registradas.")
            else:
                for reserva in reservas:
                    print(reserva)

        elif opcion == "4":
            # Se ejecuta la simulación de operaciones.
            crear_datos_iniciales()

        elif opcion == "5":
            print("Saliendo del sistema...")
            registrar_evento("INFO", "El usuario salió del sistema.")
            break

        else:
            print("Opción inválida. Intente de nuevo.")


if __name__ == "__main__":
    try:
        # Se crea información inicial antes de mostrar el menú.
        registrar_evento("INFO", "Inicio de ejecución del programa principal.")
        print("Bienvenido al sistema Software FJ")
        crear_datos_iniciales()
        mostrar_resumen()

    except Exception as e:
        # Captura general por si ocurre un error no previsto.
        registrar_evento("ERROR", f"Error inesperado en main.py: {e}")
        print("Ocurrió un error inesperado:", e)

    finally:
        # Este bloque siempre se ejecuta al final.
        print("\nEl programa terminó su ejecución.")
        registrar_evento("INFO", "Ejecución finalizada en main.py.")

    # Luego de la demostración inicial, se puede usar el menú.
    menu()