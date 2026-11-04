import os
import json
from datetime import datetime

# Configuración de archivos de almacenamiento
ARCHIVOPRODUCTOS = "productos.json"
ARCHIVOVENTAS = "ventas.json"

def cargar_datos(archivo):
    """Carga los datos desde un archivo JSON. Si no existe, devuelve un diccionario vacío."""
    if not os.path.exists(archivo):
        return {}
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"⚠️ Error al leer {archivo}. Se inicializará vacío.")
        return {}

def guardar_datos(archivo, datos):
    """Guarda los datos proporcionados en un archivo JSON con formato legible."""
    try:
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=4)
    except IOError:
        print(f"❌ Error crítico: No se pudieron guardar los datos en {archivo}.")

def limpiar_pantalla():
    """Limpia la terminal para mejorar la experiencia visual del menú."""
    os.system("cls" if os.name == "nt" else "clear")

def pausar():
    """Genera una pausa controlada antes de regresar al menú principal."""
    input("\nPresione Enter para continuar y regresar al menú...")

# --- MÓDULO DE PRODUCTOS ---

def administrar_productos (productos):
    while True:
        limpiar_pantalla()
        print("=== MÓDULO DE ADMINISTRACIÓN DE PRODUCTOS ===")
        print("1. Agregar / Actualizar Producto")
        print("2. Listar Todos los Productos")
        print("3. Consultar Stock Bajo (Alertas de Inventario)")
        print("4. Volver al Menú Principal")
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            id_prod = input("Ingrese el ID o Código del producto: ").strip()
            if not id_prod:
                print("❌ El ID no puede estar vacío.")
                pausar()
                continue
                
            nombre = input("Ingrese el nombre del producto: ").strip()
            
            try:
                precio = float(input("Ingrese el precio unitario: "))
                stock = int(input("Ingrese el stock inicial / cantidad a añadir: "))
                if precio < 0 or stock < 0:
                    print("❌ El precio y el stock no pueden ser valores negativos.")
                    pausar()
                    continue
            except ValueError:
                print("❌ Entrada inválida. El precio debe ser numérico y el stock entero.")
                pausar()
                continue
            
            if id_prod in productos:
                print(f"🔄 El producto ya existe. Se actualizarán los valores e incrementará el stock.")
                productos[id_prod]["nombre"] = nombre if nombre else productos[id_prod]["nombre"]
                productos[id_prod]["precio"] = precio if precio > 0 else productos[id_prod]["precio"]
                productos[id_prod]["stock"] += stock
            else:
                if not nombre:
                    print("❌ El nombre es requerido para productos nuevos.")
                    pausar()
                    continue
                productos[id_prod] = {"nombre": nombre, "precio": precio, "stock": stock}
            
            guardar_datos(ARCHIVOPRODUCTOS, productos)
            print("✅ Producto procesado y guardado correctamente.")
            pausar()
            
        elif opcion == "2":
            limpiar_pantalla()
            print("=== INVENTARIO GENERAL DE PRODUCTOS ===")
            if not productos:
                print("No hay productos registrados en el sistema.")
            else:
                print(f"{'ID':<10} | {'Nombre':<25} | {'Precio':<10} | {'Stock':<8}")
                print("-" * 60)
                for id_p, info in productos.items():
                    print(f"{id_p:<10} | {info['nombre']:<25} | Q{info['precio']:<9.2f} | {info['stock']:<8}")
            pausar()
            
        elif opcion == "3":
            limpiar_pantalla()
            print("=== ALERTA DE STOCK CRÍTICO (Menos de 5 unidades) ===")
            alertas = {k: v for k, v in productos.items() if v["stock"] < 5}
            if not alertas:
                print("✅ ¡Buen trabajo! Todos los productos cuentan con suficiente inventario.")
            else:
                print(f"{'ID':<10} | {'Nombre':<25} | {'Stock Actual':<12}")
                print("-" * 55)
                for id_p, info in alertas.items():
                    print(f"{id_p:<10} | {info['nombre']:<25} | 🚨 {info['stock']:<10}")
            pausar()
            
        elif opcion == "4":
            break
        else:
            print("❌ Opción no válida dentro del módulo de productos.")
            pausar()

