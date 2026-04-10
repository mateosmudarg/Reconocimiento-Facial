from gui.dialogs import mostrar_excepcion
import gui.reconocimientos as reconocimientos
from gui.movimientos import facial
def on_nuevo_usuario():
    try:
        reconocimientos.iniciar_reconocimiento()
    except Exception as e:
        mostrar_excepcion(e)

def on_agregar_movimiento(tipo):
    try:
        facial(tipo)
    except Exception as e:
        mostrar_excepcion(e)