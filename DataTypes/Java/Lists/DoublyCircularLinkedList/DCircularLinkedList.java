import java.util.Iterator;


public class DCircularLinkedList {

    public ListNode Start;
    public ListNode End;
    public int Length;

    public int GetSize() {
        return this.Length;
    }

    public boolean IsEmpty() {
        return this.Length == 0;
    }

    public Object GetHead() {
        if (this.Length == 0) {
            throw new IndexOutOfBoundsException("The list is empty");
        }
        return this.Start.Value;
    }

    public Object GetTail() {
        if (this.Length == 0) {
            throw new IndexOutOfBoundsException("The list is empty");
        }
        return this.End.Value;
    }

    public ListNode Search(Object value) {
        if (this.Length == 0) {
            throw new IndexOutOfBoundsException("The list is empty");
        }
        ListNode current = this.Start;
        for (int list_index = 0; list_index < this.Length; list_index++) {
            if (current.Value == value) {
                return current;
            }
            current = current.Next;
        }
        return null;
    }

    public boolean Add(Object value) {
        this.Append(value);
        return true;
    }

    public Iterator<ListNode> Iterator() {
        final ListNode[] current = {this.Start};
        return new Iterator<ListNode>() {
            @Override
            public boolean hasNext() {
                return current[0] != null;
            }

            @Override
            public ListNode next() {
                if (current[0] != null) {
                    ListNode result = current[0];
                    current[0] = current[0].Next;
                    return result;
                } else {
                    return null;
                }
            }
        };
    }

    public boolean Insert(ListNode node, Object value) {
        if (this.Length == 0) {
            throw new IndexOutOfBoundsException("The list is empty");
        }
        boolean found = false;
        ListNode current = this.Start;
        if (this.Length == 1) {
            if (this.Start == node) {
                this.Start = new ListNode(value);
                this.Start.Next = this.End;
                this.End.Before = this.Start;
                found = true;
            }
        } else {
            for (int list_index = 0; list_index < this.Length; list_index++) {
                if (current == node) {
                    if (list_index == 0) {
                        this.Start.Before = new ListNode(value);
                        this.Start.Before.Next = this.Start;
                        this.Start = this.Start.Before;
                    } else {
                        ListNode before = current.Before;
                        current.Before = new ListNode(value);
                        current.Before.Before = before;
                        before.Next = current.Before;
                        current.Before.Next = current;
                    }
                    found = true;
                    break;
                }
                current = current.Next;
            }
        }
        if (found) {
            this.Length++;
        }
        return found;
    }

    public Iterator<ListNode> ReverseIterator() {
        final ListNode[] current = {this.End};
        return new Iterator<ListNode>() {

            public boolean hasNext() {
                return current[0] != null;
            }

            public ListNode next() {
                if (current[0] != null) {
                    ListNode result = current[0];
                    current[0] = current[0].Before;
                    return result;
                } else {
                    return null;
                }
            }
        };
    }

    public boolean Insert(Object next_value, Object value) {
        if (this.Length == 0) {
            throw new IndexOutOfBoundsException("The list is empty");
        }
        boolean found = false;
        ListNode current = this.Start;
        if (this.Length == 1) {
            if (this.Start.Value == next_value) {
                this.Start = new ListNode(value);
                this.Start.Next = this.End;
                this.End.Before = this.Start;
                found = true;
            }
        } else {
            for (int list_index = 0; list_index < this.Length; list_index++) {
                if (current.Value == next_value) {
                    if (list_index == 0) {
                        this.Start.Before = new ListNode(value);
                        this.Start.Before.Next = this.Start;
                        this.Start = this.Start.Before;
                    } else {
                        ListNode before = current.Before;
                        current.Before = new ListNode(value);
                        current.Before.Before = before;
                        before.Next = current.Before;
                        current.Before.Next = current;
                    }
                    found = true;
                    break;
                }
                current = current.Next;
            }
        }
        if (found) {
            this.Length++;
        }
        return found;
    }

    public boolean InsertHead(Object value) {
        try {
            this.Insert(0, value);
            return true;
        } catch (IndexOutOfBoundsException e) {
            return false;
        }
    }

    public boolean InsertTail(Object value) {
        try {
            this.Insert(this.Length - 1, value);
            return true;
        } catch (IndexOutOfBoundsException e) {
            return false;
        }
    }

