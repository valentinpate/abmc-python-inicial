"""
main.py
-------

Ejecuta la ventana principal llamada **Ventana** de la interfaz gráfica de \
usuario utilizando Tkinter.
"""


from tkinter import Tk
from vista import Ventana

if __name__ == "__main__":
    root = Tk()
    app = Ventana(root)
    root.mainloop()
