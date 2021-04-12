# Linked List

<div style="text-align: center"><a href="https://commons.wikimedia.org/wiki/File:C_language_linked_list.png"><img src="/static/vendor/img/wikipedia/C_language_linked_list.png" alt="ListExample" style="width: 500px; height: auto"/></a><p>[1] C language linked list | <a href="https://commons.wikimedia.org/wiki/File:C_language_linked_list.png">https://commons.wikimedia.org/wiki/File:C_language_linked_list.png</a></p></div>

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
## Types of Lists
### - Simply Linked Lists

<div style="text-align: center"><a href="https://commons.wikimedia.org/wiki/File:Singly-linked-list.svg"><img src="/static/vendor/img/wikipedia/Singly-linked-list.svg" alt="SinglyLinkedList" style="width: 500px; height: auto"/></a><p>[2] Singly-linked-list | <a href="https://commons.wikimedia.org/wiki/File:Singly-linked-list.svg">https://commons.wikimedia.org/wiki/File:Singly-linked-list.svg</a></p></div>

The simple linked list is the base concept of the list, it handle the connection between node in only one direction, normally associating its physical orientation with the right (`next`) 

Removing an element of a list is as simple as disassociating it from the nodes conected to it. This means that to remove a node, you only need to delete the relation of the node before the targeted one.

<div style="text-align: center"><a href="https://commons.wikimedia.org/wiki/File:CPT-LinkedLists-deletingnode.svg"><img src="/static/vendor/img/wikipedia/CPT-LinkedLists-deletingnode.svg" alt="CPT-LinkedLists" style="width: 500px; height: auto"/></a><p>[3] CPT-LinkedLists-deletingnode | <a href="https://commons.wikimedia.org/wiki/File:CPT-LinkedLists-deletingnode.svg">https://commons.wikimedia.org/wiki/File:CPT-LinkedLists-deletingnode.svg</a></p></div>

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

### - Doubly Linked Lists

Doubly Linked Lists differ from Simple ones in one small detail, every node also knows which node they have before, this means that each node make use of the `before` property to point to the node that is pointing to them

<div style="text-align: center"><a href="https://commons.wikimedia.org/wiki/File:Doubly-linked-list.svg"><img src="/static/vendor/img/wikipedia/Doubly-linked-list.svg" alt="DoublyLinkedList" style="width: 500px; height: auto"/></a><p>[4] Doubly-linked-list | <a href="https://commons.wikimedia.org/wiki/File:Doubly-linked-list.svg">https://commons.wikimedia.org/wiki/File:Doubly-linked-list.svg</a></p></div>

### - Simple Circular Linked Lists

<div style="text-align: center"><a href="https://commons.wikimedia.org/wiki/File:Circurlar_linked_list.png"><img src="/static/vendor/img/wikipedia/Circurlar_linked_list.png" alt="CircularSimpleLinkedList" style="width: 500px; height: auto"/></a><p>[5] Circurlar linked list | <a href="https://commons.wikimedia.org/wiki/File:Circurlar_linked_list.png">https://commons.wikimedia.org/wiki/File:Circurlar_linked_list.png</a></p></div>

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
### - Doubly Circular Linked Lists

<div style="text-align: center"><a href="https://www.geeksforgeeks.org/doubly-circular-linked-list-set-1-introduction-and-insertion/"><img src="/static/vendor/img/geekforgeeks/DoubleCircularLinkedList.png" alt="CircularDoubleLinkedList" style="width: 500px; height: auto"/></a><p>[6] Doubly Circular Linked List | <a href="https://www.geeksforgeeks.org/doubly-circular-linked-list-set-1-introduction-and-insertion/">https://www.geeksforgeeks.org/doubly-circular-linked-list-set-1-introduction-and-insertion/</a></p></div>

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

## Minimal methods to work with `Lists`

### - `Append` or `pushBack`

The common behavior of this method is add a new element to the end of the list.

```c
bool SimpleLinkedList_append(struct SimpleLinkedList *list, void *value, size_t size) {
    if (list == NULL) {
        return FALSE;
    }
    if (list->length + 1 == SIZE_MAX) {
        return FALSE;
    }
    if (list->start == NULL) {
        list->start = malloc(sizeof(struct ListNode));
        if (size > 0) {
            list->start->value = malloc(size);
            memcpy(list->start->value, value, size);
            list->start->copied = TRUE;
        } else {
            list->start->value = value;
        }
        list->start->value_size = size;
        list->start->next = NULL;
        list->length++;
        list->end = list->start;
        return TRUE;
    }
    struct ListNode *old_last_node = list->end;
    struct ListNode *new_node = malloc(sizeof(struct ListNode));
    if (size > 0) {
        new_node->value = malloc(size);
        new_node->copied = TRUE;
        memcpy(new_node->value, value, size);
    } else {
        new_node->value = value;
    }
    new_node->value_size = size;
    new_node->next = NULL;
    old_last_node->next = new_node;
    list->end = new_node;
    list->length++;
    return TRUE;
}
```

