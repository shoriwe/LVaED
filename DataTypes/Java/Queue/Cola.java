public class Cola {

    private int size;
    Lista lista = new Lista();
    ListNode first = null;
    ListNode last = null;

    public Cola() {
        clear();
    }

    public void clear() {
        size = 0;
        lista.clear();

    }

    public boolean isEmpty() {

        return lista == null;

    }

    public Object extract() {
        lista.removeHead();
        return lista.getHead();

    }

    public boolean insert(Object object) {
        if (lista.head == null) {
            lista.insertHead(object);
        } else {
            lista.add(object);
        }

        return true;

    }
    
    public void printCola() {
        lista.printList();
    }

    public int size() {
        return lista.getSize();

    }

    public boolean search(Object object) {
        lista.contains(object);
        return true;

    }

    public void sort() {
        lista.sortList();
    }

    public void reverse() {
        lista.reverse();
    }

    public String toStrig() {
        return "Queu:"
                + "size=" + size
                + ",Elements=" + lista.toString()
                + '}';

    }
}