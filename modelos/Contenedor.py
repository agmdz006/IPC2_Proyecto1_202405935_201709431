class ResultadoOperacion:
    def __init__(self, exito, mensaje): 
        self.exito = exito     
        self.mensaje = mensaje





class Contenedor:
    #========== Constructor de Clase ======================================================================================================
    def __init__(self, identificador_servicio, nombre_designado, imagen_base_docker, puerto_red, porcentaje_uso_cpu, memoria_ram_mb):

        self.identificador_servicio = identificador_servicio
        self.nombre_designado = nombre_designado
        self.imagen_base_docker = imagen_base_docker
        
        self.puerto_red = int(puerto_red)
        self.porcentaje_uso_cpu = float(porcentaje_uso_cpu)
        self.memoria_ram_mb = int(memoria_ram_mb)
        
        self.estatus_actual = "Operativo" # Alternativas: Pausado, Restaurando, Inactivo, Detenido

    #========================================================================================================================================



    #============== función que cambia el estado de los contenedores =====================================================================
    def cambiar_estado_contenedor(self, nuevo_estatus):
        
        # Validamos y asignamos el estatus 
        #hacemos uso del método ResultadoOperacion para mostrar tanto los errores como los procesos completos
        if nuevo_estatus == "Operativo":
            self.estatus_actual = nuevo_estatus
            return ResultadoOperacion(True, f"Estatus de contenedor {self.identificador_servicio} cambiado a: Operativo")
        
        elif nuevo_estatus == "Pausado":
            self.estatus_actual = nuevo_estatus
            return ResultadoOperacion(True, f"Estatus de contenedor {self.identificador_servicio} cambiado a: Pausado")
        
        elif nuevo_estatus == "Reiniciando":
            self.estatus_actual = nuevo_estatus
            return ResultadoOperacion(True, f"Estatus de contenedor {self.identificador_servicio} cambiado a: Reiniciando")
        
        elif nuevo_estatus == "Detenido":
            self.estatus_actual = nuevo_estatus
            return ResultadoOperacion(True, f"Estatus de contenedor {self.identificador_servicio} cambiado a: Detenido")
        else:
            # Si el estatus no coincide con ninguno de los valores válidos:
            return ResultadoOperacion(False, f"Estatus inválido: {nuevo_estatus}. Estatus permitidos: Operativo, Pausado, Reiniciando, Detenido.")
    #=======================================================================================================================================
    
    
    def __str__(self):
        return (
            f"Componente {self.identificador_servicio} con Nombre: '{self.nombre_designado}' "
            f"Imagen: {self.imagen_base_docker}; Puerto de Red: {self.puerto_red} "
            f"Consumo CPU: {self.porcentaje_uso_cpu}%; RAM Asignada: {self.memoria_ram_mb} MB."
        )