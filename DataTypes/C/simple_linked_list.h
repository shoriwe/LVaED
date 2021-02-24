#pragma once
#ifndef COLLECTIONS_SIMPLE_LINKED_LIST
#define COLLECTIONS_SIMPLE_LINKED_LIST

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "list_node.h"

typedef struct SimpleLinkedList {
    unsigned long long int length;
    struct ListNode *start;
    struct ListNode *end;
} SimpleLinkedList;

struct SimpleLinkedList *SimpleLinkedList_new();

void **SimpleLinkedList_to_array(struct SimpleLinkedList *list);

unsigned long long int SimpleLinkedList_find(struct SimpleLinkedList *list, is_equal_condition condition);

bool SimpleLinkedList_contains(struct SimpleLinkedList *list, is_equal_condition condition);

void SimpleLinkedList_clear(struct SimpleLinkedList *list);

bool SimpleLinkedList_remove_by_index(struct SimpleLinkedList *list, unsigned long long int index, bool delete_object);

bool SimpleLinkedList_insert(struct SimpleLinkedList *list, unsigned long long int index, void *value, size_t size);

bool SimpleLinkedList_insert_end(struct SimpleLinkedList *list, void *value, size_t size);

int SimpleLinkedList_insert_start(struct SimpleLinkedList *list, void *value, size_t size);

bool SimpleLinkedList_set(struct SimpleLinkedList *list, unsigned long long int index, void *value, size_t size,
                          bool delete_old);

bool SimpleLinkedList_append(struct SimpleLinkedList *list, void *value, size_t size);

struct ListNode *SimpleLinkedList_get(struct SimpleLinkedList *list, unsigned long long int index);

struct SimpleLinkedList *
SimpleLinkedList_sub_list(struct SimpleLinkedList *list, unsigned long long int start, unsigned long long int end);


struct SimpleLinkedList *SimpleLinkedList_new() {
    struct SimpleLinkedList *list = malloc(sizeof(struct SimpleLinkedList));
    list->length = 0;
    list->start = NULL;
    list->end = NULL;
    return list;
}

/*
 * SimpleLinkedList_get - Done
 * append_cpy - Done
 * append_nocpy - Done
 * SimpleLinkedList_set - Done
 * SimpleLinkedList_insert - Done
 * SimpleLinkedList_sub_list - Done
 * SimpleLinkedList_insert_end - Done
 * SimpleLinkedList_insert_start - Done
 * remove - Done
 * SimpleLinkedList_clear - Done
 * SimpleLinkedList_find - Done
 * SimpleLinkedList_contains - Done
 * SimpleLinkedList_to_array - Done
 * sort
 */

void **SimpleLinkedList_to_array(struct SimpleLinkedList *list) {
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

unsigned long long int SimpleLinkedList_find(struct SimpleLinkedList *list, is_equal_condition condition) {
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

bool SimpleLinkedList_contains(struct SimpleLinkedList *list, is_equal_condition condition) {
    if (SimpleLinkedList_find(list, condition) != SIZE_MAX) {
        return TRUE;
    }
    return FALSE;
}

void SimpleLinkedList_clear(struct SimpleLinkedList *list) {
    list->length = 0;
    list->start = NULL;
    list->end = NULL;
}

bool SimpleLinkedList_remove_by_index(struct SimpleLinkedList *list, unsigned long long int index, bool delete_object) {
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
        struct ListNode *before = SimpleLinkedList_get(list, index - 1);
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
        struct ListNode *before = SimpleLinkedList_get(list, index - 1);
        before->next = current->next;
        free(current);
    }
    list->length--;
    return TRUE;
}

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

/*
 * Different from SimpleLinkedList_append since this will SimpleLinkedList_insert just before the end
 */
bool SimpleLinkedList_insert_end(struct SimpleLinkedList *list, void *value, size_t size) {
    return SimpleLinkedList_insert(list, list->length - 1, value, size);
}

int SimpleLinkedList_insert_start(struct SimpleLinkedList *list, void *value, size_t size) {
    return SimpleLinkedList_insert(list, 0, value, size);
}

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

struct SimpleLinkedList *
SimpleLinkedList_sub_list(struct SimpleLinkedList *list, unsigned long long int start, unsigned long long int end) {
    if (list == NULL) {
        return NULL;
    }
    if (list->length == 0 || start >= list->length || end >= list->length || start >= end) {
        return NULL;
    }
    struct SimpleLinkedList *result = SimpleLinkedList_new();
    bool append_it = FALSE;
    struct ListNode *current = list->start;
    for (unsigned long long int list_index = 0; list_index < list->length; list_index++) {
        if (list_index == start) {
            SimpleLinkedList_append(result, current->value, current->value_size);
            append_it = TRUE;
        } else if (list_index == end) {
            SimpleLinkedList_append(result, current->value, current->value_size);
            break;
        } else if (append_it == TRUE) {
            SimpleLinkedList_append(result, current->value, current->value_size);
        }
        current = current->next;
    }
    return result;
}

#endif