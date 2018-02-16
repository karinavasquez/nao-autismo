from Tkinter import *

from naoqi import ALProxy
import time

from allTasks import Introduccion, Saludar, RespuestaAtencion, Imitacion, AnticipacionSocial, EntregarRecibir


def createEntries(root):
    # Label widgets (order using grids)
    Label(root, text="IP").grid(row=0)
    Label(root, text="Port").grid(row=1)
    Label(root, text="Nombre").grid(row=2)
    Label(root, text="Velocidad").grid(row=3)
    # Entry dictionary
    entry = {}
    # Entry widgets
    entry["ip"]   = Entry(root)
    entry["port"] = Entry(root)
    entry["name"] = Entry(root)
    entry["vel"]  = Entry(root)
    # Default values
    entry["ip"].insert(0, "10.100.144.116")
    entry["port"].insert(0, "9559")
    entry["name"].insert(0, "Adrian")
    entry["vel"].insert(0, "80")
    # Order the entry widgets (using grids)
    entry["ip"].grid(row=0, column=1)
    entry["port"].grid(row=1, column=1)
    entry["name"].grid(row=2, column=1)
    entry["vel"].grid(row=3, column=1)
    return entry

if __name__ == '__main__':
    # TK root widget
    root = Tk()
    # Gui elements
    entry = createEntries(root)

    # Button widgets
    buttonT1_1 = Button(root, text='Introduccion',
                        command = (lambda entr=entry: Introduccion(entr)))
    buttonT1_2 = Button(root, text='Saludar',
                        command = (lambda entr=entry: Saludar(entr)))
    buttonT2_1 = Button(root, text='Respuesta a la Atencion',
                        command = (lambda entr=entry: RespuestaAtencion(entr)))
    buttonT2_2 = Button(root, text='Imitacion',
                        command = (lambda entr=entry: Imitacion(entr)))
    buttonT3_1 = Button(root, text='Anticipacion Social',
                        command = (lambda entr=entry: AnticipacionSocial(entr)))
    buttonT3_2 = Button(root, text='Entregar y Recibir',
                        command = (lambda entr=entry: EntregarRecibir(entr)))  
    buttonQuit = Button(root, text='Quit',
                        command = root.quit)

    # Order the button widgets (using grids)
    buttonT1_1.grid(row=4, column=0, sticky=W, pady=4)
    buttonT1_2.grid(row=4, column=1, sticky=W, pady=4)
    buttonT2_1.grid(row=5, column=0, sticky=W, pady=4)
    buttonT2_2.grid(row=5, column=1, sticky=W, pady=4)
    buttonT3_1.grid(row=6, column=0, sticky=W, pady=4)
    buttonT3_2.grid(row=6, column=1, sticky=W, pady=4)
    buttonQuit.grid(row=7, column=0, sticky=W, pady=4)

    # Enter the main loop and show the window
    mainloop()
