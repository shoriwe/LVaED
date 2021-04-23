# AVL Tree (C Implementation)

# Source Code

```c
#ifndef COLLECTIONS_AVL_TREE_H
#define COLLECTIONS_AVL_TREE_H

#include <stdlib.h>
#include "../primitives.h"
#include "../Lists/simple_linked_list.h"

#define LEFT 0
#define RIGHT 1
#define ANY 2

typedef struct AVLTreeNode {
    int value;
    int weight;
    struct AVLTreeNode *left;
    struct AVLTreeNode *right;
} AVLTreeNode;

AVLTreeNode *AVLTreeNode_new(int value) {
    AVLTreeNode *node = malloc(sizeof(AVLTreeNode));
    node->value = value;
    node->weight = 0;
    node->right = NULL;
    node->left = NULL;
    return node;
}

typedef struct AVLTree {
    AVLTreeNode *root;
} AVLTree;

AVLTree *AVLTree_new() {
    AVLTree *tree = malloc(sizeof(AVLTree));
    tree->root = NULL;
    return tree;
}

int AVLTree_calculate_weight(AVLTreeNode *node) {
    if (node == NULL) {
        return -1;
    }
    return node->weight;
}

static int max_weight(int left_hand_side, int right_hand_side) {
    if (left_hand_side < right_hand_side) {
        return right_hand_side;
    }
    return left_hand_side;
}

static AVLTreeNode *AVLTree_insert_backend(AVLTreeNode *target, int value);

bool AVLTree_insert(AVLTree *tree, int value) {
    AVLTreeNode *new_root = AVLTree_insert_backend(tree->root, value);
    if (new_root != NULL) {
        tree->root = new_root;
        return TRUE;
    }
    return FALSE;
}

AVLTreeNode *AVLTree_rotateLeft(AVLTreeNode *root) {
    AVLTreeNode *left = root->left;
    root->left = left->right;
    left->right = root;
    root->weight = max_weight(AVLTree_calculate_weight(root->left), AVLTree_calculate_weight(root->right)) + 1;
    left->weight = max_weight(AVLTree_calculate_weight(left->left), root->weight) + 1;
    return left;
}

AVLTreeNode *AVLTree_rotateRight(AVLTreeNode *root) {
    AVLTreeNode *right = root->right;
    root->right = right->left;
    right->left = root;
    root->weight = max_weight(AVLTree_calculate_weight(root->left), AVLTree_calculate_weight(root->right)) + 1;
    right->weight = max_weight(AVLTree_calculate_weight(right->right), root->weight) + 1;
    return right;
}

AVLTreeNode *AVLTree_rotateRightLeft(AVLTreeNode *root) {
    root->left = AVLTree_rotateRight(root->left);
    return AVLTree_rotateLeft(root);
}

AVLTreeNode *AVLTree_rotateLeftRight(AVLTreeNode *root) {
    root->left = AVLTree_rotateLeft(root->left);
    return AVLTree_rotateRight(root);
}

static AVLTreeNode *AVLTree_insert_backend(AVLTreeNode *target, int value) {
    if (target == NULL) {
        target = AVLTreeNode_new(value);
    } else if (value < target->value) {
        target->left = AVLTree_insert_backend(target->left, value);
        if (AVLTree_calculate_weight(target->left) - AVLTree_calculate_weight(target->right) == 2) {
            if (value < target->left->value) {
                target = AVLTree_rotateLeft(target);
            } else {
                target = AVLTree_rotateRightLeft(target);
            }
        }
    } else if (value > target->value) {
        target->right = AVLTree_insert_backend(target->right, value);
        if (AVLTree_calculate_weight(target->right) - AVLTree_calculate_weight(target->left) == 2) {
            if (value > target->right->value) {
                target = AVLTree_rotateRight(target);
            } else {
                target = AVLTree_rotateLeftRight(target);
            }
        }
    }
    target->weight = max_weight(AVLTree_calculate_weight(target->left), AVLTree_calculate_weight(target->right)) + 1;
    return target;
}

SimpleLinkedList *AVLTree_pre_order(AVLTreeNode *tree, SimpleLinkedList *memory) {
    if (memory == NULL) {
        memory = SimpleLinkedList_new();
    }
    if (tree != NULL) {
        SimpleLinkedList_append(memory, tree, 0);
        AVLTree_pre_order(tree->left, memory);
        AVLTree_pre_order(tree->right, memory);
    }
    return memory;
}

SimpleLinkedList *AVLTree_in_order(AVLTreeNode *tree, SimpleLinkedList *memory) {
    if (memory == NULL) {
        memory = SimpleLinkedList_new();
    }
    if (tree != NULL) {
        AVLTree_in_order(tree->left, memory);
        SimpleLinkedList_append(memory, tree, 0);
        AVLTree_in_order(tree->right, memory);
    }
    return memory;
}

SimpleLinkedList *AVLTree_pos_order(AVLTreeNode *tree, SimpleLinkedList *memory) {
    if (memory == NULL) {
        memory = SimpleLinkedList_new();
    }
    if (tree != NULL) {
        AVLTree_pos_order(tree->left, memory);
        AVLTree_pos_order(tree->right, memory);
        SimpleLinkedList_append(memory, tree, 0);
    }
    return memory;
}

AVLTreeNode *FindMostLeftRight(AVLTreeNode *start) {
    if (start == NULL) {
        return NULL;
    }
    if (start->right == NULL) {
        return NULL;
    }
    if (start->right->right == NULL) {
        AVLTreeNode *result = start->right;
        start->right = start->right->left;
        return result;
    }
    return FindMostLeftRight(start->right);
}

AVLTreeNode *FindMostRightLeft(AVLTreeNode *start) {
    if (start == NULL) {
        return NULL;
    }
    if (start->left == NULL) {
        return NULL;
    }
    if (start->left->left == NULL) {
        AVLTreeNode *result = start->left;
        start->left = start->left->right;
        return result;
    }
    return FindMostRightLeft(start->left);
}

bool AVLTree_binary_remove_int(AVLTreeNode *node, int value, AVLTreeNode *parent, char parent_direction) {
    if (node == NULL) {
        return FALSE;
    }
    if (node->value == value) {
        // DO something to updated the current state of the tree
        AVLTreeNode *left_target = NULL;
        AVLTreeNode *right_target = NULL;
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
    bool removed_left = AVLTree_binary_remove_int(node->left, value, node, LEFT);
    if (removed_left == FALSE) {
        return AVLTree_binary_remove_int(node->right, value, node, RIGHT);
    }
    return TRUE;
}

#endif //COLLECTIONS_AVL_TREE_H
```
