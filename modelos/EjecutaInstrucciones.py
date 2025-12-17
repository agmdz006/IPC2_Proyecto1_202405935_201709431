from TDAs.ListaEnlazada import ListaEnlazada
from modelos.Recursos import Recursos
class EjecutaInstrucciones:
    def __init__(self):
        # Mantenemos los nombres originales
        self.instrucciones = ListaEnlazada()
        self.historial = ListaEnlazada()
    
    #hacemos uso de la lista genérica para insertar las instrucciones
    #=======================================================
    def agregar_instruccion(self, instruccion):
        self.instrucciones.insertar(instruccion)
    #===========================================================
    




    #función que se encargar de ejecutar todas las instrucciones
    #======================================================================================

    def ejecutar_instrucciones(self, lista_centros, gestor_solicitudes):
        if self.instrucciones.primero is None:
            return "No hay instrucciones para ejecutar"
    
        nodo_instruccion_actual = self.instrucciones.primero
    
        while nodo_instruccion_actual is not None:
            instruccion = nodo_instruccion_actual.dato
            resultado = ""
        
            try:
                if instruccion.tipo == "crearVM":
                    resultado = self.ejecutar_crear_vm(instruccion, lista_centros)
            
                elif instruccion.tipo == "migrarVM":
                    resultado = self.ejecutar_migrar_vm(instruccion, lista_centros)
        
                elif instruccion.tipo == "crearContenedor":
                    resultado = self.ejecutar_crear_contenedor(instruccion, lista_centros)
            
                elif instruccion.tipo == "procesarSolicitudes":
                    resultado = self.ejecutar_procesar_solicitudes(instruccion, lista_centros, gestor_solicitudes)
            
                else:
                    resultado = f"Tipo de instruccion desconocido: {instruccion.tipo}"

            except Exception as e:
                resultado = f"ERROR FATAL en {instruccion.tipo}: {e}"
        
            print(f"  {resultado}")
            self.historial.insertar(f"[{instruccion.tipo}]: {resultado}")
        
            nodo_instruccion_actual = nodo_instruccion_actual.siguiente
        
        return "Ejecución de todas las instrucciones completada."
