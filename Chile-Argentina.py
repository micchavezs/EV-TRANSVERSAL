from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from geopy.exc import GeocoderServiceError, GeocoderTimedOut


def obtener_coordenadas(ciudad, pais):
    """
    Busca las coordenadas geográficas de una ciudad.
    """
    geolocalizador = Nominatim(
        user_agent="calculadora_viajes_chile_argentina"
    )

    ubicacion = geolocalizador.geocode(
        f"{ciudad}, {pais}",
        exactly_one=True,
        timeout=10
    )

    if ubicacion is None:
        return None

    return ubicacion.latitude, ubicacion.longitude


def seleccionar_transporte():
    """
    Permite seleccionar el medio de transporte.
    Retorna el nombre del transporte y su velocidad promedio.
    """
    transportes = {
        "1": ("Automóvil", 80),
        "2": ("Autobús", 70),
        "3": ("Motocicleta", 75),
        "4": ("Bicicleta", 20),
        "5": ("A pie", 5)
    }

    print("\nSeleccione un medio de transporte:")
    print("1. Automóvil")
    print("2. Autobús")
    print("3. Motocicleta")
    print("4. Bicicleta")
    print("5. A pie")

    opcion = input("Ingrese una opción: ").strip().lower()

    if opcion == "s":
        return None

    return transportes.get(opcion)


def convertir_duracion(horas_totales):
    """
    Convierte un número decimal de horas en días, horas y minutos.
    """
    minutos_totales = round(horas_totales * 60)

    dias = minutos_totales // 1440
    minutos_restantes = minutos_totales % 1440

    horas = minutos_restantes // 60
    minutos = minutos_restantes % 60

    return dias, horas, minutos


def mostrar_duracion(dias, horas, minutos):
    """
    Genera un texto legible con la duración del viaje.
    """
    partes = []

    if dias > 0:
        partes.append(f"{dias} día(s)")

    if horas > 0:
        partes.append(f"{horas} hora(s)")

    if minutos > 0:
        partes.append(f"{minutos} minuto(s)")

    if not partes:
        return "menos de un minuto"

    return ", ".join(partes)


def main():
    print("=" * 55)
    print("      CALCULADORA DE VIAJES CHILE - ARGENTINA")
    print("=" * 55)
    print("Puede escribir la letra 's' para salir del programa.")

    while True:
        ciudad_origen = input(
            "\nIngrese la Ciudad de Origen en Chile: "
        ).strip()

        if ciudad_origen.lower() == "s":
            print("\nPrograma finalizado.")
            break

        ciudad_destino = input(
            "Ingrese la Ciudad de Destino en Argentina: "
        ).strip()

        if ciudad_destino.lower() == "s":
            print("\nPrograma finalizado.")
            break

        transporte = seleccionar_transporte()

        if transporte is None:
            print("\nPrograma finalizado.")
            break

        nombre_transporte, velocidad_promedio = transporte

        try:
            print("\nBuscando las ciudades...")

            coordenadas_origen = obtener_coordenadas(
                ciudad_origen,
                "Chile"
            )

            coordenadas_destino = obtener_coordenadas(
                ciudad_destino,
                "Argentina"
            )

            if coordenadas_origen is None:
                print(
                    f"No fue posible encontrar la ciudad "
                    f"'{ciudad_origen}' en Chile."
                )
                continue

            if coordenadas_destino is None:
                print(
                    f"No fue posible encontrar la ciudad "
                    f"'{ciudad_destino}' en Argentina."
                )
                continue

            distancia_km = geodesic(
                coordenadas_origen,
                coordenadas_destino
            ).kilometers

            distancia_millas = distancia_km * 0.621371
            duracion_horas = distancia_km / velocidad_promedio

            dias, horas, minutos = convertir_duracion(duracion_horas)
            texto_duracion = mostrar_duracion(dias, horas, minutos)

            print("\n" + "=" * 55)
            print("RESULTADOS DEL VIAJE")
            print("=" * 55)
            print(f"Ciudad de Origen     : {ciudad_origen}, Chile")
            print(f"Ciudad de Destino    : {ciudad_destino}, Argentina")
            print(f"Medio de transporte  : {nombre_transporte}")
            print(f"Distancia aproximada : {distancia_km:.2f} kilómetros")
            print(f"Distancia en millas  : {distancia_millas:.2f} millas")
            print(f"Duración estimada    : {texto_duracion}")

            print("\nNarrativa del viaje:")
            print(
                f"El viaje comenzará en {ciudad_origen}, Chile, "
                f"y finalizará en {ciudad_destino}, Argentina. "
                f"Se utilizará {nombre_transporte.lower()} como medio "
                f"de transporte. La distancia aproximada entre ambas "
                f"ciudades es de {distancia_km:.2f} kilómetros, "
                f"equivalentes a {distancia_millas:.2f} millas. "
                f"Considerando una velocidad promedio de "
                f"{velocidad_promedio} km/h, el viaje tendría una "
                f"duración estimada de {texto_duracion}."
            )

            print("\nNota: la distancia se calcula en línea recta y la")
            print("duración es una estimación según la velocidad promedio.")

        except (GeocoderTimedOut, GeocoderServiceError):
            print("\nNo fue posible conectarse al servicio de ubicación.")
            print("Revise su conexión a Internet e inténtelo nuevamente.")

        except Exception as error:
            print(f"\nSe produjo un error inesperado: {error}")

        continuar = input(
            "\nPresione Enter para calcular otro viaje o 's' para salir: "
        ).strip().lower()

        if continuar == "s":
            print("\nPrograma finalizado.")
            break


if __name__ == "__main__":
    main()
