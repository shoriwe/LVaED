//
// Created by universidad on 2/23/2021.
//

#ifndef COLLECTIONS_LIST_NODE_H
#define COLLECTIONS_LIST_NODE_H

#include <stdio.h>

typedef unsigned char bool;

const bool TRUE = 1, FALSE = 0;

typedef struct ListNode {
    char copied;
    void *value;
    size_t value_size;
    struct ListNode *next;
    struct ListNode *before;
} ListNode;
#endif //COLLECTIONS_LIST_NODE_H
