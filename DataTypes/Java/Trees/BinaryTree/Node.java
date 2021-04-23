public class Node {
    
    public Node left;
    public Node right;
    public Object object;
    
    public Node(Object object){
        this.left = null;
        this.right = null;
        this.object = object;
    }

    public Node(Node left, Object object, Node right) {
        this.left = left;
        this.right = left;
        this.object = object;
    }

    public Object getObject() {
        return object;
    }

    public void setObject(Object object) {
        this.object = object;
    }

    public Node getRight() {
        return right;
    }

    public Node getLeft() {
        return left;
    }

    public void setRight(Node right) {
        this.right = right;
    }
    
    

    public void setLeft(Node left) {
        this.left = left;
    }

    

    @Override
    public String toString() {
        return "Node{" + 
                "left=" + left + 
                ", right=" + right + 
                ", object=" + object + 
                '}';
    }
   
    
    
    
}
