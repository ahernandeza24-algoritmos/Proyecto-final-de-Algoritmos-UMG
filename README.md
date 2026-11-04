markdown
# Sistema de Gestión Comercial v1.0.0
Sistema modular automatizado desarrollado en Python para la administración integrada de catálogos de productos, control inteligente de inventarios, procesamiento seguro de ventas y analítica comercial estática.

---

## 📊 Análisis y Diseño de Procesos

El sistema implementa una arquitectura modular con persistencia de datos relacionales en archivos JSON, estructurada bajo los siguientes lineamientos funcionales:

1. **Módulo de Gestión de Productos e Inventarios:**
   - Centraliza el catálogo mediante un diccionario indexado por un código alfanumérico único.
   - Aplica filtros estrictos de validación: bloquea registros duplicados y prohíbe valores monetarios o existencias numéricas negativas.
   - Introduce un flag lógico de estado (`activo: True/False`) para dar de baja productos de forma segura sin romper la integridad referencial del histórico de ventas.
   - Monitorea constantemente la `cantidad_disponible` frente al `stock_minimo` especificado para disparar alertas preventivas de reabastecimiento.

2. **Módulo de Procesamiento de Ventas:**
   - Valida la disponibilidad e integridad del stock antes de comprometer cualquier transacción.
   - Evalúa el estado lógico del producto; si está marcado como inactivo (`activo: False`), el sistema impide la venta.
   - Deduce de manera inmediata las cantidades del inventario central tras cada venta exitosa.

3. **Persistencia Automatizada:**
   - Los archivos `productos.json` y `ventas.json` actúan como bases de datos.
   - La lectura se ejecuta al arrancar el programa y la escritura ocurre en tiempo real tras cada modificación crítica.

---

## 🗺️ Diagramas de Flujo Estructurados

### Proceso 1: Menú Principal y Validaciones
```text
[Inicio]
   │
   ▼
[Cargar archivos JSON] ──► ¿Existen? ──► (No) ──► [Inicializar Diccionarios Vacíos]
   │                                      (Sí) ──► [Cargar Datos a Memoria]
   ▼
┌───────────────────────────────────────────┐
│          MENÚ PRINCIPAL OPERATIVO         │
│  1. Administrar Módulo de Productos       │
│  2. Registrar Nueva Transacción de Venta  │
│  3. Consultar Reportes y Estadísticas     │
│  4. Salir del Sistema y Consolidar Datos  │
└───────────────────────────────────────────┘
   │
   ▼
[Leer entrada del usuario]
   │
   ▼
¿Es una opción válida (1-4)?
   ├── NO  ──► [Mostrar Error de Entrada] ──► [Pausar Pantalla] ──► (Volver al Menú)
   └── SÍ
        ├── Opción 1 ──► [Desplegar Submenú de Productos]
        ├── Opción 2 ──► [Ejecutar Flujo de Registro de Venta]
        ├── Opción 3 ──► [Procesar Métricas e Historial]
        └── Opción 4 ──► [Guardar JSONs] ──► [Cierre Controlado] ──► [Fin]
```

### Proceso 2: Alta de Productos y Reglas de Negocio
```text
[Inicio Submódulo]
   │
   ▼
[Ingresar Código de Producto]
   │
   ▼
¿El código ya existe en el diccionario?
   ├── SÍ ──► [Mostrar Error: Código Duplicado] ──► [Abortar Registro]
   └── NO
        │
        ▼
   [Solicitar: Nombre, Categoría, Precio, Cantidad y Stock Mínimo]
        │
        ▼
   ¿El Precio < 0 O la Cantidad < 0 O el Stock Mínimo < 0?
        ├── SÍ ──► [Mostrar Error: No se admiten negativos] ──► [Abortar]
        └── NO
             │
             ▼
        [Escribir nuevo nodo en diccionario con 'activo': True]
             │
             ▼
        [Guardar cambios en productos.json] ──► [Confirmación Exitosa] ──► [Fin]
```

---

## 🛠️ Tecnologías y Requisitos de Ejecución
* **Lenguaje:** Python 3.10 o superior.
* **Bibliotecas Estándar:** `os`, `json`, `datetime` (No requiere librerías externas de terceros).
* **Compatibilidad:** Multiplataforma (Windows, macOS, Linux).

---

## 🚀 Instrucciones de Despliegue y Uso

### 1. Clonar o Descargar el Proyecto
Asegúrate de colocar tanto el código fuente (`main.py`) como este archivo (`README.md`) dentro del mismo directorio de trabajo.

### 2. Ejecución desde la Terminal
Abre la consola de comandos de tu sistema operativo dentro de la carpeta del proyecto y ejecuta:
```bash
python main.py
```

### 3. Dinámica del Sistema
* El programa generará de manera automática los ficheros `productos.json` y `ventas.json` al momento de realizar la primera operación de guardado.
* Todas las entradas de datos alfabéticas y numéricas se encuentran blindadas contra fallos involuntarios (como ingresar letras en campos de precios), asegurando que tu sistema nunca se cierre abruptamente.
