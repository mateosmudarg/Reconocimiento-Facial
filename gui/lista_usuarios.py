from tkinter import messagebox
import tkinter as tk   
from tkinter import ttk
from PIL import Image, ImageTk
import io
from data.db import obtener_usuarios, eliminar_usuarios_por_ids

def lista_usuarios(root):
    usuarios = obtener_usuarios(limit=0) 
    per_page = 3
    page = 1
    if not usuarios:
        messagebox.showinfo("Atención", "No hay registros en la base de datos.")
        return

    total_pages = (len(usuarios) + per_page - 1) // per_page
    if page > total_pages: 
        page = total_pages
    if page < 1:
        page = 1

    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    page_records = usuarios[start_index:end_index]

    if hasattr(lista_usuarios, "records_window") and lista_usuarios.records_window.winfo_exists():
        records_window = lista_usuarios.records_window
        for widget in records_window.winfo_children():
            widget.destroy()
    else:
        records_window = tk.Toplevel(root)
        lista_usuarios.records_window = records_window
        records_window.title("Registros")
        records_window.resizable(False, False)

    checkbox_vars = []
    record_ids = []

    style = ttk.Style(records_window)
    style.configure("Custom.Card.TFrame", padding=10)
    style.configure("Custom.TLabel", font=("Segoe UI", 10))
    style.configure("Custom.Title.TLabel", font=("Segoe UI", 11, "bold"))
    style.configure("Custom.TButton", font=("Segoe UI", 10), padding=6)

    container = ttk.Frame(records_window, padding=10)
    container.pack(fill="both", expand=True)

    canvas = tk.Canvas(container, highlightthickness=0)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor="nw")

    for i, row in enumerate(page_records):
        if len(row) != 4:
            continue
        record_id, fecha, nombre, img_data = row

        card = ttk.Frame(frame, style="Custom.Card.TFrame")
        card.grid(row=i, column=0, pady=5, sticky="ew")

        info = ttk.Label(
            card,
            text=f"ID: {record_id}\nFecha: {fecha}\nNombre: {nombre}",
            style="Custom.Title.TLabel",
            justify="left",
        )
        info.grid(row=0, column=0, padx=10, sticky="w")

        try:
            img = Image.open(io.BytesIO(img_data))
            img.thumbnail((80, 80))
            img_tk = ImageTk.PhotoImage(img)
            img_label = ttk.Label(card, image=img_tk)
            img_label.image = img_tk
            img_label.grid(row=0, column=1, padx=10)
        except Exception:
            ttk.Label(card, text="Sin imagen", style="Custom.TLabel").grid(
                row=0, column=1, padx=10
            )

        var = tk.IntVar()
        checkbox = ttk.Checkbutton(card, variable=var)
        checkbox.grid(row=0, column=2, padx=10)

        checkbox_vars.append(var)
        record_ids.append(record_id)

    def handle_delete():
        selected_ids = [
            record_ids[i] for i, var in enumerate(checkbox_vars) if var.get() == 1
        ]
        if not selected_ids:
            messagebox.showinfo("Aviso", "No se seleccionó ningún registro.")
            return
        if eliminar_usuarios_por_ids(selected_ids):
            messagebox.showinfo("Éxito", "Registros eliminados correctamente.")
            lista_usuarios(page=page, per_page=per_page)

    del_btn = ttk.Button(
        frame,
        text="Eliminar seleccionados",
        style="Custom.TButton",
        command=handle_delete,
    )
    del_btn.grid(row=len(page_records), column=0, pady=10, sticky="ew")

    # Barra de paginación
    nav_frame = ttk.Frame(frame)
    nav_frame.grid(row=len(page_records) + 1, column=0, pady=5)

    page_label = ttk.Label(nav_frame, text=f"Página {page} de {total_pages}", style="Custom.Title.TLabel")
    page_label.pack(side="top", pady=5)

    def go_prev():
        if page > 1:
            lista_usuarios(page=page - 1, per_page=per_page)

    def go_next():
        if page < total_pages:
            lista_usuarios(page=page + 1, per_page=per_page)

    btn_prev = ttk.Button(nav_frame, text="Anterior", style="Custom.TButton", command=go_prev)
    btn_next = ttk.Button(nav_frame, text="Siguiente", style="Custom.TButton", command=go_next)
    btn_prev.pack(side="left", padx=5)
    btn_next.pack(side="left", padx=5)

    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    width = frame.winfo_reqwidth() + 40
    height = min(frame.winfo_reqheight() + 40, 400)
    records_window.geometry(f"{width}x{height}")
    