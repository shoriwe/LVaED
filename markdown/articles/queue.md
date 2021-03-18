# Queue

[![](/static/img/DataTypes/Data_Queue.svg)](https://commons.wikimedia.org/wiki/File:Data_Queue.svg)

Queues are `FIFO` (First in, First out) data structures that let their users organize the data in the order it is received. This means that the first element added to the queue is the first element to be returned, which is specially useful in synchronization routines.

## Enqueue

Enqueue is the method responsible to add new elements to the tail of the queue.

Java implementation of the Enqueue method in a list based Queue.

```java
PENDING
```

## Dequeue

Dequeue is another queue specific method that is in charge of returning the first element of it, to then remove it.

Java implementation of the Dequeue method in a list based Queue.

```java
PENDING
```

## Priority Queue

![](/static/img/DataTypes/PriorityQueue.png)

This kind of queue differs for the first one mentioned in a peculiar way, it auto sort its content every time an element is added (really it only add the element in its respective place), it does that based on special attribute usually called `weight` which is a numeric value and let the own queue determine were it should put the new element.

Its `Dequeue` method work almost the same way in comparison with a vanilla queue, the real change is in its `Enqueue` method which decides accordingly with the mentioned `weight` element where it should put the new element.

Java implementation of the Enqueue method of a Priority Queue.

```java
PENDING
```
