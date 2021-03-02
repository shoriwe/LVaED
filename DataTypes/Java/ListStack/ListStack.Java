public class ListStack {

    private int size;
    Lista list = new Lista();
    private int top;

    public ListStack(int size, int top) {
        this.size = size;
        this.top = top;
    }

    public ListStack() {
        clear();
    }

    public void clear() {
        this.size = 0;
        this.list.clear();
    }

    public boolean isEmpty() {
        return list == null;
    }

    public Object peek() {
        return list.tail;
    }

    public Object pop() {

        Object object = list.getTail();
        list.remove(object);
        return object;

    }

    public boolean push(Object object) {

        list.insertTail(object);
        return true;

    }

    public void printListStack() {
        list.printList();
    }

    public int size() {
        return size;
    }

    public void search(Object object) {
        if (list.contains(object) == true) {
            System.out.println("true");
        } else {
            System.out.println("false");
        }

    }

    public void sort() {
        list.sortList();

    }

    public void reverse() {
        list.reverse();
    }

    public String toString() {
        return "ListStack{"
                + "size=" + size
                + ", list=" + list.toString()
                + ", top=" + top
                + '}';
    }

}
