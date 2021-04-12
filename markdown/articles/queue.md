# Queue

<div style="text-align: center"><a href="https://commons.wikimedia.org/wiki/File:Data_Queue.svg"><img src="/static/vendor/img/wikipedia/Data_Queue.svg" alt="DataQueue" style="width: 500px; height: auto"/></a><p>[1] Data Queue | <a href="https://commons.wikimedia.org/wiki/File:Data_Queue.svg">https://commons.wikimedia.org/wiki/File:Data_Queue.svg</a></p></div>

Queues are `FIFO` (First in, First out) data structures that let their users organize the data in the order it is received. This means that the first element added to the queue is the first element to be returned, which is specially useful in synchronization routines.

## Minimal methods to work with `Queues`
### - `Enqueue`

Enqueue is the method responsible to add new elements to the tail of the queue.

Java implementation of the Enqueue method in a list based Queue.

```java
public boolean insert(Object object) {
    if (lista.head == null) {
        lista.insertHead(object);
    } else {
        lista.add(object);
    }
    return true;
}
```

### - `Dequeue`

Dequeue is another queue specific method that is in charge of returning the first element of it, to then remove it.

Java implementation of the Dequeue method in a list based Queue.

```java
public Object extract() {
    Object result = lista.getHead();
    lista.removeHead();
    return result;
}
```

## Priority Queue

<div style="text-align: center"><a href="/static/img/DataTypes/PriorityQueue.png"><img src="/static/img/DataTypes/PriorityQueue.png" alt="PriorityQueue" style="width: 500px; height: auto"/></a></div>

This kind of queue differs for the first one mentioned in a peculiar way, it auto sort its content every time an element is added (really it only add the element in its respective place), it does that based on special attribute usually called `weight` which is a numeric value and let the own queue determine were it should put the new element.

Its `Dequeue` method work almost the same way in comparison with a vanilla queue, the real change is in its `Enqueue` method which decides accordingly with the mentioned `weight` element where it should put the new element.

When implementing this kind of queue, a way to approach it is by adding every element of the content as a special kind of node with a `priority` property, this way, if its contents are been handled with a Linked List, it will be easier to decide if the new element should be located near or far from the beginning of the `Queue`.

```c
typedef struct PriorityQueueElement {
    void *value;
    size_t size;
    int priority;
} PriorityQueueElement;
```

Now it should be easier to store the priority of each added element for future use.

Another important change that need to be archived is the modification of the `Enqueue` method, since now it will also receive the priority of the element to be added and append the Priority queue Node to its content.

```c
void PriorityQueue_enqueue(PriorityQueue *queue, void *value, size_t size, int priority) {
    PriorityQueueElement *element = PriorityQueueElement_new(value, size, priority);
    if (queue->length == 0) {
        DoublyLinkedList_append(queue->content, element, 0);
    } else {
        bool last_one = TRUE;
        ListNode *current = queue->content->start;
        int index;
        for (index = 0; index < queue->length; index++) {
            PriorityQueueElement *otherElement = current->value;
            if (otherElement->priority < priority) {
                last_one = FALSE;
                break;
            }
            current = current->next;
        }
        if (last_one == TRUE) {
            DoublyLinkedList_append(queue->content, element, 0);
        } else {
            DoublyLinkedList_insert(queue->content, index, element, 0);
        }
    }
    queue->length++;
}
```

# References

Identifier | Author | Source
---------- | ------ | ------
1|User:Vegpuff|[https://commons.wikimedia.org/wiki/File:Data_Queue.svg](https://commons.wikimedia.org/wiki/File:Data_Queue.svg)