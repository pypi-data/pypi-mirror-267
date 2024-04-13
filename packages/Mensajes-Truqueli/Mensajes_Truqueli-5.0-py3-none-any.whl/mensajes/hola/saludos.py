import numpy as np
def saludar():
    print("te saludo desde saludos.saludar()") 

def prueba():
    print("esta es una actualizacion del paqutete  a la v 5.0")

def generar_array(numeros): 
    return np.arange(numeros)

class Saludo():
    def __init__(self):
        print("te saludo desde __init__")

if __name__ == "__main__":
    print(generar_array(5))