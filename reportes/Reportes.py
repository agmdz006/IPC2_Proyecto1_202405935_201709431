from modelos.Contenedor import ResultadoOperacion
from modelos.Recursos import Recursos

class GeneradorReportes:
    def __init__(self, lista_centros, gestor_solicitudes):
        self.lista_centros = lista_centros
        self.gestor_solicitudes = gestor_solicitudes
    
    #================= función para generar reporte de centros ================
    def generar_reporte_centros(self):
        
        dot_content = 'digraph CentrosDatos {\n'
        dot_content += '    rankdir=TB;\n'
        dot_content += '    node [shape=box, style=filled, fillcolor="lightgray"];\n'
        dot_content += '    titulo [label="CENTROS DE DATOS", shape=ellipse];\n'
        
        nodo_centro = self.lista_centros.primero
        contador = 0
        
        try:
            while nodo_centro is not None:
                centro = nodo_centro.dato
                contador += 1
                
                label = f'{centro.id_centro}\\n{centro.nombre}\\n'
                label += f'CPU: {centro.recursos.nucleos_consumidos}/{centro.recursos.nucleos_totales}\\n'
                label += f'RAM: {centro.recursos.memoria_reservada}/{centro.recursos.memoria_maxima} GB\\n'
                label += f'ALM: {centro.recursos.espacio_ocupado}/{centro.recursos.espacio_maximo} GB'
                
                dot_content += '    centro' + str(contador) + ' [label="' + label + '"];\n'
                dot_content += '    titulo -> centro' + str(contador) + ';\n'
                
                nodo_centro = nodo_centro.siguiente
            
            dot_content += '}\n'
            
            nombre_archivo = 'reportes/reporte_centros.dot'
            with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
                archivo.write(dot_content)
                
            return ResultadoOperacion(True, nombre_archivo)
            
        except Exception as error:
            return ResultadoOperacion(False, f'Fallo al generar reporte de centros: {str(error)}')
    
    
    #=========== función para generar reportes de VMs de un centro ===================
    def generar_reporte_vms_centro(self, id_centro):
        nodo_centro = self.lista_centros.primero
        centro_encontrado = None
        
        while nodo_centro is not None:
            if nodo_centro.dato.id_centro == id_centro:
                centro_encontrado = nodo_centro.dato
                break
            nodo_centro = nodo_centro.siguiente
        
        if centro_encontrado is None:
            return ResultadoOperacion(False, f'Centro {id_centro} no encontrado')
        
        dot_content = 'digraph VMsCentro {\n'
        dot_content += '    rankdir=TB;\n'
        dot_content += '    node [shape=box, style=filled, fillcolor="bisque"];\n'
        dot_content += '    graph [fontname="Arial"];\n'
        
        label_titulo = f'MAQUINAS VIRTUALES en {centro_encontrado.nombre}'
        dot_content += f'    centro [label="{label_titulo}", shape=ellipse];\n'
        
        try:
            if centro_encontrado.maquinas_virtuales.primero is None: 
                dot_content += '    vacio [label="No hay VMs", shape=note];\n'
                dot_content += '    centro -> vacio;\n'
            else:
                nodo_vm = centro_encontrado.maquinas_virtuales.primero
                contador = 0
                
                while nodo_vm is not None:
                    vm = nodo_vm.dato
                    contador += 1
                    
                    
                    label = f'{vm.id_vm}\\nSO: {vm.sistema_operativo}\\n'
                    label += f'IP: {vm.ip}'
                    
                    dot_content += f'    vm{contador} [label="{label}"];\n'
                    dot_content += f'    centro -> vm{contador};\n'
                    
                    nodo_vm = nodo_vm.siguiente
            
            dot_content += '}\n'
            
            nombre_archivo_dot = f'reportes/reporte_vms_{id_centro}.dot'
            with open(nombre_archivo_dot, 'w', encoding='utf-8') as archivo:
                archivo.write(dot_content)
                
            return ResultadoOperacion(True, nombre_archivo_dot)
            
        except Exception as error:
            return ResultadoOperacion(False, f'Fallo al generar reporte de VMs para {id_centro}: {str(error)}')
    
    
    #============== función generar reportes de contenedores =================================
    def generar_reporte_contenedores_vm(self, id_vm):
        nodo_centro = self.lista_centros.primero
        vm_encontrada = None
        centro_nombre = ""
        
        while nodo_centro is not None:
            centro = nodo_centro.dato
            nodo_vm = centro.maquinas_virtuales.primero
            
            while nodo_vm is not None:
                if nodo_vm.dato.id_vm == id_vm:
                    vm_encontrada = nodo_vm.dato
                    centro_nombre = centro.nombre
                    break
                nodo_vm = nodo_vm.siguiente
            
            if vm_encontrada is not None:
                break
            nodo_centro = nodo_centro.siguiente
        
        if vm_encontrada is None:
            return ResultadoOperacion(False, f'VM {id_vm} no encontrada')
        
        dot_content = 'digraph ContenedoresVM {\n'
        dot_content += '    rankdir=TB;\n'
        dot_content += '    node [shape=component, style=filled, fillcolor="lightyellow"];\n'
        dot_content += '    graph [fontname="Arial"];\n'
        
        label_vm = f'Contenedores en VM: {vm_encontrada.id_vm}'
        dot_content += f'    vm [label="{label_vm}", shape=ellipse];\n'
        
        try:
            if vm_encontrada.contenedores.primero is None:
                dot_content += '    vacio [label="No hay contenedores", shape=note];\n'
                dot_content += '    vm -> vacio;\n'
            else:
                nodo_cont = vm_encontrada.contenedores.primero
                contador = 0
                
                while nodo_cont is not None:
                    cont = nodo_cont.dato
                    contador += 1
                    
                    label = cont.identificador_servicio + ' (' + cont.nombre_designado + ')\\n' 
                    label += 'Estado: ' + cont.estatus_actual + '\\n'
                    label += f'RAM: {cont.memoria_ram_mb} MB'
                    
                    dot_content += f'    cont{contador} [label="{label}"];\n'
                    dot_content += f'    vm -> cont{contador};\n'
                    
                    nodo_cont = nodo_cont.siguiente
            
            dot_content += '}\n'
            
            nombre_archivo_dot = f'reportes/reporte_contenedores_{id_vm}.dot'
            with open(nombre_archivo_dot, 'w', encoding='utf-8') as archivo:
                archivo.write(dot_content)
                
            return ResultadoOperacion(True, nombre_archivo_dot)
            
        except Exception as error:
            return ResultadoOperacion(False, f'Fallo al generar reporte de contenedores para {id_vm}: {str(error)}')
    
    
    #==================== función generar reporte de cola de solicitudes ============================
    def generar_reporte_cola_solicitudes(self):
        dot_content = 'digraph ColaSolicitudes {\n'
        dot_content += '    rankdir=TB;\n'
        dot_content += '    node [shape=box, style=filled, fillcolor="lightsalmon"];\n'
        dot_content += '    graph [fontname="Arial"];\n'
        dot_content += '    titulo [label="COLA DE SOLICITUDES", shape=ellipse];\n'
        
        try:
            if self.gestor_solicitudes.cola_solicitudes.primero is None: 
                dot_content += '    vacio [label="No hay solicitudes", shape=note];\n'
                dot_content += '    titulo -> vacio;\n'
            else:
                nodo_solicitud = self.gestor_solicitudes.cola_solicitudes.primero
                contador = 0
                nodo_anterior = 'titulo'
                
                while nodo_solicitud is not None:
                    solicitud = nodo_solicitud.dato
                    contador += 1
                    
                    
                    label = f'Prioridad: {solicitud.prioridad}\\n'
                    label += f'{solicitud.id_solicitud} ({solicitud.tipo})'
                    
                    dot_content += f'    sol{contador} [label="{label}"];\n'
                    dot_content += f'    {nodo_anterior} -> sol{contador};\n'
                    
                    nodo_anterior = f'sol{contador}'
                    nodo_solicitud = nodo_solicitud.siguiente
            
            dot_content += '}\n'
            
            nombre_archivo = 'reportes/reporte_cola_solicitudes.dot'
            with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
                archivo.write(dot_content)
                
            return ResultadoOperacion(True, nombre_archivo)
            
        except Exception as error:
            return ResultadoOperacion(False, f'Fallo al generar reporte de solicitudes: {str(error)}')