package LVaED.Lists.DoublyLinkedList;

public class ListNode {
    public Object Value;
    public ListNode Next;
    public ListNode Before;

    public ListNode(Object value) {
        this.Value = value;
        this.Next = null;
        this.Before = null;
    }

    public ListNode() {
        this.Before = null;
        this.Next = null;
        this.Value = null;
    }

    public Object getObject() {
        return this.Value;
    }

    public void setObject(Object object) {
        this.Value = object;
    }

    public boolean isEquals(Object object) {
        return this.Value == object;
    }

    public boolean isEquals(ListNode node) {
        return this == node;
    }

    @Override
    public String toString() {
        return "ListNode{" +
                "object=" + this.Value +
                '}';
    }
}
