 # Ejercicio 8: Venta de vehículo con control de stock



# Catalogo de vehiculos del concesionario
stock = [
    {"id": 1, "modelo": "Sedán Clásico", "anio": 2022,
     "precio": 68000000, "unidades": 3},
    {"id": 2, "modelo": "Hatchback Urbano", "anio": 2023,
     "precio": 52000000, "unidades": 5},
    {"id": 3, "modelo": "SUV Familiar", "anio": 2024,
     "precio": 125000000, "unidades": 2},
    {"id": 4, "modelo": "Pickup Trabajo", "anio": 2021,
     "precio": 89000000, "unidades": 0},
    {"id": 5, "modelo": "Compacto Básico", "anio": 2024,
     "precio": 43000000, "unidades": 7}
]


# Funcion para mostrar valores en pesos colombianos
def formato_pesos(valor):
    return "$" + format(round(valor), ",").replace(",", ".")


# Funcion para pedir y validar numeros enteros
def pedir_entero(mensaje, minimo=None, maximo=None,
                 min_digitos=None, max_digitos=None):
    while True:
        dato = input(mensaje).strip()

        if not dato.isdigit():
            print("Se esperaba un numero entero positivo. Recibido:", dato)
            continue

        if min_digitos is not None and len(dato) < min_digitos:
            print("El numero debe tener minimo", min_digitos,
                  "digitos. Recibido:", dato)
            continue

        if max_digitos is not None and len(dato) > max_digitos:
            print("El numero debe tener maximo", max_digitos,
                  "digitos. Recibido:", dato)
            continue

        numero = int(dato)

        if minimo is not None and numero < minimo:
            print("El numero debe ser mayor o igual a",
                  minimo, ". Recibido:", dato)
            continue

        if maximo is not None and numero > maximo:
            print("El numero debe ser menor o igual a",
                  maximo, ". Recibido:", dato)
            continue

        return numero


# Funcion para pedir y validar texto
def pedir_texto(mensaje):
    while True:
        texto = input(mensaje).strip()

        if texto:
            return texto.title()

        print("Se esperaba un texto que no estuviera vacio.")


# Funcion para preguntar si o no
def pedir_si_no(mensaje):
    while True:
        respuesta = input(mensaje).strip().upper()

        if respuesta in ["S", "SI", "SÍ"]:
            return True
        elif respuesta in ["N", "NO"]:
            return False
        else:
            print("Se esperaba S, SI, N o NO. Recibido:", respuesta)


# Funcion para mostrar el catalogo
def mostrar_catalogo():
    print("\n===== VEHICULOS DEL CONCESIONARIO =====")

    for vehiculo in stock:
        estado = "AGOTADO" if vehiculo["unidades"] == 0 else "Disponible"

        print("--------------------------------------")
        print("ID:", vehiculo["id"])
        print("Modelo:", vehiculo["modelo"])
        print("Año:", vehiculo["anio"])
        print("Precio:", formato_pesos(vehiculo["precio"]))
        print("Unidades disponibles:", vehiculo["unidades"])
        print("Estado:", estado)


# Funcion para elegir un vehiculo disponible
def elegir_vehiculo():
    while True:
        id_buscado = pedir_entero(
            "Digite el ID del vehiculo que desea: ", minimo=1
        )

        vehiculo_encontrado = None

        for vehiculo in stock:
            if vehiculo["id"] == id_buscado:
                vehiculo_encontrado = vehiculo
                break

        if vehiculo_encontrado is None:
            print("No existe un vehiculo con ese ID.")
        elif vehiculo_encontrado["unidades"] == 0:
            print("El vehiculo esta agotado. Elija otro.")
        else:
            return vehiculo_encontrado


# Funcion para validar la cantidad de unidades
def pedir_cantidad(vehiculo):
    return pedir_entero(
        "Cuantas unidades desea comprar: ",
        minimo=1,
        maximo=vehiculo["unidades"]
    )


# Funcion para calcular la cuota mensual
def calcular_cuota_mensual(saldo, plazo):
    tasa_anual = 0.16
    interes = saldo * tasa_anual * (plazo / 12)
    total_financiado = saldo + interes
    cuota_mensual = total_financiado / plazo

    return interes, total_financiado, cuota_mensual