    public boolean Remove(ListNode node) {
        try {
            this.RemoveNode(node);
            return true;
        } catch (IndexOutOfBoundsException e) {
            return false;
        }
    }

    public boolean Remove(Object value) {
        try {
            this.RemoveValue(value);
            return true;
        } catch (IndexOutOfBoundsException e) {
            return false;
        }
    }

    public void Insert(int index, Object value) {
        if (this.Length == 0) {
            throw new IndexOutOfBoundsException("List is empty");
        }
        if (this.Length <= index) {
            throw new IndexOutOfBoundsException("The list index is out of range");
        }
        if (this.Length == 1) {
            ListNode old_start = this.Start;
            this.Start = new ListNode(value);
            this.Start.Next = old_start;
            old_start.Before = this.Start;
        } else if (index == 0) {
            ListNode new_node = new ListNode(value);
            this.Start.Before = new_node;
            new_node.Next = this.Start;
            this.Start = new_node;
        } else if (index == this.Length - 1) {
            ListNode new_node = new ListNode(value);
            new_node.Next = this.End;
            this.End.Before.Next = new_node;
            new_node.Before = this.End.Before;
            this.End.Before = new_node;
        } else {
            ListNode current = this.Start;
            for (int list_index = 0; list_index < this.Length; list_index++) {
                if (list_index == index) {
                    break;
                }
                current = current.Next;
            }
            ListNode new_node = new ListNode(value);
            current.Before.Next = new_node;
            new_node.Before = current.Before;
            new_node.Next = current;
            current.Before = new_node;
        }
        this.Length++;
    }

    public void Clear() {
        this.Start = null;
        this.End = null;
        this.Length = 0;
    }

    public Object Get(int index) {
        if (this.Length == 0 || this.Length <= index) {
            throw new IndexOutOfBoundsException("The list is empty or the index is out of range");
        }
        ListNode current = this.Start;
        for (int list_index = 0; list_index < this.Length; list_index++) {
            if (list_index == index) {
                return current.Value;
            }
            current = current.Next;
        }
        return null;
    }

    public void Append(Object value) {
        if (this.Length == 0) {
            this.End = new ListNode(value);
            this.Start = this.End;
        } else {
            ListNode old_end = this.End;
            this.End = new ListNode(value);
            old_end.Next = this.Start;
            this.End.Before = old_end;
        }
        this.Length++;
    }

    public void RemoveNode(ListNode node) {
        if (this.Length == 0) {
            throw new IndexOutOfBoundsException("The list is empty");
        }
        boolean found = false;
        if (this.Length == 1 && this.Start == node) {
            this.Start = null;
            this.End = null;
            found = true;
        } else {
            ListNode current = this.Start;
            for (int list_index = 0; list_index < this.Length; list_index++) {
                if (current == node) {
                    if (list_index == 0) {
                        this.Start = this.Start.Next;
                        this.Start.Before = null;
                    } else if (list_index == this.Length - 1) {
                        this.End = this.End.Before;
                        this.End.Next = Start;
                    } else {
                        current.Next.Before = current.Before;
                        current.Before.Next = current.Next;
                    }
                    found = true;
                    break;
                }
                current = current.Next;
            }
        }
        if (!found) {
            System.out.println("Node not found in the list");
        }
        this.Length--;
    }

    public void RemoveValue(Object value) {
        if (this.Length == 0) {
            throw new IndexOutOfBoundsException("The list is empty");
        }
        boolean found = false;
        if (this.Length == 1 && this.Start.Value == value) {
            this.Start = null;
            this.End = null;
            found = true;
        } else {
            ListNode current = this.Start;
            for (int list_index = 0; list_index < this.Length; list_index++) {
                if (current.Value == value) {
                    if (list_index == 0) {
                        this.Start = this.Start.Next;
                        this.Start.Before = null;
                    } else if (list_index == this.Length - 1) {
                        this.End = this.End.Before;
                        this.End.Next = Start;
                    } else {
                        current.Next.Before = current.Before;
                        current.Before.Next = current.Next;
                    }
                    found = true;
                    break;
                }
                current = current.Next;
            }
        }
        if (!found) {
            System.out.println("Value not found in the list");
        }
        this.Length--;
    }

