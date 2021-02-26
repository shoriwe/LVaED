#pragma once
#ifndef COLLECTIONS_DOUBLY_LINKED_LIST
#define COLLECTIONS_DOUBLY_LINKED_LIST

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "list_node.h"

typedef struct DoublyLinkedList {
    unsigned long long int length;
    struct ListNode *start;
    struct ListNode *end;
} DoublyLinkedList;

struct DoublyLinkedList *DoublyLinkedList_new() {
    struct DoublyLinkedList *list = malloc(sizeof(struct DoublyLinkedList));
    list->length = 0;
    list->start = NULL;
    list->end = NULL;
    return list;
}

/*
 * DoublyLinkedList_get - Done
 * append_cpy - Done
 * append_nocpy - Done
 * DoublyLinkedList_set - Done
 * DoublyLinkedList_insert - Done
 * DoublyLinkedList_sub_list - Done
 * DoublyLinkedList_insert_end - Done
 * DoublyLinkedList_insert_start - Done
 * remove - Done
 * DoublyLinkedList_clear - Done
 * DoublyLinkedList_find - Done
 * DoublyLinkedList_contains - Done
 * DoublyLinkedList_to_array - Done
 * sort
 */

void **DoublyLinkedList_to_array(struct DoublyLinkedList *list) {
    if (list == NULL) {
        return NULL;
    }
    if (list->length == 0) {
        return NULL;
    }
    void **array = malloc(sizeof(void *) * list->length);
    struct ListNode *current = list->start;
    for (unsigned long long int index = 0; index < list->length; index++) {
        array[index] = current->value;
        current = current->next;
    }
    return array;
}

unsigned long long int DoublyLinkedList_find(struct DoublyLinkedList *list, is_equal_condition condition) {
    if (list == NULL) {
        return SIZE_MAX;
    }
    if (list->length == 0) {
        return SIZE_MAX;
    }
    struct ListNode *current = list->start;
    for (unsigned long long int index = 0; index < list->length; index++) {
        if (condition(current) == TRUE) {
            return index;
        }
        current = current->next;
    }
    return SIZE_MAX;
}

bool DoublyLinkedList_contains(struct DoublyLinkedList *list, is_equal_condition condition) {
    if (DoublyLinkedList_find(list, condition) != SIZE_MAX) {
        return TRUE;
    }
    return FALSE;
}

void DoublyLinkedList_clear(struct DoublyLinkedList *list) {
    list->length = 0;
    list->start = NULL;
    list->end = NULL;
}

bool DoublyLinkedList_remove_by_index(struct DoublyLinkedList *list, unsigned long long int index, bool delete_object) {
    if (list == NULL) {
        return FALSE;
    }
    if (list->length == 0 || index >= list->length) {
        return FALSE;
    }
    struct ListNode *current;
    if (index == 0) {
        current = list->start;
        if (list->length == 1) {
            if (delete_object == TRUE && current->copied == TRUE) {
                free(list->start->value);
            }
            free(list->start);
            list->start = NULL;
            list->end = NULL;
        } else {
            struct ListNode *next = list->start->next;
            next->before = NULL;
            if (delete_object == TRUE && current->copied == TRUE) {
                free(list->start->value);
            }
            free(list->start);
            list->start = next;
            if (list->length - 1 == 1) {
                list->end = list->start;
            }
        }
    } else if (index == list->length - 1) {
        current = list->end;
        struct ListNode *before = list->end->before;
        before->next = NULL;
        if (delete_object == TRUE && current->copied == TRUE) {
            free(list->end->value);
        }
        free(list->end);
        list->end = before;
        if (list->length - 1 == 1) {
            list->start = list->end;
        }
    } else {
        current = list->start;
        for (unsigned long long int list_index = 0; list_index != list->length; list_index++) {
            if (list_index == index) {
                break;
            }
            current = current->next;
        }
        if (delete_object == TRUE && current->copied == TRUE) {
            free(current->value);
        }
        current->next->before = current->before;
        current->before->next = current->next;
        free(current);
    }
    list->length--;
    return TRUE;
}

bool DoublyLinkedList_insert(struct DoublyLinkedList *list, unsigned long long int index, void *value, size_t size) {
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
        old_start->before = new_node;
        new_node->next = old_start;
        new_node->before = NULL;
        list->start = new_node;
    } else if (index == (list->length - 1)) {
        struct ListNode *end = list->end;
        new_node->before = end->before;
        new_node->next = end;
        end->before->next = new_node;
        end->before = new_node;
    } else {
        struct ListNode *current = list->start;
        for (unsigned long long int list_index = 0; list_index != list->length; list_index++) {
            if (list_index == index) {
                break;
            }
            current = current->next;
        }
        current->before->next = new_node;
        new_node->next = current;
        new_node->before = current->before;
        current->before = new_node;
    }
    list->length++;
    return TRUE;
}

/*
 * Different from DoublyLinkedList_append since this will DoublyLinkedList_insert just before the end
 */
bool DoublyLinkedList_insert_end(struct DoublyLinkedList *list, void *value, size_t size) {
    return DoublyLinkedList_insert(list, list->length - 1, value, size);
}

int DoublyLinkedList_insert_start(struct DoublyLinkedList *list, void *value, size_t size) {
    return DoublyLinkedList_insert(list, 0, value, size);
}

bool DoublyLinkedList_set(struct DoublyLinkedList *list, unsigned long long int index, void *value, size_t size,
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

bool DoublyLinkedList_append(struct DoublyLinkedList *list, void *value, size_t size) {
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
        list->start->before = NULL;
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
    new_node->before = old_last_node;
    new_node->next = NULL;
    old_last_node->next = new_node;
    list->end = new_node;
    list->length++;
    return TRUE;
}

struct ListNode *DoublyLinkedList_get(struct DoublyLinkedList *list, unsigned long long int index) {
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

struct DoublyLinkedList *
DoublyLinkedList_sub_list(struct DoublyLinkedList *list, unsigned long long int start, unsigned long long int end) {
    if (list == NULL) {
        return NULL;
    }
    if (list->length == 0 || start >= list->length || end >= list->length || start >= end) {
        return NULL;
    }
    struct DoublyLinkedList *result = DoublyLinkedList_new();
    bool append_it = FALSE;
    struct ListNode *current = list->start;
    for (unsigned long long int list_index = 0; list_index < list->length; list_index++) {
        if (list_index == start) {
            DoublyLinkedList_append(result, current->value, current->value_size);
            append_it = TRUE;
        } else if (list_index == end) {
            DoublyLinkedList_append(result, current->value, current->value_size);
            break;
        } else if (append_it == TRUE) {
            DoublyLinkedList_append(result, current->value, current->value_size);
        }
        current = current->next;
    }
    return result;
}

#endif