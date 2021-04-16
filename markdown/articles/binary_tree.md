# Binary Tree

Binary trees are one of the most applicable DataTypes in computer science and can represent a lot of real concepts of the real world. With the base concept of every node contains only two sub-nodes (`left` and `right`), the binary tree is able to represent perfectly mathematical expression, family successions.

<div style="text-align: center"><a href="https://commons.wikimedia.org/wiki/File:Binary_tree.svg"><img src="/static/vendor/img/wikipedia/Binary_tree.svg" alt="BinaryTree" style="width: 500px; height: auto"/></a><p>[1] Binary tree | <a href="https://commons.wikimedia.org/wiki/File:Binary_tree.svg">https://commons.wikimedia.org/wiki/File:Binary_tree.svg</a></p></div>

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

## Binary trees specific properties

This properties are Binary tree specific and all of the apply to binary trees full filled with numeric values.

### Binary Insert

The binary insertion consist in comparing each existing node in the tree with the insertion value, if the node value is greater than the reference it add the element to the left, but if the node value is lower or equal it add the insertion value to the right side.

In resume this are the insertion steps:

1. Compare node value with value insertion value.
2. If node value is greater than insertion value, go to step `4`.
3. If node value is lower or equal than insertion value go to step `5`.
4. If node's left child is null, assign the insertion value to  it, the other way repeat this sequence of step but with this child.
5. If node's right child is null, assign the insertion value to  it, the other way repeat this sequence of step but with this child.

#### Example

In this example, the program will try to insert the number `4` in the binary tree.

<div style="text-align: center"><a href="/static/img/DataTypes/BinaryInsert.png"><img src="/static/img/DataTypes/BinaryInsert.png" alt="BinaryInsert.png" style="width: 500px; height: auto"/></a></div>

### Binary search

This kind of tree traversal is specific to speed up the search a value in the content of a binary tree full filled with numbers.

This behavior can be only archived when each number was added to the tree approaching the Binary Insertion algorithm for it. Any other way will probably give unexpected results.

The algorithm consists in traverse the tree but comparing each node value with the value received, if the node value is lower than the reference value, we traverse the right sub-tree, the other way we will traverse the left one. In case we find and equal value, we return the node pointing to it.

#### Example

In this example, the program will try to insert the number `4` in the binary tree.

<div style="text-align: center"><a href="/static/img/DataTypes/BinarySearch.png"><img src="/static/img/DataTypes/BinarySearch.png" alt="BinarySearch.png" style="width: 500px; height: auto"/></a></div>

### Binary Remove

When removing in a binary tree, first the program will search the node approaching a binary search, then with the targeted node it will approach one of this rules to decide how it should connect the other nodes.

* Leaf nodes are removed directly.
* One child nodes are replaced with it's corresponding child.
* For Two child nodes. With left one the `left-most_right` rule is approached. With the right one the `right-most_left` rule is used.

#### Left-Most_Right

Taking the left node, the program will search for the most far and immediate node in the right.

#### Right-Most_Left

Taking the right node, the program will search for the most far and immediate node in the left.

#### Example

The next gif will explain visually how binary remove works

<div style="text-align: center"><a href="/static/img/DataTypes/BinaryRemove.gif"><img src="/static/img/DataTypes/BinaryRemove.gif" alt="BinaryRemove.gif" style="width: 500px; height: auto"/></a></div>

## General trees properties

When we usually refer to any kind of tree, it's possible to conclude that all have this tree properties.

### - Height

Height refers to the maximum depth level that a tree can have from it's route to it the most far node.

<div style="text-align: center"><a href="/static/img/DataTypes/BinaryTreeHeight.png"><img src="/static/img/DataTypes/BinaryTreeHeight.png" alt="BinaryTreeHeight.png" style="width: 500px; height: auto"/></a></div>

The height concept can be used to balance binary trees by targeting the same height for every sub-tree in each of the sides of every node in the tree.

<div style="text-align: center"><a href="/static/img/DataTypes/BinaryTreeBalanced.png"><img src="/static/img/DataTypes/BinaryTreeBalanced.png" alt="BinaryTreeBalanced.png" style="width: 500px; height: auto"/></a></div>

The last image shows a binary tree balanced having to perfectly balanced sub trees with height 2.

<div style="text-align: center"><a href="/static/img/DataTypes/BinaryTreeUnBalanced.png"><img src="/static/img/DataTypes/BinaryTreeUnBalanced.png" alt="BinaryTreeUnBalanced.png" style="width: 500px; height: auto"/></a></div>

By the other hand, this binary tree shows a sub-tree with height 2 perfectly balanced and other that is not balanced, making the root based tree not balanced too.

### - Level

The level of a node is determined by its depth having as reference with level 0 the root of the tree.

<div style="text-align: center"><a href="/static/img/DataTypes/BinaryTreeLevels.png"><img src="/static/img/DataTypes/BinaryTreeLevels.png" alt="BinaryTreeLevels.png" style="width: 500px; height: auto"/></a></div>
 
# References

Identifier | Author | Source
---------- | ------ | ------
1|Derrick Coetzee|[https://commons.wikimedia.org/wiki/File:Binary_tree.svg](https://commons.wikimedia.org/wiki/File:Binary_tree.svg)
