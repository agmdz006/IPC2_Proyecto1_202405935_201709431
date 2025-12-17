from TDAs.Nodo import Nodo

class ColaPrioridad:
    def __init__(self):
        self.primero = None
        self.size = 0

    def encolar(self, solicitud):
        nodo_solicitud_nueva = Nodo(solicitud)
        
        # Si la cola esta vacia, la nueva solicitud es la primera
        if self.primero is None:
            self.primero = nodo_solicitud_nueva
        # Si la nueva solicitud tiene mayor prioridad que la primera, pasa al inicio
        elif solicitud.prioridad > self.primero.dato.prioridad:
            nodo_solicitud_nueva.siguiente = self.primero
            self.primero = nodo_solicitud_nueva
        else:
            # Buscamos la posicion correcta segun la prioridad
            nodo_actual = self.primero
            while nodo_actual.siguiente is not None and nodo_actual.siguiente.dato.prioridad >= solicitud.prioridad:
                nodo_actual = nodo_actual.siguiente
            
            nodo_solicitud_nueva.siguiente = nodo_actual.siguiente
            nodo_actual.siguiente = nodo_solicitud_nueva
        
        self.size += 1

    def desencolar(self):
        if self.primero is None:
            return None
        
        # Extraemos la solicitud con mayor prioridad (la primera)
        solicitud_prioritaria = self.primero.dato
        self.primero = self.primero.siguiente
        self.size -= 1
        return solicitud_prioritaria

    def ver_primero(self):
        if self.primero is None:
            return None
        return self.primero.dato

    def esta_vacia(self):
        return self.primero is None

    def mostrar_todas(self):
        if self.primero is None:
            return
        
        nodo_solicitud_actual = self.primero
        while nodo_solicitud_actual is not None:
            print(nodo_solicitud_actual.dato)
            nodo_solicitud_actual = nodo_solicitud_actual.siguiente
