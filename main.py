# -*- coding: utf-8 -*-
"""
Sabor & Sazón - Aplicación de gestión de clientes (interfaz gráfica)
Fase 2 - Fundamentos de Abstracción y Modelado de Datos
Curso: Estructura de Datos (301305-16-04) - UNAD
Grupo colaborativo: 298
Autor: Jhon Deivid Rojas Rodriguez

Ejecutar con:  python main.py
Requisitos: Python 3.8 o superior con Tkinter (incluido en la instalación
estándar de Python en Windows). No requiere librerías externas.
"""

import os
import sys
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk

from gestion_clientes import (CLAVE_ACCESO, GENEROS, MENUS, GestionClientes,
                              formatear_pesos)

# --------------------------------------------------------------------------
# Datos del autor y paleta personalizada del formulario
# --------------------------------------------------------------------------
AUTOR = "Jhon Deivid Rojas Rodriguez"
NOMBRE_APP = "Sabor & Sazón - Gestión de Clientes"

COLOR_FONDO = "#FFF3E0"        # fondo crema (color propio del integrante)
COLOR_PANEL = "#FFFFFF"
COLOR_PRIMARIO = "#E65100"     # naranja fuerte
COLOR_PRIMARIO_OSCURO = "#BF360C"
COLOR_TEXTO = "#3E2723"
COLOR_EXITO = "#1B5E20"
COLOR_ERROR = "#B71C1C"

FUENTE = "Segoe UI"
RUTA_LOGO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo_sabor_sazon.png")


