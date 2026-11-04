import json
import os

ARCH_PRODUCTOS = "productos.json"

def cargar_productos():
    """Carga los productos desde el archivo JSON de manera segura con codificación UTF-8."""
    if not os.path.exists(ARCH_PRODUCTOS):
        return {}
    try:
        with open(ARCH_PRODUCTOS, 'r', encoding='utf-8') as archivo:
            return json.load(archivo)
    except json.JSONDecodeError:
        print("⚠️ Error al leer la base de datos. Se iniciará con un registro vacío.")
        return {}

def guardar_productos(productos):
    """Persiste el diccionario de productos en el archivo JSON."""
    try:
        with open(ARCH_PRODUCTOS, 'w', encoding='utf-8') as archivo:
            json.dump(productos, archivo, indent=4, ensure_ascii=False)
    except IOError:
        print("❌ Error crítico: No se pudieron guardar los datos en el disco.")

def leer_flotante_positivo(mensaje):
    """Valida que la entrada del usuario sea un número decimal mayor a cero (Precio en Q)."""
    while True:
        try:
            valor = float(input(mensaje))
            if valor <= 0:
                print("❌ El precio debe ser estrictamente mayor a Q 0.00.")
                continue
            return valor
        except ValueError:
            print("❌ Entrada inválida. Por favor, ingrese un número decimal válido.")

def leer_entero_no_negativo(mensaje):
    """Valida que la entrada sea un número entero mayor o igual a cero (Cantidades)."""
    while True:
        try:
            valor = int(input(mensaje))
            if valor < 0:
                print("❌ El valor no puede ser negativo.")
                continue
            return valor
        except ValueError:
            print("❌ Entrada inválida. Por favor, ingrese un número entero válido.")

# ==========================================
# MÓDULO 1: GESTIÓN DE PRODUCTOS
# ==========================================

def registrar_producto():
    print("\n--- 📦 Registrar Nuevo Producto ---")
    productos = cargar_productos()
    
    codigo = input("Ingrese el código del producto (Único): ").strip().upper()
    if not codigo:
        print("❌ El código no puede estar vacío.")
        return
        
    if codigo in productos:
        print(f"❌ Error: Ya existe un producto registrado con el código '{codigo}'.")
        return

    nombre = input("Nombre del producto: ").strip()
    categoria = input("Categoría: ").strip()
    precio = leer_flotante_positivo("Precio de venta (en Quetzales): Q ")
    cantidad = leer_entero_no_negativo("Cantidad inicial disponible en inventario: ")
    stock_min = leer_entero_no_negativo("Stock mínimo requerido de alerta: ")

    productos[codigo] = {
        "nombre": nombre,
        "categoria": categoria,
        "precio": precio,
        "cantidad": cantidad,
        "stock_minimo": stock_min,
        "activo": True
    }
    
    guardar_productos(productos)
    print(f"✅ Producto '{nombre}' registrado exitosamente con precios fijados en Quetzales.")

def consultar_producto():
    print("\n--- 🔍 Consultar Producto por Código ---")
    productos = cargar_productos()
    codigo = input("Ingrese el código a buscar: ").strip().upper()
    
    if codigo in productos:
        prod = productos[codigo]
        estado = "Disponible" if prod["activo"] else "Desactivado (No disponible para venta)"
        print(f"\n📋 Datos del Producto [{codigo}]:")
        print(f"🔹 Nombre: {prod['nombre']}")
        print(f"🔹 Categoría: {prod['categoria']}")
        print(f"🔹 Precio de Venta: Q {prod['precio']:.2f}")
        print(f"🔹 Inventario Actual: {prod['cantidad']} unidades")
        print(f"🔹 Alerta de Stock Mínimo: {prod['stock_minimo']} unidades")
        print(f"🔹 Estado en Catálogo: {estado}")
    else:
        print("❌ El código ingresado no coincide con ningún producto del sistema.")

def listar_productos():
    print("\n--- 📋 Listado Completo de Productos ---")
    productos = cargar_productos()
    
    if not productos:
        print("No hay registros de productos en el sistema.")
        return

    print(f"{'CÓDIGO':<12} | {'NOMBRE':<25} | {'CATEGORÍA':<15} | {'PRECIO':<12} | {'STOCK':<8} | {'ESTADO':<12}")
    print("-" * 95)
    for cod, p in productos.items():
        estado = "Activo" if p["activo"] else "Inactivo"
        precio_formateado = f"Q {p['precio']:.2f}"
        print(f"{cod:<12} | {p['nombre']:<25} | {p['categoria']:<15} | {precio_formateado:<12} | {p['cantidad']:<8} | {estado:<12}")

