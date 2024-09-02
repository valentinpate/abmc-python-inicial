"""
funciones.py
------------

"""

# import sqlite3
import re
from datetime import datetime
from tkinter import messagebox as msg
from base_biblioteca import Biblioteca
from peewee import IntegrityError


class Validacion():
    """
    Clase que engloba la validacion de los campos que el usuario debe ingresar
    """
    def __init__(self, anio, isbn, autor):

        self.anio = anio
        self.isbn = isbn
        self.autor = autor
        """
        :param anio: anio en que fue publicado el libro
        :param isbn: codigo identificador del libro
        :param autor: incluye nombre y apellido del autor
        """
    def validar_year(self,):
        """
        Verifica que el año sea un número de cuatro dígitos \
            y no sea mayor al año actual
        """
        anio_actual = datetime.now().year
        if re.match(r"^\d{4}$", self.anio) and int(self.anio) <= anio_actual:
            return True
        return False

    def validar_isbn(self,):
        """
        Verifica que el ISBN contenga los caracteres adecuados, \
            en las posiciones correctas
        """
        if re.match(r"^\d{3}-?\d{3}-?\d{4}-?\d{2}-?\d$", self.isbn):
            return True
        return False

    def validar_autor(self,):
        """
        Verifica las condiciones que debe cumplir el nombre de autor
        """
        regex = r"^[A-ZÑÁÉÍÓÚ][a-zñáéíóúäëïöü]{2,16},? [A-ZÑÁÉÍÓÚ][a-z\
            ñáéíóúäëïöü]{2,16}"
        if re.match(regex, self.autor):
            return True
        return False


class Abmc():

    """
    Clase que engloba los métodos para dar de alta, \
        borrar, modificar y consultar libros.
    """

    def __init__(self, ): pass

    def obtener_datos(self):
        """
        Obtiene los datos que se encuentran en la base de datos

        :returns: libros que se estan cargados en la base
        """

        return Biblioteca.select()

    def funcion_crear(self, titulo, autor, anio, isbn, tree):

        """
        Da de alta un nuevo libro en la base de datos

        :param titulo: nombre del libro
        :param autor: nombre y apellido del autor
        :param anio: anio en que fue publicado el libro
        :param isbn: codigo identificador del libro
        :param tree: impresion de pantalla de los libros que \
            se encuentran en la base de datos

        """

        try:
            print("funcion_crear llamada")
            validador = Validacion(anio.get(), isbn.get(), autor.get())
            if not validador.validar_year():
                msg.showinfo("Error", "Año inválido. Por favor ingrese un año \
                            calendario pasado.")
                return
            if not validador.validar_isbn():
                msg.showinfo("Error", "ISBN inválido. Por favor ingrese un \
                            ISBN con formato 978-950-0000-00-0.")
                return
            if not validador.validar_autor():
                msg.showinfo("Error", "Autor inválido. Por favor ingrese \
                            Apellido, Nombre, respetando mayúsculas")
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
            print(f'Cargado el título {lista.titulo}, de {lista.autor} y año\
 {lista.anio}, con el ISBN {lista.isbn}')
            self.actualizar_treeview(tree)
        except IntegrityError as int_e:
            msg.showinfo("Error", "El titulo ya existe en la base de datos.\
                         \nPor favor indique otro titulo u otro ISBN")
            print('Error al cargar item.', int_e)
        else:
            msg.showinfo("Acción Completada", "Titulo cargado exitosamente.")

    def funcion_borrar(self, tree):
        """
        Elimina el libro seleccionado de la base de datos

        :param tree: actualiza el treeview (lista de libros), excluyendo \
            el que fue eliminado
        """

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
        except ():
            msg.showinfo('Error', 'Seleccione un libro de la lista')
        else:
            msg.showinfo("Acción Completada", "Titulo borrado exitosamente.")

    def modificar(self, titulo, autor, anio, isbn, tree):
        """
        Al seleccionar un libro, modifica los valores que indiquemos, \
              pueden ser uno, varios o todos.

        :param titulo: nombre del libro
        :param autor: nombre y apellido del autor
        :param anio: anio en que fue publicado el libro
        :param isbn: codigo identificador del libro
        :param tree: impresion de pantalla de los libros que se \
            encuentran en la base de datos

        """

        print("funcion_modificar llamada")
        seleccion = tree.focus()
        if not seleccion:
            msg.showinfo("Error", "Por favor seleccione un registro \
                         para modificar")
            return
        print(tree.item(seleccion))
        fila = tree.item(seleccion)
        validador = Validacion(anio.get(), isbn.get(), autor.get())

        if (titulo.get() == "" or autor.get() == ""
                or anio.get() == "" or isbn.get() == ""):
            msg.showinfo("Error", "Por favor complete todos los campos")
            return

        if not validador.validar_year():
            msg.showinfo("Error", "Año inválido. Por favor ingrese un \
                         año calendario pasado.")
            return

        if not validador.validar_isbn():
            msg.showinfo("Error", "ISBN inválido. Por favor ingrese un ISBN \
                         con formato 978-950-0000-00-0.")
            return

        if not validador.validar_autor():
            msg.showinfo("Error", "Autor inválido. Por favor ingrese Apellido,\
                            Nombre, respetando mayúsculas.")
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

        """
        Actualiza la vista del Treeview con los libros actuales \
            de la base de datos
        """

        records = root.get_children()
        print(records)
        for element in records:
            root.delete(element)
        for fila in Biblioteca.select():
            print(fila)
            root.insert("", 0, text=fila.id,
                        values=(fila.titulo, fila.autor, fila.isbn, fila.anio))

    def consulta(self, a, b, c, d):

        """
        Muestra los libros en la base de datos según el o \
            los datos que se ingresen.

        :param a: titulo del libro
        :param b: autor del libro
        :param c: anio de publicacion
        :param d: ISBN (codigo del libro)


        """

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
