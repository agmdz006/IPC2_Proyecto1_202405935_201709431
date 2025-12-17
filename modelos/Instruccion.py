#================= importaciones ==============
from TDAs.ListaParametros import ListaParametros


class Instruccion:
    #===== constructor de la clase ==========
    def __init__(self, tipo):
        self.tipo = tipo
        self.parametros = ListaParametros()
    
    #agregar parámetros para las instrucciones
    def agregar_parametro(self, clave, valor):
        self.parametros.agregar(clave, valor)

    #obtener parámetros para las instrucciones
    def obtener_parametro(self, clave):
        return self.parametros.obtener(clave)
    
    def __str__(self):
        parametros_texto = self.parametros.obtener_todos_como_texto()
        return f"Instruccion [{self.tipo}] - {parametros_texto}"
