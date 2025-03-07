# Sistema de Gestión de Inventario en Python (Paradigma Imperativo)

# Estructura de datos para almacenar el inventario
inventario = []

# Función auxiliar para buscar un producto en el inventario
def obtener_producto(nombre):
    nombre = nombre.lower()
    for producto in inventario:
        if producto["nombre"].lower() == nombre:
            return producto
    return None

# Función para agregar un producto
def agregar_producto(nombre, cantidad):
    if obtener_producto(nombre):
        print(f"El producto '{nombre}' ya existe en el inventario.")
        return
    inventario.append({"nombre": nombre, "cantidad": cantidad})
    print(f"Producto '{nombre}' agregado con éxito.")

# Función para buscar un producto
def buscar_producto(nombre):
    producto = obtener_producto(nombre)
    if producto:
        print(f"Producto encontrado: {producto['nombre']} - Cantidad: {producto['cantidad']}")
    else:
        print(f"El producto '{nombre}' no existe en el inventario.")

# Función para actualizar la cantidad de un producto
def actualizar_cantidad(nombre, nueva_cantidad):
    producto = obtener_producto(nombre)
    if producto:
        producto["cantidad"] = nueva_cantidad
        print(f"Cantidad de '{nombre}' actualizada a {nueva_cantidad}.")
    else:
        print(f"El producto '{nombre}' no existe en el inventario.")

# Función para mostrar el inventario completo
def mostrar_inventario():
    if not inventario:
        print("El inventario está vacío.")
    else:
        print("Inventario:")
        for producto in inventario:
            print(f"- {producto['nombre']}: {producto['cantidad']} unidades")

# Menú principal
while True:
    print("\nOpciones:")
    print("1. Agregar producto")
    print("2. Buscar producto")
    print("3. Actualizar cantidad")
    print("4. Mostrar inventario")
    print("5. Salir")

    opcion = input("Ingrese la opción deseada: ")

    if opcion == "1":
        nombre = input("Ingrese el nombre del producto: ")
        cantidad = int(input("Ingrese la cantidad: "))
        agregar_producto(nombre, cantidad)
    elif opcion == "2":
        nombre = input("Ingrese el nombre del producto a buscar: ")
        buscar_producto(nombre)
    elif opcion == "3":
        nombre = input("Ingrese el nombre del producto a actualizar: ")
        nueva_cantidad = int(input("Ingrese la nueva cantidad: "))
        actualizar_cantidad(nombre, nueva_cantidad)
    elif opcion == "4":
        mostrar_inventario()
    elif opcion == "5":
        break
    else:
        print("Opción inválida. Intente de nuevo.")

print("¡Hasta luego!")