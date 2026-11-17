"""Registro de clientes y cálculo de costos para Sabor & Sazón."""

from datetime import datetime

# Clave de acceso genérica exigida por el Anexo 1 (se digita enmascarada)
CLAVE_ACCESO = "1793"

# Tabla 2 del Anexo 1: costo por sesión según el tipo de menú
MENUS = {
    "Menú ejecutivo": 35000,
    "Menú vegetariano": 28000,
    "Menú degustación": 75000,
    "Menú infantil": 20000,
    "Menú gourmet": 95000,
}

GENEROS = ("Masculino", "Femenino")

# Límite de sesiones permitido: evita valores absurdos o negativos
MAX_SESIONES = 100


def formatear_pesos(valor):
    """Devuelve un valor numérico en formato de pesos colombianos: $ 35.000"""
    try:
        return "$ " + f"{float(valor):,.0f}".replace(",", ".")
    except (TypeError, ValueError):
        return "$ 0"


class GestionClientes:
    """Datos del cliente y registros guardados durante la sesión."""

    def __init__(self):
        self.identificacion = ""
        self.nombre_completo = ""
        self.genero = ""
        self.tipo_menu = ""
        self.numero_sesiones = 0
        self.fecha_registro = ""
        self.costo_sesion = 0.0
        self.costo_total = 0.0
        self.registros = []          # historial de registros guardados

    def validar_acceso(self, clave):
        """Comprueba la contraseña de ingreso a la aplicación."""
        return str(clave) == CLAVE_ACCESO

    def consultar_costo_sesion(self, tipo_menu):
        """Devuelve el costo por sesión del menú seleccionado."""
        if tipo_menu not in MENUS:
            raise ValueError("Debe seleccionar un tipo de menú válido.")
        return MENUS[tipo_menu]

    def guardar_registro(self, identificacion, nombre_completo, genero, tipo_menu,
                         numero_sesiones, fecha_registro=None):
        """Guarda el registro después de validar los datos."""
        identificacion = str(identificacion).strip()
        nombre_completo = " ".join(str(nombre_completo).split())

        if not identificacion:
            raise ValueError("La identificación es obligatoria.")
        if not identificacion.isdigit():
            raise ValueError("La identificación debe contener solo números, sin espacios ni guiones.")
        if len(nombre_completo) < 3:
            raise ValueError("El nombre completo es obligatorio (mínimo 3 letras).")
        if not any(character.isalpha() for character in nombre_completo) or not all(
            character.isalpha() or character.isspace() or character in "-'’"
            for character in nombre_completo
        ):
            raise ValueError("El nombre completo solo debe contener letras, espacios o guiones.")
        if genero not in GENEROS:
            raise ValueError("Debe seleccionar el género.")
        if tipo_menu not in MENUS:
            raise ValueError("Debe seleccionar el tipo de menú.")

        try:
            sesiones = int(str(numero_sesiones).strip())
        except (TypeError, ValueError):
            raise ValueError("El número de sesiones debe ser un número entero.")
        if sesiones < 1:
            raise ValueError("El número de sesiones debe ser mayor que cero.")
        if sesiones > MAX_SESIONES:
            raise ValueError(f"El número de sesiones no puede superar {MAX_SESIONES}.")

        costo_sesion = self.consultar_costo_sesion(tipo_menu)
        total = self.calcular_costo_total(sesiones, costo_sesion)

        self.identificacion = identificacion
        self.nombre_completo = nombre_completo
        self.genero = genero
        self.tipo_menu = tipo_menu
        self.numero_sesiones = sesiones
        self.fecha_registro = fecha_registro or datetime.now().strftime("%Y-%m-%d %H:%M")
        self.costo_sesion = costo_sesion
        self.costo_total = total

        registro = {
            "identificacion": self.identificacion,
            "nombre_completo": self.nombre_completo,
            "genero": self.genero,
            "tipo_menu": self.tipo_menu,
            "numero_sesiones": self.numero_sesiones,
            "fecha_registro": self.fecha_registro,
            "costo_sesion": self.costo_sesion,
            "costo_total": self.costo_total,
        }
        self.registros.append(registro)
        return registro

    def calcular_costo_total(self, numero_sesiones, costo_sesion):
        """Multiplica el número de sesiones por el costo de cada una."""
        sesiones = int(numero_sesiones)
        if sesiones < 0 or float(costo_sesion) < 0:
            raise ValueError("Los valores del cálculo no pueden ser negativos.")
        return round(sesiones * float(costo_sesion), 2)

    def resumen_reporte(self):
        """Texto con los datos del último registro, listo para el reporte."""
        if not self.registros:
            return "Todavía no hay registros guardados."
        r = self.registros[-1]
        return (
            f"Identificación: {r['identificacion']}\n"
            f"Nombre completo: {r['nombre_completo']}\n"
            f"Género: {r['genero']}\n"
            f"Tipo de menú: {r['tipo_menu']}\n"
            f"Costo por sesión: {formatear_pesos(r['costo_sesion'])}\n"
            f"Número de sesiones: {r['numero_sesiones']}\n"
            f"Fecha de registro: {r['fecha_registro']}\n"
            f"Costo total del servicio: {formatear_pesos(r['costo_total'])}"
        )

    def total_recaudado(self):
        """Suma de los costos totales de todos los registros guardados."""
        return round(sum(r["costo_total"] for r in self.registros), 2)
