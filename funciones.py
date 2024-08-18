# import sqlite3
import re
from datetime import datetime
from tkinter import messagebox as msg
from base_biblioteca import Biblioteca
from peewee import IntegrityError


class Validacion():
    def __init__(self, anio):
        self.anio = anio

    def validar_year(self,):
        anio_actual = datetime.now().year
        if re.match(r"^\d{4}$", self.anio) and int(self.anio) <= anio_actual:
            return True
        return False


class Abmc():
    def __init__(self, ): pass

    def obtener_datos(self):
        return Biblioteca.select()

    def funcion_crear(self, titulo, autor, anio, isbn, tree):
        try:
            print("funcion_crear llamada")
            validador = Validacion(anio.get())
            if not validador.validar_year():
                msg.showinfo("Error", "Año inválido. Por favor ingrese un año \
                            calendario pasado.")
                return

            if (titulo.get() == "" or autor.get() == ""
                    or anio.get() == "" or isbn.get() == ""):
                msg.showinfo("Error", "Por favor complete todos los campos")
                return
            lista = Biblioteca()
            lista.titulo = titulo.get()
            lista.autor = autor.get()
            lista.isbn = isbn.get()
            lista.anio = anio.get()
            lista.save()
            print("Insertando datos en la base de datos...")
            print(titulo, autor, anio, isbn)
            print("item registrado")
            self.actualizar_treeview(tree)
        except IntegrityError as int_e:
            msg.showinfo("Error", "El titulo ya existe en la base de datos. Por favor indique otro titulo u otro ISBN")
            print('Error al cargar item.', int_e)
        else:
            msg.showinfo("Acción Completada", "Titulo cargado exitosamente.")

    def funcion_borrar(self, tree):
        try:
            print("funcion_borrar llamada")
            registro = tree.focus()
            print(registro)
            valor_id = tree.item(registro)
            print(registro)
            tree.delete(registro)
            item_base = Biblioteca.get(Biblioteca.id == valor_id['text'])
            item_base.delete_instance()
            print("Listado actualizado:")
            for registro in Biblioteca.select():
                print(registro)
            self.actualizar_treeview(tree)
        except:
            msg.showinfo('Error', 'Seleccione un libro de la lista')

    def modificar(self, titulo, autor, anio, isbn, tree):
        print("funcion_modificar llamada")
        seleccion = tree.focus()
        if not seleccion:
            msg.showinfo("Error", "Por favor seleccione un registro \
                         para modificar")
            return
        print(tree.item(seleccion))
        fila = tree.item(seleccion)
        validador = Validacion(anio.get())

        if (titulo.get() == "" or autor.get() == ""
                or anio.get() == "" or isbn.get() == ""):
            msg.showinfo("Error", "Por favor complete todos los campos")
            return

        if not validador.validar_year():
            msg.showinfo("Error", "Año inválido. Por favor ingrese un \
                         año calendario pasado.")
            return

        try: 
            nuevo_anio = int(anio.get())
        except ValueError:
            msg.showinfo("Error", "El año debe ser un número entero.")
            return

        actualizado = Biblioteca.update(titulo=titulo.get(),
                                        autor=autor.get(),
                                        anio=anio.get(),
                                        isbn=isbn.get()).where(Biblioteca.id
                                                               == fila['text'])
        actualizado.execute()
        print(titulo, autor, nuevo_anio, isbn)
        print("Item registrado")
        self.actualizar_treeview(tree)

    def actualizar_treeview(self, root):
        records = root.get_children()
        print(records)
        for element in records:
            root.delete(element)
        for fila in Biblioteca.select():
            print(fila)
            root.insert("", 0, text=fila.id,
                        values=(fila.titulo, fila.autor, fila.isbn, fila.anio))

    def consulta(self, a, b, c, d):
        select_data = [a.lower(), b.lower(), c, d]
        resultados = ""
        for dato in Biblioteca.select():
            # print("Consulta", dato.__dict__)
            try:
                datos = f"ID:{dato.id} - {dato.titulo}, {dato.autor} \
                ({dato.anio}) | ISBN: {dato.isbn} \n ~~~~~~~~~~~~~~~~~~~~~ \n"
                if (dato.titulo.lower() == select_data[0]
                    or dato.autor.lower() == select_data[1]
                    or str(dato.anio) == select_data[2]
                        or dato.isbn == select_data[3]):
                    resultados += datos
            except Exception as e:
                msg.showerror("ERROR", e)

        msg.showinfo("Resultados", resultados)
