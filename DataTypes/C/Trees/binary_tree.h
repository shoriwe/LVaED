#ifndef COLLECTIONS_BINARY_TREE_H
#define COLLECTIONS_BINARY_TREE_H

#define LEFT 0
#define RIGHT 1

#include <stdlib.h>
#include <string.h>
#include "../Lists/simple_linked_list.h"
#include "../primitives.h"

typedef struct BinaryTreeNode {
    void *value;
    size_t size;
    struct BinaryTreeNode *left;
    struct BinaryTreeNode *right;
} BinaryTreeNode;

BinaryTreeNode *BinaryTreeNode_new(void *value, size_t size, BinaryTreeNode *left, BinaryTreeNode *right) {
    BinaryTreeNode *node = malloc(sizeof(BinaryTreeNode));
    if (size == 0) {
        node->value = value;
        node->size = 0;
    } else {
        node->value = malloc(size);
        node->size = size;
        strcpy_s(node->value, size, value);
    }
    node->left = left;
    node->right = right;
    return node;
}

BinaryTreeNode *BinaryTreeNode_insert(BinaryTreeNode *tree, void *value, size_t size, int direction) {
    if (direction == LEFT) {
        if (tree->left != NULL) {
            return NULL;
        }
        tree->left = BinaryTreeNode_new(value, size, NULL, NULL);
        return tree->left;
    } else if (direction == RIGHT) {
        if (tree->right != NULL) {
            return NULL;
        }
        tree->right = BinaryTreeNode_new(value, size, NULL, NULL);
        return tree->right;
    }
    return NULL;
}

SimpleLinkedList *BinaryTree_pre_order(BinaryTreeNode *tree, SimpleLinkedList *memory) {
    if (memory == NULL) {
        memory = SimpleLinkedList_new();
    }
    if (tree != NULL) {
        SimpleLinkedList_append(memory, tree, 0);
        BinaryTree_pre_order(tree->left, memory);
        BinaryTree_pre_order(tree->right, memory);
    }
    return memory;
}

SimpleLinkedList *BinaryTree_in_order(BinaryTreeNode *tree, SimpleLinkedList *memory) {
    if (memory == NULL) {
        memory = SimpleLinkedList_new();
    }
    if (tree != NULL) {
        BinaryTree_in_order(tree->left, memory);
        SimpleLinkedList_append(memory, tree, 0);
        BinaryTree_in_order(tree->right, memory);
    }
    return memory;
}

SimpleLinkedList *BinaryTree_pos_order(BinaryTreeNode *tree, SimpleLinkedList *memory) {
    if (memory == NULL) {
        memory = SimpleLinkedList_new();
    }
    if (tree != NULL) {
        BinaryTree_pos_order(tree->left, memory);
        BinaryTree_pos_order(tree->right, memory);
        SimpleLinkedList_append(memory, tree, 0);
    }
    return memory;
}

void BinaryTree_remove(BinaryTreeNode *tree, int direction) {
    if (direction == LEFT) {
        tree->left = NULL;
    } else if (direction == RIGHT) {
        tree->right = NULL;
    }
}

BinaryTreeNode *BinaryTree_search(BinaryTreeNode *node, is_equal_condition condition) {
    SimpleLinkedList *content = BinaryTree_in_order(node, NULL);
    unsigned long long int index = SimpleLinkedList_find(content, condition);
    if (index == SIZE_MAX) {
        return NULL;
    }
    return SimpleLinkedList_get(content, index)->value;
}

#endif //COLLECTIONS_BINARY_TREE_H
