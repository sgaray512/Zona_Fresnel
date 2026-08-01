import tkinter as tk
from tkinter import ttk
from utilidades import convertir_numero, validar_obstaculo
from calculos import calcular_enlace

class PlaceholderEntry(ttk.Entry):
    def __init__(self, master, placeholder="", *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = "gray"
        self.default_fg = "black"
        self["foreground"] = self.placeholder_color
        self.insert(0, self.placeholder)
        self.bind("<FocusIn>", self._focus_in)
        self.bind("<FocusOut>", self._focus_out)

    def _focus_in(self, event):
        if self.get() == self.placeholder:
            self.delete(0, tk.END)
            self["foreground"] = self.default_fg

    def _focus_out(self, event):
        if self.get() == "":
            self["foreground"] = self.placeholder_color
            self.insert(0, self.placeholder)

    def valor(self):
        texto = self.get()
        if texto == self.placeholder:
            return ""
        return texto

    def limpiar(self):
        self.delete(0, tk.END)
        self["foreground"] = self.placeholder_color
        self.insert(0, self.placeholder)

class AplicacionFresnel:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Calculadora Zona de Fresnel")
        self.ventana.geometry("1000x800")
        self.ventana.resizable(True, True)
        self.ventana.configure(bg="#F4F6F7")
        self.crear_estilo()
        self.crear_titulo()
        self.contenedor = tk.Frame(self.ventana, bg="#F4F6F7")
        self.contenedor.pack(fill="both", expand=True, padx=20, pady=10)
        self.panel_izquierdo = tk.Frame(self.contenedor, bg="#F4F6F7")
        self.panel_izquierdo.pack(side="left", fill="both", expand=True, padx=(0, 10))
        self.panel_derecho = tk.Frame(self.contenedor, bg="#F4F6F7")
        self.panel_derecho.pack(side="right", fill="both", expand=True)
        self.crear_formulario()
        self.crear_botones()
        self.crear_resultados()
        self.crear_barra_estado()
        # Atajos de teclado
        self.ventana.bind("<Return>", self.enter_presionado)
        self.ventana.bind("<Escape>", lambda e: self.ventana.destroy())
        self.ventana.bind("<Control-l>", lambda e: self.limpiar())

    def enter_presionado(self, event):
        self.calcular()

    # --------------------------------------------------

    def crear_estilo(self):
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure(
            "TLabelframe",
            background="#F4F6F7"
        )
        estilo.configure(
            "TLabelframe.Label",
            font=("Segoe UI", 11, "bold")
        )
        estilo.configure(
            "TButton",
            font=("Segoe UI", 10),
            padding=8
        )

    # --------------------------------------------------

    def crear_titulo(self):
        superior = tk.Frame(
            self.ventana,
            bg="#0B3C5D"
        )
        superior.pack(fill="x")
        tk.Label(
            superior,
            text="CALCULADORA ZONA DE FRESNEL",
            font=("Segoe UI", 18, "bold"),
            fg="white",
            bg="#0B3C5D"
        ).pack(pady=(15, 5))
        tk.Label(
            superior,
            text="Versión 1.0",
            font=("Segoe UI", 10),
            fg="white",
            bg="#0B3C5D"
        ).pack()
        tk.Label(
            superior,
            text="Este programa permite calcular la Primera Zona de Fresnel\n"
                "y verificar si un obstáculo afecta un enlace inalámbrico.",
            font=("Segoe UI", 10),
            fg="white",
            bg="#0B3C5D",
            justify="center"
        ).pack(pady=(5, 15))

        # --------------------------------------------------

    def crear_formulario(self):
        frame = ttk.LabelFrame(
            self.panel_izquierdo,
            text="Datos del enlace",
            padding=15
        )
        frame.pack(fill="x", padx=20, pady=15)
        # Distancia
        ttk.Label(
            frame,
            text="Distancia entre antenas (km)"
        ).grid(row=0, column=0, sticky="w")
        self.entry_distancia = PlaceholderEntry(
            frame,
            "Ej.: 15"
        )
        self.entry_distancia.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        # Frecuencia
        ttk.Label(
            frame,
            text="Frecuencia (GHz)"
        ).grid(row=2, column=0, sticky="w")
        self.entry_frecuencia = PlaceholderEntry(
            frame,
            "Ej.: 5,8"
        )
        self.entry_frecuencia.grid(row=3, column=0, sticky="ew", pady=(0, 10))
        # Antena 1
        ttk.Label(
            frame,
            text="Altura Antena 1 (m)"
        ).grid(row=4, column=0, sticky="w")
        self.entry_antena1 = PlaceholderEntry(
            frame,
            "Ej.: 25"
        )
        self.entry_antena1.grid(row=5, column=0, sticky="ew", pady=(0, 10))
        # Antena 2
        ttk.Label(
            frame,
            text="Altura Antena 2 (m)"
        ).grid(row=6, column=0, sticky="w")
        self.entry_antena2 = PlaceholderEntry(
            frame,
            "Ej.: 30"
        )
        self.entry_antena2.grid(row=7, column=0, sticky="ew", pady=(0, 10))
        # Distancia obstáculo
        ttk.Label(
            frame,
            text="Distancia del obstáculo desde Antena 1 (km)"
        ).grid(row=8, column=0, sticky="w")
        self.entry_obstaculo_distancia = PlaceholderEntry(
            frame,
            "Ej.: 8"
        )
        self.entry_obstaculo_distancia.grid(row=9, column=0, sticky="ew", pady=(0, 10))
        # Altura obstáculo
        ttk.Label(
            frame,
            text="Altura del obstáculo (m)"
        ).grid(row=10, column=0, sticky="w")
        self.entry_obstaculo_altura = PlaceholderEntry(
            frame,
            "Ej.: 18"
        )
        self.entry_obstaculo_altura.grid(row=11, column=0, sticky="ew")
        frame.columnconfigure(0, weight=1)

    # --------------------------------------------------

    def crear_botones(self):
        frame = tk.Frame(
            self.panel_izquierdo,
            bg="#F4F6F7"
        )
        frame.pack(pady=10)
        self.btn_calcular = ttk.Button(
            frame,
            text="Calcular",
            command=self.calcular
        )
        self.btn_calcular.grid(row=0, column=0, padx=5)
        self.btn_limpiar = ttk.Button(
            frame,
            text="Limpiar",
            command=self.limpiar
        )
        self.btn_limpiar.grid(row=0, column=1, padx=5)
        self.btn_salir = ttk.Button(
            frame,
            text="Salir",
            command=self.ventana.destroy
        )
        self.btn_salir.grid(row=0, column=2, padx=5)

    # --------------------------------------------------

    def crear_resultados(self):
        frame = ttk.LabelFrame(
            self.panel_derecho,
            text="Resultados",
            padding=15
        )
        frame.pack(fill="x", padx=20, pady=10)
        self.lbl_fresnel = ttk.Label(
            frame,
            text="Radio de la Zona de Fresnel: --------",
            justify="left",
            font=("Segoe UI", 10)
        )
        self.lbl_fresnel.pack(anchor="w", pady=3)
        ttk.Label(
            frame,
            text="→ Radio máximo de la Primera Zona de Fresnel\n",
            foreground="gray",
            justify="left",
            font=("Segoe UI", 9)
        ).pack(anchor="w", padx=15)
        self.lbl_linea = ttk.Label(
            frame,
            text="Altura de la línea de vista: --------",
            justify="left",
            font=("Segoe UI", 10)
        )
        self.lbl_linea.pack(anchor="w", pady=3)
        ttk.Label(
            frame,
            text="→ Altura del haz directo entre las antenas en la posición del obstáculo.\n",
            foreground="gray",
            justify="left",
            font=("Segoe UI", 9)
        ).pack(anchor="w", padx=15)
        self.lbl_despeje = ttk.Label(
            frame,
            text="Despeje respecto al obstáculo: --------",
            justify="left",
            font=("Segoe UI", 10)
        )
        self.lbl_despeje.pack(anchor="w", pady=3)
        ttk.Label(
            frame,
            text="→ Distancia vertical entre la línea de vista y la parte superior del obstáculo.\n",
            foreground="gray",
            justify="left",
            font=("Segoe UI", 9)
        ).pack(anchor="w", padx=15)
        self.lbl_invasion = ttk.Label(
            frame,
            text="Invasión de la Zona de Fresnel: --------",
            justify="left",
            font=("Segoe UI", 10)
        )
        self.lbl_invasion.pack(anchor="w", pady=3)
        ttk.Label(
            frame,
            text="→ Porcentaje de la Zona de Fresnel\n   ocupado por el obstáculo.",
            foreground="gray",
            justify="left",
            font=("Segoe UI", 9)
        ).pack(anchor="w", padx=15)
        ttk.Separator(frame).pack(fill="x", pady=10)
        self.lbl_estado = tk.Label(
            frame,
            text="Esperando cálculo...",
            bg="white",
            fg="blue",
            font=("Segoe UI", 13, "bold")
        )
        self.lbl_estado.pack(fill="x")
        self.lbl_mensaje = tk.Label(
            frame,
            text="Ingrese los datos del enlace y presione CALCULAR.",
            justify="center",
            bg="white",
            font=("Segoe UI", 10)
        )
        self.lbl_mensaje.pack(fill="x", pady=10)

    # --------------------------------------------------

    def crear_barra_estado(self):
        self.barra_estado = tk.Label(
            self.ventana,
            text="Programa listo.",
            anchor="w",
            bg="#D6EAF8",
            padx=10
        )
        self.barra_estado.pack(
            side="bottom",
            fill="x"
        )
        tk.Label(
            self.ventana,
            text="Desarrollado por: Santiago Garay",
            bg="#F4F6F7",
            fg="gray"
        ).pack(
            side="bottom",
            pady=5
        )

        # --------------------------------------------------

    def calcular(self):
        try:
            distancia = convertir_numero(
                self.entry_distancia.valor()
            )
            frecuencia = convertir_numero(
                self.entry_frecuencia.valor()
            )
            altura1 = convertir_numero(
                self.entry_antena1.valor()
            )
            altura2 = convertir_numero(
                self.entry_antena2.valor()
            )
            distancia_obstaculo = convertir_numero(
                self.entry_obstaculo_distancia.valor()
            )
            altura_obstaculo = convertir_numero(
                self.entry_obstaculo_altura.valor()
            )
            validar_obstaculo(
                distancia,
                distancia_obstaculo
            )
            resultado = calcular_enlace(
                distancia,
                frecuencia,
                altura1,
                altura2,
                distancia_obstaculo,
                altura_obstaculo
            )
            self.lbl_fresnel.config(
                text=f"Radio de la Zona de Fresnel: {resultado['fresnel']} m"
            )
            self.lbl_linea.config(
                text=f"Altura de la línea de vista: {resultado['linea']} m"
            )
            self.lbl_despeje.config(
                text=f"Despeje respecto al obstáculo: {resultado['despeje']} m"
            )
            self.lbl_invasion.config(
                text=f"Invasión de la Zona de Fresnel: {resultado['invasion']} %"
            )
            self.lbl_estado.config(
                text=resultado["estado"],
                fg=resultado["color"]
            )
            self.lbl_mensaje.config(
                text=resultado["mensaje"]
            )
            self.barra_estado.config(
                text="✔ Cálculo realizado correctamente."
            )
        except Exception as e:
            self.lbl_estado.config(
                text="ERROR",
                fg="red"
            )
            self.lbl_mensaje.config(
                text=str(e)
            )
            self.barra_estado.config(
                text="⚠ Revise los datos ingresados."
            )

    # --------------------------------------------------

    def limpiar(self):
        self.entry_distancia.limpiar()
        self.entry_frecuencia.limpiar()
        self.entry_antena1.limpiar()
        self.entry_antena2.limpiar()
        self.entry_obstaculo_distancia.limpiar()
        self.entry_obstaculo_altura.limpiar()
        self.lbl_fresnel.config(
            text="Zona de Fresnel: --------"
        )
        self.lbl_linea.config(
            text="Altura de la línea: --------"
        )
        self.lbl_despeje.config(
            text="Espacio libre: --------"
        )
        self.lbl_invasion.config(
            text="Invasión: --------"
        )
        self.lbl_estado.config(
            text="Esperando cálculo...",
            fg="blue"
        )
        self.lbl_mensaje.config(
            text="Ingrese los datos del enlace y presione CALCULAR."
        )
        self.barra_estado.config(
            text="Formulario limpiado."
        )

    # --------------------------------------------------

    def iniciar(self):
        self.ventana.mainloop()

def iniciar_aplicacion():
    app = AplicacionFresnel()
    app.iniciar()