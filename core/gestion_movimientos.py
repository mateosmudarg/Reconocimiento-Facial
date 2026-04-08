import os
from tkinter import messagebox
import cv2
import datetime
import numpy as np
from PIL import Image
import io
from data.db import obtener_usuarios
from data.guardado import guardar_movimiento

def facial(tipo):
    try:
        registros = obtener_usuarios(asc=True, limit=0)
        if not registros:
            messagebox.showinfo("Salida", "No hay imágenes en la base de datos.")
            return

        known_faces = []
        known_names = []
        known_ids = []

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        for id, fecha, nombre, imagen in registros:
            img = Image.open(io.BytesIO(imagen)).convert('L')
            img_np = np.array(img)
            faces = face_cascade.detectMultiScale(img_np, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                known_faces.append(img_np[y:y+h, x:x+w])
                known_names.append(nombre)
                known_ids.append(id)

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Error", "No se pudo abrir la cámara.")
            return

        encontrado = False
        usuario_encontrado = None
        usuario_id = None

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                rostro_actual = gray[y:y+h, x:x+w]

                for i, known in enumerate(known_faces):
                    try:
                        rostro_actual_resized = cv2.resize(rostro_actual, (known.shape[1], known.shape[0]))
                        diff = cv2.absdiff(rostro_actual_resized, known)

                        if np.mean(diff) < 40:
                            encontrado = True
                            usuario_encontrado = known_names[i]
                            usuario_id = known_ids[i]
                            break
                    except Exception:
                        continue

                if encontrado:
                    break

            if encontrado:
                fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                fecha_actual2 = datetime.datetime.now().strftime("%H:%M:%S")
                cv2.imwrite("temp_face.jpg", frame)
                messagebox.showinfo("Entrada registrada",f"Bienvenido: {usuario_encontrado}\nFecha y hora: {fecha_actual2}")
                guardar_movimiento(usuario_id, fecha_actual, "temp_face.jpg", tipo)
                
                cap.release()
                cv2.destroyAllWindows()
                os.remove("temp_face.jpg")
                break
            cv2.imshow('Activar entrada', frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break

        if not encontrado:
            messagebox.showinfo("Entrada", "No se encontró coincidencia de rostro.")


    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")
