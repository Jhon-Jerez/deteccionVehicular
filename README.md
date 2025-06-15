# 🚗 Sistema de Detección de Tránsito con IA

Un sistema avanzado de detección y conteo de vehículos utilizando YOLO v8 y una interfaz gráfica moderna desarrollada en Python.

## ✨ Características

- **Detección en tiempo real** de múltiples tipos de vehículos
- **Tracking único** para evitar conteo duplicado
- **Interfaz moderna** con mejor experiencia de usuario
- **Generación de reportes** en múltiples formatos (JSON, CSV, TXT)
- **Visualización fluida** sin parpadeos
- **Arquitectura modular** para fácil mantenimiento

## 🚙 Tipos de Vehículos Detectados

- 🚗 Automóviles
- 🚌 Autobuses  
- 🚚 Camiones
- 🏍️ Motocicletas
- 🚲 Bicicletas
- 🚐 Camionetas

## 📋 Requisitos

### Requisitos del Sistema
- Python 3.8 o superior
- 4GB de RAM mínimo (8GB recomendado)
- GPU compatible con CUDA (opcional, para mejor rendimiento)

### Dependencias
```bash
pip install -r requirements.txt
```

## 🚀 Instalación

1. **Clonar el repositorio**
```bash
git clone <url-del-repositorio>
cd sistema-deteccion-transito
```

2. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Descargar modelo YOLO**
El modelo `yolov8n.pt` se descargará automáticamente en la primera ejecución.

## 🎮 Uso

### Ejecución Básica
```bash
python main.py
```

### Estructura de Archivos
```
sistema-deteccion-transito/
├── main.py                 # Archivo principal
├── gui/                    # Módulo de interfaz gráfica
│   ├── __init__.py
│   ├── main_window.py      # Ventana principal
│   ├── detector_manager.py # Gestor de detección
│   ├── report_generator.py # Generador de reportes
│   └── styles.py          # Estilos de la aplicación
├── reports/               # Reportes generados
├── requirements.txt       # Dependencias
└── README.md             # Este archivo
```

### Funcionalidades

#### 🎯 Detección de Vehículos
1. Ejecutar la aplicación
2. Seleccionar un archivo de video con "📁 Seleccionar Video"
3. Hacer clic en "▶️ Iniciar Detección"
4. Observar el conteo en tiempo real en el panel de estadísticas

#### 📊 Generación de Reportes
1. Después de realizar detecciones, hacer clic en "📊 Generar Reporte"
2. Seleccionar el formato deseado (JSON, CSV, o TXT)
3. El reporte se guardará en la carpeta `reports/`

#### 🧹 Gestión de Datos
- **Limpiar Datos**: Reinicia todos los contadores
- **Detener**: Para la detección actual
- **Seleccionar Video**: Cambia la fuente de video

## 🔧 Configuración

### Fuentes de Video Soportadas
- Archivos de video: `.mp4`, `.avi`, `.mov`, `.mkv`
- Cámaras web: Cambiar `"1.mp4"` por `0` en `detector_manager.py`
- Streams RTSP: Usar URL del stream

### Personalización del Modelo
Para usar un modelo YOLO diferente, modificar en `detector_manager.py`:
```python
self.model = YOLO("yolov8s.pt")  # Para mejor precisión
# o
self.model = YOLO("yolov8x.pt")  # Para máxima precisión
```

## 📈 Optimización de Rendimiento

### Para mejor rendimiento:
1. **GPU**: Instalar CUDA y PyTorch con soporte GPU
2. **Modelo más ligero**: Usar `yolov8n.pt` (nano)
3. **Resolución**: Redimensionar video de entrada si es muy grande
4. **FPS**: Ajustar `fps_limit` en `detector_manager.py`

### Control de FPS
```python
# En detector_manager.py
self.fps_limit = 15  # Reducir para mejor rendimiento
```

## 🐛 Solución de Problemas

### Problemas Comunes

**Error al cargar el video**
- Verificar que el archivo existe y es un formato soportado
- Instalar codecs adicionales: `pip install opencv-contrib-python`

**Parpadeo en la visualización**
- El nuevo sistema incluye control de FPS para eliminar parpadeos
- Ajustar `frame_delay` si es necesario

**Detección lenta**
- Usar un modelo más ligero (`yolov8n.pt`)
- Reducir resolución del video
- Verificar uso de GPU

**Memoria insuficiente**
- Cerrar otras aplicaciones
- Usar modelo nano (`yolov8n.pt`)
- Reducir `fps_limit`

## 📊 Formatos de Reporte

### JSON
Datos estructurados con metadata completa, ideal para integración con otros sistemas.

### CSV
Compatible con Excel y herramientas de análisis, incluye resumen y detalle.

### TXT
Reporte legible con estadísticas y timeline de detecciones.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork del proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit de cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 🆘 Soporte

Si tienes problemas o preguntas:
- Crear un issue en GitHub
- Revisar la documentación de [Ultralytics YOLO](https://docs.ultralytics.com/)
- Consultar la documentación de [OpenCV](https://docs.opencv.org/)

## 🔄 Actualizaciones

### v2.0.0 (Actual)
- ✅ Interfaz completamente rediseñada
- ✅ Eliminación de parpadeos
- ✅ Sistema de reportes avanzado
- ✅ Arquitectura modular
- ✅ Mejor UX/UI
- ✅ Control de rendimiento

### v1.0.0
- Funcionalidad básica de detección
- Interfaz simple
- Conteo básico

---

**Desarrollado con ❤️ usando Python, YOLO v8 y Tkinter**