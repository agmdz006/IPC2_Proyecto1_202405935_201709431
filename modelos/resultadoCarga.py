class ResultadoCarga:
    """Clase para retornar las tres estructuras"""
    def __init__(self, centros=None, solicitudes=None, instrucciones=None, exito=True, mensaje="Carga exitosa."):
        self.centros = centros
        self.solicitudes = solicitudes
        self.instrucciones = instrucciones
        self.exito = exito
        self.mensaje = mensaje


#clase que se encarga de retornar el resultado de la carga de las estructuras de centros, solicitudes y las instrucciones
#se usa en las clases que retornan un resultado de la carga como en Contenedor.py