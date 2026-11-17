# Fase 2 — Abstracción y modelado de datos

Aplicación de escritorio en Python para el caso del restaurante Sabor & Sazón. Permite registrar clientes, consultar el precio del menú elegido y calcular el valor total según el número de sesiones.

## Ejecutar

Requiere Python 3 y Tkinter. Desde esta carpeta, ejecuta:

```bash
python main.py
```

La aplicación guarda los registros en memoria; al cerrarla, se borran.

## Archivos principales

- `main.py`: interfaz gráfica y flujo de registro y consulta.
- `gestion_clientes.py`: datos, validaciones, tarifas y cálculo del total.
- `pruebas_gestion_clientes.py`: comprobaciones incluidas con el proyecto.
- `docs/abstraccion/abstraccion-fase2.md`: tabla de abstracción en formato Markdown.
- `logo_sabor_sazon.png`: recurso visual de la aplicación.

## Cálculo

`total = número de sesiones × tarifa del menú`

La tabla de abstracción está transcrita en Markdown para que GitHub pueda mostrarla directamente. Este repositorio no incluye la guía de la actividad ni la plantilla gráfica institucional.
