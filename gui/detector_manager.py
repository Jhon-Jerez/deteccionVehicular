import cv2
import threading
import time
from datetime import datetime
from ultralytics import YOLO
from collections import defaultdict

class DetectorManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.model = YOLO("yolov8n.pt")
        
        # Estado de detección
        self.detecting = False
        self.cap = None
        self.detection_thread = None
        
        # Datos de detección - CORREGIDO
        self.vehicle_counters = defaultdict(set)  # Para tracking único
        self.detection_history = []  # Historial de detecciones
        self.tracked_vehicles = set()  # NUEVO: Set para rastrear vehículos ya procesados
        self.first_detection_time = {}  # NUEVO: Tiempo de primera detección por track_id
        self.video_source = "1.mp4"  # Fuente por defecto
        
        # FPS control para suavizar la visualización
        self.fps_limit = 30
        self.frame_delay = 1.0 / self.fps_limit
        
        # Configuración de clases de vehículos
        self.vehicle_classes = {
            'car': 'Automóvil',
            'bus': 'Autobús', 
            'truck': 'Camión',
            'motorbike': 'Motocicleta',
            'bicycle': 'Bicicleta',
            'van': 'Camioneta'
        }
        
    def set_video_source(self, source):
        """Establecer fuente de video"""
        self.video_source = source
        
    def iniciar_deteccion(self):
        """Iniciar proceso de detección"""
        if self.detecting:
            return
            
        self.detecting = True
        self.clear_data()
        
        # Inicializar captura de video
        self.cap = cv2.VideoCapture(self.video_source)
        if not self.cap.isOpened():
            raise Exception(f"No se pudo abrir el video: {self.video_source}")
            
        # Configurar captura
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        
        # Iniciar hilo de detección
        self.detection_thread = threading.Thread(target=self._process_video, daemon=True)
        self.detection_thread.start()
        
    def detener_deteccion(self):
        """Detener proceso de detección"""
        self.detecting = False
        
        if self.cap:
            self.cap.release()
            self.cap = None
            
        if self.detection_thread and self.detection_thread.is_alive():
            self.detection_thread.join(timeout=1.0)
            
    def _process_video(self):
        """Procesamiento principal de video"""
        last_frame_time = time.time()
        
        while self.detecting and self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            
            if not ret:
                # Reiniciar video si llegamos al final
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
                
            # Control de FPS
            current_time = time.time()
            if current_time - last_frame_time < self.frame_delay:
                time.sleep(self.frame_delay - (current_time - last_frame_time))
                
            last_frame_time = time.time()
            
            # Procesar frame
            processed_frame = self._process_frame(frame)
            
            # Actualizar UI en el hilo principal
            self.main_window.root.after(0, self._update_ui, processed_frame)
            
    def _process_frame(self, frame):
        """Procesar un frame individual"""
        try:
            # Ejecutar detección con tracking
            results = self.model.track(
                frame, 
                persist=True, 
                tracker="bytetrack.yaml",
                verbose=False
            )
            
            if results and len(results) > 0:
                result = results[0]
                
                # Procesar detecciones si hay IDs
                if result.boxes.id is not None:
                    self._process_detections(result)
                    
                # Obtener frame anotado
                annotated_frame = result.plot()
                return annotated_frame
                
        except Exception as e:
            print(f"Error procesando frame: {e}")
            
        return frame
        
    def _process_detections(self, result):
        """Procesar detecciones del frame actual - MÉTODO CORREGIDO"""
        ids = result.boxes.id.cpu().numpy()
        classes = result.boxes.cls.cpu().numpy()
        confidences = result.boxes.conf.cpu().numpy()
        
        timestamp = datetime.now()
        
        for track_id, class_id, confidence in zip(ids, classes, confidences):
            class_name = self.model.names[int(class_id)]
            
            # Solo procesar vehículos
            if class_name in self.vehicle_classes:
                track_id = int(track_id)
                
                # CORREGIDO: Solo agregar al historial si es la primera vez que vemos este vehículo
                vehicle_key = f"{class_name}_{track_id}"
                
                if vehicle_key not in self.tracked_vehicles:
                    # Primera detección de este vehículo específico
                    self.tracked_vehicles.add(vehicle_key)
                    self.first_detection_time[track_id] = timestamp
                    
                    # Agregar a contador único
                    self.vehicle_counters[class_name].add(track_id)
                    
                    # Agregar al historial SOLO la primera vez
                    self.detection_history.append({
                        'timestamp': timestamp,
                        'track_id': track_id,
                        'class_name': class_name,
                        'class_display': self.vehicle_classes[class_name],
                        'confidence': float(confidence),
                        'first_seen': True  # NUEVO: Marcador de primera detección
                    })
                    
                    print(f"Nueva detección: {self.vehicle_classes[class_name]} ID={track_id}")
                
    def _update_ui(self, frame):
        """Actualizar interfaz de usuario"""
        if not self.detecting:
            return
            
        # Actualizar video
        self.main_window.update_video_display(frame)
        
        # Actualizar estadísticas
        counts = {class_name: len(ids) for class_name, ids in self.vehicle_counters.items()}
        self.main_window.update_statistics(counts)
        
    def get_detection_data(self):
        """Obtener datos de detección para reportes - MÉTODO MEJORADO"""
        # Contar detecciones por tipo
        type_counts = defaultdict(int)
        for class_name, ids in self.vehicle_counters.items():
            type_counts[self.vehicle_classes[class_name]] = len(ids)
            
        # NUEVO: Estadísticas adicionales
        total_unique_vehicles = sum(len(ids) for ids in self.vehicle_counters.values())
        
        # Preparar datos del reporte
        report_data = {
            'timestamp': datetime.now(),
            'video_source': self.video_source,
            'total_detections': total_unique_vehicles,  # CORREGIDO: usar vehículos únicos
            'detection_counts': dict(type_counts),
            'detection_history': self.detection_history.copy(),
            'unique_vehicles': {k: list(v) for k, v in self.vehicle_counters.items()},  # Convertir sets a listas
            'total_tracked_vehicles': len(self.tracked_vehicles),  # NUEVO: total de vehículos rastreados
            'detection_summary': {  # NUEVO: resumen mejorado
                'unique_vehicles_by_type': dict(type_counts),
                'detection_start_time': min([d['timestamp'] for d in self.detection_history]) if self.detection_history else None,
                'detection_end_time': max([d['timestamp'] for d in self.detection_history]) if self.detection_history else None
            }
        }
        
        return report_data
        
    def clear_data(self):
        """Limpiar todos los datos de detección - MÉTODO ACTUALIZADO"""
        self.vehicle_counters.clear()
        self.detection_history.clear()
        self.tracked_vehicles.clear()  # NUEVO: limpiar vehículos rastreados
        self.first_detection_time.clear()  # NUEVO: limpiar tiempos de primera detección
        
    def get_detection_statistics(self):
        """NUEVO: Obtener estadísticas detalladas de detección"""
        stats = {
            'total_unique_vehicles': sum(len(ids) for ids in self.vehicle_counters.values()),
            'vehicles_by_type': {self.vehicle_classes[k]: len(v) for k, v in self.vehicle_counters.items()},
            'total_detection_events': len(self.detection_history),
            'tracking_active': self.detecting,
            'tracked_vehicle_keys': len(self.tracked_vehicles)
        }
        return stats