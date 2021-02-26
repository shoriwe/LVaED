# Linked List
[![ListExample](/static/img/DataTypes/C_language_linked_list.png)](https://commons.wikimedia.org/wiki/File:C_language_linked_list.png)

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

Andrea
## Doubly Linked Lists
Christian
## Simple Circular Linked Lists
[![CircularSimpleLinkedList](/static/img/DataTypes/Circurlar_linked_list.png)](https://commons.wikimedia.org/wiki/File:Circurlar_linked_list.png)

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
ANY