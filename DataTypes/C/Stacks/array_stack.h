//
// Created by universidad on 2/26/2021.
//

#ifndef COLLECTIONS_ARRAY_STACK_H
#define COLLECTIONS_ARRAY_STACK_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../primitives.h"

typedef struct ArrayStack {
    void **content;
    size_t length;
    bool reversed;
} ArrayStack;

struct ArrayStack *ArrayStack_new() {
    struct ArrayStack *result = malloc(sizeof(struct ArrayStack));
    result->length = 0;
    result->content = NULL;
    result->reversed = FALSE;
    return result;
}

bool ArrayStack_is_empty(struct ArrayStack *array_stack) {
    return array_stack->length == 0;
}

void ArrayStack_clear(struct ArrayStack *array_stack) {
    free(array_stack->content);
    array_stack->content = NULL;
    array_stack->length = 0;
}

void *ArrayStack_peek(struct ArrayStack *array_stack) {
    if (array_stack->length == 0) {
        return NULL;
    }
    if (array_stack->reversed) {
        return array_stack->content[0];
    } else {
        return array_stack->content[array_stack->length - 1];
    }
}

void *ArrayStack_pop(struct ArrayStack *array_stack) {
    if (array_stack->length == 0) {
        return NULL;
    }
    void *result;
    int start;
    int step;
    unsigned long long int end;
    if (array_stack->reversed) {
        result = array_stack->content[0];
        start = 1;
        step = 1;
        end = array_stack->length;
    } else {
        result = array_stack->content[array_stack->length - 1];
        start = 0;
        step = 0;
        end = array_stack->length - 1;
    }
    if (array_stack->length - 1 == 0) {
        array_stack->content = NULL;
    } else {
        void **old = malloc(sizeof(void *) * array_stack->length);
        memcpy(old, array_stack->content, array_stack->length * sizeof(void *));
        free(array_stack->content);
        array_stack->content = malloc(sizeof(void *) * (array_stack->length - 1));
        for (int index = start; index < end; index++) {
            array_stack->content[index - step] = old[index];
        }
    }
    array_stack->length--;
    return result;
}


void ArrayStack_push(struct ArrayStack *array_stack, void *value, size_t _) {
    if (array_stack->length == 0) {
        array_stack->content = malloc(sizeof(void *));
        array_stack->content[0] = value;
    } else if (array_stack->reversed) {
        void **old = malloc(sizeof(void *) * array_stack->length);
        memcpy(old, array_stack->content, sizeof(void *) * array_stack->length);
        free(array_stack->content);
        array_stack->content = malloc(sizeof(void *) * (array_stack->length + 1));
        array_stack->content[0] = value;
        for (int index = 0; index < array_stack->length; index++) {
            array_stack->content[index + 1] = old[index];
        }
    } else {
        array_stack->content = realloc(array_stack->content, sizeof(void *) * (array_stack->length + 1));
        array_stack->content[array_stack->length] = value;
    }
    array_stack->length++;
}

size_t ArrayStack_size(struct ArrayStack *array_stack) {
    return array_stack->length;
}

bool ArrayStack_search(struct ArrayStack *array_stack, void *value) {
    if (array_stack->length == 0) {
        return FALSE;
    }
    for (int index = 0; index < array_stack->length; index++) {
        if (array_stack->content[index] == value) {
            return TRUE;
        }
    }
    return FALSE;
}

void ArrayStack_reverse(struct ArrayStack *array_stack) {
    array_stack->reversed = !array_stack->reversed;
}

#endif //COLLECTIONS_ARRAY_STACK_H
