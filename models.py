from tkinter import *
from tkinter import ttk, messagebox
import sqlite3


class VentanaEditar:
    def __init__(self, ventana_principal, screen, nombre, precio):
        self.db = 'database/productos.db'
        self.ventana_principal = ventana_principal
        self.nombre = nombre
        self.precio = precio
        self.ventana = screen
        self.ventana.title("Editor de Productos")
        self.ventana.resizable(1, 1)
        self.ventana.wm_iconbitmap('recursos/icon.ico')
        self.frame = LabelFrame(self.ventana, text="Editar un Producto", font=('Calibri', 14, 'bold'))
        self.frame.grid(row=0, column=0, columnspan=2, pady=20, padx=20)

        self.etiqueta_nombre_antiguo = Label(self.frame, text="Nombre Antiguo: ")
        self.etiqueta_nombre_antiguo.grid(row=1, column=0)
        self.nombre_antiguo = Entry(self.frame)
        self.nombre_antiguo.insert(0, f"{self.nombre}")
        self.nombre_antiguo.config(state="readonly")
        self.nombre_antiguo.grid(row=1, column=1)

        self.etiqueta_nombre_nuevo = Label(self.frame, text="Nombre Nuevo: ")
        self.etiqueta_nombre_nuevo.grid(row=2, column=0)
        self.nombre_nuevo = Entry(self.frame)
        self.nombre_nuevo.grid(row=2, column=1)

        self.etiqueta_precio_antiguo = Label(self.frame, text="Precio Antiguo: ")
        self.etiqueta_precio_antiguo.grid(row=3, column=0)
        self.precio_antiguo = Entry(self.frame)
        self.precio_antiguo.insert(0, f"{self.precio}")
        self.precio_antiguo.config(state="readonly")
        self.precio_antiguo.grid(row=3, column=1)

        self.etiqueta_precio_nuevo = Label(self.frame, text="Precio Nuevo: ")
        self.etiqueta_precio_nuevo.grid(row=4, column=0)
        self.precio_nuevo = Entry(self.frame)
        self.precio_nuevo.grid(row=4, column=1)


        self.guardar_cambios_boton = Button(self.frame, text="Guardar Cambios", command=self.actualizar_producto,
                                            font=('Calibri', 12, 'bold'))
        self.guardar_cambios_boton.grid(row=5, column=0, columnspan=2, sticky= W + E)

    def actualizar_producto(self):
        nombre_antiguo = self.nombre_antiguo.get()
        nombre_nuevo = self.nombre_nuevo.get()
        precio_antiguo = self.precio_antiguo.get()
        precio_nuevo = self.precio_nuevo.get()
        if nombre_nuevo == "":
            nombre_nuevo = nombre_antiguo
        if precio_nuevo == "":
            precio_nuevo = precio_antiguo

        information_correcta = messagebox.askokcancel(title="Confirm Info",
                                                      message=f"Esta informacion es correcta?:\n"
                                                              f"Nombre Nuevo: {nombre_nuevo}\n"
                                                              f"Precio Nuevo: {precio_nuevo}\n")
        if information_correcta:
            query = "UPDATE producto SET nombre = ?, precio = ? WHERE nombre = ?"
            parametros = (nombre_nuevo, precio_nuevo, self.nombre)
            self.ventana_principal.db_consulta(query, parametros)
            self.ventana_principal.get_productos()
            self.ventana.destroy()


