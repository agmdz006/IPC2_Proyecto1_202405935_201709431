from TDAs.ParametroNodo import ParametroNodo

class ListaParametros:
    def __init__(self):
        self.primero = None
    

    #======== función agregar parametro =================
    def agregar(self, clave, valor):
        nodo_parametro_nuevo = ParametroNodo(clave, valor)
        
        if self.primero is None:
            self.primero = nodo_parametro_nuevo
        else:
            
            nodo_actual = self.primero
            while nodo_actual is not None:
                if nodo_actual.clave == clave:
                    nodo_actual.valor = valor
                    return
                nodo_actual = nodo_actual.siguiente
            
            nodo_actual = self.primero
            while nodo_actual.siguiente is not None:
                nodo_actual = nodo_actual.siguiente
            nodo_actual.siguiente = nodo_parametro_nuevo
    

    #============ función obtener parametro ==================
    def obtener(self, clave):
        nodo_actual = self.primero
        while nodo_actual is not None:
            if nodo_actual.clave == clave:
                return nodo_actual.valor
            nodo_actual = nodo_actual.siguiente
        return None
    

    #========== función obtener todos como texto ===================
    def obtener_todos_como_texto(self):
        if self.primero is None:
            return ""
        
        partes_texto = ""
        nodo_actual = self.primero
        primera_vez = True
        
        while nodo_actual is not None:
            if not primera_vez:
                partes_texto += ", "
            partes_texto += f"{nodo_actual.clave}: {nodo_actual.valor}"
            primera_vez = False
            nodo_actual = nodo_actual.siguiente
        
        return partes_texto