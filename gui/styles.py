import tkinter as tk
from tkinter import ttk

class AppStyles:
    """Clase para manejar estilos y temas de la aplicación"""
    
    def __init__(self):
        self.setup_colors()
        self.setup_fonts()
        
    def setup_colors(self):
        """Definir paleta de colores"""
        self.BG_COLOR = "#f0f0f0"
        self.PRIMARY_COLOR = "#2196F3"
        self.SUCCESS_COLOR = "#4CAF50"
        self.WARNING_COLOR = "#FF9800"
        self.DANGER_COLOR = "#f44336"
        self.INFO_COLOR = "#17a2b8"
        self.DARK_COLOR = "#343a40"
        self.LIGHT_COLOR = "#f8f9fa"
        
    def setup_fonts(self):
        """Definir fuentes"""
        self.FONT_FAMILY = "Segoe UI"
        self.FONT_SIZE_SMALL = 9
        self.FONT_SIZE_NORMAL = 10
        self.FONT_SIZE_LARGE = 12
        self.FONT_SIZE_TITLE = 14
        
    def configure_ttk_styles(self):
        """Configurar estilos de ttk"""
        style = ttk.Style()
        
        # Configurar tema base
        style.theme_use('clam')
        
        # Estilos para botones
        style.configure(
            "Success.TButton",
            background=self.SUCCESS_COLOR,
            foreground="white",
            focuscolor="none",
            borderwidth=0,
            font=(self.FONT_FAMILY, self.FONT_SIZE_NORMAL, "bold")
        )
        
        style.map(
            "Success.TButton",
            background=[('active', '#45a049'), ('pressed', '#3d8b40')]
        )
        
        style.configure(
            "Danger.TButton",
            background=self.DANGER_COLOR,
            foreground="white",
            focuscolor="none",
            borderwidth=0,
            font=(self.FONT_FAMILY, self.FONT_SIZE_NORMAL, "bold")
        )
        
        style.map(
            "Danger.TButton",
            background=[('active', '#da190b'), ('pressed', '#c0392b')]
        )
        
        style.configure(
            "Info.TButton",
            background=self.INFO_COLOR,
            foreground="white",
            focuscolor="none",
            borderwidth=0,
            font=(self.FONT_FAMILY, self.FONT_SIZE_NORMAL, "bold")
        )
        
        style.map(
            "Info.TButton",
            background=[('active', '#138496'), ('pressed', '#117a8b')]
        )
        
        # Estilo para LabelFrames
        style.configure(
            "TLabelframe",
            background=self.BG_COLOR,
            borderwidth=2,
            relief="groove"
        )
        
        style.configure(
            "TLabelframe.Label",
            background=self.BG_COLOR,
            font=(self.FONT_FAMILY, self.FONT_SIZE_NORMAL, "bold")
        )
        
        # Estilo para Treeview
        style.configure(
            "Treeview",
            background="white",
            foreground="black",
            rowheight=25,
            fieldbackground="white",
            font=(self.FONT_FAMILY, self.FONT_SIZE_SMALL)
        )
        
        style.configure(
            "Treeview.Heading",
            font=(self.FONT_FAMILY, self.FONT_SIZE_SMALL, "bold"),
            background=self.LIGHT_COLOR,
            foreground=self.DARK_COLOR
        )
        
        style.map(
            "Treeview",
            background=[('selected', self.PRIMARY_COLOR)],
            foreground=[('selected', 'white')]
        )
        
        # Estilo para Progressbar
        style.configure(
            "TProgressbar",
            background=self.PRIMARY_COLOR,
            troughcolor=self.LIGHT_COLOR,
            borderwidth=0,
            lightcolor=self.PRIMARY_COLOR,
            darkcolor=self.PRIMARY_COLOR
        )
        
        return style