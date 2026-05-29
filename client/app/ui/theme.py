"""Hoja de estilos (QSS) moderna y oscura, coherente con el panel web."""

QSS = """
* { font-family: 'Segoe UI', sans-serif; color: #e2e8f0; }
QWidget#root { background: #0f172a; }
QLabel#logo { font-size: 26px; font-weight: 700; }
QLabel#title { font-size: 20px; font-weight: 600; }
QLabel#subtitle { color: #94a3b8; font-size: 13px; }
QLabel#video { background: #1e293b; border: 1px solid #334155; border-radius: 14px; }
QLabel#status { font-size: 15px; font-weight: 600; padding: 10px; border-radius: 10px; background: #1e293b; }

QFrame#card { background: #1e293b; border: 1px solid #334155; border-radius: 16px; }

QLineEdit, QComboBox {
    background: #273449; border: 1px solid #334155; border-radius: 10px;
    padding: 10px 12px; font-size: 14px; selection-background-color: #6366f1;
}
QLineEdit:focus, QComboBox:focus { border: 1px solid #6366f1; }

QPushButton {
    border: none; border-radius: 10px; padding: 12px 18px;
    font-size: 14px; font-weight: 600; background: #273449;
}
QPushButton:hover { background: #334155; }
QPushButton#primary { background: #6366f1; color: white; }
QPushButton#primary:hover { background: #818cf8; }
QPushButton#entrada { background: #16a34a; color: white; font-size: 16px; padding: 18px; }
QPushButton#entrada:hover { background: #22c55e; }
QPushButton#salida  { background: #dc2626; color: white; font-size: 16px; padding: 18px; }
QPushButton#salida:hover { background: #ef4444; }

QLabel#err { color: #ef4444; font-size: 13px; }
"""
