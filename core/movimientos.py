import cv2
import datetime
import numpy as np
from PIL import Image
import io

def reconocer_usuario(registros):
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )

    known_faces = []
    known_names = []
    known_ids = []

    for id, fecha, nombre, imagen in registros:
        img = Image.open(io.BytesIO(imagen)).convert('L')
        img_np = np.array(img)

        faces = face_cascade.detectMultiScale(
            img_np, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
        )

        for (x, y, w, h) in faces:
            known_faces.append(img_np[y:y+h, x:x+w])
            known_names.append(nombre)
            known_ids.append(id)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return {"error": "No se pudo abrir la cámara."}

    encontrado = False
    usuario_encontrado = None
    usuario_id = None
    path = "temp_face.jpg"

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
        )

        for (x, y, w, h) in faces:
            rostro_actual = gray[y:y+h, x:x+w]

            for i, known in enumerate(known_faces):
                try:
                    rostro_actual_resized = cv2.resize(
                        rostro_actual, (known.shape[1], known.shape[0])
                    )

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
            fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            hora = datetime.datetime.now().strftime("%H:%M:%S")

            cv2.imwrite(path, frame)

            cap.release()
            cv2.destroyAllWindows()

            return {
                "ok": True,
                "usuario": usuario_encontrado,
                "id": usuario_id,
                "fecha": fecha,
                "hora": hora,
                "imagen": path
            }

        cv2.imshow('Activar entrada', frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    return {"ok": False}