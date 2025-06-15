
"""
Módulo GUI para el Sistema de Detección de Tránsito
"""

from .main_window import MainWindow
from .detector_manager import DetectorManager
from .report_generator import ReportGenerator
from .styles import AppStyles

__all__ = ['MainWindow', 'DetectorManager', 'ReportGenerator', 'AppStyles']