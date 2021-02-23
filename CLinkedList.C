#include <iostream>
using namespace std;

class ListNode
{

public:
    ListNode *next;

    int object;
};

class Lista
{
public:
    Lista();

    void clear();

    bool isEmpty();

    int getSize();

    int getHead() const;

    int getTail();

    bool add(ListNode** head_ref, int new_data);

    bool removeHead();

    bool removeTail();

    bool insert(ListNode node, int object);

    bool insert(int ob, int object);

    bool insertHead(int object);

    bool insertTail(int object);

    void printList() const;

    bool contains(int object);

    ListNode getBeforeTo();

    ListNode getBeforeTo(ListNode node);

    int getNextTo();

    int getNextTo(ListNode node);

    ~Lista();

private:
    ListNode *head;
    ListNode *tail;
    int size = 0;
};

int main()
{

    return 0;
}

Lista ::Lista()
{
    clear();
}

void Lista ::clear()
{
    head = NULL;
    tail = NULL;
    size = 0;
}

bool Lista ::isEmpty()
{
    return head == NULL;
}

int Lista ::getSize()
{
    return size;
}

int Lista ::getHead() const
{
    return head->object;
}

int Lista ::getTail()
{
    return tail->object;
}

bool Lista ::add(ListNode** head_ref, int new_data)
{
    ListNode *inode = new ListNode(); 
  
    ListNode *tail = *head_ref; 
    inode->object = new_data;  
  
   
    inode->next = NULL;  
  
    
    if (*head_ref == NULL)  
    {  
        *head_ref = inode;  
        return;  
    }  
  
    while (tail->next != NULL)  
        tail = tail->next;  
  
  
    tail->next = inode;  
    return;  
}

bool Lista ::removeHead()
{
    ListNode *inode = head->next;
    delete head;

    head = inode;
}

bool Lista ::removeTail()
{
    ListNode *inode =  tail->next;
    delete tail;

    tail = inode;
}

bool Lista ::insert(ListNode node, int object)
{
}

bool Lista ::insert(int ob, int object)
{
}

bool Lista ::insertHead(int object)
{
    ListNode *pnt = new ListNode;
    pnt->object = object;
    pnt->next = head;

    head = pnt;
    return true;
}

bool Lista ::insertTail(int object)
{
    if (isEmpty())
    {
        ListNode *pnt = new ListNode;
        pnt->object = object;
        pnt->next = head;

        head = pnt;
    }
    else
    {
        ListNode(object) = tail->next;
        tail = tail->next;
    }
    size++;
    return true;
}

void Lista ::printList() const
{
    ListNode *inode =head;
    while(inode != NULL){
        cout << inode ->object<< " ";
        inode = inode  ->next;
    }

}

Lista ::~Lista()
{
    while (head != NULL)
    removeHead();

}
