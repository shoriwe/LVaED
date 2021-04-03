import java.util.Arrays;


public class QueuArray {

    private int size;
    private Object[] array;
    private int first = 0;
    private int last = 0;

    public QueuArray(int size) {
        this.size = size;
        this.array = new Object[(size > 0) ? size : 1];
        clear();
    }

    public void clear() {
        for (int i = 0; i < array.length; i++) {
            array[i] = null;
        }
        first = -1;

    }

    public boolean isEmpty() {

        return array[0] == null;

    }

    public Object extract() {
        if (first == last) {
            System.out.printf("empty");
            
        }
  
       
        else {
            for (int i = 0; i < last - 1; i++) {
                array[i] = array[i + 1];
            }
  
            if (last < size)
                array[last] = 0;
  
            last--;
        }
        return null;
      
    }

    public void insert(Object object) {
        if (size == last) {
            System.out.printf("full");
            return;
        } else {
            array[last] = object;
            last++;
        }
        return;

    }

    public void printCola() {
   
        if (first == last) {
            System.out.printf("Queue is Empty");

        } else {
            for(int i = 0; i < array.length; i++)
        {
            
            System.out.println(""+array[i]);
        } 
        }

    }

    public int size() {
        return array.length;

    }

    public boolean search(Object object) {
        if (Arrays.asList(array).contains(object)) {
            return true;
        } else {
            return false;
        }

    }

    public void reverse(Object[] array) {

        for (int i = 0; i < array.length / 2; i++) {
            Object temp = array[i];
            array[i] = array[array.length - 1 - i];
            array[array.length - 1 - i] = temp;

        }
    }

    public String toString() {
        return "ArrayStack{"
                + "size=" + size
                + ", array=" + Arrays.toString(array)
                + ", first element=" + first
                + '}';
    }

}
