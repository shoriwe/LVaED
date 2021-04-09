# Priority Queue (Java Implementation)

# Source Code

```java
import java.util.Arrays;
import java.util.Queue;


public class QueuePriority {

    public int MAX;
    private int[] array;
    private int item;

    public QueuePriority() {
        MAX = 5;
        array = new int[MAX];
        item = 0;

    }

    public void insert(int val) {
        int i;
        if (item == 0) {
            array[0] = val;
            item++;
            return;

        }
        for (i = item - 1; i >= 0; i--) {
            if (val > array[i]) {
                array[i+1] = array[i];
            } else {
                break;
            }
        }

        array[i + 1] = val;
        item++;
    }

    public void print() {
        for (int i = 0; i < item; i++) {
            System.out.println(array[i] + "");

        }
    }

    public int remove() {
        return array[--item];
    }

    public boolean isEmpty() {
        return item == 0;
    }
}
```
