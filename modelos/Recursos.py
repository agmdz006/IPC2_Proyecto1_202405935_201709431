class Recursos:
    def __init__(self, nucleos_totales, memoria_maxima, espacio_maximo):
        # Atributos de capacidad total
        self.nucleos_totales = int(nucleos_totales)
        self.memoria_maxima = int(memoria_maxima)
        self.espacio_maximo = int(espacio_maximo)
        
        # Atributos de consumo actual inicializados en cero
        self.nucleos_consumidos = 0
        self.memoria_reservada = 0
        self.espacio_ocupado = 0

    #====================== getters =============================
    def obtener_cpu_disponible(self):
        return self.nucleos_totales - self.nucleos_consumidos

    def obtener_ram_disponible(self):
        return self.memoria_maxima - self.memoria_reservada

    def obtener_almacenamiento_disponible(self):
        return self.espacio_maximo - self.espacio_ocupado



    #============================ funcion para verificar disponibilidad ===================================
    def verificar_disponibilidad(self, cpu_solicitada, ram_solicitada, alm_solicitado):
        
        #variables encargadas de almacenar y analizar la disponibilidad de los recursos
        hay_cpu = self.obtener_cpu_disponible() >= cpu_solicitada
        hay_ram = self.obtener_ram_disponible() >= ram_solicitada
        hay_almacenamiento = self.obtener_almacenamiento_disponible() >= alm_solicitado
        
        return hay_cpu and hay_ram and hay_almacenamiento #retornamos los valores de espacio disponible




    #================== función para asignar recursos =========================================
    def asignar_recursos(self, cpu_req, ram_req, alm_req):
        if self.verificar_disponibilidad(cpu_req, ram_req, alm_req):
            self.nucleos_consumidos += cpu_req
            self.memoria_reservada += ram_req
            self.espacio_ocupado += alm_req
            return True
        return False



    #======================= función para liberar recursos ========================================
    def liberar_recursos(self, cpu_liberar, ram_liberar, alm_liberar):
        self.nucleos_consumidos -= cpu_liberar
        self.memoria_reservada -= ram_liberar
        self.espacio_ocupado -= alm_liberar
        
        # Asegurar que los valores no sean negativos, mejor se asigna un valor cero 
        if self.nucleos_consumidos < 0:
            self.nucleos_consumidos = 0
        if self.memoria_reservada < 0:
            self.memoria_reservada = 0
        if self.espacio_ocupado < 0:
            self.espacio_ocupado = 0



    def __str__(self):
        return f"CPU: {self.nucleos_consumidos}/{self.nucleos_totales} nucleos | RAM: {self.memoria_reservada}/{self.memoria_maxima} GB | Almacenamiento: {self.espacio_ocupado}/{self.espacio_maximo} GB"
    
