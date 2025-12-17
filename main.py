#======== importaciones ==================0
from XMLReader.xmlReader import XMLReader
from TDAs.ListaEnlazada import ListaEnlazada
from modelos.CentroDatos import CentroDatos
from modelos.GestorSolicitudes import GestorSolicitudes
from modelos.EjecutaInstrucciones import EjecutaInstrucciones
from datetime import datetime
from reportes.Reportes import GeneradorReportes
from modelos.Contenedor import Contenedor
from modelos.Instruccion import Instruccion 
from modelos.MaquinaVirtual import MaquinaVirtual

# Variables Globales
lista_centros = None
lista_solicitudes = None
lista_instrucciones = None
gestor_solicitudes = None
ejecutor_instrucciones = None

#============ función para obtener nombre del estado ================
def obtener_nombre_estado(clave):
    if clave == '1':
        return 'Pausado'
    elif clave == '2':
        return 'Reiniciando'
    elif clave == '3':
        return 'Operativo' 
    elif clave == '4':
        return 'Detenido'
    return None



#============== función del menú principal ===============================
def menu_principal():
    global lista_centros, lista_solicitudes, lista_instrucciones
    global gestor_solicitudes, ejecutor_instrucciones
    
    while True:
        print('\n')
        print("="*50)
        print('CloudSync Manager - Sistema de la Nube')
        print("="*50)
        print('1. Cargar Archivo XML')
        print('2. Gestión de Centros de Datos')
        print('3. Gestión de Máquinas Virtuales')
        print('4. Gestión de Contenedores')
        print('5. Gestión de Solicitudes')
        print('6. Reportes Graphviz')
        print('7. Generar XML de Salida')
        print('8. Historial de Operaciones')
        print('9. Salir')
        print("="*50)
        
        opcion = input('\nElige una opción: ')
        
        if opcion == '1':
            cargar_archivo_xml()
        elif opcion == '2':
            if lista_centros is None:
                print('\n   Primero debes cargar un archivo XML')
            else:
                menu_centros_datos()
        elif opcion == '3':
            if lista_centros is None:
                print('\n   Primero debes cargar un archivo XML')
            else:
                menu_maquinas_virtuales()
        elif opcion == '4':
            if lista_centros is None:
                print('\n   Primero debes cargar un archivo XML')
            else:
                menu_contenedores()
        elif opcion == '5':
            if lista_centros is None or gestor_solicitudes is None:
                print('\n   Primero debes cargar un archivo XML')
            else:
                menu_solicitudes()
        elif opcion == '6':
            if lista_centros is None or gestor_solicitudes is None:
                print('\n   Primero debes cargar un archivo XML')
            else:
                menu_reportes()
        elif opcion == '7':
            if lista_centros is None:
                print('\n   Primero debes cargar un archivo XML')
            else:
                generar_xml_salida()
        elif opcion == '8':
            if ejecutor_instrucciones is not None:
                mostrar_historial()
            else:
                print('\n   No hay historial disponible')
        elif opcion == '9':
            print('\n   ¡Hasta pronto!')
            break
        else:
            print('\n   Error: Opción inválida. Elige entre 1 y 9')






#================== función para cargar el archivo xml ==========================================0
def cargar_archivo_xml():
    global lista_centros, lista_solicitudes, lista_instrucciones
    global gestor_solicitudes, ejecutor_instrucciones
    
    print('\n=== CARGAR ARCHIVO XML ===\n')
    ruta_archivo = input('Ingresa la ruta del archivo XML: ')
    
    try:
        lector = XMLReader()
        resultado_carga = lector.analizar_archivoXML(ruta_archivo)

        #Acceder a las estructuras a través de los atributos del objeto
        if resultado_carga.exito:
            lista_centros = resultado_carga.centros
            lista_solicitudes = resultado_carga.solicitudes
            lista_instrucciones = resultado_carga.instrucciones
    
            print("Carga de estructuras finalizada.")
        else:
         # Manejar el error de carga
            print(f"Fallo en la carga de XML: {resultado_carga.mensaje}")
        
        if lista_centros is None:
            print('\n   Error al cargar el archivo')
            return
        
        #instanciamos el gestor de solicitudes y cargamos las solicitudes
        gestor_solicitudes = GestorSolicitudes()
        nodo_solicitud = lista_solicitudes.primero
        while nodo_solicitud is not None:
            gestor_solicitudes.encolar_solicitud(nodo_solicitud.dato)
            nodo_solicitud = nodo_solicitud.siguiente
        
        # Inicializamos el ejecutor de instrucciones
        ejecutor_instrucciones = EjecutaInstrucciones()
        ejecutor_instrucciones.instrucciones = lista_instrucciones
        
        # Ejecutamos automáticamente las instrucciones
        ejecutor_instrucciones.ejecutar_instrucciones(lista_centros, gestor_solicitudes) 
        
        print('\n   Archivo XML cargado exitosamente')
        
    except Exception as e:
        print(f'\n   Error al cargar el archivo: {e}')



