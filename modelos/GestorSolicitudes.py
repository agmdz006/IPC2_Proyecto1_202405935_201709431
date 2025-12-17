from TDAs.ColaPrioridad import ColaPrioridad
from modelos.Solicitud import Solicitud
from modelos.Contenedor import ResultadoOperacion

class GestorSolicitudes:
    #=============== Constructor de la clase =====================
    def __init__(self):
        self.cola_solicitudes = ColaPrioridad()
        self.historial = None



    #============================= función para agregar solicitud ===============================
    def agregar_solicitud(self, id_solicitud, cliente, tipo, prioridad, cpu, ram, almacenamiento, tiempo_estimado):
        if tipo not in ("Deploy", "Backup"):

            return ResultadoOperacion(False, f"Tipo de solicitud invalido: {tipo}. Debe ser 'Deploy' o 'Backup'")
        
        prioridad_num = int(prioridad)
        if prioridad_num < 1 or prioridad_num > 10:

            return ResultadoOperacion(False, f"Prioridad invalida: {prioridad}. Debe estar entre 1 y 10")
        
        nueva_solicitud = Solicitud(id_solicitud, cliente, tipo, prioridad_num, cpu, ram, almacenamiento, tiempo_estimado)
        self.cola_solicitudes.encolar(nueva_solicitud)
        
        return ResultadoOperacion(True, f"Solicitud {id_solicitud} agregada a la cola con prioridad {prioridad_num}")
    



    #=========================== función para enconlar solicitudes ====================================
    def encolar_solicitud(self, solicitud):
        """Encola una solicitud ya creada directamente a la cola de prioridad"""
        self.cola_solicitudes.encolar(solicitud)
        return ResultadoOperacion(True, f"Solicitud {solicitud.id_solicitud} encolada con prioridad {solicitud.prioridad}")


    #=========== función para procesar la siguiente solicitud =============================
    def procesar_siguiente_solicitud(self, lista_centros):
        if self.cola_solicitudes.esta_vacia():
            return ResultadoOperacion(False, "No hay solicitudes pendientes en la cola")
        
        solicitud = self.cola_solicitudes.desencolar()
        
        if solicitud.tipo == "Deploy":
            return self.procesar_deploy(solicitud, lista_centros)
        elif solicitud.tipo == "Backup":
            return self.procesar_backup(solicitud, lista_centros)
        
        return ResultadoOperacion(False, f"Tipo de solicitud desconocido: {solicitud.tipo}")



    #========================= función para procesar un deploy ==============================================
    def procesar_deploy(self, solicitud, lista_centros):
        centro_seleccionado = self.encontrar_centro_con_mas_recursos(lista_centros, solicitud.cpu, solicitud.ram, solicitud.almacenamiento)
        
        if centro_seleccionado is None:
            solicitud.estado = "Rechazada - Sin recursos"
            return ResultadoOperacion(False, f"Solicitud {solicitud.id_solicitud} rechazada. No hay centros con recursos suficientes")
        
        resultado_vm = centro_seleccionado.crear_vm(
            solicitud.id_solicitud,
            "Sistema Automatico",
            "Auto-asignada",
            solicitud.cpu,
            solicitud.ram,
            solicitud.almacenamiento
        )
        
        if resultado_vm.exito:
            solicitud.estado = "Completada - Deploy"
            return ResultadoOperacion(True, f"Deploy exitoso: VM {solicitud.id_solicitud} creada en {centro_seleccionado.nombre}. Cliente: {solicitud.cliente}")
        else:
            solicitud.estado = "Rechazada - Error al crear VM"
            return ResultadoOperacion(False, f"Error en Deploy: {resultado_vm.mensaje}")


    # ======================================= función para procesar un backup ==============================================
    def procesar_backup(self, solicitud, lista_centros):
        centro_seleccionado = self.encontrar_centro_con_mas_recursos(lista_centros, solicitud.cpu, solicitud.ram, solicitud.almacenamiento)
        
        if centro_seleccionado is None:
            solicitud.estado = "Rechazada - Sin recursos"
            return ResultadoOperacion(False, f"Solicitud {solicitud.id_solicitud} rechazada. No hay centros con recursos suficientes")
        
        resultado_vm = centro_seleccionado.crear_vm(
            f"{solicitud.id_solicitud}_BKP",
            "Sistema Backup - Suspendida",
            "Auto-asignada",
            solicitud.cpu,
            solicitud.ram,
            solicitud.almacenamiento
        )
        
        if resultado_vm.exito:
            solicitud.estado = "Completada - Backup"
            
            return ResultadoOperacion(True, f"Backup exitoso: VM {solicitud.id_solicitud}_BKP creada en estado suspendido en {centro_seleccionado.nombre}. Cliente: {solicitud.cliente}")
        else:
            solicitud.estado = "Rechazada - Error al crear VM"
            return ResultadoOperacion(False, f"Error en Backup: {resultado_vm.mensaje}")



    #============================== función para encontrar centros con más recursos ==================================
    def encontrar_centro_con_mas_recursos(self, lista_centros, cpu_requerida, ram_requerida, almacenamiento_requerido):
        if lista_centros.primero is None:
            return None
        
        centro_con_mas_recursos = None
        puntuacion_maxima = -1
        
        # Recorremos todos los centros para encontrar el que tenga mas recursos disponibles
        nodo_centro_actual = lista_centros.primero
        while nodo_centro_actual is not None:
            centro_evaluado = nodo_centro_actual.dato
            
            cpu_disponible_centro = centro_evaluado.recursos.obtener_cpu_disponible()
            ram_disponible_centro = centro_evaluado.recursos.obtener_ram_disponible()
            almacenamiento_disponible_centro = centro_evaluado.recursos.obtener_almacenamiento_disponible()
            
            # Verificamos si el centro tiene suficientes recursos para la solicitud
            if cpu_disponible_centro >= cpu_requerida and ram_disponible_centro >= ram_requerida and almacenamiento_disponible_centro >= almacenamiento_requerido:
                # Calculamos una puntuacion sumando todos los recursos disponibles
                puntuacion_centro = cpu_disponible_centro + ram_disponible_centro + almacenamiento_disponible_centro
                
                # Si este centro tiene mas recursos que el mejor encontrado, lo guardamos
                if puntuacion_centro > puntuacion_maxima:
                    puntuacion_maxima = puntuacion_centro
                    centro_con_mas_recursos = centro_evaluado
            
            nodo_centro_actual = nodo_centro_actual.siguiente
        
        return centro_con_mas_recursos



    #======= función ver cola de solicitudes ====================
    def ver_cola_solicitudes(self):
        if self.cola_solicitudes.esta_vacia():
            return "No hay solicitudes en la cola"
        
        return self.cola_solicitudes.mostrar_todas()


    #======= función obtener cantidad de pendientes ================
    def obtener_cantidad_pendientes(self):
        return self.cola_solicitudes.size