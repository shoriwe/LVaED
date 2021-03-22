import static java.lang.System.out;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;
import java.util.Spliterator;
import java.util.function.Consumer;


public class Lista {

    private ListNode inode;
    private int size = 0;

    public ListNode head;
    public ListNode tail;

//inicializar la lista 
    public Lista() {
        clear();
    }

//agregar objeto
    public Lista(Object object) {
        add(object);
    }

//saber si la lista esta vacia
    public boolean isEmpty() {
        return head == null;
    }

//tener el tamaño de la lista
    public int getSize() {
        return size;
    }

//limpiar la lista
    public void clear() {
        head = null;
        tail = null;
        size = 0;
    }

//obtener la cabeza
    public Object getHead() {
        return head.getObject();
    }

//metodo que permite obtener un elemento de acuerdo al index
    public Object getIndex(int n) {
        if (head == null) {
            return null;
        } else {
            ListNode puntero = head;
            int contador = 0;
            while (contador < n && puntero.next != null) {
                puntero = puntero.next;
                contador++;
            }
            if (contador != n) {
                return null;
            } else {
                return puntero.getObject();
            }
        }

    }
    
    
    
    

//Obtener la cola
    public Object getTail() {
        return tail.getObject();
    }

    // Encontrar el indice de un objeto
    public ListNode search(Object object) {
        Iterator<ListNode> i = this.iterator();
        ListNode inode;
        while ((inode = i.next()) != null) {
            if (inode.getObject().toString().equals(object.toString())) {
                return inode;
            }
        }
        return null;
    }

//añadir un objeto a la lista
    public boolean add(Object object) {
        return insertTail(object);
    }

//Insertar un objeto despues del  nodo indicado
    public boolean insert(ListNode node, Object object) {
        try {
            if (node.next == null) {
                add(object);
            } else {
                ListNode newNode = new ListNode(object);
                newNode.next = node.next;
                node.next = newNode;
                size++;
            }
            return true;
        } catch (Exception e) {
            return false;
        }
    }

//insertar un objeto despues de un objeto ob de la lista
    public boolean insert(Object ob, Object object) {
        try {
            if (ob != null) {
                ListNode node = this.search(ob);
                if (node != null) {
                    return insert(node, object);
                } else {
                    return false;
                }
            } else {
                return false;
            }
        } catch (Exception e) {
            return false;
        }
    }

//insertar un objeto en la cabeza
    public boolean insertHead(Object object) {
        try {
            if (isEmpty()) {
                head = new ListNode(object);
                tail = head;
            } else {
                head = new ListNode(object, head);
            }
            this.size++;
            return true;
        } catch (Exception e) {
            return false;
        }
    }

//insertar un objeto por la cola
    public boolean insertTail(Object object) {
        try {
            if (isEmpty()) {
                head = new ListNode(object);
                tail = head;
            } else {
                tail.next = new ListNode(object);
                tail = tail.next;
            }
            this.size++;
            return true;
        } catch (Exception e) {
            return false;
        }
    }

    //remueve un nodo en especifico
    public boolean remove(ListNode node) {
        ListNode previous = head;
        ListNode current = head.next;

        while (current != tail) {
            if (current.getObject().equals(node)) {
                previous.setNext(current.getNext());

                return true;
            }

            previous = current;
            current = current.getNext();
        }

        return true;
    }

    //remover, eliminar un objeto en especifico
    public boolean remove(Object object) {

        ListNode previous = head;
        ListNode current = head.next;

        while (current != tail) {
            if (current.getObject().equals(object)) {
                previous.setNext(current.getNext());

                return true;
            }

            previous = current;
            current = current.getNext();
        }

        return false;

    }

//pregunta si contine algun elemento, si si lo contiene retorna true, si no false
    public boolean contains(Object object) {
        Iterator<ListNode> i = this.iterator();
        ListNode inode;
        while ((inode = i.next()) != null) {
            if (inode.getObject().toString().equals(object.toString())) {
                return true;
            }
        }
        return false;
    }

//iterador
    public Iterator<ListNode> iterator() {
        inode = head;
        return new Iterator<ListNode>() {
            @Override
            public boolean hasNext() {
                return inode.next != null;
            }

            @Override
            public ListNode next() {
                if (inode != null) {
                    ListNode tmp = inode;
                    inode = inode.next;
                    return tmp;
                } else {
                    return null;
                }
            }
        };
    }

//vuelve el linkedlist un array
    public Object[] toArray() {
        Object[] array = new Object[this.size];
        ListNode current_node = head;
        for (int list_index = 0; list_index < this.size; list_index++) {
            array[list_index] = current_node.getObject();
            current_node = current_node.next;
        }
        return array;
    }

    public Object[] toArray(Object[] object) {

        Object[] array = new Object[this.size];
        ListNode current_node = head;
        for (int list_index = 0; list_index < this.size; list_index++) {
            array[list_index] = current_node.getObject();
            current_node = current_node.next;
        }
        return array;

    }

//imprime la lista
    public void printList() {
        ListNode n = head;
        while (n != null) {
            System.out.print(n.getObject() + " ");
            n = n.next;
        }
    }

    // Devuelve el la cola y el nodo anterior a la cola 
    public ListNode getBeforeTo() {
        ListNode n = head;
        while (n.next.next != null) {
            n.getObject();
            n = n.next;
        }
        return n;
    }

    // Devuelve el la cola y el nodo anterior al nodo propuesto
    public ListNode getBeforeTo(ListNode node) {
        node = head;
        while (node.next.next != null) {
            node.getObject();
            node = node.next;
        }
        return node;
    }

    //Devuelve el siguiente a la cabeza
    public Object getNextTo() {
        ListNode node = head;
        return node.next.getObject();
    }

    //devuelve el siguiente del nodo propuesto
    public Object getNextTo(ListNode node) {

        return node.next.getObject();
    }

    //devuelve una sub list del linkedList
    public List subList(int from, int to
    ) {
        List list = new LinkedList();
        ListNode nod = this.head.next;
        int count = 0;
        while (nod != null) {
            if (count >= from && count < to) {
                list.add(nod.getObject());
            }
            nod = nod.next;
            count++;
        }

        return list;
    }
    
//organiza la lista cuando esta son numeros
    public List sortList() {

        List list = new LinkedList();
        ListNode nod = this.head.next;
        int count = 0;
        while (nod != null) {
            list.sort((o1, o2) -> {
                return 0;
            });
        }

        return list;

    }

   int longitud() {
        ListNode actual = this.head;
        int lon = 0;
        while (actual != null) {
            lon++;
            actual = actual.next;
        }
        return lon;
    }

    public void reverse() {

        int cont = this.longitud();
        while (cont > 0) {
            ListNode actual = this.head;

            while (actual.next != null) {

                if (actual.next.next== null) {
                    System.out.print(actual.next.getObject() + " ");
                    actual.next = null;
                } else {
                    actual = actual.next;

                }
            }
            cont--;
        }
        System.out.print(head.getObject());
    }


   

    //recorrer de forma recursiva la lista
    public void rec(ListNode node) {
        if (node.next != null) {
            rec(node.next);
            // <- ;) ->
        }
        out.println(node.toString());
    }

    public Spliterator<ListNode> spliterator() {
        return null;
    }

}
