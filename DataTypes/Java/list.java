
import java.util.Iterator;
import java.util.List;


public class Lista {

    private Nodo head = null;
    public Nodo tail = null;
    private int longitud = 0;
    private Nodo inode;

    private class Nodo {

        public Object getObject() {
            return object;
        }

        public void setObject(Object object) {
            this.object = object;
        }

        public Nodo getNext() {
            return next;
        }

        public void setNext(Nodo next) {
            this.next = next;
        }

        public Object object;
        public Nodo next = null;

        public Nodo(Object object) {
            this.object = object;
        }

    }

    //metodo que permite insertar dependiendo de una referencia en la lista
    public void insert(int n, Object object) {
        Nodo nodo = new Nodo(object);
        if (head == null) {
            head = nodo;

        } else {
            Nodo puntero = head;
            int contador = 0;
            while (contador < n && puntero.next != null) {
                puntero = puntero.next;
                contador++;
            }
            nodo.next = puntero.next;
            puntero.next = nodo;
        }
        longitud++;
    }

    //metodo que permite insertar en la cabeza de la lista
    public void insertHead(Object object) {
        Nodo nodo = new Nodo(object);
        nodo.next = head;
        head = nodo;
        longitud++;

    }

    //metodo que permite insertar en la cabeza de la lista
    public void insertTail(Object object) {
        Nodo nodo = new Nodo(object);
        if (head == null) {
            head = nodo;
        } else {
            Nodo puntero = head;
            while (puntero.next != null) {
                puntero = puntero.next;
            }
            puntero.next = nodo;
        }
        longitud++;
    }

    //metodo que permite obtener un elemento de acuerdo al index
    public Object getIndex(int n) {
        if (head == null) {
            return null;
        } else {
            Nodo puntero = head;
            int contador = 0;
            while (contador < n && puntero.next != null) {
                puntero = puntero.next;
                contador++;
            }
            if (contador != n) {
                return null;
            } else {
                return puntero.object;
            }
        }

    }

    //metodo para saber si la lista esta vacia
    public boolean isEmpty() {
        return head == null;
    }

    //metodo para obtener la longitud de la lista
    public int Size() {
        return longitud;
    }

    //metodo para remover el elemento de la cabeza de la lista
    public void removeHead() {
        if (head != null) {
            Nodo primer = head;
            head = head.next;
            primer.next = null;
            longitud--;
        }

    }

    //metodo para remover la cola
    public void removeTail() {
        tail = null;
        longitud--;
    }

    //metodo para añadir un objeto a la lsta
    public void add(Object object) {
        insertTail(object);
    }

    //metodo que retorna la cabeza
    public Nodo getHead() {

        return head;
    }

    //metodo que retorna la cola
    public Nodo getTail() {

        return tail;
    }

    // metodo que borra todos los de la lista
    public void clear() {
        head = null;
        tail = null;
        longitud = 0;
    }

    //metodo que deberia pasar a un array OJO aun no funciona como deberia
    public Object[] toArray() {
        Object[] array = new Object[Size()];
        Nodo object = head;
        int i = 0;
        while (object.next != null) {
            array = new Object[i];
            i++;

        }
        return new Object[0];

    }

    //itarator propuesto
    public Iterator<Nodo> iterator() {
        inode = head;
        return new Iterator<Nodo>() {
            @Override
            public boolean hasNext() {
                return inode.next != null;
            }

            @Override
            public Nodo next() {
                if (inode != null) {
                    Nodo tmp = inode;
                    inode = inode.next;
                    return tmp;
                } else {
                    return null;
                }
            }
        };
    }

    //el metodo debe retornar si esta o no el objero buscado/ aun no funciona tan bien
    public Nodo search(Object object) {
        Iterator<Nodo> i = this.iterator();
        Nodo inode;
        while ((inode = i.next()) != null) {
            if (inode.getObject().toString().equals(object.toString())) {
                return inode;
            }
        }
        return null;
    }

   

}