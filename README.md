# Fase 2 — Abstracción y modelado de datos

Estudiante: Jhon Deivid Rojas Rodriguez. Grupo: 301305_298.

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
- `logo_sabor_sazon.png`: recurso visual de la aplicación.

## Cálculo

`total = número de sesiones × tarifa del menú`
