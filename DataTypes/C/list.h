#pragma once
#ifndef COLLECTIONS_LIST
#define COLLECTIONS_LIST

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned int bool;

const bool TRUE = 0, FALSE = 1;

typedef struct ListNode {
    char copied;
    void *value;
    size_t value_size;
    struct ListNode *next;
    struct ListNode *before;
} ListNode;

typedef bool (*is_equal_condition)(struct ListNode *node);

typedef struct List {
    unsigned long long int length;
    struct ListNode *start;
    struct ListNode *end;
} List;

struct List *new_list() {
    struct List *list = malloc(sizeof(struct List));
    list->length = 0;
    list->start = NULL;
    list->end = NULL;
    return list;
}

/*
 * get - Done
 * append_cpy - Done
 * append_nocpy - Done
 * set - Done
 * insert - Done
 * sub_list - Done
 * insert_end - Done
 * insert_start - Done
 * remove - Done
 * clear - Done
 * find - Done
 * contains - Done
 * to_array - Done
 * sort
 */

void **to_array(struct List *list) {
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

struct ListNode *find(struct List *list, is_equal_condition condition) {
    if (list == NULL) {
        return NULL;
    }
    if (list->length == 0) {
        return NULL;
    }
    struct ListNode *current = list->start;
    for (unsigned long long int index = 0; index < list->length; index++) {
        if (condition(current) == TRUE) {
            return current;
        }
        current = current->next;
    }
    return NULL;
}

bool contains(struct List *list, is_equal_condition condition) {
    if (find(list, condition) != NULL) {
        return TRUE;
    }
    return FALSE;
}

struct List *sub_list(struct List *list, unsigned long long int start, unsigned long long int end) {
    if (list == NULL) {
        return NULL;
    }
    if (list->length == 0 || start >= list->length || end >= list->length || start >= end) {
        return NULL;
    }
    struct List *new_list = malloc(sizeof(struct List));
    new_list->length = end - start + 1;
    new_list->start = malloc(sizeof(struct ListNode));
    new_list->end = malloc(sizeof(struct ListNode));
    struct ListNode *current = list->start;
    for (unsigned long long int list_index = 0; list_index < list->length; list_index++) {
        if (list_index == start) {
            memcpy(new_list->start, current, sizeof(struct ListNode));
        } else if (list_index == end) {
            memcpy(new_list->end, current, sizeof(struct ListNode));
            break;
        }
        current = current->next;
    }
    new_list->end->next = NULL;
    new_list->start->before = NULL;
    return new_list;
}

void clear(struct List *list) {
    list->length = 0;
    list->start = NULL;
    list->end = NULL;
}

int remove_by_index(struct List *list, unsigned long long int index, bool delete_object) {
    if (list == NULL) {
        return 1;
    }
    if (list->length == 0 || index >= list->length) {
        return 1;
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
    return 1;
}

int insert(struct List *list, unsigned long long int index, void *value, size_t size) {
    if (list == NULL) {
        return 1;
    }
    if (list->length == 0 || index >= list->length) {
        return 1;
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
    return 0;
}

/*
 * Different from append since this will insert just before the end
 */
int insert_end(struct List *list, void *value, size_t size) {
    return insert(list, list->length - 1, value, size);
}

int insert_start(struct List *list, void *value, size_t size) {
    return insert(list, 0, value, size);
}

int set(struct List *list, unsigned long long int index, void *value, size_t size, bool delete_old) {
    if (list == NULL) {
        return 1;
    }
    if (list->length == 0 || index >= list->length) {
        return 1;
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
    return 0;
}

int append(struct List *list, void *value, size_t size) {
    if (list == NULL) {
        return 1;
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
        return 0;
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
    return 0;
}

struct ListNode *get(struct List *list, unsigned long long int index) {
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

#endif