#=========== función para el menú de centros de datos ==================
def menu_centros_datos():
    global lista_centros
    
    while True:
        print('\n')
        print("="*50)
        print('Gestión de Centros de Datos')
        print("="*50)
        print('1. Listar todos los Centros')
        print('2. Buscar Centro por ID')
        print('3. Ver centro con más recursos')
        print('4. Volver al menú principal')
        print('5. Ver detalles de un centro (incluye VMs y Contenedores)')
        print("="*50)
        
        opcion = input('\nSeleccione una opción: ')
        
        if opcion == '1':
            listar_centros()
        elif opcion == '2':
            buscar_centro_por_id()
        elif opcion == '3':
            ver_centro_mas_recursos()
        elif opcion == '4':
            break
        elif opcion == '5':
            ver_detalles_centro() # Agregado para completar el menú anterior
        else:
            print('\n   Opción inválida')





#============ función para listar los centros ==========================
def listar_centros():
    global lista_centros
    
    print('\n=== CENTROS DE DATOS REGISTRADOS ===\n')
    
    nodo_centro = lista_centros.primero
    contador = 1
    
    while nodo_centro is not None:
        centro = nodo_centro.dato
        
        # Calculamos porcentajes de uso
        cpu_usado = centro.recursos.nucleos_consumidos
        cpu_total = centro.recursos.nucleos_totales
        porcentaje_cpu = (cpu_usado * 100.0) / cpu_total if cpu_total > 0 else 0.0
        
        ram_usado = centro.recursos.memoria_reservada
        ram_total = centro.recursos.memoria_maxima
        porcentaje_ram = (ram_usado * 100.0) / ram_total if ram_total > 0 else 0.0
        
        alm_usado = centro.recursos.espacio_ocupado
        alm_total = centro.recursos.espacio_maximo
        porcentaje_alm = (alm_usado * 100.0) / alm_total if alm_total > 0 else 0.0
        
        # Mostramos la información del centro
        print(f'{contador}. Centro: {centro.nombre} ({centro.id_centro}) - {centro.ciudad}, {centro.pais}')
        print(f'   Ubicación: {centro.ciudad}, {centro.pais}')
        print(f'   CPU: {cpu_usado}/{cpu_total} ({porcentaje_cpu:.2f}% usado)')
        print(f'   RAM: {ram_usado}/{ram_total} GB ({porcentaje_ram:.2f}% usado)')
        print(f'   Almacenamiento: {alm_usado}/{alm_total} TB ')
        print(f'   VMs activas: {centro.maquinas_virtuales.size}\n')
        
        nodo_centro = nodo_centro.siguiente
        contador += 1





#=============== función para buscar centros por id ===============================
def buscar_centro_por_id():
    global lista_centros
    
    id_centro = input('\nIngresa el ID del centro a buscar: ')
    
    nodo_centro = lista_centros.primero
    while nodo_centro is not None:
        if nodo_centro.dato.id_centro == id_centro:
            centro = nodo_centro.dato
            
            # Calculamos porcentajes de uso
            cpu_usado = centro.recursos.nucleos_consumidos
            cpu_total = centro.recursos.nucleos_totales
            porcentaje_cpu = (cpu_usado * 100.0) / cpu_total if cpu_total > 0 else 0.0
            
            ram_usado = centro.recursos.memoria_reservada
            ram_total = centro.recursos.memoria_maxima
            porcentaje_ram = (ram_usado * 100.0) / ram_total if ram_total > 0 else 0.0
            
            alm_usado = centro.recursos.espacio_ocupado
            alm_total = centro.recursos.espacio_maximo
            porcentaje_alm = (alm_usado * 100.0) / alm_total if alm_total > 0 else 0.0
            
            # Mostramos la información del centro
            print(f'\n1. Centro: {centro.nombre} ({centro.id_centro}) - {centro.ciudad}, {centro.pais}')
            print(f'   Ubicación: {centro.ciudad}, {centro.pais}')
            print(f'   CPU: {cpu_usado}/{cpu_total} ({porcentaje_cpu:.2f}% usado)')
            print(f'   RAM: {ram_usado}/{ram_total} GB ({porcentaje_ram:.2f}% usado)')
            print(f'   Almacenamiento: {alm_usado}/{alm_total} TB ')
            print(f'   VMs activas: {centro.maquinas_virtuales.size}\n')
            return
        nodo_centro = nodo_centro.siguiente
    
    print(f'\n Centro con ID {id_centro} no encontrado')





#============== función para ver centros con más recursos =========================
def ver_centro_mas_recursos():
    global lista_centros
    
    if lista_centros.primero is None:
        print('\n   No hay centros disponibles')
        return
    
    centro_max = None
    recursos_max = 0
    
    nodo_centro = lista_centros.primero
    while nodo_centro is not None:
        centro = nodo_centro.dato
        recursos_disponibles = (centro.recursos.obtener_cpu_disponible() + 
                               centro.recursos.obtener_ram_disponible() + 
                               centro.recursos.obtener_almacenamiento_disponible())
        
        if recursos_disponibles > recursos_max:
            recursos_max = recursos_disponibles
            centro_max = centro
        
        nodo_centro = nodo_centro.siguiente
    
    if centro_max is not None:
        # Calculamos porcentajes de uso
        cpu_usado = centro_max.recursos.nucleos_consumidos
        cpu_total = centro_max.recursos.nucleos_totales
        porcentaje_cpu = (cpu_usado * 100.0) / cpu_total if cpu_total > 0 else 0.0
        
        ram_usado = centro_max.recursos.memoria_reservada
        ram_total = centro_max.recursos.memoria_maxima
        porcentaje_ram = (ram_usado * 100.0) / ram_total if ram_total > 0 else 0.0
        
        alm_usado = centro_max.recursos.espacio_ocupado
        alm_total = centro_max.recursos.espacio_maximo
        porcentaje_alm = (alm_usado * 100.0) / alm_total if alm_total > 0 else 0.0
        
        print(f'\n1. Centro: {centro_max.nombre} ({centro_max.id_centro}) - {centro_max.ciudad}, {centro_max.pais}')
        print(f'   Ubicación: {centro_max.ciudad}, {centro_max.pais}')
        print(f'   CPU: {cpu_usado}/{cpu_total} ({porcentaje_cpu:.2f}% usado)')
        print(f'   RAM: {ram_usado}/{ram_total} GB ({porcentaje_ram:.2f}% usado)')
        print(f'   Almacenamiento: {alm_usado}/{alm_total} TB ')
        print(f'   VMs activas: {centro_max.maquinas_virtuales.size}\n')




