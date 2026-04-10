# 🎯 Sistema de Reconocimiento Facial

Aplicación de escritorio desarrollada en Python que permite identificar y gestionar usuarios mediante reconocimiento facial, utilizando una interfaz gráfica basada en Tkinter y almacenamiento local con SQLite.

---

## 🚧 Estado del proyecto

⚠️ **En desarrollo activo**
El proyecto se encuentra en una etapa temprana. Algunas funcionalidades pueden ser inestables o estar incompletas.

---

## 📌 Descripción

Este sistema permite registrar usuarios junto con sus datos faciales y posteriormente identificarlos mediante procesamiento de imágenes en tiempo real. Está orientado a fines educativos y experimentales en el área de visión por computadora.

---

## ✨ Funcionalidades actuales

* Registro de usuarios
* Captura de datos faciales desde cámara
* Identificación básica de usuarios
* Almacenamiento de datos en SQLite (Configurable)
* Interfaz gráfica con Tkinter
* Inicialización automática de base de datos

---

## 🛠️ Tecnologías utilizadas

* **Python 3**
* **Tkinter** — interfaz gráfica
* **SQLite** — base de datos local
* **OpenCV** — procesamiento de imágenes

---

## 📦 Requisitos

* Python 3.8 o superior
* pip
* Cámara web funcional

---

## ⚙️ Instalación

Clonar el repositorio:

```bash
git clone https://github.com/tu-usuario/sistema-reconocimiento-facial.git
cd sistema-reconocimiento-facial
```

Crear entorno virtual (recomendado):

```bash
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

---

## ▶️ Ejecución

```bash
python main.py
```

Al iniciar por primera vez:

* Se creará automáticamente la base de datos (`recfac.db`)
* Se inicializarán las tablas necesarias

---

## 📁 Estructura del proyecto

```bash
.
├── main.py              # Punto de entrada de la aplicación
├── db.py                # Gestión de base de datos
├── reconocimientos.db   # Base de datos SQLite
├── requirements.txt
└── README.md
```

---

## ⚠️ Consideraciones

* Este proyecto no está optimizado para entornos productivos
* El reconocimiento facial puede variar según condiciones de iluminación y calidad de cámara
* No se implementan aún medidas avanzadas de seguridad o privacidad de datos

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para cambios importantes, se recomienda abrir un issue previamente para discutir la propuesta.

---

## 📄 Licencia

Este proyecto no tiene una licencia pública por el momento.  
Todos los derechos están reservados.

No está permitido usar, copiar, modificar ni distribuir este código sin autorización explícita del autor.
