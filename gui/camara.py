from tkinter import messagebox, simpledialog
import os
import data.guardado as guardado
from core.reconocimiento import empezar_reconocimiento_facial

def iniciar_reconocimiento():
    
    def on_capture(path):
        name = simpledialog.askstring("Nombre", "Ingrese el nombre:")
        
        if name:
            guardado.guardar_reconocimiento_facial(path, name)
            os.remove(path)
            messagebox.showinfo("Éxito", "Rostro guardado correctamente")
        else:
            messagebox.showwarning("Error", "No se ingresó un nombre.")

    def on_error(msg):
        messagebox.showerror("Error", msg)

    empezar_reconocimiento_facial(on_capture, on_error)