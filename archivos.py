def limpiar_pantalla ():
        def id_prod():
            if id_prod in productos:
                print(f"🔄 El producto ya existe. Se actualizarán los valores e incrementará el stock.")
                productos[id_prod]["nombre"] = nombre if nombre else productos[id_prod]["nombre"]
                productos[id_prod]["precio"] = precio if precio > 0 else productos[id_prod]["precio"]
                productos[id_prod]["stock"] += stock
            else:
                if not nombre:
                    print("❌ El nombre es requerido para productos nuevos.")
                    pausar()
                
                productos[id_prod] = {"nombre": nombre, "precio": precio, "stock": stock}
            
            guardar_datos(ARCHIVOPRODUCTOS, productos)
            print("✅ Producto procesado y guardado correctamente.")
            pausar()