import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import cv2
from .detector_manager import DetectorManager
from .report_generator import ReportGenerator
from .styles import AppStyles

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.detector_manager = DetectorManager(self)
        self.report_generator = ReportGenerator()
        self.styles = AppStyles()
        
        self.setup_window()
        self.create_widgets()
        self.apply_styles()
        
    def setup_window(self):
        """Configuración inicial de la ventana"""
        self.root.title("🚗 Sistema de Detección de Tránsito IA")
        self.root.geometry("1200x800")
        self.root.configure(bg=self.styles.BG_COLOR)
        self.root.resizable(True, True)
        
        # Configurar grid weights para responsive design
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
    def create_widgets(self):
        """Crear todos los widgets de la interfaz"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Header
        self.create_header(main_frame)
        
        # Panel izquierdo (controles)
        self.create_control_panel(main_frame)
        
        # Panel central (video)
        self.create_video_panel(main_frame)
        
        # Panel derecho (estadísticas)
        self.create_stats_panel(main_frame)
        
        # Footer
        self.create_footer(main_frame)
        
    def create_header(self, parent):
        """Crear header de la aplicación"""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 10))
        
        title_label = ttk.Label(
            header_frame,
            text="🚗 Sistema de Detección de Tránsito con IA",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=5)
        
        subtitle_label = ttk.Label(
            header_frame,
            text="Conteo automático y clasificación de vehículos en tiempo real",
            font=("Arial", 10)
        )
        subtitle_label.pack()
        
    def create_control_panel(self, parent):
        """Crear panel de controles"""
        control_frame = ttk.LabelFrame(parent, text="🎮 Controles", padding="10")
        control_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 5))
        
        # Botón iniciar
        self.btn_iniciar = ttk.Button(
            control_frame,
            text="▶️ Iniciar Detección",
            command=self.iniciar_deteccion,
           
        )
        self.btn_iniciar.pack(pady=5, fill="x")
        
        # Botón detener
        self.btn_detener = ttk.Button(
            control_frame,
            text="⏹️ Detener",
            command=self.detener_deteccion,
           
            state="disabled"
        )
        self.btn_detener.pack(pady=5, fill="x")
        
        # Botón seleccionar video
        self.btn_seleccionar = ttk.Button(
            control_frame,
            text="📁 Seleccionar Video",
            command=self.seleccionar_video
        )
        self.btn_seleccionar.pack(pady=5, fill="x")
        
        # Separador
        ttk.Separator(control_frame, orient="horizontal").pack(fill="x", pady=10)
        
        # Botón generar reporte
        self.btn_reporte = ttk.Button(
            control_frame,
            text="📊 Generar Reporte",
            command=self.generar_reporte
        )
        self.btn_reporte.pack(pady=5, fill="x")
        
        # Botón limpiar datos
        self.btn_limpiar = ttk.Button(
            control_frame,
            text="🧹 Limpiar Datos",
            command=self.limpiar_datos
        )
        self.btn_limpiar.pack(pady=5, fill="x")
        
    def create_video_panel(self, parent):
        """Crear panel de video"""
        video_frame = ttk.LabelFrame(parent, text="📹 Vista de Video", padding="10")
        video_frame.grid(row=1, column=1, sticky="nsew", padx=5)
        video_frame.grid_rowconfigure(0, weight=1)
        video_frame.grid_columnconfigure(0, weight=1)
        
        # Canvas para video
        self.canvas_video = tk.Canvas(
            video_frame,
            bg="black",
            width=640,
            height=480
        )
        self.canvas_video.grid(row=0, column=0, sticky="nsew")
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(video_frame, orient="vertical", command=self.canvas_video.yview)
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas_video.configure(yscrollcommand=v_scrollbar.set)
        
        h_scrollbar = ttk.Scrollbar(video_frame, orient="horizontal", command=self.canvas_video.xview)
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        self.canvas_video.configure(xscrollcommand=h_scrollbar.set)
        
        # Texto de placeholder
        self.canvas_video.create_text(
            320, 240,
            text="📹 Selecciona un video para comenzar",
            fill="white",
            font=("Arial", 14)
        )
        
    def create_stats_panel(self, parent):
        """Crear panel de estadísticas"""
        stats_frame = ttk.LabelFrame(parent, text="📊 Estadísticas", padding="10")
        stats_frame.grid(row=1, column=2, sticky="nsew", padx=(5, 0))
        
        # Estado actual
        estado_frame = ttk.Frame(stats_frame)
        estado_frame.pack(fill="x", pady=5)
        
        ttk.Label(estado_frame, text="🔄 Estado:", font=("Arial", 10, "bold")).pack(anchor="w")
        self.lbl_estado = ttk.Label(estado_frame, text="Detenido", foreground="red")
        self.lbl_estado.pack(anchor="w")
        
        # Separador
        ttk.Separator(stats_frame, orient="horizontal").pack(fill="x", pady=10)
        
        # Contadores
        self.create_counter_widgets(stats_frame)
        
        # Separador
        ttk.Separator(stats_frame, orient="horizontal").pack(fill="x", pady=10)
        
        # Detalles de detección
        detalles_frame = ttk.Frame(stats_frame)
        detalles_frame.pack(fill="both", expand=True)
        
        ttk.Label(detalles_frame, text="🔍 Detalles:", font=("Arial", 10, "bold")).pack(anchor="w")
        
        # Treeview para mostrar detecciones
        self.tree_detecciones = ttk.Treeview(
            detalles_frame,
            columns=("Tipo", "Cantidad"),
            show="headings",
            height=8
        )
        self.tree_detecciones.heading("Tipo", text="Tipo de Vehículo")
        self.tree_detecciones.heading("Cantidad", text="Cantidad")
        self.tree_detecciones.column("Tipo", width=120)
        self.tree_detecciones.column("Cantidad", width=80)
        self.tree_detecciones.pack(fill="both", expand=True, pady=5)
        
        # Scrollbar para treeview
        scrollbar_tree = ttk.Scrollbar(detalles_frame, orient="vertical", command=self.tree_detecciones.yview)
        scrollbar_tree.pack(side="right", fill="y")
        self.tree_detecciones.configure(yscrollcommand=scrollbar_tree.set)
        
    def create_counter_widgets(self, parent):
        """Crear widgets de contadores"""
        self.counter_vars = {}
        
        # Definir tipos de vehículos con emojis
        vehicle_types = [
            ("🚗 Autos", "cars"),
            ("🚌 Autobuses", "buses"),
            ("🚚 Camiones", "trucks"),
            ("🏍️ Motocicletas", "motorcycles"),
            ("🚲 Bicicletas", "bicycles"),
            ("🚐 Camionetas", "vans")
        ]
        
        for display_name, var_name in vehicle_types:
            frame = ttk.Frame(parent)
            frame.pack(fill="x", pady=2)
            
            ttk.Label(frame, text=display_name, font=("Arial", 9)).pack(side="left")
            
            var = tk.StringVar(value="0")
            self.counter_vars[var_name] = var
            
            count_label = ttk.Label(
                frame,
                textvariable=var,
                font=("Arial", 10, "bold"),
                foreground="blue"
            )
            count_label.pack(side="right")
        
        # Total
        total_frame = ttk.Frame(parent)
        total_frame.pack(fill="x", pady=5)
        
        ttk.Label(total_frame, text="📊 Total:", font=("Arial", 10, "bold")).pack(side="left")
        
        self.total_var = tk.StringVar(value="0")
        total_label = ttk.Label(
            total_frame,
            textvariable=self.total_var,
            font=("Arial", 12, "bold"),
            foreground="green"
        )
        total_label.pack(side="right")
        
    def create_footer(self, parent):
        """Crear footer de la aplicación"""
        footer_frame = ttk.Frame(parent)
        footer_frame.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(10, 0))
        
        # Barra de progreso
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            footer_frame,
            variable=self.progress_var,
            mode="indeterminate"
        )
        self.progress_bar.pack(fill="x", pady=5)
        
        # Información del estado
        self.status_var = tk.StringVar(value="Listo para iniciar")
        status_label = ttk.Label(footer_frame, textvariable=self.status_var)
        status_label.pack()
        
    def apply_styles(self):
        """Aplicar estilos personalizados"""
        style = ttk.Style()
        
        # Estilo para botones
        style.configure("Success.TButton", foreground="white")
        style.configure("Danger.TButton", foreground="white")
        style.configure("Info.TButton", foreground="white")
        
    def iniciar_deteccion(self):
        """Iniciar la detección de vehículos"""
        try:
            self.detector_manager.iniciar_deteccion()
            self.btn_iniciar.config(state="disabled")
            self.btn_detener.config(state="normal")
            self.lbl_estado.config(text="Ejecutándose", foreground="green")
            self.status_var.set("Detección iniciada...")
            self.progress_bar.start()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo iniciar la detección: {str(e)}")
            
    def detener_deteccion(self):
        """Detener la detección de vehículos"""
        self.detector_manager.detener_deteccion()
        self.btn_iniciar.config(state="normal")
        self.btn_detener.config(state="disabled")
        self.lbl_estado.config(text="Detenido", foreground="red")
        self.status_var.set("Detección detenida")
        self.progress_bar.stop()
        
    def seleccionar_video(self):
        """Seleccionar archivo de video"""
        file_path = filedialog.askopenfilename(
            title="Seleccionar video",
            filetypes=[
                ("Videos", "*.mp4 *.avi *.mov *.mkv"),
                ("Todos los archivos", "*.*")
            ]
        )
        if file_path:
            self.detector_manager.set_video_source(file_path)
            self.status_var.set(f"Video seleccionado: {file_path.split('/')[-1]}")
            
    def generar_reporte(self):
        """Generar reporte de detecciones"""
        try:
            data = self.detector_manager.get_detection_data()
            if not data:
                messagebox.showwarning("Advertencia", "No hay datos para generar reporte")
                return
                
            filename = self.report_generator.generate_report(data)
            messagebox.showinfo("Éxito", f"Reporte generado: {filename}")
            self.status_var.set(f"Reporte generado: {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte: {str(e)}")
            
    def limpiar_datos(self):
        """Limpiar todos los datos de detección"""
        if messagebox.askyesno("Confirmar", "¿Estás seguro de limpiar todos los datos?"):
            self.detector_manager.clear_data()
            self.update_statistics({})
            self.status_var.set("Datos limpiados")
            
    def update_video_display(self, frame):
        """Actualizar la visualización del video"""
        if frame is not None:
            # Convertir frame a formato compatible con tkinter
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame_rgb)
            
            # Redimensionar si es necesario
            canvas_w = self.canvas_video.winfo_width()
            canvas_h = self.canvas_video.winfo_height()
            
            if canvas_w > 1 and canvas_h > 1:
                image = image.resize((min(canvas_w, 800), min(canvas_h, 600)), Image.Resampling.LANCZOS)
            
            photo = ImageTk.PhotoImage(image)
            
            # Limpiar canvas y mostrar nueva imagen
            self.canvas_video.delete("all")
            self.canvas_video.create_image(0, 0, anchor="nw", image=photo)
            self.canvas_video.image = photo  # Mantener referencia
            
            # Actualizar scroll region
            self.canvas_video.configure(scrollregion=self.canvas_video.bbox("all"))
            
    def update_statistics(self, detection_counts):
        """Actualizar estadísticas de detección"""
        # Mapeo de clases YOLO a nuestros contadores
        class_mapping = {
            'car': 'cars',
            'bus': 'buses',
            'truck': 'trucks',
            'motorbike': 'motorcycles',
            'bicycle': 'bicycles',
            'van': 'vans'
        }
        
        # Resetear contadores
        for var in self.counter_vars.values():
            var.set("0")
            
        # Actualizar contadores
        total = 0
        for class_name, count in detection_counts.items():
            if class_name in class_mapping:
                var_name = class_mapping[class_name]
                if var_name in self.counter_vars:
                    self.counter_vars[var_name].set(str(count))
                    total += count
                    
        self.total_var.set(str(total))
        
        # Actualizar treeview
        self.tree_detecciones.delete(*self.tree_detecciones.get_children())
        for class_name, count in detection_counts.items():
            if count > 0:
                self.tree_detecciones.insert("", "end", values=(class_name.title(), count))