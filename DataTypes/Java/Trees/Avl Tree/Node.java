public class Node {

 
     
     Comparable object;
     public Node left;
     public Node right;
     public int height;
 
     public Node(Comparable object) {
         this.object = object;
     }
 
     public Node(Comparable object, Node left, Node right) {
         this.object = object;
         this.left = left;
         this.right = right;
         height = 0;
     }
 
     public Object getObject() {
         return object;
     }
 
     public void setObject(Comparable object) {
         this.object = object;
     }
 
     public Node getLeft() {
         return left;
     }
 
     public void setLeft(Node left) {
         this.left = left;
     }
 
     public Node getRight() {
         return right;
     }
 
     public void setRight(Node right) {
         this.right = right;
     }
 
     public int getHeight() {
         return height;
     }
 
     public void setHeight(int height) {
         this.height = height;
     }
     
     
     
     
     
 
 }
 