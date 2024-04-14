from list.listNode import ListNode

class LinkedListBasic:
    def __init__(self): 
        self.__head = ListNode('dummy', None)
        self.__numItems = 0

    def insert(self, i, newItem):
        if i>0 and i<=self.__numItems:
            prev =  self.__getNode(i-1)
            newNode = ListNode(newItem, prev.next)
            prev.next = newNode
            self.__numItems += 1

        elif i == 0 and i <= self.__numItems: 
            prev = self.__head
            newNode = ListNode(newItem, prev.next)
            prev.next = newNode
            self.__numItems += 1

    def __getNode(self, i):
        curr = self.__head
        for index in range(i+1):
            curr = curr.next
        return curr

    def append(self, newItem):
        prev = self.__getNode(self.__numItems - 1)
        newNode = ListNode(newItem, prev.next)
        prev.next = newNode
        self.__numItems += 1

    def pop(self, i):
        if(i>=0 and i<=self.__numItems-1):
            prev = self.__getNode(i - 1)
            curr = prev.next
            prev.next = curr.next
            self.__numItems -= 1
        else:
            return None

    def remove(self, x):    #x node 삭제
        (prev, curr) = self.__findeNode(x)
        prev.next = curr.next
        self.__numItems -= 1

    def __findNode(self, x):  #node x 찾기
        prev = self.__head
        curr = prev.next
        while curr != None:
            if curr.item == x:
                return (prev, curr)
            else: 
                prev = curr
                curr = curr.next
        return (None, None)
    
    def get(self, i): #i번 원소 알려주기 
        if self.isEmpty(): 
            return None
        if(i>=0 and i<self.__numItems):
            return self.__getNode(i).item
        else:
            return None
        
    