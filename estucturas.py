"""Estructuras y funciones del sistema de gestión comercial."""

def menu_principal():
    
    
    while True:

        print("=================================================")
        print("     SISTEMA DE GESTIÓN COMERCIAL v1.0.0         ")
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
            print("💾 Guardando estados y cerrando flujos de datos...")
            guardar_datos(ARCHIVOPRODUCTOS, productos)
            guardar_datos(ARCHIVOVENTAS, ventas)
            print("👋 Muchas gracias por utilizar nuestro sistema comercial. ¡Hasta pronto!")
            break
        else:
            print("❌ Opción inválida. Ingrese un número entre 1 y 4.")
            pausar()

if __name__ == "__main__":
    menu_principal()