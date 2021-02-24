//
// Created by universidad on 2/24/2021.
//

#ifndef COLLECTIONS_SIMPLE_CIRCULAR_LINKED_LIST_H
#define COLLECTIONS_SIMPLE_CIRCULAR_LINKED_LIST_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "list_node.h"
#include "simple_linked_list.h"


typedef struct SimpleCircularLinkedList {
    struct SimpleLinkedList* content;
    unsigned long long int length;
    struct ListNode *start;
    struct ListNode *end;
} SimpleCircularLinkedList;

struct SimpleCircularLinkedList *SimpleCircularLinkedList_new() {
    struct SimpleCircularLinkedList *list = malloc(sizeof(struct SimpleCircularLinkedList));
    list->content = SimpleLinkedList_new();
    list->length = 0;
    list->start = NULL;
    list->end = NULL;
    return list;
}

void SimpleCircularLinkedList_update(struct SimpleCircularLinkedList* list) {
    list->length = list->content->length;
    list->start = list->content->start;
    list->end = list->content->end;
    list->end->next = list->start;
}

/*
 * SimpleCircularLinkedList_get
 * append_cpy
 * append_nocpy
 * SimpleCircularLinkedList_set
 * SimpleCircularLinkedList_insert
 * SimpleCircularLinkedList_sub_list
 * SimpleCircularLinkedList_insert_end
 * SimpleCircularLinkedList_insert_start
 * remove
 * SimpleCircularLinkedList_clear
 * SimpleCircularLinkedList_find
 * SimpleCircularLinkedList_contains
 * SimpleCircularLinkedList_to_array
 * sort
 */

void **SimpleCircularLinkedList_to_array(struct SimpleCircularLinkedList *list) {
    return SimpleLinkedList_to_array(list->content);
}

unsigned long long int SimpleCircularLinkedList_find(struct SimpleCircularLinkedList *list, is_equal_condition condition) {
    return SimpleLinkedList_find(list->content, condition);
}

bool SimpleCircularLinkedList_contains(struct SimpleCircularLinkedList *list, is_equal_condition condition) {
    return SimpleLinkedList_contains(list->content, condition);
}

void SimpleCircularLinkedList_clear(struct SimpleCircularLinkedList *list) {
    SimpleLinkedList_clear(list->content);
    list->length = 0;
    list->start = NULL;
    list->end = NULL;
}

bool SimpleCircularLinkedList_remove_by_index(struct SimpleCircularLinkedList *list, unsigned long long int index, bool delete_object) {
    bool result = SimpleLinkedList_remove_by_index(list->content, index, delete_object);
    if (result == TRUE) {
        SimpleCircularLinkedList_update(list);
    }
    return result;
}

bool SimpleCircularLinkedList_insert(struct SimpleCircularLinkedList *list, unsigned long long int index, void *value, size_t size) {
    bool result = SimpleLinkedList_insert(list->content, index, value, size);
    if (result == TRUE) {
        SimpleCircularLinkedList_update(list);
    }
    return result;
}

/*
 * Different from SimpleCircularLinkedList_append since this will SimpleCircularLinkedList_insert just before the end
 */
bool SimpleCircularLinkedList_insert_end(struct SimpleCircularLinkedList *list, void *value, size_t size) {
    return SimpleCircularLinkedList_insert(list, list->length - 1, value, size);
}

int SimpleCircularLinkedList_insert_start(struct SimpleCircularLinkedList *list, void *value, size_t size) {
    return SimpleCircularLinkedList_insert(list, 0, value, size);
}

bool SimpleCircularLinkedList_set(struct SimpleCircularLinkedList *list, unsigned long long int index, void *value, size_t size,
                          bool delete_old) {
    return SimpleLinkedList_set(list->content, index, value, size, delete_old);
}

bool SimpleCircularLinkedList_append(struct SimpleCircularLinkedList *list, void *value, size_t size) {
    bool result = SimpleLinkedList_append(list->content, value, size);
    if (result == TRUE) {
        SimpleCircularLinkedList_update(list);
    }
    return result;
}

struct ListNode *SimpleCircularLinkedList_get(struct SimpleCircularLinkedList *list, unsigned long long int index) {
    return SimpleLinkedList_get(list->content, index);
}

struct SimpleCircularLinkedList *
SimpleCircularLinkedList_sub_list(struct SimpleCircularLinkedList *list, unsigned long long int start, unsigned long long int end) {
    struct SimpleLinkedList* result_content = SimpleLinkedList_sub_list(list->content, start, end);
    if (result_content == NULL) {
        return NULL;
    }
    struct SimpleCircularLinkedList* result = SimpleCircularLinkedList_new();
    result->content  =result_content;
    SimpleCircularLinkedList_update(result);
    return result;
}
#endif //COLLECTIONS_SIMPLE_CIRCULAR_LINKED_LIST_H
