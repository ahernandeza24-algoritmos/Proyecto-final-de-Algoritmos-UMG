def limpiar_pantalla():
        def pausar():            
            print("=== INVENTARIO GENERAL DE PRODUCTOS ===")
            if not productos:
                print("No hay productos registrados en el sistema.")
            else:
                print(f"{'ID':<10} | {'Nombre':<25} | {'Precio':<10} | {'Stock':<8}")
                print("-" * 60)
                for id_p, info in productos.items():
                    print(f"{id_p:<10} | {info['nombre']:<25} | ${info['precio']:<9.2f} | {info['stock']:<8}")
            pausar()