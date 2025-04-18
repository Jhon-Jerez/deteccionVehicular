import cv2
import threading
from tkinter import *
from ultralytics import YOLO
from PIL import Image, ImageTk

# Cargar el modelo
model = YOLO("yolov8n.pt")

# Variables globales
detectando = False
cap = None

def iniciar_deteccion():
    global detectando, cap
    detectando = True
    cap = cv2.VideoCapture(0)  # Cámara del portátil o celular
    thread = threading.Thread(target=procesar_video)
    thread.start()

def detener_deteccion():
    global detectando, cap
    detectando = False
    if cap:
        cap.release()
    lbl_video.config(image='')

def procesar_video():
    global detectando
    while detectando:
        ret, frame = cap.read()
        if not ret:
            break

        resultados = model(frame)
        anotado = resultados[0].plot()

        # Mostrar imagen en la GUI
        img = cv2.cvtColor(anotado, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        lbl_video.imgtk = imgtk
        lbl_video.configure(image=imgtk)

# Crear ventana
ventana = Tk()
ventana.title("Detección de Tránsito con YOLOv8")
ventana.geometry("800x600")

lbl_video = Label(ventana)
lbl_video.pack()

btn_iniciar = Button(ventana, text="Iniciar Detección", command=iniciar_deteccion, bg='green', fg='white')
btn_iniciar.pack(pady=10)

btn_detener = Button(ventana, text="Detener Detección", command=detener_deteccion, bg='red', fg='white')
btn_detener.pack(pady=10)

ventana.mainloop()
