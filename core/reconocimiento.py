import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import data.guardado as guardado
import cv2
import datetime
import os

def empezar_reconocimiento_facial():
    try:
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Error", "No se pudo abrir la cámara.")
            return

        countdown_started = False
        countdown_start_time = None

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            if len(faces) > 0:
                if not countdown_started:
                    countdown_started = True
                    countdown_start_time = datetime.datetime.now()

                elapsed = (datetime.datetime.now() - countdown_start_time).total_seconds()
                remaining = int(5 - elapsed)

                if remaining > 0:
                    cv2.putText(frame, f"Capturando en {remaining} segundos...", (50, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                else:
                    cv2.imwrite("temp_face.jpg", frame)
                    cap.release()
                    cv2.destroyAllWindows()

                    name = simpledialog.askstring("Nombre", "Por favor, ingrese el nombre de la persona:")
                    if name:
                        guardado.guardar_reconocimiento_facial("temp_face.jpg", name)
                        os.remove("temp_face.jpg")
                    else:
                        messagebox.showwarning("Error", "No se ingresó un nombre.")
                    return
            else:
                countdown_started = False
                countdown_start_time = None

            cv2.imshow('Reconocimiento Facial', frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break

        cap.release()
        cv2.destroyAllWindows()

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")