### - `Insert`

Insert is usually implemented in to be used anytime but just when the list is not empty, this way the  user can specify, usually an index to put the new value into it.

```c
bool SimpleLinkedList_insert(struct SimpleLinkedList *list, unsigned long long int index, void *value, size_t size) {
    if (list == NULL) {
        return FALSE;
    }
    if (list->length == 0 || index >= list->length) {
        return FALSE;
    }
    if (list->length + 1 == SIZE_MAX) {
        return FALSE;
    }
    struct ListNode *new_node = malloc(sizeof(struct ListNode));
    if (size != 0) {
        new_node->value = malloc(size);
        new_node->copied = TRUE;
        memcpy(new_node->value, value, size);
    } else {
        new_node->value = value;
    }
    new_node->value_size = size;
    if (index == 0) {
        struct ListNode *old_start = list->start;
        new_node->next = old_start;
        list->start = new_node;
    } else if (index == (list->length - 1)) {
        struct ListNode *end = list->end;
        new_node->next = end;
        struct ListNode *before_end = SimpleLinkedList_get(list, list->length - 2);
        before_end->next = new_node;
    } else {
        struct ListNode *current = SimpleLinkedList_get(list, index);
        struct ListNode *before = SimpleLinkedList_get(list, index - 1);
        before->next = new_node;
        new_node->next = current;
    }
    list->length++;
    return TRUE;
}
```

### - `Set`

Set is a method which is used when the list is not empty and the user needs to update an existing value inside the list.

```c
bool SimpleLinkedList_set(struct SimpleLinkedList *list, unsigned long long int index, void *value, size_t size,
                          bool delete_old) {
    if (list == NULL) {
        return FALSE;
    }
    if (list->length == 0 || index >= list->length) {
        return FALSE;
    }
    struct ListNode *current = list->start;
    for (unsigned long long int list_index = 0; list_index != list->length; list_index++) {
        if (list_index == index) {
            break;
        }
        current = current->next;
    }
    void *old_value = current->value;
    if (size != 0) {
        void *new_value = malloc(size);
        memcpy(new_value, value, size);
        current->copied = TRUE;
        current->value = new_value;
    } else {
        current->value = value;
    }
    current->value_size = size;
    if (delete_old == TRUE && current->copied == TRUE) {
        free(old_value);
    }
    return FALSE;
}
```

### - `Remove`

Remove deletes the first element found in the list that is equal to the element provided as reference.

### - `Get`

Get is used when the list is not empty and the user wants to retrieve an element of it approaching the element `index`.

```c
struct ListNode *SimpleLinkedList_get(struct SimpleLinkedList *list, unsigned long long int index) {
    if (list == NULL) {
        return NULL;
    }
    if (list->length == 0 || index >= list->length) {
        return NULL;
    }
    struct ListNode *current = list->start;
    for (unsigned long long int list_index = 0; list_index < list->length; list_index++) {
        if (list_index == index) {
            break;
        }
        current = current->next;
    }
    if (current == NULL) {
        return NULL;
    }
    return current;
}
```

# References

Identifier | Author | Source
---------- | ------ | ------
1|Thedsadude|[https://commons.wikimedia.org/wiki/File:C_language_linked_list.png](https://commons.wikimedia.org/wiki/File:C_language_linked_list.png)
2|Lasindi|[https://commons.wikimedia.org/wiki/File:Singly-linked-list.svg](https://commons.wikimedia.org/wiki/File:Singly-linked-list.svg)
3|Derrick Coetzee|[https://commons.wikimedia.org/wiki/File:CPT-LinkedLists-deletingnode.svg](https://commons.wikimedia.org/wiki/File:CPT-LinkedLists-deletingnode.svg)
4|Lasindi|[https://commons.wikimedia.org/wiki/File:Doubly-linked-list.svg](https://commons.wikimedia.org/wiki/File:Doubly-linked-list.svg)
5|UNKNOWN|[https://commons.wikimedia.org/wiki/File:Circurlar_linked_list.png](https://commons.wikimedia.org/wiki/File:Circurlar_linked_list.png)
6|GeekForGeeks|[https://www.geeksforgeeks.org/doubly-circular-linked-list-set-1-introduction-and-insertion/](https://www.geeksforgeeks.org/doubly-circular-linked-list-set-1-introduction-and-insertion/)
