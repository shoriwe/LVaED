package LVaED.Lists.DoublyLinkedList;

import java.util.Iterator;

public interface DoublyListInterface {

    /*
    essential operations
    */
    public boolean isEmpty(); // Done

    public int getSize(); // Done

    public void clear(); // Done

    public Object getHead(); // Done

    public Object getTail(); // Done

    public ListNode search(Object object); // Done

    public boolean add(Object object); // Done

    public boolean insert(ListNode node, Object object); // Done

    public boolean insert(Object ob, Object object); // Done

    public boolean insertHead(Object object); // Done

    public boolean insertTail(Object object); // Done

    public boolean remove(ListNode node); // Done

    public boolean remove(Object object); // Done

    /*
    expansion operations
     */
    public boolean contains(Object object); // Done

    public Iterator<ListNode> iterator(); // Done

    public Iterator<ListNode> ReverseIterator() // Done

    public Object[] toArray(); // Done

    public Object[] toArray(Object[] object);

    public Object getBeforeTo();

    public ListNode getBeforeTo(ListNode node); // Done

    public Object getNextTo();

    public Object getNextTo(ListNode node); // Done

    public DoublyLinkedList subList(ListNode from, ListNode to); // Done

    public DoublyLinkedList sortList();

}
