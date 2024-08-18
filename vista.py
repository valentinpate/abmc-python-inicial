import tkinter as tk
from funciones import Abmc
from tkinter import ttk
# from tkinter import messagebox as msg
# from base_biblioteca import Biblioteca


class Ventana():

    def __init__(self, window) -> None:
        self.root = window
        self.objeto_base = Abmc()
        self.root.configure(background="purple")
        self.root.title("Biblioteca")
        #self.root.get_children()

        self.titulo = tk.Label(self.root, text="Biblioteca",
                               bg="black", fg="white",
                               padx="30", pady="5", height=1, width=20)
        self.titulo.grid(row=0, column=0, columnspan=4, pady="10")

        # bib_id = 0
        self.titulo_val = tk.StringVar()
        self.autor_val = tk.StringVar()
        self.year_val = tk.StringVar()
        self.isbn_val = tk.StringVar()
        self.nuevo_titulo = tk.StringVar()
        self.nuevo_autor = tk.StringVar()
        self.nuevo_anio = tk.IntVar()
        self.nuevo_isbn = tk.StringVar()

        self.nombre = tk.Label(self.root, text="Nombre",
                               bg="purple", fg="white")
        self.nombre.grid(row=1, column=0)
        self.nombre_e = tk.Entry(self.root)
        self.nombre_e.grid(row=2, column=0)
        self.nombre_e.config(textvariable=self.titulo_val)

        self.autor = tk.Label(self.root, text="Autor", bg="purple", fg="white")
        self.autor.grid(row=1, column=1)
        self.autor_e = tk.Entry(self.root)
        self.autor_e.grid(row=2, column=1)
        self.autor_e.config(textvariable=self.autor_val)

        self.year = tk.Label(self.root, text="Año de lanzamiento",
                             bg="purple", fg="white")
        self.year.grid(row=1, column=2)
        self.year_e = tk.Entry(self.root)
        self.year_e.grid(row=2, column=2)
        self.year_e.config(textvariable=self.year_val)

        self.isbn = tk.Label(self.root, text="ISBN", bg="purple", fg="white")
        self.isbn.grid(row=1, column=3)
        self.isbn_e = tk.Entry(self.root)
        self.isbn_e.grid(row=2, column=3)
        self.isbn_e.config(textvariable=self.isbn_val)
        self.tree = ttk.Treeview(self.root)
        self.tree["columns"] = ("#1", "#2", "#3", "#4")
        self.tree.column("#0", width=60)
        self.tree.column("#1", width=160)
        self.tree.column("#2", width=160)
        self.tree.column("#3", width=160)
        self.tree.column("#4", width=160)
        self.tree.grid(column=0, row=5, columnspan=4)
        self.tree.heading(text="ID", column="#0")
        self.tree.heading(text="Nombre", column="#1")
        self.tree.heading(text="Autor", column="#2")
        self.tree.heading(text="Año de lanzamiento", column="#4")
        self.tree.heading(text="ISBN", column="#3")

        alta = Abmc()
        baja = Abmc()
        modificacion = Abmc()
        consul = Abmc()

        boton_alta = tk.Button(self.root, text="Alta",
                               bg="black", fg="white", padx="30",
                               pady="3", command=lambda:
                               alta.funcion_crear(self.titulo_val,
                                                  self.autor_val,
                                                  self.year_val,
                                                  self.isbn_val,
                                                  self.tree))
        boton_alta.grid(row=4, column=0)

        boton_consulta = tk.Button(self.root, text="Consultar",
                                   bg="black", fg="white",
                                   padx="30", pady="3", command=lambda:
                                   consul.consulta(self.titulo_val.get(),
                                                   self.autor_val.get(),
                                                   self.year_val.get(),
                                                   self.isbn_val.get()))
        boton_consulta.grid(row=4, column=2)

        boton_modificar = tk.Button(self.root, text="Modificar",
                                    bg="black", fg="white", padx="30",
                                    pady="3", command=lambda:
                                    modificacion.modificar(self.titulo_val,
                                                           self.autor_val,
                                                           self.year_val,
                                                           self.isbn_val,
                                                           self.tree))
        boton_modificar.grid(row=4, column=1)

        boton_borrar = tk.Button(self.root, text="Borrar",
                                 bg="black", fg="white", padx="30",
                                 pady="3", command=lambda:
                                 baja.funcion_borrar(self.tree))
        boton_borrar.grid(row=4, column=3)

        datos = self.objeto_base.obtener_datos()
        for dato in datos:
            self.tree.insert("", "end", text=dato.id,
                             values=(dato.titulo, dato.autor,
                                     dato.anio, dato.isbn))