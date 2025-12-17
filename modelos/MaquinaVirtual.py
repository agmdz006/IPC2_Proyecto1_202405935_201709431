from modelos.Contenedor import ResultadoOperacion 
from modelos.Recursos import Recursos
from TDAs.ListaEnlazada import ListaEnlazada
from modelos.Contenedor import Contenedor 


class MaquinaVirtual:
    def __init__(self, id_vm, centro_asignado, sistema_operativo, ip, cpu, ram, almacenamiento):
        self.id_vm = id_vm
        self.centro_asignado = centro_asignado
        self.sistema_operativo = sistema_operativo
        self.ip = ip
        self.recursos = Recursos(cpu, ram, almacenamiento)
        self.contenedores = ListaEnlazada()
        self.cpu_porcentaje_usado = 0.0
        self.ram_mb_usado = 0

    def obtener_cpu_disponible_porcentaje(self):
        return 100.0 - self.cpu_porcentaje_usado

    def obtener_ram_disponible_mb(self):
        # Asumo que self.recursos.memoria_maxima está en GB, por eso lo multiplicamos por 1024
        ram_total_mb = self.recursos.memoria_maxima * 1024
        return ram_total_mb - self.ram_mb_usado

    def agregar_contenedor(self, id_contenedor, nombre, imagen, puerto, cpu_porcentaje, ram_mb):
        # Nota: La importación de Contenedor se movió al inicio del archivo
        
        cpu_porcentaje_necesario = float(cpu_porcentaje)
        ram_megabytes_necesarios = int(ram_mb)
        
        cpu_disponible_porcentaje = self.obtener_cpu_disponible_porcentaje()
        ram_disponible_mb = self.obtener_ram_disponible_mb()
        
        # Verificamos si la VM tiene suficiente porcentaje de CPU para el contenedor
        if cpu_porcentaje_necesario > cpu_disponible_porcentaje:
            # CORREGIDO: Retorna objeto ResultadoOperacion
            return ResultadoOperacion(False, f"CPU insuficiente. Disponible: {cpu_disponible_porcentaje:.2f}%, Requerido: {cpu_porcentaje_necesario}%")
        
        # Verificamos si la VM tiene suficiente RAM en megabytes para el contenedor
        if ram_megabytes_necesarios > ram_disponible_mb:
            # CORREGIDO: Retorna objeto ResultadoOperacion
            return ResultadoOperacion(False, f"RAM insuficiente. Disponible: {ram_disponible_mb} MB, Requerido: {ram_megabytes_necesarios} MB")
        
        # Creamos el nuevo contenedor y lo agregamos a la lista de contenedores
        contenedor_nuevo = Contenedor(
            id_contenedor, 
            nombre, 
            imagen, 
            puerto, 
            cpu_porcentaje_necesario, 
            ram_megabytes_necesarios
        )
        self.contenedores.insertar(contenedor_nuevo)
        
        # Consumimos los recursos de la VM para el contenedor (Consistente con los atributos de la VM)
        self.cpu_porcentaje_usado += cpu_porcentaje_necesario
        self.ram_mb_usado += ram_megabytes_necesarios
        
        # CORREGIDO: Retorna objeto ResultadoOperacion
        return ResultadoOperacion(True, f"Contenedor {id_contenedor} agregado exitosamente a VM {self.id_vm}")


    def eliminar_contenedor(self, id_contenedor):
        nodo_contenedor_actual = self.contenedores.primero
        nodo_contenedor_anterior = None
        
        # Recorremos la lista de contenedores para encontrar el que queremos eliminar
        while nodo_contenedor_actual is not None:
            if nodo_contenedor_actual.dato.identificador_servicio.strip() == id_contenedor.strip():
                contenedor_a_eliminar = nodo_contenedor_actual.dato
                
                # Liberamos los recursos que estaba consumiendo el contenedor
                # LÓGICA CORREGIDA para usar los atributos de la VM (consistente con agregar_contenedor)
                self.cpu_porcentaje_usado -= contenedor_a_eliminar.porcentaje_uso_cpu 
                self.ram_mb_usado -= contenedor_a_eliminar.memoria_ram_mb
                
                # Evitamos valores negativos y asignamos un valor 0 de una vez
                if self.cpu_porcentaje_usado < 0:
                    self.cpu_porcentaje_usado = 0.0
                if self.ram_mb_usado < 0:
                    self.ram_mb_usado = 0
                
                if nodo_contenedor_anterior is None:
                    self.contenedores.primero = nodo_contenedor_actual.siguiente
                else:
                    nodo_contenedor_anterior.siguiente = nodo_contenedor_actual.siguiente
                
                return ResultadoOperacion(True, f"Contenedor {id_contenedor} eliminado exitosamente. CPU liberada: {contenedor_a_eliminar.porcentaje_uso_cpu}%, RAM liberada: {contenedor_a_eliminar.memoria_ram_mb} MB")
            
            nodo_contenedor_anterior = nodo_contenedor_actual
            nodo_contenedor_actual = nodo_contenedor_actual.siguiente
        
        return ResultadoOperacion(False, f"Contenedor {id_contenedor} no encontrado en VM {self.id_vm}")

    def __str__(self):
        ram_total_mb = self.recursos.memoria_maxima * 1024
        return f"VM {self.id_vm} - SO: {self.sistema_operativo} - IP: {self.ip} - CPU Contenedores: {self.cpu_porcentaje_usado:.2f}%/100% - RAM Contenedores: {self.ram_mb_usado}/{ram_total_mb} MB"