class AplicacionSaborSazon:
    """Ventana principal: acceso, registro de datos e historial."""

    def __init__(self):
        self.gestion = GestionClientes()

        self.root = tk.Tk()
        self.root.title(NOMBRE_APP)
        self.root.geometry("640x660")
        self.root.minsize(600, 620)
        self.root.configure(bg=COLOR_FONDO)
        self.root.resizable(True, True)

        self.logo = self._cargar_logo()

        self.contenedor = tk.Frame(self.root, bg=COLOR_FONDO)
        self.contenedor.pack(fill="both", expand=True)

        self.mostrar_acceso()

    # ------------------------------------------------------------------
    def _cargar_logo(self):
        """Carga el logo de la aplicación; si no está, devuelve None."""
        try:
            return tk.PhotoImage(file=RUTA_LOGO)
        except Exception:
            return None

    def _limpiar(self):
        for widget in self.contenedor.winfo_children():
            widget.destroy()

    def _titulo(self, texto, subtitulo=None):
        marco = tk.Frame(self.contenedor, bg=COLOR_FONDO)
        marco.pack(fill="x", pady=(18, 6))
        if self.logo is not None:
            tk.Label(marco, image=self.logo, bg=COLOR_FONDO).pack()
        tk.Label(marco, text=texto, font=(FUENTE, 17, "bold"),
                 bg=COLOR_FONDO, fg=COLOR_PRIMARIO).pack(pady=(6, 0))
        if subtitulo:
            tk.Label(marco, text=subtitulo, font=(FUENTE, 10),
                     bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(pady=(2, 0))
        return marco

    # ------------------------------------------------------------------
    # 1. Interfaz de acceso (Figura 1 del Anexo 1)
    # ------------------------------------------------------------------
    def mostrar_acceso(self):
        self._limpiar()
        self._titulo(NOMBRE_APP, f"Autor: {AUTOR}")

        panel = tk.Frame(self.contenedor, bg=COLOR_PANEL, bd=1, relief="solid")
        panel.pack(pady=24, padx=40, fill="x")

        tk.Label(panel, text="Ingrese la contraseña de acceso:", font=(FUENTE, 11),
                 bg=COLOR_PANEL, fg=COLOR_TEXTO).pack(pady=(20, 6))

        self.var_clave = tk.StringVar()
        entrada = tk.Entry(panel, textvariable=self.var_clave, show="*",
                           font=(FUENTE, 13), justify="center", width=16)
        entrada.pack(pady=6)
        entrada.focus_set()

        self.etiqueta_mensaje = tk.Label(panel, text="", font=(FUENTE, 10),
                                         bg=COLOR_PANEL, fg=COLOR_ERROR)
        self.etiqueta_mensaje.pack(pady=(4, 0))

        tk.Button(panel, text="Ingresar", font=(FUENTE, 11, "bold"),
                  bg=COLOR_PRIMARIO, fg="white", activebackground=COLOR_PRIMARIO_OSCURO,
                  activeforeground="white", cursor="hand2", width=18,
                  command=self.validar_acceso).pack(pady=(14, 6))
        tk.Button(panel, text="Salir", font=(FUENTE, 10), bg="#EFEBE9",
                  fg=COLOR_TEXTO, cursor="hand2", width=18,
                  command=self.confirmar_salida).pack(pady=(0, 20))

        self.root.bind("<Return>", lambda evento: self.validar_acceso())

    def validar_acceso(self):
        if self.gestion.validar_acceso(self.var_clave.get().strip()):
            self.mostrar_registro()
        else:
            self.etiqueta_mensaje.config(text="Contraseña incorrecta. Intente de nuevo.")
            self.var_clave.set("")

    # ------------------------------------------------------------------
    # 2. Interfaz de registro de datos (Figura 2 del Anexo 1)
    # ------------------------------------------------------------------
    def mostrar_registro(self):
        self._limpiar()
        self.root.unbind("<Return>")
        self._titulo("Registro de datos del cliente",
                     "Complete los datos y presione «Guardar Registro»")

        panel = tk.Frame(self.contenedor, bg=COLOR_PANEL, bd=1, relief="solid")
        panel.pack(pady=10, padx=30, fill="x")

        self.var_identificacion = tk.StringVar()
        self.var_nombre = tk.StringVar()
        self.var_genero = tk.StringVar(value="")
        self.var_menu = tk.StringVar()
        self.var_sesiones = tk.StringVar(value="1")
        self.var_costo = tk.StringVar(value="")
        self.var_fecha = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d %H:%M"))

        fila = 0

        def etiqueta(texto):
            nonlocal fila
            tk.Label(panel, text=texto, font=(FUENTE, 10, "bold"), bg=COLOR_PANEL,
                     fg=COLOR_TEXTO, anchor="w").grid(row=fila, column=0, sticky="w",
                                                      padx=(18, 8), pady=6)
            return fila

        etiqueta("Identificación:")
        tk.Entry(panel, textvariable=self.var_identificacion, font=(FUENTE, 11),
                 width=28).grid(row=fila, column=1, sticky="w", pady=6)
        fila += 1

        etiqueta("Nombre completo:")
        tk.Entry(panel, textvariable=self.var_nombre, font=(FUENTE, 11),
                 width=28).grid(row=fila, column=1, sticky="w", pady=6)
        fila += 1

        etiqueta("Género:")
        marco_genero = tk.Frame(panel, bg=COLOR_PANEL)
        marco_genero.grid(row=fila, column=1, sticky="w", pady=6)
        for genero in GENEROS:
            tk.Radiobutton(marco_genero, text=genero, value=genero,
                           variable=self.var_genero, bg=COLOR_PANEL,
                           font=(FUENTE, 10), fg=COLOR_TEXTO,
                           activebackground=COLOR_PANEL).pack(side="left", padx=(0, 14))
        fila += 1

        etiqueta("Tipo de menú:")
        combo = ttk.Combobox(panel, textvariable=self.var_menu, state="readonly",
                             values=list(MENUS.keys()), font=(FUENTE, 11), width=26)
        combo.grid(row=fila, column=1, sticky="w", pady=6)
        combo.bind("<<ComboboxSelected>>", self.actualizar_costo)
        fila += 1

        etiqueta("Costo por sesión:")
        tk.Entry(panel, textvariable=self.var_costo, font=(FUENTE, 11), width=28,
                 state="disabled", disabledforeground=COLOR_PRIMARIO_OSCURO,
                 disabledbackground="#F5F5F5").grid(row=fila, column=1, sticky="w", pady=6)
        fila += 1

        etiqueta("Número de sesiones:")
        tk.Spinbox(panel, from_=1, to=100, textvariable=self.var_sesiones,
                   font=(FUENTE, 11), width=8).grid(row=fila, column=1, sticky="w", pady=6)
        fila += 1

        etiqueta("Fecha de registro:")
        tk.Entry(panel, textvariable=self.var_fecha, font=(FUENTE, 11), width=28,
                 state="disabled", disabledforeground=COLOR_TEXTO,
                 disabledbackground="#F5F5F5").grid(row=fila, column=1, sticky="w", pady=6)
        fila += 1

        self.etiqueta_estado = tk.Label(panel, text="", font=(FUENTE, 10),
                                        bg=COLOR_PANEL, fg=COLOR_EXITO, wraplength=440,
                                        justify="left")
        self.etiqueta_estado.grid(row=fila, column=0, columnspan=2, sticky="w",
                                  padx=18, pady=(8, 0))
        fila += 1

        botones = tk.Frame(panel, bg=COLOR_PANEL)
        botones.grid(row=fila, column=0, columnspan=2, pady=18)
        tk.Button(botones, text="Guardar Registro", font=(FUENTE, 10, "bold"),
                  bg=COLOR_PRIMARIO, fg="white", cursor="hand2", width=20,
                  activebackground=COLOR_PRIMARIO_OSCURO,
                  command=self.guardar_registro).pack(side="left", padx=6)
        tk.Button(botones, text="Calcular Costo / Mostrar Reporte", font=(FUENTE, 10, "bold"),
                  bg="#2E7D32", fg="white", cursor="hand2", width=28,
                  activebackground=COLOR_EXITO,
                  command=self.mostrar_reporte).pack(side="left", padx=6)
        tk.Button(botones, text="Salir de la Aplicación", font=(FUENTE, 10),
                  bg="#EFEBE9", fg=COLOR_TEXTO, cursor="hand2", width=20,
                  command=self.confirmar_salida).pack(side="left", padx=6)

        # Historial de registros guardados
        tk.Label(self.contenedor, text="Registros guardados en esta sesión:",
                 font=(FUENTE, 10, "bold"), bg=COLOR_FONDO,
                 fg=COLOR_TEXTO).pack(anchor="w", padx=32, pady=(12, 2))
        columnas = ("identificacion", "nombre", "menu", "sesiones", "total")
        self.tabla = ttk.Treeview(self.contenedor, columns=columnas, show="headings", height=6)
        for columna, titulo, ancho in zip(
                columnas,
                ("Identificación", "Nombre", "Menú", "Sesiones", "Total a pagar"),
                (110, 170, 130, 70, 100)):
            self.tabla.heading(columna, text=titulo)
            self.tabla.column(columna, width=ancho, anchor="center")
        self.tabla.pack(fill="x", padx=30, pady=(0, 16))

    def actualizar_costo(self, evento=None):
        """Muestra automáticamente el costo por sesión del menú elegido."""
        try:
            self.var_costo.set(formatear_pesos(MENUS[self.var_menu.get()]))
        except KeyError:
            self.var_costo.set("")

    def guardar_registro(self):
        try:
            registro = self.gestion.guardar_registro(
                self.var_identificacion.get(),
                self.var_nombre.get(),
                self.var_genero.get(),
                self.var_menu.get(),
                self.var_sesiones.get(),
                self.var_fecha.get(),
            )
        except ValueError as error:
            self.etiqueta_estado.config(text=f"⚠ {error}", fg=COLOR_ERROR)
            return

        self.tabla.insert("", "end", values=(
            registro["identificacion"], registro["nombre_completo"],
            registro["tipo_menu"], registro["numero_sesiones"],
            formatear_pesos(registro["costo_total"])))
        self.etiqueta_estado.config(
            text=(f"✔ Registro guardado. Costo total del servicio: "
                  f"{formatear_pesos(registro['costo_total'])}"), fg=COLOR_EXITO)
        self.limpiar_formulario()

    def limpiar_formulario(self):
        self.var_identificacion.set("")
        self.var_nombre.set("")
        self.var_genero.set("")
        self.var_menu.set("")
        self.var_sesiones.set("1")
        self.var_costo.set("")
        self.var_fecha.set(datetime.now().strftime("%Y-%m-%d %H:%M"))

    # ------------------------------------------------------------------
    # 3. Interfaz de reporte (Figura 3 del Anexo 1)
    # ------------------------------------------------------------------
    def mostrar_reporte(self):
        if not self.gestion.registros:
            messagebox.showinfo("Sin registros",
                                "Primero debe guardar al menos un registro.")
            return

        registro = self.gestion.registros[-1]
        reporte = tk.Toplevel(self.root)
        reporte.title("Reporte del cliente")
        reporte.configure(bg=COLOR_FONDO)
        reporte.geometry("480x520")
        reporte.transient(self.root)
        reporte.grab_set()

        tk.Label(reporte, text="REPORTE DEL SERVICIO", font=(FUENTE, 15, "bold"),
                 bg=COLOR_FONDO, fg=COLOR_PRIMARIO).pack(pady=(18, 2))
        tk.Label(reporte, text=NOMBRE_APP, font=(FUENTE, 10), bg=COLOR_FONDO,
                 fg=COLOR_TEXTO).pack(pady=(0, 12))

        panel = tk.Frame(reporte, bg=COLOR_PANEL, bd=1, relief="solid")
        panel.pack(fill="both", expand=True, padx=24, pady=(0, 12))

        datos = [
            ("Identificación", registro["identificacion"]),
            ("Nombre completo", registro["nombre_completo"]),
            ("Género", registro["genero"]),
            ("Tipo de menú", registro["tipo_menu"]),
            ("Costo por sesión", formatear_pesos(registro["costo_sesion"])),
            ("Número de sesiones", registro["numero_sesiones"]),
            ("Fecha de registro", registro["fecha_registro"]),
        ]
        for i, (etiqueta, valor) in enumerate(datos):
            tk.Label(panel, text=f"{etiqueta}:", font=(FUENTE, 10, "bold"),
                     bg=COLOR_PANEL, fg=COLOR_TEXTO, anchor="w").grid(
                row=i, column=0, sticky="w", padx=(18, 10), pady=6)
            tk.Label(panel, text=str(valor), font=(FUENTE, 10), bg=COLOR_PANEL,
                     fg=COLOR_TEXTO, anchor="w").grid(row=i, column=1, sticky="w", pady=6)

        tk.Label(panel, text="Costo total del servicio:",
                 font=(FUENTE, 12, "bold"), bg=COLOR_PANEL,
                 fg=COLOR_TEXTO).grid(row=len(datos), column=0, sticky="w",
                                      padx=(18, 10), pady=(16, 6))
        tk.Label(panel, text=formatear_pesos(registro["costo_total"]),
                 font=(FUENTE, 16, "bold"), bg=COLOR_PANEL,
                 fg=COLOR_PRIMARIO_OSCURO).grid(row=len(datos), column=1,
                                                sticky="w", pady=(16, 6))

        tk.Label(panel, text=f"Total recaudado en la sesión: "
                             f"{formatear_pesos(self.gestion.total_recaudado())}",
                 font=(FUENTE, 9, "italic"), bg=COLOR_PANEL,
                 fg=COLOR_TEXTO).grid(row=len(datos) + 1, column=0, columnspan=2,
                                      pady=(10, 14))

        tk.Button(reporte, text="Cerrar reporte", font=(FUENTE, 10, "bold"),
                  bg=COLOR_PRIMARIO, fg="white", cursor="hand2", width=20,
                  command=reporte.destroy).pack(pady=(0, 16))

    # ------------------------------------------------------------------
    def confirmar_salida(self):
        if messagebox.askyesno("Confirmar salida",
                               "¿Está seguro de que desea salir de la aplicación?"):
            self.root.destroy()

    def ejecutar(self):
        self.root.mainloop()


def main():
    aplicacion = AplicacionSaborSazon()
    aplicacion.ejecutar()


if __name__ == "__main__":
    main()
