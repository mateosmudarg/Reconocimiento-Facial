import cv2
import datetime

def guardar_usuario_facial(callback_on_capture, callback_on_error):
    try:
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            callback_on_error("No se pudo abrir la cámara.")
            return

        countdown_started = False
        countdown_start_time = None

        while True:
            ret, frame = cap.read()
            if not ret:
                callback_on_error("No se pudo leer la cámara.")
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            if len(faces) > 0:
                if not countdown_started:
                    countdown_started = True
                    countdown_start_time = datetime.datetime.now()

                elapsed = (datetime.datetime.now() - countdown_start_time).total_seconds()
                remaining = int(5 - elapsed)

                if remaining > 0:
                    cv2.putText(
                        frame,
                        f"Capturando en {remaining} segundos...",
                        (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),
                        2
                    )
                else:
                    path = "temp_face.jpg"
                    cv2.imwrite(path, frame)

                    cap.release()
                    cv2.destroyAllWindows()

                    callback_on_capture(path)
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
        callback_on_error(f"Ocurrió un error: {e}")