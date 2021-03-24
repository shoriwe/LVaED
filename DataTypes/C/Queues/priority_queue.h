#ifndef COLLECTIONS_PRIORITY_QUEUE_H
#define COLLECTIONS_PRIORITY_QUEUE_H

#include "../Lists/doubly_linked_list.h"
#include "../primitives.h"

typedef struct PriorityQueueElement {
    void *value;
    size_t size;
    int priority;
} PriorityQueueElement;

PriorityQueueElement *PriorityQueueElement_new(void *value, size_t size, int priority) {
    PriorityQueueElement *element = malloc(sizeof(PriorityQueueElement));
    element->value = value;
    element->priority = priority;
    element->size = size;
    return element;
}

typedef struct PriorityQueue {
    DoublyLinkedList *content;
    size_t length;
    bool reversed;
} PriorityQueue;

PriorityQueue *PriorityQueue_new() {
    PriorityQueue *queue = malloc(sizeof(PriorityQueue));
    queue->length = 0;
    queue->reversed = FALSE;
    queue->content = DoublyLinkedList_new();
    return queue;
}

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

PriorityQueueElement *PriorityQueue_dequeue(PriorityQueue *queue) {
    ListNode *result;
    if (queue->length == 0) {
        return NULL;
    }
    if (queue->reversed) {
        result = queue->content->end;
        if (result->before != NULL) {
            result->before->next = result->next;
        }
        if (result->next != NULL) {
            result->next->before = result->before;
        }
        if (queue->content->length == 1) {
            queue->content->start = NULL;
            queue->content->end = NULL;
        } else if (queue->content->length == 2) {
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
            result->next->before = result->before;
        }
        if (queue->content->length == 1) {
            queue->content->start = NULL;
            queue->content->end = NULL;
        } else if (queue->content->length == 2) {
            queue->content->start = queue->content->end;
        } else {
            queue->content->start = queue->content->start->next;
        }
    }
    queue->content->length--;
    queue->length--;
    return result->value;
}

void PriorityQueue_clear(PriorityQueue *queue) {
    DoublyLinkedList_clear(queue->content);
    queue->length = 0;
}

bool PriorityQueue_is_empty(PriorityQueue *queue) {
    return queue->length == 0;
}

bool PriorityQueue_search(PriorityQueue *queue, is_equal_condition condition) {
    return DoublyLinkedList_contains(queue->content, condition);
}

void PriorityQueue_reverse(PriorityQueue *queue) {
    queue->reversed = !queue->reversed;
}

#endif //COLLECTIONS_PRIORITY_QUEUE_H
