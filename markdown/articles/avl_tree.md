# AVL Binary Tree

AVL trees are an subtype of binary trees specialized in the auto-balance of the child trees by approaching four special kinds of rotations.

AVL trees in difference with traditional binary trees, have a unique attribute usually called `weight` or its more common counterpart `height`. Based on that its class will looks like something like this in `Java`.

```java
public class AVLTreeNode {
    public int value;
    public int weight;
    public AVLTreeNode left;
    public AVLTreeNode right;

    public AVLTreeNode(int value) {
        this.left = null;
        this.right = null;
        this.value = value;
        this.weight = 0;
    }
}
```

The `weight` property is important since based on its value we can determine which kind of rotation will be executed in top of it.

## Minimal methods to work with `AVL trees`

### Rotations

Here we are going to explain the basic rotations of the AVL tree.

### `Left Rotation`

`Left Rotation` consist in having tree nodes in a left row, this means the first has as right child the second one and this one have as right child the third one.

Now, the algorithm consist in putting the second one as the new root of the tree with left child the first one and right child the third one.

The `Left` rotation can be simplified in setting the second node left child as the first node.

<div style="text-align: center"><a href="/static/img/DataTypes/LeftRotationCompatibleTree.png"><img src="/static/img/DataTypes/LeftRotationCompatibleTree.png" alt="LeftRotationCompatibleTree.png" style="width: 500px; height: auto"/></a></div>

Its implementation in `Java` will looks like:

```java
private AVLTreeNode rotateLeft(AVLTreeNode source) {
    AVLTreeNode left = source.left;
    source.left = left.right;
    left.right = source;
    source.weight = Math.max(calculateHeight(source.left), calculateHeight(source.right)) + 1;
    left.weight = Math.max(calculateHeight(left.left), source.weight) + 1;
    return left;
}
```

### `Right Rotation`

`Right Rotation` rotation consist in having tree nodes in a right row, this means the first has as left child the second one and this one has as left child the third one.

Now, the algorithm consist in putting the second one as the new root of the tree with right child the first one and left child the third one.

The `Right` rotation can be simplified in setting the second node right child as the first node.

<div style="text-align: center"><a href="/static/img/DataTypes/RightRotationCompatibleTree.png"><img src="/static/img/DataTypes/RightRotationCompatibleTree.png" alt="RightRotationCompatibleTree.png" style="width: 500px; height: auto"/></a></div>

Its implementation in `Java` will looks like:

```java
private AVLTreeNode rotateRight(AVLTreeNode source) {
    AVLTreeNode right = source.right;
    source.right = right.left;
    right.left = source;
    source.weight = Math.max(calculateHeight(source.left), calculateHeight(source.right)) + 1;
    right.weight = Math.max(calculateHeight(right.right), source.weight) + 1;
    return right;
}
```

### `Left Rotation then Right Rotation`

`Left Rotation then Right Rotation` consist if first making a left rotation in the `left` child of the root to then apply again a rotation but this time a `right` one.

<div style="text-align: center"><a href="/static/img/DataTypes/LeftRotationRightRotation.png"><img src="/static/img/DataTypes/LeftRotationRightRotation.png" alt="LeftRotationRightRotation.png" style="width: 500px; height: auto"/></a></div>

Its implementation in `Java` will looks like:

```java
private AVLTreeNode rotateLeftRight(AVLTreeNode source) {
    source.right = this.rotateLeft(source.right);
    return this.rotateRight(source);
}
```

### `Right Rotation then Left Rotation`

`Right Rotation then Left Rotation` consist if first making a left rotation in the `right` child of the root to then apply again a rotation but this time a `left` one.

<div style="text-align: center"><a href="/static/img/DataTypes/RightRotationLeftRotation.png"><img src="/static/img/DataTypes/RightRotationLeftRotation.png" alt="RightRotationLeftRotation.png" style="width: 500px; height: auto"/></a></div>

Its implementation in `Java` will looks like:

```java
private AVLTreeNode rotateRightLeft(AVLTreeNode source) {
    source.left = this.rotateRight(source.left);
    return this.rotateLeft(source);
}
```

### `Insert`

In AVL trees the insert has a similar behavior in comparison with the `binary insert` by the only difference that after inserting the new value, it will also balance the tree at the end.

```java
private AVLTreeNode insert(int value, AVLTreeNode target) {
    if (target == null) {
        target = new AVLTreeNode(value);
    } else if (value < target.value) {
        target.left = this.insert(value, target.left);
        if (this.calculateHeight(target.left) - this.calculateHeight(target.right) == 2) {
            if (value < target.left.value) {
                target = this.rotateLeft(target);
            } else {
                target = this.rotateRightLeft(target);
            }
        }
    } else if (value > target.value) {
        target.right = this.insert(value, target.right);
        if (this.calculateHeight(target.right) - this.calculateHeight(target.left) == 2) {
            if (value > target.right.value) {
                target = this.rotateRight(target);
            } else {
                target = this.rotateLeftRight(target);
            }
        }
    }
    target.weight = Math.max(calculateHeight(target.left), calculateHeight(target.right)) + 1;
    // This should be the new root
    return target;
}
```

Based on the source code of before, you will notice that it auto-balance the tree after it added the node. When the weight of a tree if greater than `1` or less than `-1`, it will rotate it's children until this value is equal to `0`, `-1` or `1`.

### `Binary Remove`

Vanilla binary remove should work for this kind of trees, the only difference is that executing it, it will also execute the balance algorithm.

### Walk algorithms

Vanilla `In-Order`, `Pre-Order` and `Post-Order` should also work for this kind of tree.