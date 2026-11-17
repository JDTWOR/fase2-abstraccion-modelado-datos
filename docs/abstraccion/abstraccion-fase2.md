# Tabla de abstracción — Fase 2

**Estudiante:** Jhon Deivid Rojas Rodriguez<br>
**Curso:** Estructura de Datos (301305)<br>
**Grupo colaborativo:** 298

**Planteamiento:** El restaurante Sabor & Sazón necesita registrar clientes, calcular el valor de las sesiones consumidas y presentar un reporte. La aplicación también controla el acceso.

| Clase y visibilidad | Atributos y tipos | Métodos y responsabilidad | Regla de cálculo |
|---|---|---|---|
| `GestionClientes` — pública. Administra los registros del cliente y los cálculos del servicio. | `identificacion: str`<br>`nombre_completo: str`<br>`genero: str`<br>`tipo_menu: str`<br>`numero_sesiones: int`<br>`fecha_registro: str`<br>`costo_sesion: float`<br>`costo_total: float`<br>`registros: list[dict]` | `validar_acceso(clave)` comprueba la clave de acceso.<br>`consultar_costo_sesion(tipo_menu)` obtiene la tarifa del menú.<br>`guardar_registro(...)` valida y almacena el cliente.<br>`calcular_costo_total(...)` calcula el valor del servicio.<br>`resumen_reporte()` presenta el último registro.<br>`total_recaudado()` suma los totales guardados. | `costo_total = número de sesiones × costo por sesión`<br>`costo por sesión = tarifa del menú elegido` |

*Nota.* Esta tabla resume la clase implementada en `gestion_clientes.py`.
