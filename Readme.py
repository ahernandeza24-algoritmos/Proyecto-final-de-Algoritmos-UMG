import os
def limpiar_pantalla():
    """Limpia la consola segun el sistema operativo."""
    os.system('cls' if os.name == 'nt' else 'clear')
def pausar():
        """Pausa la ejecución para que el usuario puede leer los resultados."""
        input('\nPresione Enter para regresar al menú principal...') 

def modulo_productos():
      limpiar_pantalla()
      print("=== MÓDULO DE GESTIÓN DE PRODUCTOS ===")
      print("Aqui se podrá agregar, modificar y eliminar productos.")

      pausar()

def modulo_inventario():
      limpiar_pantalla()
      print("=== MODULO DE CONTROL DE INVENTRIOS ===")
      print("aqui se realizarán los ajustes de stock y alertas de niveles bajos.")
      pausar()

def modulo_ventas():
      limpiar_pantalla()
      print("=== MÓDULO DE REGISTRO DE VENTAS ===")
      print("Aqui se procesarán las transacciones comerciales.")
      pausar()

def modulo_reportes():
      limpiar_pantalla()
      print("=== MÓDULO DE REPORTES ESTADÍSTICOS ===") 
      pausar()

def menu_principal(): 
    """Muestra y valida las opciones del menú principal."""
    while True: 
        limpiar_pantalla() 
        print("   SISTEMA DE GESTIÓN COMERCIAL (POS)   ")
        print("1. Administrar Productos")
        print("2. Control de Inventarios")
        print("3. Registrar Ventas")
        print("4. Reportes Estadísticos")
        print("5. Salir del Sistema")
        
        try:
            opcion = int(input("Seleccione una opción (1-5): "))
            
            if opcion == 1:
                modulo_productos()
            elif opcion == 2:
                modulo_inventarios()
            elif opcion == 3:
                modulo_ventas()
            elif opcion == 4:
                modulo_reportes()
            elif opcion == 5:
                print("\nCerrando el sistema de forma segura. ¡Hasta luego!")
                break
            else:
                print("\n[Error] Opción no válida. Elija un número entre 1 y 5.")
                pausar()
if __name__ == "__main__":
menu_principal()