#============= función para ver los detaller de un centro =======================
def ver_detalles_centro():
    global lista_centros
    
    id_centro = input('\nIngresa el ID del centro: ')
    
    nodo_centro = lista_centros.primero
    while nodo_centro is not None:
        if nodo_centro.dato.id_centro == id_centro:
            centro = nodo_centro.dato
            print(f'\n{"="*50}')
            print(f'{centro.nombre} ({centro.id_centro})')
            print(f'{"="*50}')
            print(f'Ubicación: {centro.ciudad}, {centro.pais}')
            print(f'{centro.recursos}')
            print(f'\nMáquinas Virtuales: {centro.maquinas_virtuales.size}')
            
            nodo_vm = centro.maquinas_virtuales.primero
            while nodo_vm is not None:
                vm = nodo_vm.dato
                print(f'\n      {vm.id_vm}: {vm.sistema_operativo}')
                print(f'      IP: {vm.ip}')
                print(f'      {vm.recursos}')
                print(f'      Contenedores: {vm.contenedores.size}')
                
                nodo_cont = vm.contenedores.primero
                while nodo_cont is not None:
                    cont = nodo_cont.dato
                    print(f'               {cont.identificador_servicio}: {cont.nombre_designado}')
                    print(f'               Imagen: {cont.imagen_base_docker}')
                    print(f'               CPU: {cont.porcentaje_uso_cpu}%, RAM: {cont.memoria_ram_mb} MB')
                    nodo_cont = nodo_cont.siguiente
                
                nodo_vm = nodo_vm.siguiente
            return
        nodo_centro = nodo_centro.siguiente
    
    print(f'\n   Centro con ID {id_centro} no encontrado')





#=============== función para el menú de máquinas virtuales =========================
def menu_maquinas_virtuales():
    while True:
        print('\n')
        print("="*50)
        print('Gestión de Máquinas Virtuales')
        print("="*50)
        print('1. Buscar VM por ID')
        print('2. Listar VMs de un centro')
        print('3. Migrar VM entre centros')
        print('4. Volver al menú principal')
        print("="*50)
        
        opcion = input('\nSeleccione una opción: ')
        
        if opcion == '1':
            buscar_vm_por_id()
        elif opcion == '2':
            listar_vms_de_un_centro()
        elif opcion == '3':
            migrar_vm()
        elif opcion == '4':
            break
        else:
            print('\n   Opción inválida')




#============== función para listas las VMs de un centro ===========================
def listar_vms_de_un_centro():
    global lista_centros
    
    id_centro = input('\nIngresa el ID del centro: ')
    
    nodo_centro = lista_centros.primero
    while nodo_centro is not None:
        if nodo_centro.dato.id_centro == id_centro:
            centro = nodo_centro.dato
            
            print(f'\n=== VMs en {centro.nombre} ===\n')
            
            if centro.maquinas_virtuales.size == 0:
                print('   No hay VMs en este centro\n')
                return
            
            nodo_vm = centro.maquinas_virtuales.primero
            contador = 1
            
            while nodo_vm is not None:
                vm = nodo_vm.dato
                
                # Determinamos el estado basado en si tiene contenedores activos
                estado = "Activa" if vm.contenedores.size > 0 else "Activa" 
                
                print(f'{contador}. VM: {vm.id_vm} - {vm.sistema_operativo} (CPU: {vm.recursos.nucleos_totales}, RAM: {vm.recursos.memoria_maxima}GB)')
                print(f'   Estado: {estado}')
                print(f'   IP: {vm.ip}')
                print(f'   Contenedores: {vm.contenedores.size}\n')
                
                nodo_vm = nodo_vm.siguiente
                contador += 1
            
            return
        nodo_centro = nodo_centro.siguiente
    
    print(f'\n   Centro con ID {id_centro} no encontrado')





#============== función para listar todas las VMs ===============================
def listar_todas_vms():
    global lista_centros
    
    print('\n' + "="*50)
    print('MÁQUINAS VIRTUALES')
    print("="*50)
    
    total_vms = 0
    nodo_centro = lista_centros.primero
    
    while nodo_centro is not None:
        centro = nodo_centro.dato
        
        if centro.maquinas_virtuales.size > 0:
            print(f'\n   Centro: {centro.nombre}')
            
            nodo_vm = centro.maquinas_virtuales.primero
            while nodo_vm is not None:
                vm = nodo_vm.dato
                print(f'      {vm.id_vm}: {vm.sistema_operativo} ({vm.ip})')
                print(f'      {vm.recursos}')
                total_vms += 1
                nodo_vm = nodo_vm.siguiente
        
        nodo_centro = nodo_centro.siguiente
    
    print(f'\n   Total de VMs en el sistema: {total_vms}')







