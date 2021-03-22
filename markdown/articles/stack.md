# Stack

Stacks are the result of approaching a `LIFO` (Last in, First out) ordering with list node connection behavior. This means that element inside the stack are connected like a list but are added and extracted approaching `LIFO`.

[![](/static/vendor/img/wikipedia/lifo_stack.png)](https://commons.wikimedia.org/wiki/File:Lifo_stack.png)

Based on that, the to methods that a stack should have to be called that way are `pop` which remove and element from the stack and returns it, and `push` which adds a new element to the stack.

## Pop

Java implementation of the `pop` method in an array based stack

```java
public Object pop() {
        if (!isEmpty()) {
            Object object = array[top];
            array[top--] = null;
            return object;
        } else {
            return null;
        }
    }
```

As you see, after obtaining the element in top of the stack, it is immediately removed from it.

## Push

Java implementation of the `push` method in an array based stack

```java
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
```

## Peek

In some circumstances the user may want to check the value stored in the top of the stack without removing it. In this scenarios is where `peek` method is useful, since it return the value without removing it from the stack. This way and extra `push` is not necessary.

Java implementation of `peek` in a Array based stack

```java
public Object peek() {
    return (!isEmpty()) ? array[top] : null;
}
```

## Array and List based stacks

Example of an array based stack, of four elements. It will only receive four elements, if it reach it's max length, incoming values were not be added.

[![](/static/vendor/img/wikipedia/Stack_(data_structure)_LIFO.svg)](https://commons.wikimedia.org/wiki/File:Stack_(data_structure)_LIFO.svg)

The mayor difference between an array based stack and one implemented using lists is that the first one is usually implemented with a static size, this means that it will only accept a specific number of element, the other one, will allow the user to add elements until memory  is full.