class VentanaPrincipal:

    def __init__(self, screen):
        self.db = 'database/productos.db'
        self.ventana = screen
        self.ventana.title("Gestor de Productos")
        self.ventana.resizable(1, 1)
        self.ventana.wm_iconbitmap('recursos/icon.ico')
        self.frame = LabelFrame(self.ventana, text="Registrar un nuevo Producto", font=('Calibri', 10, 'bold'))
        self.frame.grid(row=0, column=0, columnspan=3, pady=20)
        self.etiqueta_nombre = Label(self.frame, text="Nombre: ")
        self.etiqueta_nombre.grid(row=1, column=0)
        self.nombre = Entry(self.frame)
        self.nombre.focus()
        self.nombre.grid(row=1, column=1)
        self.etiqueta_precio = Label(self.frame, text="Precio: ")
        self.etiqueta_precio.grid(row=2, column=0)
        self.precio = Entry(self.frame)
        self.precio.grid(row=2, column=1)
        self.boton_guardar_producto = Button(self.frame, text="Guardar Producto", command=self.agregar_producto,
                                             font=('Calibri', 12, 'bold'))
        self.boton_guardar_producto.grid(row=3, column=0, columnspan=3, sticky=W + E)
        self.boton_editar_producto = Button(text="Editar", command=self.editar_producto, font=('Calibri', 12, 'bold'))
        self.boton_editar_producto.grid(row=5, column=0, sticky=W + E)
        self.boton_eliminar_producto = Button(text="Eliminar", command=self.eliminar_producto, font=('Calibri', 12, 'bold'))
        self.boton_eliminar_producto.grid(row=5, column=1, sticky=W + E)

        # ------------------- TABLA DE PRODUCTOS ------------------#

        self.style = ttk.Style()
        self.style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11))
        self.style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'))
        self.style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

        self.tabla = ttk.Treeview(height=20, columns=2, style="mystyle.Treeview")
        self.tabla.grid(row=4, column=0, columnspan=2)
        self.tabla.heading('#0', text='Nombre', anchor=CENTER)
        self.tabla.heading('#1', text='Precio', anchor=CENTER)

        # ------------------- CORRER FUNCIONES ------------------#

        self.get_productos()

    def db_consulta(self, consulta, parametros=()):
        with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            resultado = cursor.execute(consulta, parametros)
            con.commit()
        return resultado

    def get_productos(self):
        registros_tabla = self.tabla.get_children()
        for fila in registros_tabla:
            self.tabla.delete(fila)

        query = 'SELECT * FROM producto ORDER BY nombre DESC'
        registros_db = self.db_consulta(query)
        for fila in registros_db:
            self.tabla.insert('', 0, text=fila[1], values=fila[2])

    def validar_nombre(self):
        return self.nombre.get().strip() != ""

    def validar_precio(self):
        try:
            precio = float(self.precio.get())
            return precio > 0
        except ValueError:
            return False

    def agregar_producto(self):
        if not self.validar_nombre():
            messagebox.showerror(title="Error", message="El nombre es obligatorio!")
            return
        if not self.validar_precio():
            messagebox.showerror(title="Error", message="El precio es obligatorio!")
            return
        else:
            information_correcta = messagebox.askokcancel(title="Confirm Info",
                                                         message=f"Esta informacion es correcta?:\n"
                                                                 f"Nombre: {self.nombre.get()}\n"
                                                                 f"Precio: {self.precio.get()}\n")
            if information_correcta:
                query = 'INSERT INTO producto VALUES(NULL, ?, ?)'
                parametros = (self.nombre.get(), self.precio.get())
                self.db_consulta(query, parametros)
                self.get_productos()
                messagebox.showinfo(title="Producto Agregado",
                                    message=f"El producto {self.nombre.get()} ha sido agregado correctamente")
                self.nombre.delete(0, END)
                self.precio.delete(0, END)
            else:
                pass

    def eliminar_producto(self):
        producto = self.tabla.item(self.tabla.selection())["text"]
        if producto != "":
            eliminar_confirmacion = messagebox.showwarning(title="Advertencia",
                                                           message=f"Esta a punto de eliminar {producto}\n"
                                                                   f"Desea continuar?")
            if eliminar_confirmacion:
                query = "DELETE FROM producto WHERE nombre = ?"
                self.db_consulta(query, (producto,))
                self.get_productos()
        else:
            messagebox.showerror(title="Error", message="Debe seleccionar un producto")

    def editar_producto(self):
        producto = self.tabla.item(self.tabla.selection())
        if producto["text"] != "":
            nombre = producto["text"]
            precio = producto["values"][0]
            screen = Tk()
            VentanaEditar(self, screen, nombre, precio)

        else:
            messagebox.showerror(title="Error", message="Debe seleccionar un producto")