#================== función para crear una nueva VM ==============================
def crear_nueva_vm():
    global lista_centros
    
    print('\n--- Crear Nueva VM ---')
    id_vm = input('ID de la VM: ')
    id_centro = input('ID del Centro donde crearla: ')
    sistema_operativo = input('Sistema Operativo: ')
    ip = input('Dirección IP: ')
    cpu = input('CPU (núcleos): ')
    ram = input('RAM (GB): ')
    almacenamiento = input('Almacenamiento (GB): ')
    
    # Buscamos el centro
    nodo_centro = lista_centros.primero
    while nodo_centro is not None:
        if nodo_centro.dato.id_centro == id_centro:
            centro = nodo_centro.dato
            exito = centro.crear_vm(id_vm, sistema_operativo, ip, cpu, ram, almacenamiento)
            
            if exito:
                print(f'\n   VM {id_vm} creada exitosamente en {centro.id_centro}')
            else:
                print('\n   Error: No se pudo crear la VM en el centro (recursos insuficientes o ID duplicado).')
            return
        nodo_centro = nodo_centro.siguiente
    
    print(f'\n   Centro {id_centro} no encontrado')





#===============función para buscar VM por id =============================
def buscar_vm_por_id():
    global lista_centros
    
    print('\n=== BUSCAR MÁQUINA VIRTUAL ===\n')
    id_vm = input('ID de la VM a buscar: ')
    
    nodo_centro = lista_centros.primero
    while nodo_centro is not None:
        centro = nodo_centro.dato
        
        nodo_vm = centro.maquinas_virtuales.primero
        while nodo_vm is not None:
            if nodo_vm.dato.id_vm == id_vm:
                vm = nodo_vm.dato
                
                # Determinamos el estado basado en si tiene contenedores activos
                estado = "Activa" if vm.contenedores.size > 0 else "Inactiva"
                
                print(f'\n   VM encontrada:')
                print(f'   VM: {vm.id_vm} - {vm.sistema_operativo} (CPU: {vm.recursos.nucleos_totales}, RAM: {vm.recursos.memoria_maxima}GB)')
                print(f'   Estado: {estado}')
                print(f'   IP: {vm.ip}')
                print(f'   Centro asignado: {centro.nombre}')
                print(f'   Contenedores: {vm.contenedores.size}\n')
                return
            nodo_vm = nodo_vm.siguiente
        
        nodo_centro = nodo_centro.siguiente
    
    print(f'\n   VM {id_vm} no encontrada\n')






#========== función para migrar VM a otro centro ======================
def migrar_vm():
    global lista_centros, ejecutor_instrucciones
    
    print('\n--- Migrar VM ---')
    id_vm = input('ID de la VM a migrar: ').strip()
    id_origen = input('ID del Centro origen: ').strip()
    id_destino = input('ID del Centro destino: ').strip()
    
    # Usamos el ejecutor de instrucciones para migrar
    instruccion = Instruccion('migrarVM')
    instruccion.agregar_parametro('vmId', id_vm)
    instruccion.agregar_parametro('centroOrigen', id_origen)
    instruccion.agregar_parametro('centroDestino', id_destino)
    
    resultado = ejecutor_instrucciones.ejecutar_migrar_vm(instruccion, lista_centros)
    print(f'\n{resultado}')





#============= función para el menú de contenedores ======================
def menu_contenedores():
    while True:
        print('\n')
        print("="*50)
        print('Gestión de Contenedores')
        print("="*50)
        print('1. Desplegar contenedor en VM')
        print('2. Listar contenedores de una VM')
        print('3. Cambiar estado de contenedor')
        print('4. Eliminar contenedor')
        print('5. Volver al menú principal')
        print("="*50)
        
        opcion = input('\nSeleccione una opción: ')
        
        if opcion == '1':
            desplegar_contenedor()
        elif opcion == '2':
            listar_contenedores_vm()
        elif opcion == '3':
            cambiar_estado_contenedor()
        elif opcion == '4':
            eliminar_contenedor()
        elif opcion == '5':
            break
        else:
            print('\n Opción inválida')







