# Array Based Queue (C Implementation)

# Source Code

```c
#ifndef COLLECTIONS_ARRAY_QUEUE_H
#define COLLECTIONS_ARRAY_QUEUE_H

#include <stdlib.h>
#include <string.h>
#include "../primitives.h"

typedef struct QueueElement {
    void *value;
    size_t size;
} QueueElement;

typedef bool (*is_equal_condition)(struct QueueElement *node);


typedef struct ArrayQueue {
    unsigned long long int length;
    unsigned long long int current_length;
    bool reversed;
    QueueElement **content;
} ArrayQueue;


QueueElement *QueueElement_new(void *value, size_t size) {
    QueueElement *element = malloc(sizeof(QueueElement));
    if (size > 0) {
        element->value = malloc(size);
        strcpy_s(element->value, size, value);
    } else {
        element->value = value;
        element->size = 0;
    }
    return element;
}

ArrayQueue *ArrayQueue_new(unsigned long long int length) {
    ArrayQueue *queue = malloc(sizeof(ArrayQueue));
    queue->length = length;
    queue->current_length = 0;
    queue->content = malloc(sizeof(QueueElement *) * length);
    return queue;
}

bool ArrayQueue_isEmpty(ArrayQueue *queue) {
    return queue->current_length == 0;
}

void ArrayQueue_clear(ArrayQueue *queue) {
    if (queue->current_length == 0) {
        return;
    }
    for (int index = 0; index < queue->length; index++) {
        queue->content[index] = NULL;
    }
    queue->current_length = 0;
}

QueueElement **CopyElements(unsigned long long int length, QueueElement **elements) {
    QueueElement **result = malloc(sizeof(QueueElement *) * length);
    for (int index = 0; index < length; index++) {
        result[index] = elements[index];
    }
    return result;
}

bool ArrayQueue_enqueue(ArrayQueue *queue, void *value, size_t size) {
    if (queue->current_length + 1 > queue->length) {
        return FALSE;
    }
    QueueElement *element = QueueElement_new(value, size);
    if (queue->reversed) {
        QueueElement **backup = CopyElements(queue->current_length, queue->content);
        queue->content[0] = element;
        for (int index = 0; index < queue->current_length; index++) {
            queue->content[index + 1] = backup[index];
        }
    } else {
        queue->content[queue->current_length] = element;
    }
    queue->current_length++;
    return TRUE;
}

QueueElement *ArrayQueue_dequeue(ArrayQueue *queue) {
    if (queue->current_length == 0) {
        return NULL;
    }
    QueueElement *element;
    if (queue->reversed) {
        element = queue->content[queue->current_length - 1];
        queue->content[queue->current_length - 1] = NULL;
    } else {
        QueueElement **backup = CopyElements(queue->current_length, queue->content);
        element = queue->content[0];
        for (int index = 1; index < queue->current_length; index++) {
            queue->content[index - 1] = backup[index];
        }
    }
    queue->current_length--;
    return element;
}

bool ArrayQueue_search(ArrayQueue* queue, is_equal_condition condition) {
    for (int index = 0; index < queue->current_length; index++) {
        if (condition(queue->content[index]) == TRUE) {
            return TRUE;
        }
    }
    return FALSE;
}

#endif //COLLECTIONS_ARRAY_QUEUE_H
```