    public void Remove(int index) {
        if (this.Length == 0 || this.Length <= index) {
            throw new IndexOutOfBoundsException("The list is empty or the index is out of range");
        }
        if (index == 0) {
            if (this.Length == 1) {
                this.Start = null;
                this.End = null;
            } else {
                this.Start = this.Start.Next;
                this.Start.Before = null;
            }
        } else if (index == this.Length - 1) {
            this.End = this.End.Before;
            this.End.Next = Start;
        } else {
            ListNode target = this.Start;
            for (int list_index = 0; list_index < this.Length; list_index++) {
                if (list_index == index) {
                    target.Before.Next = target.Next;
                    target.Next.Before = target.Before;
                    break;
                }
                target = target.Next;
            }
        }
        this.Length--;
    }

    public int Find(Object value) {
        if (this.Length == 0) {
            throw new IndexOutOfBoundsException("The list is empty");
        }
        ListNode current = this.Start;
        for (int list_index = 0; list_index < this.Length; list_index++) {
            if (current.Value == value) {
                return list_index;
            }
            current = current.Next;
        }
        return -1;
    }

    public boolean Contains(Object value) {
        return (this.Find(value) != -1);
    }

    public DoublyLinkedList SubList(int start, int end) {
        if (this.Length == 0) {
            throw new IndexOutOfBoundsException("The list is empty or the index is out of range");
        }
        if (start > end) {
            throw new IndexOutOfBoundsException("Start can't be greater than end");
        }
        if (end >= this.Length) {
            throw new IndexOutOfBoundsException("End can't be equal or greater to the list length");
        }
        ListNode current = this.Start;
        DoublyLinkedList result = new DoublyLinkedList();
        boolean appendIt = false;
        for (int list_index = 0; list_index < this.Length; list_index++) {
            if (list_index == start) {
                appendIt = true;
                result.Append(current.Value);
            } else if (list_index == end) {
                result.Append(current.Value);
                return result;
            } else if (appendIt) {
                result.Append(current.Value);
            }
            current = current.Next;
        }
        return null;
    }

    public Object[] ToArray() {
        if (this.Length == 0) {
            throw new IndexOutOfBoundsException("The list is empty");
        }
        Object[] array = new Object[this.Length];
        ListNode current = this.Start;
        for (int list_index = 0; list_index < this.Length; list_index++) {
            array[list_index] = current.Value;
            current = current.Next;
        }
        return array;
    }

    public ListNode GetBeforeTo(ListNode node) {
        return node.Before;
    }

    public ListNode GetNextTo(ListNode node) {
        return node.Next;
    }

    public DoublyLinkedList SubList(ListNode from, ListNode to) {
        if (this.Length == 0) {
            throw new IndexOutOfBoundsException("The list is empty");
        }
        DoublyLinkedList result = new DoublyLinkedList();
        ListNode current = from;
        while (current != to) {
            result.Append(current.Value);
            current = current.Next;
        }
        result.Append(to.Value);
        return result;
    }

    public boolean isEmpty() {
        return this.IsEmpty();
    }

    public int getSize() {
        return this.GetSize();
    }

    public void clear() {
        this.Clear();
    }

    public Object getHead() {
        return this.GetHead();
    }

    public Object getTail() {
        return this.GetTail();
    }

    public ListNode search(Object object) {
        return this.Search(object);
    }

    public boolean add(Object object) {
        return this.Add(object);
    }

    public boolean insert(ListNode node, Object object) {
        return this.Insert(node, object);
    }

    public boolean insert(Object ob, Object object) {
        return this.Insert(ob, object);
    }

    public boolean insertHead(Object object) {
        return this.InsertHead(object);
    }

    public boolean insertTail(Object object) {
        return this.InsertTail(object);
    }

    public boolean remove(ListNode node) {
        return this.Remove(node);
    }

    public boolean remove(Object object) {
        return this.Remove(object);
    }

    public boolean contains(Object object) {
        return this.Contains(object);
    }

    public Iterator<ListNode> iterator() {
        return this.Iterator();
    }

    public Object[] toArray() {
        return this.ToArray();
    }

    public Object[] toArray(Object[] object) {
        return this.ToArray();
    }

    public Object getBeforeTo() {
        return this.GetBeforeTo(this.End);
    }

    public ListNode getBeforeTo(ListNode node) {
        return this.GetBeforeTo(node);
    }

    public Object getNextTo() {
        return this.GetNextTo(this.Start);
    }

    public Object getNextTo(ListNode node) {
        return this.GetNextTo(node);
    }

    public DoublyLinkedList subList(ListNode from, ListNode to) {
        return this.SubList(from, to);
    }

    public DoublyLinkedList sortList() {
        return null;
    }
}
