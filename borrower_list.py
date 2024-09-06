#Define BorrowerNode with next and prev pointer(References)
class BorrowerNode:
    def __init__(self, borrower):
        self.borrower = borrower
        self.next = None #Reference of next node
        self.prev = None #Reference of prev node
        
#Head and tail of the linked list(pseudo head and tail)
class BorrowerList:
    def __init__(self):
        self.head = None
        self.tail = None
    
    #Add node at the tail of linked list
    def append(self, borrower):
        new_node = BorrowerNode(borrower)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
    
    #Find node and return a borrower by username in linked list
    def find(self, username):
        current = self.head
        while current:
            if current.borrower.username == username:
                return current.borrower
            current = current.next
        return None
    
    #Delete node by username in linked list. Return true if deleted, false if not found
    def delete(self, username):
        current = self.head
        while current:
            if current.borrower.username == username:
                if current.prev:
                    current.prev.next = current.next
                if current.next:
                    current.next.prev = current.prev
                if current == self.head:
                    self.head = current.next
                if current == self.tail:
                    self.tail = current.prev
                return True
            current = current.next
        return False
    
    #Iterate over the borrowers in the linked list
    def __iter__(self):
        current = self.head
        while current:
            yield current.borrower
            current = current.next