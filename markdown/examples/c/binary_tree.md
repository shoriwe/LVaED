# Binary Tree (C Implementation)

# Source Code

```c
#ifndef COLLECTIONS_BINARY_TREE_H
#define COLLECTIONS_BINARY_TREE_H

#define LEFT 0
#define RIGHT 1
#define ANY 2

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

BinaryTreeNode *BinaryTree_int_binary_search(BinaryTreeNode *node, int value) {
    if (node == NULL) {
        return NULL;
    }
    if ((*(int *) node->value) == value) {
        return node;
    }
    BinaryTreeNode *result = NULL;
    if ((*(int *) node->value) > value) {
        result = BinaryTree_int_binary_search(node->left, value);
    }
    if (((*(int *) node->value) < value) && result == NULL) {
        result = BinaryTree_int_binary_search(node->right, value);
    }

    return result;
}

BinaryTreeNode *FindMostLeftRight(BinaryTreeNode *start) {
    if (start == NULL) {
        return NULL;
    }
    if (start->right == NULL) {
        return NULL;
    }
    if (start->right->right == NULL) {
        BinaryTreeNode *result = start->right;
        start->right = start->right->left;
        return result;
    }
    return FindMostLeftRight(start->right);
}

BinaryTreeNode *FindMostRightLeft(BinaryTreeNode *start) {
    if (start == NULL) {
        return NULL;
    }
    if (start->left == NULL) {
        return NULL;
    }
    if (start->left->left == NULL) {
        BinaryTreeNode *result = start->left;
        start->left = start->left->right;
        return result;
    }
    return FindMostRightLeft(start->left);
}

BinaryTreeNode *BinaryTree_int_binary_insert(BinaryTreeNode *node, int *value) {
    if (node == NULL) {
        return BinaryTreeNode_new(value, 0, NULL, NULL);
    }
    if ((*(int *) node->value) < (*value)) {
        node->right = BinaryTree_int_binary_insert(node->right, value);
    } else if ((*(int *) node->value) > (*value)) {
        node->left = BinaryTree_int_binary_insert(node->left, value);

    }
    return node;
}

bool BinaryTree_binary_remove_int(BinaryTreeNode *node, int value, BinaryTreeNode *parent, char parent_direction) {
    if (node == NULL) {
        return FALSE;
    }
    if ((*(int *) node->value) == value) {
        // DO something to updated the current state of the tree
        BinaryTreeNode *left_target = NULL;
        BinaryTreeNode *right_target = NULL;
        bool isLeaf = TRUE;
        bool appendLast = TRUE;
        if (node->left != NULL && node->right == NULL) {
            left_target = node->left;
            isLeaf = FALSE;
            appendLast = FALSE;
        } else if (node->left == NULL && node->right != NULL) {
            right_target = node->right;
            isLeaf = FALSE;
            appendLast = FALSE;
        } else if (node->left != NULL && node->right != NULL) {
            left_target = FindMostLeftRight(node->left);
            if (left_target == NULL) {
                right_target = FindMostRightLeft(node->right);
                // Do something when both are null
                if (right_target == NULL) {
                    left_target = node->left;
                    node->left = NULL;
                }
            }
            isLeaf = FALSE;
        }
        if (isLeaf == TRUE) { // Node is leaf
            switch (parent_direction) {
                case LEFT:
                    parent->left = NULL;
                    break;
                case RIGHT:
                    parent->right = NULL;
                    break;
                default:
                    break;
            }
        } else {
            if (parent != NULL) {
                switch (parent_direction) {
                    case LEFT:
                        if (right_target != NULL) {
                            parent->left = right_target;
                        } else if (left_target != NULL) {
                            parent->left = left_target;
                        } else {
                            break;
                        }
                        if (appendLast == TRUE) {
                            parent->left->left = node->left;
                            parent->left->right = node->right;
                        }
                        break;
                    case RIGHT:
                        if (right_target != NULL) {
                            parent->right = right_target;
                        } else if (left_target != NULL) {
                            parent->right = left_target;
                        } else {
                            break;
                        }
                        if (appendLast == TRUE) {
                            parent->right->left = node->left;
                            parent->right->right = node->right;
                        }
                        break;
                    default:
                        break;
                }
            } else { // Node is root
                if (left_target != NULL) {
                    left_target->left = node->left;
                    left_target->right = node->right;
                } else if (right_target != NULL) {
                    right_target->left = node->left;
                    right_target->right = node->right;
                }
            }
        }
        // Finally Disconnect the node
        node->left = NULL;
        node->right = NULL;
        return TRUE;
    }
    bool removed_left = BinaryTree_binary_remove_int(node->left, value, node, LEFT);
    if (removed_left == FALSE) {
        return BinaryTree_binary_remove_int(node->right, value, node, RIGHT);
    }
    return TRUE;
}

#endif //COLLECTIONS_BINARY_TREE_H
```