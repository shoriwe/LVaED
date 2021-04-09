# Binary Tree

Binary trees are one of the most applicable DataTypes in computer science and can represent a lot of real concepts of the real world. With the base concept of every node contains only two sub-nodes (`left` and `right`), the binary tree is able to represent perfectly mathematical expression, family successions,

<div style="text-align: center"><a href="https://commons.wikimedia.org/wiki/File:Binary_tree.svg"><img src="/static/vendor/img/wikipedia/Binary_tree.svg" alt="BinaryTree" style="width: 500px; height: auto"/></a><p>[1] https://commons.wikimedia.org/wiki/File:Binary_tree.svg</p></div>

## Node

When two or more nodes are connected, then that combination can be called tree, so based in that, in nature, every element of a tree, including its `root` is a node and usually have this three attributes.

* Value: Which is the corresponding value.
* Left: This is the left sub-node that is connected to it.
* Right: This is the right sub-node that is connected to it.

In `C` the code will look like:

```c
typedef struct BinaryTreeNode {
    void *value;
    size_t size;
    struct BinaryTreeNode *left;
    struct BinaryTreeNode *right;
} BinaryTreeNode;
```

## Adding elements

To add an element to a binary tree is as simple like setting its `left` or `right` pointing to the wanted subtree or node.

Adding an element will look something like this in `C`:

```c
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
```

## Iteration

This iteration algorithms will be explained with this example:

<div style="text-align: center"><a href="/static/img/DataTypes/BinaryTreeExample.png"><img src="/static/img/DataTypes/BinaryTreeExample.png" alt="BinaryTreeExample.png" style="width: 500px; height: auto"/></a></div>

By the nature of tree, is almost always common to iterate over their nodes with recursion, since binary trees have only three special kinds of iteration with specifically three operations, there is not too heavy lifting for the algorithm.

### Pre-order

If a tree is full filled with a mathematical expresion, like the one of the example, iterating over it will look in a Polish notation syntax.

#### Operations

1. Yield the root
2. Yield the left sub-tree (repeat 1, 2, 3 but with this tree)
3. Yield the right sub-tree (repeat 1, 2, 3 but with this tree)

The `C` implementation of this steps will look like:

```c
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
```

Based on the example, the result iteration using this steps will be: `+ * a b / c d`

### Pos-order

This kind of iteration, if the tree is full filled with mathematical elements, the result will be a reverse polish notation.

#### Operations

1. Yield the left sub-tree (repeat 1, 2, 3 but with this tree)
2. Yield the right sub-tree (repeat 1, 2, 3 but with this tree)
3. Yield the root

The `C` implementation of this steps will look like:

```c
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
```

Based on the example, the result iteration using this steps will be: `a b * c d / +`

### In-Order

If the Binary tree is full filled with a mathematical expression, after iterating with this steps, the result will be a vanilla math expression, written in common human pattern.

#### Operations

1. Yield the left sub-tree (repeat 1, 2, 3 but with this tree)
2. Yield the root
3. Yield the right sub-tree (repeat 1, 2, 3 but with this tree)

The `C` implementation of this steps will look like:

```c
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
```

Based on the example, the result iteration using this steps will be: `a * b + c / d`

# References

Identifier | Author | Source
---------- | ------ | ------
1|Derrick Coetzee|[https://commons.wikimedia.org/wiki/File:Binary_tree.svg](https://commons.wikimedia.org/wiki/File:Binary_tree.svg)
