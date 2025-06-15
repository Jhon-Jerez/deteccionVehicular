# test_detector_debug.py
"""
Script para probar y debuggear el DetectorManager
Ejecuta este script para identificar exactamente dónde está el problema de conteo
"""

import time
from detector_manager import DetectorManager

class MockMainWindow:
    """Mock de la ventana principal para testing"""
    def __init__(self):
        self.root = None
    
    def update_video_display(self, frame):
        pass
    
    def update_statistics(self, counts):
        print(f"📊 UI Update - Counts: {counts}")

def test_detector_counting():
    """Función de prueba para verificar el conteo"""
    print("🧪 INICIANDO PRUEBA DE CONTEO DE VEHÍCULOS")
    print("="*60)
    
    # Crear instancia del detector
    mock_window = MockMainWindow()
    detector = DetectorManager(mock_window)
    
    # Configurar video de prueba
    detector.set_video_source("1.mp4")  # Asegúrate de que este archivo existe
    
    try:
        # Iniciar detección
        print("▶️  Iniciando detección...")
        detector.iniciar_deteccion()
        
        # Dejar correr por 30 segundos para capturar suficientes datos
        print("⏳ Ejecutando detección por 30 segundos...")
        
        for i in range(30):
            time.sleep(1)
            
            # Cada 5 segundos, mostrar estadísticas
            if (i + 1) % 5 == 0:
                print(f"\n--- Segundo {i+1} ---")
                stats = detector.get_detection_statistics()
                
                # Verificar consistencia
                detector.debug_detection_state()
        
        # Estadísticas finales
        print("\n" + "="*60)
        print("📊 ESTADÍSTICAS FINALES")
        print("="*60)
        
        final_stats = detector.get_detection_statistics()
        
        # Obtener datos para reporte
        report_data = detector.get_detection_data()
        
        print(f"\n🎯 RESULTADOS DE LA PRUEBA:")
        print(f"   - Vehículos únicos detectados: {report_data['total_detections']}")
        print(f"   - Eventos en historial: {len(report_data['detection_history'])}")
        print(f"   - IDs únicos rastreados: {len(detector.tracked_vehicles)}")
        
        # Verificar si hay inconsistencias
        total_from_counters = sum(len(ids) for ids in detector.vehicle_counters.values())
        history_count = len(report_data['detection_history'])
        tracked_count = len(detector.tracked_vehicles)
        
        print(f"\n🔍 VERIFICACIÓN DE CONSISTENCIA:")
        print(f"   - Total desde contadores: {total_from_counters}")
        print(f"   - Total desde historial: {history_count}")
        print(f"   - Total IDs rastreados: {tracked_count}")
        
        all_consistent = (total_from_counters == history_count == tracked_count)
        print(f"   - ¿Todos consistentes?: {'✅ SÍ' if all_consistent else '❌ NO'}")
        
        if not all_consistent:
            print("\n⚠️  PROBLEMA DETECTADO - INCONSISTENCIA EN CONTEOS")
            print("🔧 Posibles causas:")
            print("   1. IDs duplicados en contadores")
            print("   2. Historial con entradas duplicadas")
            print("   3. Problema en la lógica de tracking")
            
            # Debug detallado
            detector.debug_detection_state()
        else:
            print("\n✅ ¡CONTEOS CONSISTENTES! El problema está resuelto.")
        
        # Detener detección
        print("\n⏹️  Deteniendo detección...")
        detector.detener_deteccion()
        
        return report_data
        
    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")
        detector.detener_deteccion()
        return None

def verify_report_data(report_data):
    """Verificar la integridad de los datos del reporte"""
    if not report_data:
        return
    
    print("\n" + "="*60)
    print("📋 VERIFICACIÓN DE DATOS DEL REPORTE")
    print("="*60)
    
    # Verificar duplicados en el historial
    track_ids_in_history = []
    for detection in report_data['detection_history']:
        track_ids_in_history.append(detection['track_id'])
    
    unique_ids_in_history = set(track_ids_in_history)
    
    print(f"🔍 Análisis del historial:")
    print(f"   - Total entradas: {len(track_ids_in_history)}")
    print(f"   - IDs únicos: {len(unique_ids_in_history)}")
    print(f"   - ¿Hay duplicados?: {'❌ SÍ' if len(track_ids_in_history) != len(unique_ids_in_history) else '✅ NO'}")
    
    if len(track_ids_in_history) != len(unique_ids_in_history):
        # Encontrar duplicados
        duplicates = []
        seen = set()
        for tid in track_ids_in_history:
            if tid in seen:
                duplicates.append(tid)
            seen.add(tid)
        
        print(f"   - IDs duplicados: {set(duplicates)}")
    
    # Verificar conteos por tipo
    print(f"\n📊 Conteos por tipo:")
    for vehicle_type, count in report_data['detection_counts'].items():
        print(f"   - {vehicle_type}: {count}")

if __name__ == "__main__":
    # Ejecutar prueba
    report_data = test_detector_counting()
    
    # Verificar datos del reporte
    verify_report_data(report_data)
    
    print("\n" + "="*60)
    print("🏁 PRUEBA COMPLETADA")
    print("="*60)