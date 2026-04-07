import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import sqlite3
import io
import cv2
import numpy as np
import serial
import datetime
import os

# Conexión con Arduino (cambia 'COM4' si es necesario)
# try:
#     arduino = serial.Serial('COM4', 9600, timeout=1)
# except Exception as e:
#     arduino = None
#     print(f"No se pudo conectar con Arduino: {e}")

# checkbox_vars = []
# record_ids = []


# def create_table():
#     try:
#         conn = sqlite3.connect('reconocimientos.db')
#         cursor = conn.cursor()
#         cursor.execute("DROP TABLE IF EXISTS reconocimientos")
#         cursor.execute('''
#         CREATE TABLE IF NOT EXISTS reconocimientos (
#             id INTEGER PRIMARY KEY,
#             fecha TEXT,
#             nombre TEXT,
#             imagen BLOB
#         )''')
#         conn.commit()
#         conn.close()
#         messagebox.showinfo("Éxito", "Tabla creada correctamente.")
#     except Exception as e:
#         messagebox.showerror("Error", f"Ocurrió un error al crear la tabla: {e}") 
def save_recognition(image_path, name):
    try:
        conn = sqlite3.connect('reconocimientos.db')
        cursor = conn.cursor()
        with open(image_path, 'rb') as image_file:
            img_data = image_file.read()
        cursor.execute("INSERT INTO usuarios (fecha, nombre, imagen) VALUES (strftime('%Y-%m-%d', 'now', 'localtime'), ?, ?)", (name, img_data))
        conn.commit()
        conn.close()
        messagebox.showinfo("Éxito", "Reconocimiento e imagen guardados exitosamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")


