import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import io
from data.db import obtener_movimientos, obtener_usuarios
from datetime import datetime

def mostrar_movimientos(parent):
    top = tk.Toplevel(parent)
    top.title("Movimientos Registrados")
    top.geometry("950x550")
    top.configure(bg="#f0f0f0")

    container = ttk.Frame(top)
    container.pack(fill="both", expand=True, padx=10, pady=10)

    style = ttk.Style()
    style.configure("Treeview", font=("Helvetica", 10), rowheight=25)
    style.configure("Treeview.Heading", font=("Helvetica", 11, "bold"))
    style.map("Treeview.Heading", background=[("active", "#d9d9d9")])
    style.configure("TLabel", background="#f0f0f0")

    filtro_frame = ttk.Frame(container)
    filtro_frame.pack(side="top", fill="x", pady=5)
    ttk.Label(filtro_frame, text="Filtrar por tipo:").pack(side="left", padx=5)
    tipo_var = tk.StringVar()
    tipo_filtro = ttk.Combobox(filtro_frame, textvariable=tipo_var, state="readonly")
    tipo_filtro['values'] = ("Todos", "Entrada", "Salida")
    tipo_filtro.current(0)
    tipo_filtro.pack(side="left", padx=5)

    columnas = ("ID", "Usuario", "Fecha", "Tipo")
    tree = ttk.Treeview(container, columns=columnas, show="headings")
    tree.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(container, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="left", fill="y")

    panel = ttk.Frame(container, width=250)
    panel.pack(side="right", fill="y")
    label_img = tk.Label(panel, bg="#e0e0e0", width=200, height=200)
    label_img.pack(pady=20)
    img_preview = None

    try:
        movimientos = obtener_movimientos(limit=0)
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return

    try:
        usuarios = obtener_usuarios(limit=0)
        id_a_nombre = {u[0]: u[2] for u in usuarios}
    except Exception as e:
        messagebox.showerror("Error al cargar usuarios", str(e))
        return

    movimientos_filtrados = movimientos.copy()

    def actualizar_tabla(data):
        tree.delete(*tree.get_children())
        for i, mov in enumerate(data):
            usuario_nombre = id_a_nombre.get(mov[1], f"Usuario {mov[1]}")
            tree.insert("", tk.END, values=(mov[0], usuario_nombre, mov[2], mov[4]),
                        tags=("evenrow" if i % 2 == 0 else "oddrow",))
        tree.tag_configure("evenrow", background="#ffffff")
        tree.tag_configure("oddrow", background="#f9f9f9")

    def aplicar_filtro(*args):
        tipo = tipo_var.get()
        if tipo == "Todos":
            movimientos_filtrados[:] = movimientos
        else:
            movimientos_filtrados[:] = [m for m in movimientos if m[4] == tipo]
        actualizar_tabla(movimientos_filtrados)

    tipo_var.trace_add("write", aplicar_filtro)
    actualizar_tabla(movimientos_filtrados)

    def mostrar_preview(event):
        nonlocal img_preview
        sel = tree.selection()
        if not sel:
            return
        index = tree.index(sel[0])
        blob = movimientos_filtrados[index][3]
        try:
            img = Image.open(io.BytesIO(blob))
            img.thumbnail((200, 200))
            img_preview = ImageTk.PhotoImage(img)
            label_img.config(image=img_preview)
        except:
            label_img.config(image="", text="Sin imagen")

    def abrir_imagen(event):
        sel = tree.selection()
        if not sel:
            return
        index = tree.index(sel[0])
        blob = movimientos_filtrados[index][3]
        try:
            top_img = tk.Toplevel(top)
            top_img.title("Imagen completa")
            img = Image.open(io.BytesIO(blob))
            img_tk = ImageTk.PhotoImage(img)
            lbl = tk.Label(top_img, image=img_tk)
            lbl.image = img_tk
            lbl.pack()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    sort_asc = True
    def ordenar_fecha():
        nonlocal sort_asc, movimientos_filtrados
        movimientos_filtrados.sort(
            key=lambda x: datetime.strptime(x[2], "%Y-%m-%d %H:%M:%S"),
            reverse=not sort_asc
        )
        sort_asc = not sort_asc
        actualizar_tabla(movimientos_filtrados)
        tree.heading("Fecha", text=f"Fecha {'▲' if sort_asc else '▼'}")

    for col in columnas:
        tree.heading(col, text=col)
    tree.heading("Fecha", text="Fecha ▲", command=ordenar_fecha)

    tree.bind("<<TreeviewSelect>>", mostrar_preview)
    tree.bind("<Double-1>", abrir_imagen)