#========================================================================================================






    #función específica para ejecutar la instrucción de crear una máquina virtual   
    #================================================================================ 
    def ejecutar_crear_vm(self, instruccion, lista_centros):
        # SOPORTE DE PARÁMETROS
        id_vm = instruccion.obtener_parametro("id")
        id_centro = instruccion.obtener_parametro("centroAsignado")
        if id_centro is None:
            id_centro = instruccion.obtener_parametro("centro")
        
        sistema_operativo = instruccion.obtener_parametro("sistemaOperativo")
        if sistema_operativo is None:
            sistema_operativo = instruccion.obtener_parametro("so")
        
        ip = instruccion.obtener_parametro("ip")
        if ip is None:
            ip = "192.168.1.100"
        
        cpu = instruccion.obtener_parametro("cpu")
        ram = instruccion.obtener_parametro("ram")
        almacenamiento = instruccion.obtener_parametro("almacenamiento")
        
        #verificando que estén completos los parámetros para poder crear una máquina virtual
        parametros_ok = True
        if id_vm is None: parametros_ok = False
        if id_centro is None: parametros_ok = False
        if sistema_operativo is None: parametros_ok = False
        if cpu is None: parametros_ok = False
        if ram is None: parametros_ok = False
        if almacenamiento is None: parametros_ok = False
        
        #en caso de no cumplir con todos los parámetros, se manda un mensaje de error
        if not parametros_ok:
            return "Faltan parametros para crear VM"
        
        #buscamos el centro para poder crear la máquina virtual y si no se encuentra, imprimimos un mensaje de error
        centro = self.buscar_centro_por_id(lista_centros, id_centro)
        if centro is None:
            return f"Centro {id_centro} no encontrado"
        
        #creando el objeto máquina virtual y almacenándola en una variable llamada éxito
        exito = centro.crear_vm(id_vm, sistema_operativo, ip, cpu, ram, almacenamiento)
        
        
        if exito:
            return "VM creada exitosamente!!"
        else:
            return f"Error al crear VM:"
    #==============================================================================================================
    




    #función específica para ejecutar la instrucción de migrar máquina virtual
    #==========================================================================================================
    def ejecutar_migrar_vm(self, instruccion, lista_centros):
        # SOPORTE DE PARÁMETROS:
        id_vm = instruccion.obtener_parametro("id")
        if id_vm is None:
            id_vm = instruccion.obtener_parametro("vmId")
        
        centro_origen_id = instruccion.obtener_parametro("centroOrigen")
        centro_destino_id = instruccion.obtener_parametro("centroDestino")
        
        #verificando que hayan parámetros suficientes para migrar la máquina virtual
        ids_ok = True
        if id_vm is None: ids_ok = False
        if centro_origen_id is None: ids_ok = False
        if centro_destino_id is None: ids_ok = False
        
        if not ids_ok:
            return "Faltan parametros para migrar VM"
        
        centro_origen = self.buscar_centro_por_id(lista_centros, centro_origen_id)
        centro_destino = self.buscar_centro_por_id(lista_centros, centro_destino_id)
        
        if centro_origen is None:
            return f"No se encontró el centro de origen con id: {centro_origen_id}"
        
        if centro_destino is None:
            return f"No se encontró el centro de destino con id: {centro_destino_id}"
        
        vm = self.buscar_vm_en_centro(centro_origen, id_vm)
        if vm is None:
            return f"Error: máquina virtual {id_vm} no encontrada en Centro de Datos: {centro_origen.nombre}"
        
        # VERIFICACIÓN DE RECURSOS 
        cpu_disponible = centro_destino.recursos.obtener_cpu_disponible()
        ram_disponible = centro_destino.recursos.obtener_ram_disponible()
        almacenamiento_disponible = centro_destino.recursos.obtener_almacenamiento_disponible()
        
        if vm.recursos.nucleos_totales > cpu_disponible:
            return f"Error: CPU insuficiente en destino. Disponible: {cpu_disponible}, Requerido: {vm.recursos.nucleos_totales}"
        
        if vm.recursos.memoria_maxima > ram_disponible:
            return f"Error: RAM insuficiente en destino. Disponible: {ram_disponible}, Requerido: {vm.recursos.memoria_maxima}"
        
        if vm.recursos.espacio_maximo > almacenamiento_disponible:
            return f"Error: Almacenamiento insuficiente en destino. Disponible: {almacenamiento_disponible}, Requerido: {vm.recursos.espacio_maximo}"
        
        exito = self.eliminar_vm_de_centro(centro_origen, id_vm)
        if not exito:
            return f"Error: No se pudo eliminar VM {id_vm} del centro origen"
    
        centro_destino.maquinas_virtuales.insertar(vm)
    
        centro_destino.recursos.asignar_recursos(vm.recursos.nucleos_totales, vm.recursos.memoria_maxima, vm.recursos.espacio_maximo)
        vm.centro_asignado = centro_destino.id_centro
    
        return f"VM {id_vm} migrada exitosamente a {centro_destino.nombre}"
    
    def ejecutar_procesar_solicitudes(self, instruccion, lista_centros, gestor_solicitudes):
        cantidad_str = instruccion.obtener_parametro("cantidad")
        
        if cantidad_str is None:
            return "Error: Falta parametro cantidad"
        
        try:
            cantidad = int(cantidad_str)
        except ValueError:
            return "Error: La cantidad no es un número válido."
        
        if gestor_solicitudes is None:
            return "Error: No hay gestor de solicitudes disponible"
        
        # Uso de variables simples para contadores
        procesadas = 0
        exitosas = 0
        fallidas = 0
        
        while procesadas < cantidad and not gestor_solicitudes.cola_solicitudes.esta_vacia():
            # --- CAMBIO CRÍTICO: Recibe solo el estado booleano ---
            exito = gestor_solicitudes.procesar_siguiente_solicitud(lista_centros)
            
            if exito:
                exitosas += 1
            else:
                fallidas += 1
            
            procesadas += 1
        
        return f"Procesadas: {procesadas}, Completadas: {exitosas}, Fallidas: {fallidas}"
    

    def buscar_centro_por_id(self, lista_centros, id_centro):
        if lista_centros.primero is None:
            return None
    
        id_buscado_normalizado = str(id_centro).strip() 
    
        nodo_centro_actual = lista_centros.primero
        while nodo_centro_actual is not None:
        
            if nodo_centro_actual.dato is None:
                nodo_centro_actual = nodo_centro_actual.siguiente
                continue

            id_guardado_normalizado = str(nodo_centro_actual.dato.id_centro).strip() 
        
            if id_guardado_normalizado == id_buscado_normalizado:
                return nodo_centro_actual.dato 
        
            nodo_centro_actual = nodo_centro_actual.siguiente
    
        return None

    def buscar_vm_en_centro(self, centro, id_vm):
        if centro.maquinas_virtuales.primero is None:
            return None
    
        id_buscada_normalizada = str(id_vm).strip() 

        nodo_vm_actual = centro.maquinas_virtuales.primero
        while nodo_vm_actual is not None:
        
            if nodo_vm_actual.dato is None:
                nodo_vm_actual = nodo_vm_actual.siguiente
                continue
            
            id_guardada_normalizada = str(nodo_vm_actual.dato.id_vm).strip() 
        
            if id_guardada_normalizada == id_buscada_normalizada:
                return nodo_vm_actual.dato 
        
            nodo_vm_actual = nodo_vm_actual.siguiente
    
        return None
    
    def eliminar_vm_de_centro(self, centro, id_vm):
        if centro.maquinas_virtuales.primero is None:
            return False
        
        nodo_vm_actual = centro.maquinas_virtuales.primero
        nodo_vm_anterior = None
        
        while nodo_vm_actual is not None:
            if nodo_vm_actual.dato.id_vm == id_vm:
                vm_a_eliminar = nodo_vm_actual.dato
                
                # Liberamos los recursos
                centro.recursos.liberar_recursos(vm_a_eliminar.recursos.nucleos_totales, vm_a_eliminar.recursos.memoria_maxima, vm_a_eliminar.recursos.espacio_maximo)
                
                # Eliminamos el nodo
                if nodo_vm_anterior is None:
                    centro.maquinas_virtuales.primero = nodo_vm_actual.siguiente
                else:
                    nodo_vm_anterior.siguiente = nodo_vm_actual.siguiente
                
                # Decrementamos el contador
                centro.maquinas_virtuales.size -= 1
                
                return True
            
            nodo_vm_anterior = nodo_vm_actual
            nodo_vm_actual = nodo_vm_actual.siguiente
        
        return False