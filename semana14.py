import tkinter as tk
from tkinter import ttk, messagebox

# =========================
# MODELO
# =========================
class Visitante:
    def __init__(self, cedula, nombre, motivo):
        self.cedula = cedula
        self.nombre = nombre
        self.motivo = motivo


# =========================
# SERVICIO (CRUD)
# =========================
class VisitaServicio:
    def __init__(self):
        self.visitantes = []

    def registrar(self, visitante):
        # Validar cédula única
        for v in self.visitantes:
            if v.cedula == visitante.cedula:
                return False
        self.visitantes.append(visitante)
        return True

    def listar(self):
        return self.visitantes

    def eliminar(self, cedula):
        for v in self.visitantes:
            if v.cedula == cedula:
                self.visitantes.remove(v)
                return True
        return False


# =========================
# UI (Tkinter)
# =========================
class AppTkinter:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Visitantes")
        self.root.geometry("600x400")

        self.servicio = VisitaServicio()

        # =========================
        # FORMULARIO
        # =========================
        frame_form = tk.LabelFrame(root, text="Datos del Visitante")
        frame_form.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_form, text="Cédula:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_cedula = tk.Entry(frame_form)
        self.entry_cedula.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Nombre:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_nombre = tk.Entry(frame_form)
        self.entry_nombre.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Motivo:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_motivo = tk.Entry(frame_form)
        self.entry_motivo.grid(row=2, column=1, padx=5, pady=5)

        # =========================
        # BOTONES
        # =========================
        frame_botones = tk.Frame(root)
        frame_botones.pack(fill="x", padx=10, pady=5)

        tk.Button(frame_botones, text="Registrar", command=self.registrar).pack(side="left", padx=5)
        tk.Button(frame_botones, text="Eliminar", command=self.eliminar).pack(side="left", padx=5)
        tk.Button(frame_botones, text="Limpiar", command=self.limpiar_campos).pack(side="left", padx=5)

        # =========================
        # TABLA (TREEVIEW)
        # =========================
        frame_tabla = tk.Frame(root)
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(frame_tabla, columns=("Cedula", "Nombre", "Motivo"), show="headings")
        self.tree.heading("Cedula", text="Cédula")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Motivo", text="Motivo")

        self.tree.pack(fill="both", expand=True)

    # =========================
    # FUNCIONES UI
    # =========================
    def registrar(self):
        cedula = self.entry_cedula.get()
        nombre = self.entry_nombre.get()
        motivo = self.entry_motivo.get()

        if not cedula or not nombre or not motivo:
            messagebox.showwarning("Error", "Todos los campos son obligatorios")
            return

        visitante = Visitante(cedula, nombre, motivo)

        if self.servicio.registrar(visitante):
            messagebox.showinfo("Éxito", "Visitante registrado correctamente")
            self.actualizar_tabla()
            self.limpiar_campos()
        else:
            messagebox.showerror("Error", "La cédula ya existe")

    def actualizar_tabla(self):
        for fila in self.tree.get_children():
            self.tree.delete(fila)

        for v in self.servicio.listar():
            self.tree.insert("", "end", values=(v.cedula, v.nombre, v.motivo))

    def eliminar(self):
        seleccionado = self.tree.selection()

        if not seleccionado:
            messagebox.showwarning("Error", "Seleccione un registro")
            return

        valores = self.tree.item(seleccionado)["values"]
        cedula = valores[0]

        if self.servicio.eliminar(cedula):
            messagebox.showinfo("Éxito", "Registro eliminado")
            self.actualizar_tabla()
        else:
            messagebox.showerror("Error", "No se pudo eliminar")

    def limpiar_campos(self):
        self.entry_cedula.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)
        self.entry_motivo.delete(0, tk.END)


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    root = tk.Tk()
    app = AppTkinter(root)
    root.mainloop()