#================ función para desplegar un contenedor ================================
def desplegar_contenedor():
    global lista_centros
    
    print('\n=== DESPLEGAR CONTENEDOR ===\n')
    
    id_vm = input('ID de la VM: ').strip() 
    identificador_servicio = input('ID del Contenedor (identificador_servicio): ').strip()
    nombre_designado = input('Nombre (nombre_designado): ').strip()
    imagen_base_docker = input('Imagen (imagen_base_docker): ').strip()
    puerto_red = input('Puerto (puerto_red): ').strip()
    
    try:
        porcentaje_uso_cpu = float(input('CPU (%): ')) 
        memoria_ram_mb = float(input('RAM (MB): ')) 
    except ValueError:
        print("\nError: Los valores de CPU (%) y RAM (MB) deben ser números.")
        return
    
    vm_encontrada = None 
    
    nodo_centro = lista_centros.primero
    while nodo_centro is not None:
        centro = nodo_centro.dato
        
        nodo_vm = centro.maquinas_virtuales.primero
        while nodo_vm is not None:
            
            if nodo_vm.dato.id_vm.strip() == id_vm:
                vm_encontrada = nodo_vm.dato
                
            nodo_vm = nodo_vm.siguiente 
    
        if vm_encontrada is not None:
            break
        
        nodo_centro = nodo_centro.siguiente

    
    if vm_encontrada is None:
        print(f"\nError: Máquina Virtual con ID '{id_vm}' no encontrada en ningún centro.")
        return

    #recursos solicitados para el contenedor
    cpu_solicitada_porcentaje = porcentaje_uso_cpu  
    ram_solicitada_mb = memoria_ram_mb              

    #Obtener la capacidad total de la VM (para calcular el consumo en núcleos)
    nucleos_totales_vm = vm_encontrada.recursos.nucleos_totales

    import math 
    nucleos_solicitados = math.ceil(nucleos_totales_vm * (cpu_solicitada_porcentaje / 100.0))

    #verificación de recursos usando la clase Recursos
    ram_disponible = vm_encontrada.recursos.obtener_ram_disponible()
    nucleos_disponibles = vm_encontrada.recursos.obtener_cpu_disponible()

    #Verificar CPU 
    if nucleos_solicitados > nucleos_disponibles:
        print(f"\nError de Recursos: CPU insuficiente en VM '{id_vm}'. Disponible: {nucleos_disponibles} nucleos, Requerido: {nucleos_solicitados} nucleos ({cpu_solicitada_porcentaje}%)")
        return
    
    #Verificar RAM 
    if ram_solicitada_mb > ram_disponible:
        print(f"\nError de Recursos: RAM insuficiente en VM '{id_vm}'. Disponible: {ram_disponible} MB, Requerido: {ram_solicitada_mb} MB")
        return

    nuevo_contenedor = Contenedor(
        identificador_servicio, 
        nombre_designado, 
        imagen_base_docker, 
        puerto_red, 
        cpu_solicitada_porcentaje, 
        ram_solicitada_mb
)


    exito_asignacion = vm_encontrada.recursos.asignar_recursos(nucleos_solicitados, ram_solicitada_mb, 0)

    if not exito_asignacion:
        #En caso de no obtener éxito en la asignación de recursos
        print(f"\nError interno: Falló la asignación de recursos en VM '{id_vm}'.")
        return

    #Insertando el contenedor en la lista enlazada de la VM
    vm_encontrada.contenedores.insertar(nuevo_contenedor)

    print(f"\nContenedor '{identificador_servicio}' desplegado exitosamente en VM '{id_vm}'.")





#===================== función para listar los contenedores de una VM específica ========================
def listar_contenedores_vm():
    global lista_centros
    
    print('\n=== LISTAR CONTENEDORES DE VM ===\n')
    
    #Identificación de la VM
    id_maquina_virtual = input('Ingrese la ID de la VM cuyos contenedores desea listar: ').strip() 
    
    maquina_hallada = None # Variable para almacenar el objeto VM si se encuentra
    
    # Iniciamos la revisión de la lista de Centros de Datos
    nodo_centro_actual = lista_centros.primero
    while nodo_centro_actual is not None:
        centro_actual = nodo_centro_actual.dato
        
        nodo_vm_actual = centro_actual.maquinas_virtuales.primero
        while nodo_vm_actual is not None:
            
            # Verificamos si la ID de la VM coincide 
            if nodo_vm_actual.dato.id_vm.strip() == id_maquina_virtual:
                maquina_hallada = nodo_vm_actual.dato
                break 
            
            nodo_vm_actual = nodo_vm_actual.siguiente 
        
        if maquina_hallada is not None:
            break
        
        nodo_centro_actual = nodo_centro_actual.siguiente # Avanzamos al siguiente nodo Centro

    if maquina_hallada is None:
        print(f"\nError: Máquina Virtual con ID '{id_maquina_virtual}' no fue encontrada en ningún centro.")
        return

    # Si la VM se encontró, procedemos a listar sus contenedores
    print(f"\n--- Contenedores en VM: {maquina_hallada.id_vm} ({maquina_hallada.recursos.nucleos_consumidos}/{maquina_hallada.recursos.nucleos_totales} núcleos usados) ---")

    # Verificamos si la lista de contenedores está vacía
    if maquina_hallada.contenedores.primero is None:
        print(f"La VM '{id_maquina_virtual}' no tiene contenedores activos.")
        return

    # Iteramos sobre la lista enlazada de Contenedores de la VM
    nodo_contenedor_actual = maquina_hallada.contenedores.primero
    indice = 1
    while nodo_contenedor_actual is not None:
        contenedor = nodo_contenedor_actual.dato
        
        print(f"  {indice}. ID: {contenedor.identificador_servicio} | Nombre: {contenedor.nombre_designado}")
        print(f"     -> Imagen: {contenedor.imagen_base_docker} | Puerto: {contenedor.puerto_red}")
        print(f"     -> Recursos Asignados: CPU: {contenedor.porcentaje_uso_cpu}% | RAM: {contenedor.memoria_ram_mb} MB")
        
        nodo_contenedor_actual = nodo_contenedor_actual.siguiente # ¡Avanzamos!
        indice += 1

    print("\n--- Fin de la lista de contenedores ---")






