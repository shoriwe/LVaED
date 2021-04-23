public class AVLTree {

    private Node root;

    public AVLTree() {
        this.root = null;
    }

  
    //altura del arbol
    public int height(Node node) {
        return node == null ? -1 : node.height;

    }

    public static int max(int leftHeight, int rightHeight) {
        return leftHeight > rightHeight ? leftHeight : rightHeight;

    }

    //rotacion por la izquierda
    public Node leftRotation(Node node) {
        Node aux = node.left;
        node.left = aux.right;
        aux.right = node;
        node.height = max(height(aux.left), height(aux.right)) + 1;
        aux.height = max(height(aux.left), node.height) + 1;
        return aux;
    }

    //rotacion por la derecha
    public Node rightRotation(Node node) {
        Node aux = node.right;
        node.left = aux.left;
        aux.right = node;
        node.height = max(height(aux.left), height(aux.right)) + 1;
        aux.height = max(height(aux.right), node.height) + 1;
        return aux;
    }

    //rotacion doble por la izquierda
    public Node doubleLeftRotation(Node node) {
        node.left = rightRotation(node.left);
        return leftRotation(node);
    }

    //rotacion doble por la derecha
    public Node doubleRightRotation(Node node) {
        node.right = leftRotation(node.right);
        return rightRotation(node);
    }

    //insertar
    public Node insert(Comparable obj, Node node) {

        if (node == null) {
            node = new Node(obj, null, null);
        } else if (obj.compareTo(node.object) < 0) {
            node.left = insert(obj, node.left);
            if (node.left.height - node.right.height == 2) {
                if (obj.compareTo(node.left.object) < 0) {
                    node = leftRotation(node);
                } else {
                    node = doubleLeftRotation(node);
                }
            }
        } else if (obj.compareTo(node.object) > 0) {
            node.right = insert(obj, node.right);
            if ((node.right.height) - (node.left.height) == 2) {
                if (obj.compareTo(node.right.object) > 0) {
                    node = rightRotation(node);
                } else {
                    node = doubleRightRotation(node);
                }
            }
        }
        return node;

    }
}