def modificar_producto():
    print("\n--- 📝 Modificar Información de Producto ---")
    productos = cargar_productos()
    codigo = input("Ingrese el código del producto a actualizar: ").strip().upper()
    
    if codigo not in productos:
        print("❌ Código de producto no encontrado.")
        return
        
    prod = productos[codigo]
    print(f"Editando: {prod['nombre']} (Deje el campo vacío para conservar el dato actual)")
    
    nuevo_nombre = input(f"Nuevo nombre [{prod['nombre']}]: ").strip()
    if nuevo_nombre:
        prod["nombre"] = nuevo_nombre
        
    nueva_cat = input(f"Nueva categoría [{prod['categoria']}]: ").strip()
    if nueva_cat:
        prod["categoria"] = nueva_cat

    # Modificación controlada del Precio en Quetzales
    act_precio = input(f"Nuevo precio en Quetzales [{prod['precio']}]: Q ").strip()
    if act_precio:
        while True:
            try:
                val = float(act_precio)
                if val <= 0: raise ValueError
                prod["precio"] = val
                break
            except ValueError:
                print("❌ Valor inválido. Debe ingresar un valor numérico mayor a Q 0.00.")
                act_precio = input("Ingrese un precio válido: Q ").strip()

    # Modificación controlada del Stock Mínimo
    act_min = input(f"Nuevo stock mínimo de alerta [{prod['stock_minimo']}]: ").strip()
    if act_min:
        while True:
            try:
                val = int(act_min)
                if val < 0: raise ValueError
                prod["stock_minimo"] = val
                break
            except ValueError:
                print("❌ Valor numérico inválido. Debe ser un entero no negativo.")
                act_min = input("Ingrese un stock mínimo válido: ").strip()

    guardar_productos(productos)
    print("✅ La información del producto se ha actualizado en el archivo correctamente.")

def desactivar_producto():
    print("\n--- 🚫 Desactivar Producto (Baja Lógica) ---")
    productos = cargar_productos()
    codigo = input("Ingrese el código del producto a dar de baja: ").strip().upper()
    
    if codigo in productos:
        if not productos[codigo]["activo"]:
            print("⚠️ Este producto ya se encuentra registrado como Inactivo.")
        else:
            confirmar = input(f"¿Desea quitar de la venta el producto '{productos[codigo]['nombre']}'? (s/n): ").strip().lower()
            if confirmar == 's':
                productos[codigo]["activo"] = False
                guardar_productos(productos)
                print("✅ El producto fue desactivado de forma lógica en la base de datos.")
            else:
                print("Operación cancelada por el usuario.")
    else:
        print("❌ El código de producto ingresado no existe.")

# ==========================================
# MENÚ PRINCIPAL Y ARQUITECTURA DE FLUJO
# ==========================================

def menu_principal():
    while True:
        print("\n" + "="*45)
        print("🏪 SISTEMA DE GESTIÓN COMERCIAL - GUATEMALA")
        print("="*45)
        print("1. Módulo 1: Gestión de Productos")
        print("2. Módulo 2: Control de Inventarios (Bloqueado)")
        print("3. Módulo 3: Registro de Ventas (Bloqueado)")
        print("4. Módulo 4: Reportes Estadísticos (Bloqueado)")
        print("5. Salir del Sistema")
        print("="*45)
        
        opcion = input("Seleccione una opción (1-5): ").strip()
        
        if opcion == "1":
            menu_productos()
        elif opcion in ["2", "3", "4"]:
            print("\n⚙️ Opción en desarrollo. Este módulo se integrará en la fase posterior.")
            input("\nPresione Enter para retornar al menú principal...")
        elif opcion == "5":
            print("\n👋 Cierre de sesión controlado. Finalizando el programa de forma segura.")
            break
        else:
            print("❌ Error: Opción no válida. Por favor, seleccione un número del 1 al 5.")
            input("\nPresione Enter para continuar...")

def menu_productos():
    while True:
        print("\n" + "-"*40)
        print("📦 SUBMENÚ - GESTIÓN DE PRODUCTOS")
        print("-"*40)
        print("1. Registrar Producto")
        print("2. Consultar Producto por Código")
        print("3. Mostrar Listado de Productos")
        print("4. Modificar Producto")
        print("5. Desactivar Producto")
        print("6. ← Regresar al Menú Principal")
        print("-"*40)
        
        sub_opcion = input("Seleccione una operación (1-6): ").strip()
        
        if sub_opcion == "1":
            registrar_producto()
        elif sub_opcion == "2":
            consultar_producto()
        elif sub_opcion == "3":
            listar_productos()
        elif sub_opcion == "4":
            modificar_producto()
        elif sub_opcion == "5":
            desactivar_producto()
        elif sub_opcion == "6":
            break
        else:
            print("❌ Error: Selección inválida. Reintente.")
        
        input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    menu_principal()