#================= función para cambiar estado del contenedor ==============================
def cambiar_estado_contenedor():
    global lista_centros
    
    print('\n=== CAMBIAR ESTADO DE CONTENEDOR ===\n')
    id_vm = input('ID de la VM: ')
    id_contenedor = input('ID del Contenedor: ')
    
    print('\nEstados disponibles:')
    print('1. Pausado')
    print('2. Reiniciando')
    print('3. Activo')
    print('4. Detenido')
    
    nuevo_estado = input('\nSeleccione el nuevo estado (1-4): ')
    
    estado_nombre = obtener_nombre_estado(nuevo_estado)
    
    if estado_nombre is None:
        print('\n Estado inválido')
        return
    
    # Buscamos la VM y el contenedor
    nodo_centro = lista_centros.primero
    while nodo_centro is not None:
        centro = nodo_centro.dato
        
        nodo_vm = centro.maquinas_virtuales.primero
        while nodo_vm is not None:
            if nodo_vm.dato.id_vm == id_vm:
                vm = nodo_vm.dato
                
                # Buscamos el contenedor
                nodo_cont = vm.contenedores.primero
                while nodo_cont is not None:
                    if nodo_cont.dato.identificador_servicio.strip() == id_contenedor.strip():
                        # Cambiamos el estado del contenedor
                        nodo_cont.dato.estatus_actual = estado_nombre
                        print(f'\n   Estado del contenedor {id_contenedor} cambiado a: {estado_nombre}')
                        return
                    nodo_cont = nodo_cont.siguiente
                
                print(f'\n Contenedor {id_contenedor} no encontrado en VM {id_vm}')
                return
            nodo_vm = nodo_vm.siguiente
        
        nodo_centro = nodo_centro.siguiente
    
    print(f'\n VM {id_vm} no encontrada')







#============ función para eliminar un contenedor =============================
def eliminar_contenedor():
    global lista_centros
    
    print('\n=== ELIMINAR CONTENEDOR ===\n')
    id_vm = input('ID de la VM: ')
    id_contenedor = input('ID del Contenedor a eliminar: ')
    
    # Buscamos la VM en todos los centros
    nodo_centro = lista_centros.primero
    while nodo_centro is not None:
        centro = nodo_centro.dato
        
        nodo_vm = centro.maquinas_virtuales.primero
        while nodo_vm is not None:
            if nodo_vm.dato.id_vm == id_vm:
                vm = nodo_vm.dato
                exito = vm.eliminar_contenedor(id_contenedor)
                
                if exito:
                    print(f'\n   Contenedor {id_contenedor} eliminado exitosamente.')
                    print(f'\n   Recursos de VM {id_vm} actualizados:')
                    print(f'   CPU usado: {vm.cpu_porcentaje_usado:.1f}%')
                    print(f'   RAM usado: {vm.ram_mb_usado} MB')
                    print(f'   CPU disponible: {vm.obtener_cpu_disponible_porcentaje():.1f}%')
                    print(f'   RAM disponible: {vm.obtener_ram_disponible_mb()} MB')
                else:
                    print('\n   Error: No se pudo eliminar el contenedor (ID no encontrado).')
                return
            nodo_vm = nodo_vm.siguiente
        
        nodo_centro = nodo_centro.siguiente
    
    print(f'\n VM {id_vm} no encontrada')





#=============== menú solicitudes ===================================
def menu_solicitudes():
    while True:
        print('\n')
        print("="*50)
        print('Gestión de Solicitudes')
        print("="*50)
        print('1. Agregar nueva solicitud')
        print('2. Procesar solicitud de mayor prioridad')
        print('3. Procesar N solicitudes')
        print('4. Ver cola de solicitudes')
        print('5. Volver al menú principal')
        print("="*50)
        
        opcion = input('\nSeleccione una opción: ')
        
        if opcion == '1':
            agregar_nueva_solicitud()
        elif opcion == '2':
            procesar_solicitud_mayor_prioridad()
        elif opcion == '3':
            procesar_n_solicitudes()
        elif opcion == '4':
            ver_cola_solicitudes()
        elif opcion == '5':
            break
        else:
            print('\n   Opción inválida')


#========== función para agregar una nueva solicitud ====================
def agregar_nueva_solicitud():
    global gestor_solicitudes
    
    print('\n=== AGREGAR NUEVA SOLICITUD ===\n')
    id_solicitud = input('ID de la solicitud: ')
    cliente = input('Cliente: ')
    
    print('\nTipo de solicitud:')
    print('1. Deploy')
    print('2. Backup')
    tipo_opcion = input('Selecciona (1-2): ')
    tipo = 'Deploy' if tipo_opcion == '1' else 'Backup'
    
    prioridad = input('Prioridad (1-10): ')
    cpu = input('CPU requerido (núcleos): ')
    ram = input('RAM requerido (GB): ')
    almacenamiento = input('Almacenamiento requerido (GB): ')
    tiempo_estimado = input('Tiempo estimado (minutos): ')
    
    exito = gestor_solicitudes.agregar_solicitud(
        id_solicitud, cliente, tipo, prioridad, cpu, ram, almacenamiento, tiempo_estimado
    )
    
    if exito:
        print(f'\n   Solicitud {id_solicitud} agregada a la cola.')
    else:
        print(f'\n   Error: No se pudo agregar la solicitud.')






