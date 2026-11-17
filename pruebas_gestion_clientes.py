# -*- coding: utf-8 -*-
"""Pruebas de la lógica de la aplicación Sabor & Sazón.

Se ejecutan sin Tkinter:  python pruebas_gestion_clientes.py
"""

from gestion_clientes import (CLAVE_ACCESO, MENUS, GestionClientes,
                              formatear_pesos)


def esperar_error(funcion, *args, **kwargs):
    try:
        funcion(*args, **kwargs)
    except ValueError:
        return True
    return False


def main():
    pruebas = []

    # 1. Tabla de valores del Anexo 1
    esperado = {"Menú ejecutivo": 35000, "Menú vegetariano": 28000,
                "Menú degustación": 75000, "Menú infantil": 20000,
                "Menú gourmet": 95000}
    pruebas.append(("Tabla de menús del Anexo 1", MENUS == esperado))

    # 2. Fórmula: costo_total = sesiones x costo_sesion
    g = GestionClientes()
    casos = [(1, 35000, 35000), (3, 35000, 105000), (4, 75000, 300000),
             (5, 20000, 100000), (2, 95000, 190000)]
    for sesiones, costo, total in casos:
        pruebas.append((f"cálculo {sesiones} x {costo}", g.calcular_costo_total(sesiones, costo) == total))

    # 3. Clave de acceso
    pruebas.append(("clave correcta", g.validar_acceso(CLAVE_ACCESO) is True))
    pruebas.append(("clave incorrecta", g.validar_acceso("0000") is False))

    # 4. Consulta del costo por menú
    pruebas.append(("costo gourmet", g.consultar_costo_sesion("Menú gourmet") == 95000))
    pruebas.append(("menú inválido", esperar_error(g.consultar_costo_sesion, "Menú espacial")))

    # 5. Guardar registro correcto
    registro = g.guardar_registro("1023456789", "Ana María Pérez", "Femenino",
                                  "Menú degustación", 3)
    pruebas.append(("registro guardado", registro["costo_total"] == 225000))
    pruebas.append(("historial con 1 registro", len(g.registros) == 1))
    pruebas.append(("fecha automática", bool(registro["fecha_registro"])))
    pruebas.append(("resumen con datos", "Costo total" in g.resumen_reporte()))

    # 6. Validaciones del formulario
    validaciones = [
        ("identificación vacía", ("", "Ana Pérez", "Femenino", "Menú infantil", 1)),
        ("identificación con letras", ("ABC123", "Ana Pérez", "Femenino", "Menú infantil", 1)),
        ("nombre muy corto", ("123", "Al", "Femenino", "Menú infantil", 1)),
        ("sin género", ("123", "Ana Pérez", "", "Menú infantil", 1)),
        ("sin menú", ("123", "Ana Pérez", "Femenino", "", 1)),
        ("sesiones en texto", ("123", "Ana Pérez", "Femenino", "Menú infantil", "dos")),
        ("sesiones en cero", ("123", "Ana Pérez", "Femenino", "Menú infantil", 0)),
        ("sesiones negativas", ("123", "Ana Pérez", "Femenino", "Menú infantil", -3)),
        ("sesiones excesivas", ("123", "Ana Pérez", "Femenino", "Menú infantil", 500)),
    ]
    for nombre, args in validaciones:
        pruebas.append((f"rechaza {nombre}", esperar_error(g.guardar_registro, *args)))

    # 7. Varios registros y total recaudado
    g.guardar_registro("987654321", "Carlos Ruiz", "Masculino", "Menú ejecutivo", 2)
    g.guardar_registro("555555", "Luisa Gómez", "Femenino", "Menú infantil", 4)
    pruebas.append(("3 registros", len(g.registros) == 3))
    pruebas.append(("total recaudado", g.total_recaudado() == 225000 + 70000 + 80000))

    # 8. Formato de pesos colombianos
    pruebas.append(("formato 35000", formatear_pesos(35000) == "$ 35.000"))
    pruebas.append(("formato 225000", formatear_pesos(225000) == "$ 225.000"))

    fallos = [nombre for nombre, ok in pruebas if not ok]
    for nombre, ok in pruebas:
        print(f"  [{'OK' if ok else 'FALLO'}] {nombre}")
    print(f"\n{len(pruebas) - len(fallos)}/{len(pruebas)} pruebas correctas")
    if fallos:
        print("Fallaron:", ", ".join(fallos))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
