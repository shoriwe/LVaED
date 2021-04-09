# Binary Tree (Java implementation)

# Source Code

```java
public class BiTree {

    public Node root;
    public Node left;
    public Node right;

    public BiTree() {
        this.root = null;
    }

    public BiTree(Object object) {
        Node root = (Node) object;
        left = null;
        right = null;

    }

    //sub arbol
    public Node subBitree(Node left, Object object, Node rigth) {
        return new Node(left, object, rigth);
    }

    public boolean isEmpty() {
        return root == null;
    }

    //agrega a la raiz
    public boolean root(Object object) {

        try {
            root = subBitree(null, object, null);
            return true;

        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }

    public boolean insetleft(Object object) {
        try {
            if (!isEmpty()) {
                root.left = subBitree(null, object, null);
                return true;

            } else {
                return false;
            }
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }

    public boolean insertRight(Object object) {
        try {
            if (!isEmpty()) {
                root.right = subBitree(null, object, null);
                return true;
            } else {
                return false;
            }
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }

    public String preOrder(Node root) {
        String obj = "";
        obj = (root.object instanceof Node) ? ((Node) root.object).object.toString() : root.object.toString();
        obj = obj + ((root.left != null) ? preOrder(root.left) : "");
        obj = obj + ((root.right != null) ? preOrder(root.right) : "");
        return obj;
    }

    public String inOrder(Node root) {
        String obj = "";
        obj = obj + ((root.left != null) ? preOrder(root.left) : "");
        obj = (root.object instanceof Node) ? ((Node) root.object).object.toString() : root.object.toString();
        obj = obj + ((root.right != null) ? preOrder(root.right) : "");
        return obj;
    }

    public String posOrder(Node root) {
        String obj = "";
        obj = obj + ((root.left != null) ? preOrder(root.left) : "");
        obj = obj + ((root.right != null) ? preOrder(root.right) : "");
        obj = (root.object instanceof Node) ? ((Node) root.object).object.toString() : root.object.toString();
        return obj;
    }

    public Node eliminarNode(Node node, int value) {
        if (node == null) {
            System.out.println("El nodo no se encontro");
        } else if (value < (int) node.getObject()) {
            left = eliminarNode(node.getLeft(), value);
            node.setLeft(left);
        } else if (value > (int) node.getObject()) {
            right = eliminarNode(node.getRight(), value);
            node.setRight(right);
        } else {
            Node n = node;
            if (n.getRight() == null) {
                node = n.getLeft();
            } else if (n.getLeft() == null) {
                node = n.getRight();
            } else {
                n = change(n);
            }
        }

        return node;
    }

    public Node change(Node node) {
        Node n = node;
        Node no = node.getLeft();
        while (no.getRight() != null) {
            n = no;
            no = no.getRight();
        }
        node.setObject(no.getObject());
        if (n == node) {
            n.setLeft(no.getLeft());
        } else {
            n.setRight(no.getLeft());
        }
        return no;
    }

    public Node delete(Integer value) {
        root = eliminarNode(root, value);
        return null;

    }
    
    public Node search(int n){
        Node node = root;
        while((int)node.getObject() != n){
            if(n< (int)node.getObject()){
                node = node.getLeft();
            }else{
                node = node.getRight();
            }
            if(node == null){
                return null;
            }
        }
        return node;
    }

    @Override
    public String toString() {
        return "BiTree{" + "root=" + root + ", left=" + left + ", right=" + right + '}';
    }

}
```