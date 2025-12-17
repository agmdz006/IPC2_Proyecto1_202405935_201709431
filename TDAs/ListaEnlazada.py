from TDAs.Nodo import Nodo

class ListaEnlazada:
    #======== Constructor de la clase =============
    def __init__(self):
        self.primero = None
        self.size = 0
    

    #========= función insertar =====================
    def insertar(self, dato):
        nodo_nuevo = Nodo(dato)
        
        if self.primero is None:
            self.primero = nodo_nuevo
        else:
            nodo_actual = self.primero
            while nodo_actual.siguiente is not None:
                nodo_actual = nodo_actual.siguiente
            nodo_actual.siguiente = nodo_nuevo
        
        self.size += 1
    


    #================= función mostrar ==========================
    def mostrar(self):
        nodo_actual = self.primero
        while nodo_actual is not None:
            print(nodo_actual.dato)
            nodo_actual = nodo_actual.siguiente
    


    #============== función buscar ==============
    def buscar(self, id_buscado):
        nodo_actual = self.primero
        while nodo_actual is not None:
            if nodo_actual.dato.id == id_buscado:
                return nodo_actual.dato
            nodo_actual = nodo_actual.siguiente
        return None


    
            