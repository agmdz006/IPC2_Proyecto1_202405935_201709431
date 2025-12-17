class Solicitud:
    def __init__(self, id_solicitud, cliente, tipo, prioridad, cpu, ram, almacenamiento, tiempo_estimado):
        self.id_solicitud = id_solicitud
        self.cliente = cliente
        self.tipo = tipo
        self.prioridad = int(prioridad)
        self.cpu = int(cpu)
        self.ram = int(ram)
        self.almacenamiento = int(almacenamiento)
        self.tiempo_estimado = int(tiempo_estimado)
        self.estado = "Pendiente"

    def __str__(self):
        return f"Solicitud {self.id_solicitud} - Cliente: {self.cliente} - Tipo: {self.tipo} - Prioridad: {self.prioridad} - Estado: {self.estado} - CPU: {self.cpu}, RAM: {self.ram} GB, Almacenamiento: {self.almacenamiento} GB"
    
    
#clase que se encarga de inicializar las variables/parámetros de las solicitudes que ingrese el usuario
