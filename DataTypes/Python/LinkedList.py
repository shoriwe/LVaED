#Clase nodo creada
class Node(object):


    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next_node = next_node

    def get_data(self):
        return self.data

    def get_next(self):
        return self.next_node

    def set_next(self, new_next):
        self.next_node = new_next

#Clase de la lista creada
class LinkedList(object):
    def __init__(self, head=None):
        self.head = head

#Metodo insertar
    def insert(self, data):
        new_node = Node(data)
        new_node.set_next(self.head)
        self.head = new_node
#Metodo tamaño
    def size(self):
        current = self.head
        count = 0
        while current:
            count += 1
            current = current.get_next()
        return count
#Metodo buscar
    def search(self, data):
        current = self.head
        found = False
        while current and found is False:
            if current.get_data() == data:
                found = True
            else:
                current = current.get_next()
        if current is None:
            raise ValueError("Data not in list")
        return current
#Metodo Eliminar
    def delete(self, data):
        current = self.head
        previous = None
        found = False
        while current and found is False:
            if current.get_data() == data:
                found = True
            else:
                previous = current
                current = current.get_next()
        if current is None:
            raise ValueError("Data not in list")
        if previous is None:
            self.head = current.get_next()
        else:
            previous.set_next(current.get_next())
#Metodo Anexar
    def append(self,data):
        node = Node(data)

        if self.head is not node:
            current = self.head
            while current.next:
                current = current.next
            current.next = node
        else:
            self.head = node

#Metodo insertar por cabeza
    def insertHead(self, data):
        new_node = Node(data)
        new_node.ref = self.start_node
        self.head = new_node

#Metodo insertar por cola
    def insertTail(self,data):
        new_node = Node(data)
        if self.start_node is None:
            self.head = new_node
            return
        n = self.start_node
        while n.ref is not None:
            n = n.ref
        n.ref = new_node;
#Metodo limpiar
    def deleteAll(self):
        temp = self.head
        if temp is None:
            print("\n Not possible to delete empty list")
        while temp:
            self.head = temp.get_next()
            temp = self.head