def start_face_recognition():
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
                remaining = int(10 - elapsed)

                if remaining > 0:
                    cv2.putText(frame, f"Capturando en {remaining} segundos...", (50, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                else:
                    cv2.imwrite("temp_face.jpg", frame)
                    cap.release()
                    cv2.destroyAllWindows()

                    name = simpledialog.askstring("Nombre", "Por favor, ingrese el nombre de la persona:")
                    if name:
                        save_recognition("temp_face.jpg", name)
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


def show_records():
    global checkbox_vars, record_ids
    checkbox_vars = []
    record_ids = []
    try:
        conn = sqlite3.connect('reconocimientos.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios ORDER BY fecha DESC")
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            messagebox.showinfo("Consulta", "No hay registros en la base de datos.")
            return

        records_window = tk.Toplevel(root)
        records_window.title("Registros de Reconocimientos")

        canvas = tk.Canvas(records_window)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(records_window, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)
        frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor="nw")

        for i, row in enumerate(rows):
            if len(row) != 4:
                continue
            record_id, fecha, nombre, img_data = row
            tk.Label(frame, text=f"ID: {record_id}\nFecha de Registro: {fecha}\nNombre: {nombre}").grid(row=i, column=0, padx=10, pady=5, sticky="w")

            try:
                img = Image.open(io.BytesIO(img_data))
                img.thumbnail((100, 100))
                img_tk = ImageTk.PhotoImage(img)
                img_label = tk.Label(frame, image=img_tk)
                img_label.image = img_tk
                img_label.grid(row=i, column=1, padx=10, pady=5)
            except Exception:
                tk.Label(frame, text="Imagen no disponible").grid(row=i, column=1, padx=10, pady=5)

            var = tk.IntVar()
            checkbox = tk.Checkbutton(frame, variable=var)
            checkbox.grid(row=i, column=2, padx=10, pady=5)
            checkbox_vars.append(var)
            record_ids.append(record_id)

        del_btn = tk.Button(frame, text="Eliminar seleccionados", command=lambda: delete_selected_records(records_window))
        del_btn.grid(row=len(rows)+1, column=0, columnspan=3, pady=10)

        frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")


def delete_selected_records(records_window=None):
    try:
        conn = sqlite3.connect('reconocimientos.db')
        cursor = conn.cursor()
        selected_ids = [record_ids[i] for i, var in enumerate(checkbox_vars) if var.get() == 1]

        if selected_ids:
            cursor.execute(f"DELETE FROM usuarios WHERE id IN ({','.join('?' for _ in selected_ids)})", selected_ids)
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Registros eliminados exitosamente.")

            if records_window:
                records_window.destroy()
                show_records()
        else:
            messagebox.showinfo("Error", "No se ha seleccionado ningún registro para eliminar.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")


def validate_face_recognition():
    try:
        conn = sqlite3.connect('reconocimientos.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios ORDER BY fecha DESC LIMIT 1")
        row = cursor.fetchone()
        conn.close()

        if row:
            img_data = row[3]
            img = Image.open(io.BytesIO(img_data))
            img_tk = ImageTk.PhotoImage(img)

            top = tk.Toplevel(root)
            top.title("Última Imagen Reconocida")
            label = tk.Label(top, image=img_tk)
            label.image = img_tk
            label.pack()
        else:
            messagebox.showinfo("Validación", "No hay registros para validar.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al validar la imagen: {e}")


def entrada():
    try:
        conn = sqlite3.connect('reconocimientos.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, imagen FROM usuarios")
        registros = cursor.fetchall()

        if not registros:
            messagebox.showinfo("Salida", "No hay imágenes en la base de datos.")
            conn.close()
            return

        known_faces = []
        known_names = []
        known_ids = []

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        for id_usuario, nombre, img_data in registros:
            img = Image.open(io.BytesIO(img_data)).convert('L')
            img_np = np.array(img)
            faces = face_cascade.detectMultiScale(img_np, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                known_faces.append(img_np[y:y+h, x:x+w])
                known_names.append(nombre)
                known_ids.append(id_usuario)

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Error", "No se pudo abrir la cámara.")
            conn.close()
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
                cursor.execute("INSERT INTO movimientos (fk_id_usuarios, fecha) VALUES (?, ?)",(usuario_id, fecha_actual))
                conn.commit()

                messagebox.showinfo("Entrada registrada",f"Bienvenido: {usuario_encontrado}\nFecha y hora: {fecha_actual2}")

                cap.release()
                cv2.destroyAllWindows()
                break

            cv2.imshow('Activar entrada', frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break

        if not encontrado:
            messagebox.showinfo("Entrada", "No se encontró coincidencia de rostro.")

        conn.close()

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

def salida():
    try:
        conn = sqlite3.connect('reconocimientos.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, imagen FROM usuarios")
        registros = cursor.fetchall()

        if not registros:
            messagebox.showinfo("Salida", "No hay imágenes en la base de datos.")
            conn.close()
            return

        known_faces = []
        known_names = []
        known_ids = []

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        for id_usuario, nombre, img_data in registros:
            img = Image.open(io.BytesIO(img_data)).convert('L')
            img_np = np.array(img)
            faces = face_cascade.detectMultiScale(img_np, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                known_faces.append(img_np[y:y+h, x:x+w])
                known_names.append(nombre)
                known_ids.append(id_usuario)

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Error", "No se pudo abrir la cámara.")
            conn.close()
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
                cursor.execute(
                    "INSERT INTO movimientos (fk_id_usuarios, fecha) VALUES (?, ?)",(usuario_id, fecha_actual))
                conn.commit()

                messagebox.showinfo("Salida registrada",f"Hasta luego: {usuario_encontrado}\nFecha y hora: {fecha_actual2}")

                cap.release()
                cv2.destroyAllWindows()
                break

            cv2.imshow('Activar salida', frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break

        if not encontrado:
            messagebox.showinfo("Salida", "No se encontró coincidencia de rostro.")

        conn.close()

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")


root = tk.Tk()
root.title("Reconocimiento Facial y Gestión de Registros")

btn_start_recognition = tk.Button(root, text="Nuevo usuario", command=start_face_recognition)
btn_start_recognition.pack(pady=5)

btn_show_records = tk.Button(root, text="Mostrar Usuarios", command=show_records)
btn_show_records.pack(pady=5)

btn_apertura = tk.Button(root, text="Validar entrada", command=entrada)
btn_apertura.pack(pady=5)   

btn_apertura = tk.Button(root, text="Validar salida", command=salida)
btn_apertura.pack(pady=5)



root.mainloop()
