from tkinter import messagebox

def info(mensaje, titulo="Información"):
    messagebox.showinfo(titulo, mensaje)

def exito(mensaje="Operación realizada correctamente", titulo="Éxito"):
    messagebox.showinfo(titulo, mensaje)

def advertencia(mensaje, titulo="Atención"):
    messagebox.showwarning(titulo, mensaje)

def error(mensaje="Ocurrió un error", titulo="Error"):
    messagebox.showerror(titulo, mensaje)


def confirmar(mensaje="¿Estás seguro?", titulo="Confirmar"):
    return messagebox.askyesno(titulo, mensaje)

def confirmar_eliminacion():
    return messagebox.askyesno(
        "Confirmar eliminación",
        "¿Seguro que querés eliminar este registro? Esta acción no se puede deshacer."
    )

def mostrar_excepcion(e, titulo="Error"):
    mensaje = str(e) if str(e) else "Ocurrió un error inesperado"
    messagebox.showerror(titulo, mensaje)

def ejecutar_con_mensajes(func, exito_msg=None):
    try:
        resultado = func()
        if exito_msg:
            exito(exito_msg)
        return resultado
    except Exception as e:
        mostrar_excepcion(e)
        return None