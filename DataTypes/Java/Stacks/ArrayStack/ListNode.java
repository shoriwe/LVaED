
 */
public class ListNode {
     private Object object;
    public ListNode next;

    public ListNode getNext() {
        return next;
    }

    public void setNext(ListNode next) {
        this.next = next;
    }

    public ListNode() {
        this.object = null;
        this.next = null;
    }

    public ListNode(Object object) {
        this.object = object;
        this.next = null;
    }

    public ListNode(Object object, ListNode next) {
        this.object = object;
        this.next = next;
    }

    public Object getObject() {
        return object;
    }

    public void setObject(Object object) {
        this.object = object;
    }

    public boolean isEquals(Object object) {
        if (this.getObject().toString().equals(object.toString())) {
            return true;
        }
        return false;
    }

    public boolean isEquals(ListNode node) {
        if (this.toString().equals(node.toString())) {
            return true;
        }
        return false;
    }

    @Override
    public String toString() {
        return "ListNode{"
                + "object=" + object
                + ", next=" + next
                + '}';
    }
}
