//
// Created by universidad on 2/26/2021.
//

#ifndef COLLECTIONS_LIST_STACK_H
#define COLLECTIONS_LIST_STACK_H

#include "../Lists/doubly_linked_list.h"
#include "../primitives.h"

typedef struct ListStack {
    DoublyLinkedList *content;
    bool reversed;
} ListStack;

struct ListStack *ListStack_new() {
    struct ListStack *result = malloc(sizeof(struct ListStack));
    result->content = DoublyLinkedList_new();
    result->reversed = FALSE;
    return result;
}

void ListStack_clear(struct ListStack *list_stack) {
    DoublyLinkedList_clear(list_stack->content);
}

bool ListStack_is_empty(struct ListStack *list_stack) {
    return list_stack->content->length == 0;
}

void *ListStack_peek(struct ListStack *list_stack) {
    struct ListNode *result;
    if (list_stack->content->length == 0) {
        return NULL;
    }
    if (list_stack->reversed) {
        result = DoublyLinkedList_get(list_stack->content, 0)->value;
    } else {
        result = DoublyLinkedList_get(list_stack->content, list_stack->content->length - 1)->value;
    }
    return result;
}

void *ListStack_pop(struct ListStack *list_stack) {
    void *result;
    if (list_stack->content->length == 0) {
        return NULL;
    }
    if (list_stack->reversed) {
        result = DoublyLinkedList_get(list_stack->content, 0)->value;
        DoublyLinkedList_remove_by_index(list_stack->content, 0, FALSE);
    } else {
        result = DoublyLinkedList_get(list_stack->content, list_stack->content->length - 1)->value;
        DoublyLinkedList_remove_by_index(list_stack->content, list_stack->content->length - 1, FALSE);
    }
    return result;
}

void ListStack_push(struct ListStack *list_stack, void *value, size_t size) {
    if (list_stack->reversed) {
        if (list_stack->content->length == 0) {
            DoublyLinkedList_append(list_stack->content, value, size);
        } else {
            DoublyLinkedList_insert(list_stack->content, 0, value, size);
        }
    } else {
        DoublyLinkedList_append(list_stack->content, value, size);
    };
}

size_t ListStack_size(struct ListStack *list_stack) {
    return list_stack->content->length;
}

bool ListStack_search(struct ListStack *list_stack, is_equal_condition condition) {
    return DoublyLinkedList_contains(list_stack->content, condition);
}

void ListStack_reverse(struct ListStack *list_stack) {
    list_stack->reversed = !list_stack->reversed;
}

#endif //COLLECTIONS_LIST_STACK_H
