# Array Based Stack (Java Implementation)

# Source Code

```java

import java.util.Arrays;

public class ArrayStack {

    private int size;
    private Object[] array;
    private int top;

    public ArrayStack(int size) {
        this.size = size;
        this.array = new Object[(size > 0) ? size : 1];
        clear();
    }

    public void clear() {
        for (int i = 0; i < array.length; i++) {
            array[i] = null;
        }
        top = -1;
    }

    public boolean isEmpty() {
        return array[0] == null;
    }

    public Object peek() {
        return (!isEmpty()) ? array[top] : null;
    }

    public Object pop() {
        if (!isEmpty()) {
            Object object = array[top];
            array[top--] = null;
            return object;
        } else {
            return null;
        }
    }

    public boolean push(Object object) {
        if (top + 1 < size) {
            try {
                array[++top] = object;
                return true;
            } catch (Exception e) {
                System.out.println(e);
                return false;
            }
        } else {
            return false;
        }
    }

    public int size() {
        return top + 1;
    }

    public void search(Object object) {
        if (Arrays.asList(array).contains(object) == true) {
            System.out.println("true");
        } else {
            System.out.println("false");
        }

    }

    public void sort() {
        Arrays.asList(array).sort(array);
    }

    public void reverse() {
        Object[] myArray = new Object[]{array};
        Lista myList = new Lista();
        myList =myList.add(array);
        myList.reverse();
    }

    @Override
    public String toString() {
        return "ArrayStack{"
                + "size=" + size
                + ", array=" + Arrays.toString(array)
                + ", top=" + top
                + '}';
    }
}
```
