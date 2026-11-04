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