# Funcion para mostrar alternativas viables
def mostrar_alternativas(dinero_disponible, capacidad_pago, plazo):
    print("\n===== ALTERNATIVAS VIABLES =====")
    hay_alternativas = False

    for vehiculo in stock:
        if vehiculo["unidades"] > 0:
            precio = vehiculo["precio"]

            # Se calcula cuantas unidades puede comprar
            # respetando el minimo del 20 por ciento inicial
            cantidad_maxima = min(
                vehiculo["unidades"],
                int(dinero_disponible // (precio * 0.20))
            )

            if cantidad_maxima >= 1:
                precio_total = precio * cantidad_maxima
                cuota_inicial = dinero_disponible
                saldo = max(0, precio_total - cuota_inicial)

                interes, total_financiado, cuota = (
                    calcular_cuota_mensual(saldo, plazo)
                )

                if cuota <= capacidad_pago:
                    print("--------------------------------------")
                    print("Modelo:", vehiculo["modelo"])
                    print("Cantidad posible:", cantidad_maxima)
                    print("Precio total:", formato_pesos(precio_total))
                    print("Cuota inicial disponible:",
                          formato_pesos(cuota_inicial))
                    print("Cuota mensual estimada:", formato_pesos(cuota))
                    hay_alternativas = True

    if not hay_alternativas:
        print("No se encontraron vehiculos que cumplan ambas condiciones.")
        print("Dinero disponible para cuota inicial:",
              formato_pesos(dinero_disponible))
        print("Capacidad de pago mensual:",
              formato_pesos(capacidad_pago))

        print("\nFaltante para la cuota inicial de cada modelo disponible:")
        for vehiculo in stock:
            if vehiculo["unidades"] > 0:
                cuota_minima = vehiculo["precio"] * 0.20
                faltante = max(0, cuota_minima - dinero_disponible)

                print(
                    vehiculo["modelo"],
                    "- Faltante:", formato_pesos(faltante)
                )


# Funcion para mostrar el inventario actualizado
def mostrar_inventario():
    print("\n===== INVENTARIO ACTUALIZADO =====")

    for vehiculo in stock:
        estado = "AGOTADO" if vehiculo["unidades"] == 0 else "Disponible"

        print(
            "ID:", vehiculo["id"],
            "| Modelo:", vehiculo["modelo"],
            "| Año:", vehiculo["anio"],
            "| Precio:", formato_pesos(vehiculo["precio"]),
            "| Unidades:", vehiculo["unidades"],
            "| Estado:", estado
        )

# Funcion principal del programa
def venta_vehiculo():
    print("===== SISTEMA DE VENTA DE VEHICULOS =====")

    # Mostrar catalogo inicial
    mostrar_catalogo()

    # Solicitar datos del cliente
    print("\n===== DATOS DEL CLIENTE =====")

    nombre = pedir_texto("Nombre completo del cliente: ")

    documento = pedir_entero(
        "Numero de documento (entre 6 y 10 digitos): ",
        min_digitos=6,
        max_digitos=10
    )

    ingresos = pedir_entero(
        "Ingresos mensuales: ", minimo=1
    )

    gastos = pedir_entero(
        "Gastos mensuales: ", minimo=0
    )

    ahorros = pedir_entero(
        "Ahorros para la cuota inicial: ", minimo=0
    )

    # Preguntar si entrega otro vehiculo como parte de pago
    entrega_vehiculo = pedir_si_no(
        "Entrega un vehiculo como parte de pago? (S/N): "
    )

    if entrega_vehiculo:
        valor_parte_pago = pedir_entero(
            "Valor del vehiculo que entrega: ", minimo=1
        )
    else:
        valor_parte_pago = 0

    # Elegir vehiculo y cantidad
    vehiculo = elegir_vehiculo()
    cantidad = pedir_cantidad(vehiculo)

    # Solicitar y validar el plazo
    while True:
        plazo = pedir_entero(
            "Plazo de financiacion (12 a 84 meses): ",
            minimo=12,
            maximo=84
        )

        if plazo % 12 == 0:
            break

        print("El plazo debe ser multiplo de 12. Recibido:", plazo)

    # Calcular precio total y cuota inicial
    precio_total = vehiculo["precio"] * cantidad
    cuota_inicial = ahorros + valor_parte_pago
    cuota_minima = precio_total * 0.20
    porcentaje_cuota = cuota_inicial / precio_total * 100

    # Calcular capacidad de pago
    capacidad_pago = (ingresos - gastos) * 0.30

    # Mostrar resumen de la seleccion
    print("\n===== RESUMEN DE LA SELECCION =====")
    print("Cliente:", nombre)
    print("Documento:", documento)
    print("Vehiculo:", vehiculo["modelo"])
    print("Año:", vehiculo["anio"])
    print("Cantidad:", cantidad)
    print("Precio total:", formato_pesos(precio_total))
    print("Ahorros:", formato_pesos(ahorros))
    print("Parte de pago:", formato_pesos(valor_parte_pago))
    print("Cuota inicial disponible:", formato_pesos(cuota_inicial))
    print("Porcentaje de cuota inicial:", round(porcentaje_cuota, 2), "%")
    print("Cuota inicial minima:", formato_pesos(cuota_minima))

    # Validar que la cuota inicial alcance el 20 por ciento
    if cuota_inicial < cuota_minima:
        faltante = cuota_minima - cuota_inicial

        print("\nVENTA NO CONTINUA")
        print("La cuota inicial no alcanza el 20 por ciento requerido.")
        print("Faltante para este vehiculo:", formato_pesos(faltante))

        mostrar_alternativas(cuota_inicial, capacidad_pago, plazo)
        return

    # Calcular saldo e intereses segun el plazo elegido
    saldo_financiar = max(0, precio_total - cuota_inicial)

    interes, total_financiado, cuota_mensual = (
        calcular_cuota_mensual(saldo_financiar, plazo)
    )

    # Mostrar desglose financiero
    print("\n===== DESGLOSE FINANCIERO =====")
    print("Precio total:", formato_pesos(precio_total))
    print("Cuota inicial:", formato_pesos(cuota_inicial))
    print("Saldo a financiar:", formato_pesos(saldo_financiar))
    print("Interes simple total:", formato_pesos(interes))
    print("Total financiado con intereses:",
          formato_pesos(total_financiado))
    print("Plazo:", plazo, "meses")
    print("Cuota mensual:", formato_pesos(cuota_mensual))
    print("Capacidad de pago mensual:", formato_pesos(capacidad_pago))

    # Aprobar o rechazar la venta
    if cuota_mensual <= capacidad_pago:
        print("\nVENTA APROBADA")
        print("La cuota mensual cabe dentro de la capacidad de pago.")

        # Descontar unidades unicamente cuando se aprueba la venta
        vehiculo["unidades"] -= cantidad

        print("La compra se registro correctamente.")
        mostrar_inventario()

    else:
        print("\nVENTA RECHAZADA")
        print("La cuota mensual supera la capacidad de pago.")
        mostrar_alternativas(cuota_inicial, capacidad_pago, plazo)

        # El inventario no cambia cuando se rechaza la venta
        mostrar_inventario()


# Ejecutar el programa
venta_vehiculo()