#========== función para procesar una solicitud de mayor prioridad =================0
def procesar_solicitud_mayor_prioridad():
    global lista_centros, gestor_solicitudes
    
    print('\n=== PROCESAR SOLICITUD DE MAYOR PRIORIDAD ===\n')
    
    if gestor_solicitudes.cola_solicitudes.esta_vacia():
        print('   No hay solicitudes pendientes en la cola\n')
        return
    
    exito = gestor_solicitudes.procesar_siguiente_solicitud(lista_centros)
    
    if exito:
        print(f'   Solicitud procesada y completada exitosamente.\n')
    else:
        print(f'   Error: No se pudo procesar la solicitud (recursos insuficientes).\n')







#=========== función para procesar n solicitudes =========================
def procesar_n_solicitudes():
    global lista_centros, gestor_solicitudes
    
    print('\n=== PROCESAR N SOLICITUDES ===\n')
    
    if gestor_solicitudes.cola_solicitudes.esta_vacia():
        print('   No hay solicitudes pendientes en la cola\n')
        return
    
    cantidad = input('¿Cuántas solicitudes deseas procesar?: ')
    
    try:
        cantidad_num = int(cantidad)
        
        if cantidad_num <= 0:
            print('\n   La cantidad debe ser mayor a 0\n')
            return
        
        print(f'\n   Procesando {cantidad_num} solicitud(es)...\n')
        
        procesadas = 0
        exitosas = 0
        fallidas = 0
        
        while procesadas < cantidad_num and not gestor_solicitudes.cola_solicitudes.esta_vacia():
            exito = gestor_solicitudes.procesar_siguiente_solicitud(lista_centros)
            
            if exito:
                print(f'   Solicitud #{procesadas + 1} completada.')
                exitosas += 1
            else:
                print(f'   Error al procesar solicitud #{procesadas + 1} (recursos insuficientes).')
                fallidas += 1
            
            procesadas += 1
        
        print(f'\n   Resumen:')
        print(f'   Total procesadas: {procesadas}')
        print(f'   Exitosas: {exitosas}')
        print(f'   Fallidas: {fallidas}\n')
        
    except ValueError:
        print('\n   Cantidad inválida. Debe ser un número entero\n')







#============= función para ver cola de solicitudes ====================
def ver_cola_solicitudes():
    global gestor_solicitudes
    
    print('\n=== COLA DE SOLICITUDES ===\n')
    
    if gestor_solicitudes.cola_solicitudes.esta_vacia():
        print('   No hay solicitudes pendientes\n')
        return
    
    # Mostramos el TDA cola
    nodo_solicitud = gestor_solicitudes.cola_solicitudes.primero
    contador = 1
    
    while nodo_solicitud is not None:
        solicitud = nodo_solicitud.dato
        
        print(f'{contador}. Solicitud: {solicitud.id_solicitud} - {solicitud.cliente} ({solicitud.tipo}) - Prioridad: {solicitud.prioridad}')
        print(f'   Estado: Pendiente')
        print(f'   Recursos: CPU={solicitud.cpu}, RAM={solicitud.ram}GB\n')
        
        nodo_solicitud = nodo_solicitud.siguiente
        contador += 1








#=============== función para ejecutar instrucciones ===============================
def ejecutar_instrucciones():
    global lista_centros, gestor_solicitudes, ejecutor_instrucciones
    
    print('\n' + "="*50)
    print('EJECUTANDO INSTRUCCIONES')
    print("="*50)
    
    ejecutor_instrucciones.ejecutar_todas(lista_centros, gestor_solicitudes)

def menu_reportes():
    global lista_centros, gestor_solicitudes
    
    while True:
        print('\n')
        print("="*50)
        print('Reportes Graphviz')
        print("="*50)
        print('1. Reporte general de centros de datos')
        print('2. Reporte de VMs de un centro')
        print('3. Reporte de contenedores de una VM')
        print('4. Reporte de cola de solicitudes')
        print('5. Volver al menu principal')
        print("="*50)
        
        opcion = input('\nSeleccione una opcion: ')
        
        if opcion == '1':
            generar_reporte_centros()
        elif opcion == '2':
            generar_reporte_vms()
        elif opcion == '3':
            generar_reporte_contenedores()
        elif opcion == '4':
            generar_reporte_solicitudes()
        elif opcion == '5':
            break
        else:
            print('\n   Opcion invalida')






#================ función para generar reportes de centros =====================
def generar_reporte_centros():
    global lista_centros, gestor_solicitudes
    
    print('\n=== REPORTE GENERAL DE CENTROS ===\n')
    
    generador = GeneradorReportes(lista_centros, gestor_solicitudes)
    
    res = generador.generar_reporte_centros()
    
    if res.exito:
        print(f'   Reporte generado: {res.mensaje}\n')
    else:
        print(f'   Error: {res.mensaje}\n')








#============función para generar reportes de VMs ===================
def generar_reporte_vms():
    global lista_centros, gestor_solicitudes
    
    print('\n=== REPORTE DE VMS DE UN CENTRO ===\n')
    id_centro = input('ID del centro: ')
    
    generador = GeneradorReportes(lista_centros, gestor_solicitudes)
    
    res = generador.generar_reporte_vms_centro(id_centro)
    
    if res.exito:
        print(f'\n   Reporte generado: {res.mensaje}\n')
    else:
        print(f'\n   Error: {res.mensaje}\n')






