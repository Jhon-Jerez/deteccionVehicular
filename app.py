
"""
Sistema de Detección de Tránsito con IA
Aplicación principal para conteo y clasificación de vehículos
"""

import tkinter as tk
from gui.main_window import MainWindow

def main():
    """Función principal de la aplicación"""
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()