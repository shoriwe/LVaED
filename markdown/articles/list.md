# Linked List

[![ListExample](/static/vendor/img/wikipedia/C_language_linked_list.png)](https://commons.wikimedia.org/wiki/File:C_language_linked_list.png)

A linked list is a special data type with the interesting behavior of not having a predefined length during it's initialization, this means that it's length will increase until memory became insufficient. The difference with a traditional array, is that elements are acceded by iterating it until we reach the target value, instead of a memory address offset pointing to it, that behavior can make lists a problem specially when they have to many elements.

The primarily element of a list is the `node` which is pointing to the `next` or `before` depending on the implementation. This way it is possible for the developer the knowledge of the current index inside it, which is deduced by counting the number of  `next` or `before` calls.

```java
// Basic node implementation in Java
public class ListNode {
    public Object Value;
    public ListNode Next;
    public ListNode Before;

    public ListNode(Object value) {
        this.Value = value;
        this.Next = null;
        this.Before = null;
    }

    public ListNode() {
        this.Before = null;
        this.Next = null;
        this.Value = null;
    }

    public Object getObject() {
        return this.Value;
    }

    public void setObject(Object object) {
        this.Value = object;
    }

    public boolean isEquals(Object object) {
        return this.Value == object;
    }

    public boolean isEquals(ListNode node) {
        return this == node;
    }

    @Override
    public String toString() {
        return "ListNode{" +
                "object=" + this.Value +
                '}';
    }
}
```

## Simply Linked Lists

[![Simple Linked List](/static/vendor/img/wikipedia/Singly-linked-list.svg)](https://commons.wikimedia.org/wiki/File:Singly-linked-list.svg)

The simple linked list is the base concept of the list, it handle the connection between node in only one direction, normally associating its physical orientation with the right (`next`) 

Removing an element of a list is as simple as disassociating it from the nodes conected to it. This means that to remove a node, you only need to delete the relation of the node before the targeted one.

[![Deleting element from a list](/static/vendor/img/wikipedia/CPT-LinkedLists-deletingnode.svg)](https://commons.wikimedia.org/wiki/File:CPT-LinkedLists-deletingnode.svg)

In `Java` its append operation will be like:

```java
public void Append(Object value) {
    if (this.Length == 0) {
        this.End = new ListNode(value);
        this.Start = this.End;
    } else {
        ListNode old_end = this.End;
        this.End = new ListNode(value);
        old_end.Next = this.End;
    }
    this.Length++;
}
```

## Doubly Linked Lists

Doubly Linked Lists differ from Simple ones in one small detail, every node also knows which node they have before, this means that each node make use of the `before` property to point to the node that is pointing to them

[![DoublyLinkedList](/static/vendor/img/wikipedia/Doubly-linked-list.svg)](https://commons.wikimedia.org/wiki/File:Doubly-linked-list.svg)

## Simple Circular Linked Lists

[![CircularSimpleLinkedList](/static/vendor/img/wikipedia/Circurlar_linked_list.png)](https://commons.wikimedia.org/wiki/File:Circurlar_linked_list.png)

The difference between circular and more traditional list is that this kind of list doesn't have an end, or at least they don't have it when we iterate over it. This means that we can still point to a virtual last `node` but this last node will have its `next`, pointing to the first value this way, when ever we request the next value we will received.

In resume, this list has the same basic behavior of a `Simple Linked List` but additionally its last element is pointing in his `next` value to the first element of the list.

```java
// Append example in Java of a Simple Circular Linked List
public void Append(Object value) {
        if (this.Length == 0) {
            this.End = new ListNode(value);
            this.Start = this.End;
        } else {
            ListNode old_end = this.End;
            this.End = new ListNode(value);
            old_end.Next = this.End;
            this.End.Before = old_end;
        }
        this.Length++;
        this.End.Next = this.Start; // Unique behavior of circular lists
    }
```
## Doubly Circular Linked Lists

[![CircularDoubleLinkedList](/static/vendor/img/geekforgeeks/DoubleCircularLinkedList.png)](https://www.geeksforgeeks.org/doubly-circular-linked-list-set-1-introduction-and-insertion/)


Similar to the behavior of the `Simple Circular Linked List`, this kind of list have associated its end with its start and the other way around, this means that when it is iterated from the end to start, it will never stop since the `before` of the start is pointing to the `end` node

This kind of list are usually implemented with a normal `Doubly Linked List` in its inside to handle the control operation of the elements

```java
public boolean add(Object object) {

    boolean result = this.Content.add(object); // Using a Doubly Linked List in it's inside to handle the data added
    if (result) {
        this.Length = this.Content.Length;
        this.Start = this.Content.Start;
        this.End = this.Content.End;
        this.End.Next = this.Start;
        this.Start.Before = this.End;
    }
    return result;
}
```
