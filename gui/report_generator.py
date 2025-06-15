import json
import csv
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, filedialog

class ReportGenerator:
    def __init__(self):
        self.reports_dir = Path("reports")
        self.reports_dir.mkdir(exist_ok=True)
        
    def generate_report(self, data, format_type="json"):
        """Generar reporte en el formato especificado"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format_type == "json":
            return self._generate_json_report(data, timestamp)
        elif format_type == "csv":
            return self._generate_csv_report(data, timestamp)
        elif format_type == "txt":
            return self._generate_text_report(data, timestamp)
        else:
            raise ValueError(f"Formato no soportado: {format_type}")
            
    def _generate_json_report(self, data, timestamp):
        """Generar reporte en formato JSON - MEJORADO"""
        filename = f"reporte_trafico_{timestamp}.json"
        filepath = self.reports_dir / filename
        
        # Preparar datos para JSON (convertir objetos no serializables)
        json_data = {
            'metadata': {
                'fecha_generacion': data['timestamp'].isoformat(),
                'fuente_video': data['video_source'],
                'total_vehiculos_unicos': data['total_detections'],  # CORREGIDO: nombre más claro
                'total_eventos_deteccion': len(data['detection_history']),  # NUEVO
                'periodo_analisis': {
                    'inicio': data['detection_summary']['detection_start_time'].isoformat() if data['detection_summary']['detection_start_time'] else None,
                    'fin': data['detection_summary']['detection_end_time'].isoformat() if data['detection_summary']['detection_end_time'] else None
                } if 'detection_summary' in data else None
            },
            'resumen_por_tipo': data['detection_counts'],
            'vehiculos_unicos_detectados': data.get('unique_vehicles', {}),  # NUEVO: IDs únicos por tipo
            'detecciones_primera_aparicion': []  # NUEVO: solo primeras detecciones
        }
        
        # Agregar historial de PRIMERAS detecciones (sin duplicados)
        for detection in data['detection_history']:
            json_data['detecciones_primera_aparicion'].append({
                'timestamp': detection['timestamp'].isoformat(),
                'id_seguimiento': detection['track_id'],
                'tipo_vehiculo': detection['class_display'],
                'confianza': detection['confidence'],
                'primera_deteccion': detection.get('first_seen', True)
            })
            
        # Escribir archivo JSON
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
            
        return filename
        
    def _generate_csv_report(self, data, timestamp):
        """Generar reporte en formato CSV - MEJORADO"""
        filename = f"reporte_trafico_{timestamp}.csv"
        filepath = self.reports_dir / filename
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Header del reporte
            writer.writerow(['REPORTE DE TRÁFICO - DETECCIÓN DE VEHÍCULOS (SIN DUPLICADOS)'])
            writer.writerow(['Fecha de generación:', data['timestamp'].strftime('%Y-%m-%d %H:%M:%S')])
            writer.writerow(['Fuente de video:', data['video_source']])
            writer.writerow(['Total de vehículos únicos:', data['total_detections']])
            writer.writerow(['Total de eventos de detección:', len(data['detection_history'])])
            writer.writerow([])  # Línea vacía
            
            # Resumen por tipo
            writer.writerow(['RESUMEN POR TIPO DE VEHÍCULO (CONTEO ÚNICO)'])
            writer.writerow(['Tipo de Vehículo', 'Cantidad Única', 'IDs Detectados'])
            for vehicle_type, count in data['detection_counts'].items():
                # Buscar IDs correspondientes
                ids_for_type = []
                for class_name, vehicle_ids in data.get('unique_vehicles', {}).items():
                    if data.get('vehicle_classes', {}).get(class_name) == vehicle_type:
                        ids_for_type = vehicle_ids
                        break
                
                ids_str = ', '.join(map(str, sorted(ids_for_type))) if ids_for_type else 'N/A'
                writer.writerow([vehicle_type, count, ids_str])
                
            writer.writerow([])  # Línea vacía
            
            # Detecciones únicas (primera aparición)
            writer.writerow(['PRIMERA DETECCIÓN DE CADA VEHÍCULO'])
            writer.writerow(['Timestamp', 'ID Seguimiento', 'Tipo Vehículo', 'Confianza', 'Estado'])
            
            for detection in data['detection_history']:
                writer.writerow([
                    detection['timestamp'].strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
                    detection['track_id'],
                    detection['class_display'],
                    f"{detection['confidence']:.2f}",
                    'Primera detección' if detection.get('first_seen', True) else 'Detección continua'
                ])
                
        return filename
        
    def _generate_text_report(self, data, timestamp):
        """Generar reporte en formato texto - MEJORADO"""
        filename = f"reporte_trafico_{timestamp}.txt"
        filepath = self.reports_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            # Header
            f.write("=" * 70 + "\n")
            f.write("🚗 REPORTE DE DETECCIÓN DE TRÁFICO (SIN DUPLICADOS)\n")
            f.write("=" * 70 + "\n\n")
            
            # Información general
            f.write("📋 INFORMACIÓN GENERAL\n")
            f.write("-" * 30 + "\n")
            f.write(f"Fecha de generación: {data['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Fuente de video: {data['video_source']}\n")
            f.write(f"Total de vehículos únicos: {data['total_detections']}\n")
            f.write(f"Total de eventos de detección: {len(data['detection_history'])}\n")
            
            # Período de análisis
            if 'detection_summary' in data and data['detection_summary']['detection_start_time']:
                f.write(f"Período de análisis: {data['detection_summary']['detection_start_time'].strftime('%H:%M:%S')}")
                f.write(f" - {data['detection_summary']['detection_end_time'].strftime('%H:%M:%S')}\n")
            
            f.write("\n")
            
            # Resumen por tipo
            f.write("📊 RESUMEN POR TIPO DE VEHÍCULO\n")
            f.write("-" * 40 + "\n")
            
            total_vehicles = 0
            for vehicle_type, count in data['detection_counts'].items():
                f.write(f"{vehicle_type:15} : {count:3d} vehículos\n")
                total_vehicles += count
                
            f.write("-" * 40 + "\n")
            f.write(f"{'TOTAL':15} : {total_vehicles:3d} vehículos\n\n")
            
            # Detalle de vehículos únicos
            f.write("🔍 DETALLE DE VEHÍCULOS ÚNICOS\n")
            f.write("-" * 50 + "\n")
            
            for class_name, vehicle_ids in data.get('unique_vehicles', {}).items():
                display_name = data.get('vehicle_classes', {}).get(class_name, class_name)
                if vehicle_ids:
                    f.write(f"{display_name}:\n")
                    f.write(f"  IDs detectados: {', '.join(map(str, sorted(vehicle_ids)))}\n")
                    f.write(f"  Cantidad: {len(vehicle_ids)}\n\n")
            
            # Cronología de primeras detecciones
            f.write("⏰ CRONOLOGÍA DE PRIMERAS DETECCIONES\n")
            f.write("-" * 60 + "\n")
            f.write(f"{'Hora':12} {'ID':4} {'Tipo':15} {'Confianza':10}\n")
            f.write("-" * 60 + "\n")
            
            # Ordenar por timestamp
            sorted_detections = sorted(data['detection_history'], key=lambda x: x['timestamp'])
            
            for detection in sorted_detections:
                time_str = detection['timestamp'].strftime('%H:%M:%S.%f')[:-3]
                f.write(f"{time_str:12} {detection['track_id']:4d} {detection['class_display']:15} {detection['confidence']:8.2f}\n")
            
            f.write("\n" + "=" * 70 + "\n")
            f.write("Reporte generado por Sistema de Detección de Tráfico\n")
            f.write("⚠️  Los conteos son de vehículos únicos (sin duplicados)\n")
            f.write("=" * 70 + "\n")
                
        return filename
        
    def validate_data_integrity(self, data):
        """NUEVO: Validar la integridad de los datos antes de generar reportes"""
        issues = []
        
        # Verificar que no hay duplicados en el historial
        track_ids_seen = set()
        for detection in data['detection_history']:
            vehicle_key = f"{detection['class_name']}_{detection['track_id']}"
            if vehicle_key in track_ids_seen:
                issues.append(f"Duplicado encontrado: {vehicle_key}")
            track_ids_seen.add(vehicle_key)
        
        # Verificar consistencia entre contadores y historial
        history_counts = {}
        for detection in data['detection_history']:
            class_display = detection['class_display']
            history_counts[class_display] = history_counts.get(class_display, 0) + 1
        
        for vehicle_type, expected_count in data['detection_counts'].items():
            actual_count = history_counts.get(vehicle_type, 0)
            if expected_count != actual_count:
                issues.append(f"Inconsistencia en {vehicle_type}: esperado {expected_count}, encontrado {actual_count}")
        
        return issues