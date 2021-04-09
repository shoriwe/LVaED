# List Based Stack (C Implementation)

# Source Code

```c
#ifndef COLLECTIONS_LIST_QUEUE_H
#define COLLECTIONS_LIST_QUEUE_H
#include "../Lists/doubly_linked_list.h"
#include "../primitives.h"


typedef struct ListQueue {
    DoublyLinkedList *content;
    bool reversed;
    unsigned long long int length;
} ListQueue;

ListQueue* ListQueue_new() {
    ListQueue* queue = malloc(sizeof(ListQueue));
    queue->content = DoublyLinkedList_new();
    queue->reversed = FALSE;
    queue->length = 0;
    return queue;
}

void ListQueue_update(ListQueue* queue) {
    queue->length = queue->content->length;
}

bool ListQueue_enqueue(ListQueue *queue, void *value, size_t size) {
    bool result;
    if (queue->reversed == TRUE) {
        if (queue->length == 0) {
            result = DoublyLinkedList_append(queue->content, value, size);
        } else {
            result = DoublyLinkedList_insert(queue->content, 0, value, size);
        }
    } else {
        result = DoublyLinkedList_append(queue->content, value, size);
    }
    ListQueue_update(queue);
    return result;
}

ListNode* ListQueue_dequeue(ListQueue *queue) {
    ListNode* result;
    if (queue->length == 0) {
        return NULL;
    }
    if (queue->reversed) {
        result = queue->content->end;
        if (result->before != NULL) {
            result->before->next = result->next;
        }
        if (result->next != NULL) {
            result->next->before  = result->before;
        }
        if (queue->content->length == 1) {
            queue->content->start = NULL;
            queue->content->end = NULL;
        } else if (queue->content->length == 2){
            queue->content->end = queue->content->start;
        } else {
            queue->content->end = queue->content->end->before;
        }
    } else {
        result = DoublyLinkedList_get(queue->content, 0);
        if (result->before != NULL) {
            result->before->next = result->next;
        }
        if (result->next != NULL) {
            result->next->before  = result->before;
        }
        if (queue->content->length == 1) {
            queue->content->start = NULL;
            queue->content->end = NULL;
        } else if (queue->content->length == 2){
            queue->content->start = queue->content->end;
        } else {
            queue->content->start = queue->content->start->next;
        }
    }
    queue->content->length--;
    ListQueue_update(queue);
    return result;
}

bool ListQueue_isEmpty(ListQueue* queue) {
    return queue->length == 0;
}


void ListQueue_clear(ListQueue* queue) {
    DoublyLinkedList_clear(queue->content);
    ListQueue_update(queue);
}

bool ListQueue_search(ListQueue *queue, is_equal_condition condition) {
    return DoublyLinkedList_contains(queue->content, condition);
}

#endif //COLLECTIONS_LIST_QUEUE_H
```
