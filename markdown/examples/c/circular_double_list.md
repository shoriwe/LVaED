# Circular Double Linked List (C Implementation)

# Source Code

```c
#ifndef COLLECTIONS_DOUBLE_CIRCULAR_LINKED_LIST_H
#define COLLECTIONS_DOUBLE_CIRCULAR_LINKED_LIST_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "list_node.h"
#include "doubly_linked_list.h"


typedef struct DoubleCircularLinkedList {
    struct DoublyLinkedList* content;
    unsigned long long int length;
    struct ListNode *start;
    struct ListNode *end;
} DoubleCircularLinkedList;

struct DoubleCircularLinkedList *DoubleCircularLinkedList_new() {
    struct DoubleCircularLinkedList *list = malloc(sizeof(struct DoubleCircularLinkedList));
    list->content = DoublyLinkedList_new();
    list->length = 0;
    list->start = NULL;
    list->end = NULL;
    return list;
}

void DoubleCircularLinkedList_update(struct DoubleCircularLinkedList* list) {
    list->length = list->content->length;
    list->start = list->content->start;
    list->end = list->content->end;
    list->end->next = list->start;
    list->start->before = list->end;
}

void **DoubleCircularLinkedList_to_array(struct DoubleCircularLinkedList *list) {
    return DoublyLinkedList_to_array(list->content);
}

unsigned long long int DoubleCircularLinkedList_find(struct DoubleCircularLinkedList *list, is_equal_condition condition) {
    return DoublyLinkedList_find(list->content, condition);
}

bool DoubleCircularLinkedList_contains(struct DoubleCircularLinkedList *list, is_equal_condition condition) {
    return DoublyLinkedList_contains(list->content, condition);
}

void DoubleCircularLinkedList_clear(struct DoubleCircularLinkedList *list) {
    DoublyLinkedList_clear(list->content);
    list->length = 0;
    list->start = NULL;
    list->end = NULL;
}

bool DoubleCircularLinkedList_remove_by_index(struct DoubleCircularLinkedList *list, unsigned long long int index, bool delete_object) {
    bool result = DoublyLinkedList_remove_by_index(list->content, index, delete_object);
    if (result == TRUE) {
        DoubleCircularLinkedList_update(list);
    }
    return result;
}

bool DoubleCircularLinkedList_insert(struct DoubleCircularLinkedList *list, unsigned long long int index, void *value, size_t size) {
    bool result = DoublyLinkedList_insert(list->content, index, value, size);
    if (result == TRUE) {
        DoubleCircularLinkedList_update(list);
    }
    return result;
}

/*
 * Different from DoubleCircularLinkedList_append since this will DoubleCircularLinkedList_insert just before the end
 */
bool DoubleCircularLinkedList_insert_end(struct DoubleCircularLinkedList *list, void *value, size_t size) {
    return DoubleCircularLinkedList_insert(list, list->length - 1, value, size);
}

int DoubleCircularLinkedList_insert_start(struct DoubleCircularLinkedList *list, void *value, size_t size) {
    return DoubleCircularLinkedList_insert(list, 0, value, size);
}

bool DoubleCircularLinkedList_set(struct DoubleCircularLinkedList *list, unsigned long long int index, void *value, size_t size,
                          bool delete_old) {
    return DoublyLinkedList_set(list->content, index, value, size, delete_old);
}

bool DoubleCircularLinkedList_append(struct DoubleCircularLinkedList *list, void *value, size_t size) {
    bool result = DoublyLinkedList_append(list->content, value, size);
    if (result == TRUE) {
        DoubleCircularLinkedList_update(list);
    }
    return result;
}

struct ListNode *DoubleCircularLinkedList_get(struct DoubleCircularLinkedList *list, unsigned long long int index) {
    return DoublyLinkedList_get(list->content, index);
}

struct DoubleCircularLinkedList *
DoubleCircularLinkedList_sub_list(struct DoubleCircularLinkedList *list, unsigned long long int start, unsigned long long int end) {
    struct DoublyLinkedList* result_content = DoublyLinkedList_sub_list(list->content, start, end);
    if (result_content == NULL) {
        return NULL;
    }
    struct DoubleCircularLinkedList* result = DoubleCircularLinkedList_new();
    result->content  =result_content;
    DoubleCircularLinkedList_update(result);
    return result;
}
#endif //COLLECTIONS_DOUBLE_CIRCULAR_LINKED_LIST_H
```