# --- MÓDULO DE VENTAS ---
def registrar_venta(productos, ventas):
    limpiar_pantalla()
    print("=== REGISTRO DE NUEVA VENTA ===")
    if not productos:
        print("❌ No se pueden realizar ventas porque no hay productos en el sistema.")
        pausar()
        return

    id_prod = input("Ingrese el ID del producto a vender: ").strip()
    if id_prod not in productos:
        print("❌ El producto especificado no existe.")
        pausar()
        return
        
    producto = productos[id_prod]
    print(f"Producto seleccionado: {producto['nombre']} | Stock disponible: {producto['stock']} | Precio: Q{producto['precio']:.2f}")
    
    try:
        cantidad = int(input("Ingrese la cantidad a vender: "))
        if cantidad <= 0:
            print("❌ La cantidad debe ser mayor a cero.")
            pausar()
            return
        if cantidad > producto["stock"]:
            print("❌ Operación cancelada: Stock insuficiente para cubrir la demanda.")
            pausar()
            return
    except ValueError:
        print("❌ Error: Debe ingresar una cantidad entera válida.")
        pausar()
        return

    # Cálculos económicos de la venta
    subtotal = producto["precio"] * cantidad
    iva = subtotal * 0.12  # Tasa impositiva del 12%
    total = subtotal + iva
    
    # Procesar la transacción
    producto["stock"] -= cantidad
    id_venta = str(len(ventas) + 1).zfill(6)
    
    ventas[id_venta] = {
        "fecha_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "id_producto": id_prod,
        "nombre_producto": producto["nombre"],
        "cantidad": cantidad,
        "subtotal": subtotal,
        "iva": iva,
        "total": total
    }
    
    guardar_datos(ARCHIVOPRODUCTOS, productos)
    guardar_datos(ARCHIVOVENTAS, ventas)
    
    print("\n🎉 ¡VENTA REGISTRADA CON ÉXITO!")
    print(f"Ticket N°: {id_venta}")
    print(f"Subtotal:  Q{subtotal:.2f}")
    print(f"IVA (12%): Q{iva:.2f}")
    print(f"Total:     Q{total:.2f}")
    pausar()

# --- MÓDULO DE REPORTES ---
def generar_reportes(ventas):
    limpiar_pantalla()
    print("=== REPORTE ESTADÍSTICO Y ANÁLISIS DE VENTAS ===")
    if not ventas:
        print("No se registran transacciones de venta en el historial.")
        pausar()
        return

    total_ingresos = 0.0
    total_articulos = 0
    productos_vendidos = {}
    
    for v in ventas.values():
        total_ingresos += v["total"]
        total_articulos += v["cantidad"]
        prod_name = v["nombre_producto"]
        productos_vendidos[prod_name] = productos_vendidos.get(prod_name, 0) + v["cantidad"]
    
    mas_vendido = max(productos_vendidos, key=productos_vendidos.get) if productos_vendidos else "N/A"
    
    print(f"📊 Total de transacciones procesadas: {len(ventas)}")
    print(f"📦 Total de artículos vendidos:       {total_articulos}")
    print(f"💰 Ingresos totales acumulados:       Q{total_ingresos:.2f}")
    print(f"⭐ Producto estrella (más vendido):   {mas_vendido} ({productos_vendidos.get(mas_vendido, 0)} unidades)")
    print("-" * 50)
    print("Historial de ventas recientes:")
    for id_v, v in ventas.items():
        print(f"[{v['fecha_hora']}] Ticket #{id_v}: {v['nombre_producto']} x{v['cantidad']} - Total: Q{v['total']:.2f}")
    pausar()

# --- MENÚ PRINCIPAL ---
def menu_principal():
    # Inicialización y carga de bases de datos persistentes
    productos = cargar_datos(ARCHIVOPRODUCTOS)
    ventas = cargar_datos(ARCHIVOVENTAS)
    
    while True:
        limpiar_pantalla()
        print("=================================================")
        print("     SISTEMA DE GESTIÓN COMERCIAL v1.0.4         ")
        print("=================================================")
        print("1. Administrar Productos e Inventario")
        print("2. Registrar Nueva Venta")
        print("3. Consultar Reportes Estadísticos")
        print("4. Salir del Sistema")
        print("=================================================")
        
        opcion = input("Seleccione una opción (1-4): ").strip()
        
        if opcion == "1":
            administrar_productos(productos)
        elif opcion == "2":
            registrar_venta(productos, ventas)
        elif opcion == "3":
            generar_reportes(ventas)
        elif opcion == "4":
            limpiar_pantalla()
            print("💾 Guardando estados y cerrando flujos de datos...")
            guardar_datos(ARCHIVOPRODUCTOS, productos)
            guardar_datos(ARCHIVOVENTAS, ventas)
            print("👋 Muchas gracias por utilizar nuestro sistema comercial. ¡Hasta pronto!")
            break
        else:
            print("❌ Opción inválida. Ingrese un número entre 1 y 4.")
        

if __name__ == "__main__":
    menu_principal()