#=========== función para generar reportes de contenedores =============
def generar_reporte_contenedores():
    global lista_centros, gestor_solicitudes
    
    print('\n=== REPORTE DE CONTENEDORES DE UNA VM ===\n')
    id_vm = input('ID de la VM: ')
    
    generador = GeneradorReportes(lista_centros, gestor_solicitudes)
    
    res = generador.generar_reporte_contenedores_vm(id_vm)
    
    if res.exito:
        print(f'\n   Reporte generado: {res.mensaje}\n')
    else:
        print(f'\n   Error: {res.mensaje}\n')





#============ función para generar reportes de solicitudes ========================
def generar_reporte_solicitudes():
    global lista_centros, gestor_solicitudes
    
    print('\n=== REPORTE DE COLA DE SOLICITUDES ===\n')
    
    generador = GeneradorReportes(lista_centros, gestor_solicitudes)
    
    res = generador.generar_reporte_cola_solicitudes()
    
    if res.exito:
        print(f'   Reporte generado: {res.mensaje}\n')
    else:
        print(f'   Error: {res.mensaje}\n')





#============ función para mostrar historial =======================000
def mostrar_historial():
    global ejecutor_instrucciones
    
    print('\n' + "="*50)
    print('HISTORIAL DE OPERACIONES')
    print("="*50)
    
    if ejecutor_instrucciones.historial.primero is None:
        print('\n   No hay operaciones en el historial')
        return
    
    nodo_hist = ejecutor_instrucciones.historial.primero
    while nodo_hist is not None:
        print(f'   • {nodo_hist.dato}')
        nodo_hist = nodo_hist.siguiente




#============ función para generar el xml de salida ============================
def generar_xml_salida():
    global lista_centros
    
    print('\n=== GENERAR XML DE SALIDA ===\n')
    nombre_archivo = input('Nombre del archivo de salida: ')
    
    if not nombre_archivo:
        nombre_archivo = 'resultado'
    
    nombre_archivo = nombre_archivo + '.xml'
    
    timestamp_actual = datetime.now().isoformat()
    
    vms_totales = 0
    contenedores_totales = 0
    
    contenido_xml = '<?xml version="1.0"?>\n'
    contenido_xml += '<resultadoCloudSync>\n'
    contenido_xml += f'      <timestamp>{timestamp_actual}</timestamp>\n'
    contenido_xml += '      <estadoCentros>\n'
    
    nodo_centro = lista_centros.primero
    while nodo_centro is not None:
        centro = nodo_centro.dato
        
        cpu_total = centro.recursos.nucleos_totales
        cpu_disponible = centro.recursos.obtener_cpu_disponible()
        cpu_usado = centro.recursos.memoria_reservada
        
        cpu_utilizacion = (cpu_usado / cpu_total * 100) if cpu_total > 0 else 0
        
        ram_total = centro.recursos.memoria_maxima
        ram_disponible = centro.recursos.obtener_ram_disponible()
        ram_usado = centro.recursos.memoria_reservada
        
        ram_utilizacion = (ram_usado / ram_total * 100) if ram_total > 0 else 0
        
        cantidad_vms = centro.maquinas_virtuales.size
        vms_totales += cantidad_vms
        
        cantidad_contenedores = 0
        nodo_vm = centro.maquinas_virtuales.primero
        while nodo_vm is not None:
            vm = nodo_vm.dato
            cantidad_contenedores += vm.contenedores.size
            nodo_vm = nodo_vm.siguiente
        
        contenedores_totales += cantidad_contenedores
        
        contenido_xml += f'         <centro id="{centro.id_centro}">\n'
        contenido_xml += f'            <nombre>{centro.nombre}</nombre>\n'
        contenido_xml += '            <recursos>\n'
        contenido_xml += f'               <cpuTotal>{cpu_total}</cpuTotal>\n'
        contenido_xml += f'               <cpuDisponible>{cpu_disponible}</cpuDisponible>\n'
        contenido_xml += f'               <cpuUtilizacion>{cpu_utilizacion:.2f}%</cpuUtilizacion>\n'
        contenido_xml += f'               <ramTotal>{ram_total}</ramTotal>\n'
        contenido_xml += f'               <ramDisponible>{ram_disponible}</ramDisponible>\n'
        contenido_xml += f'               <ramUtilizacion>{ram_utilizacion:.2f}%</ramUtilizacion>\n'
        contenido_xml += '            </recursos>\n'
        contenido_xml += f'            <cantidadVMs>{cantidad_vms}</cantidadVMs>\n'
        contenido_xml += f'            <cantidadContenedores>{cantidad_contenedores}</cantidadContenedores>\n'
        contenido_xml += '         </centro>\n'
        
        nodo_centro = nodo_centro.siguiente
    
    contenido_xml += '      </estadoCentros>\n'
    contenido_xml += '      <estadisticas>\n'
    contenido_xml += f'         <vmsActivas>{vms_totales}</vmsActivas>\n'
    contenido_xml += f'         <contenedoresTotales>{contenedores_totales}</contenedoresTotales>\n'
    contenido_xml += '      </estadisticas>\n'
    contenido_xml += '</resultadoCloudSync>\n'
    
    try:
        archivo = open(nombre_archivo, 'w', encoding='utf-8')
        archivo.write(contenido_xml)
        archivo.close()
        
        print(f'\n   Archivo {nombre_archivo} generado exitosamente')
        print(f'   VMs totales: {vms_totales}')
        print(f'   Contenedores totales: {contenedores_totales}\n')
    except Exception as error:
        print(f'\n   Error al generar el archivo: {error}\n')

if __name__ == "__main__":
    menu_principal()