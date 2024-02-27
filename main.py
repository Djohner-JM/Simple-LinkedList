from dataclasses import dataclass
from typing import ClassVar, TypeVar, NoReturn, Self


@dataclass
class Llist:
    TNode = TypeVar("TNode", bound="_Node")
    
    @dataclass
    class _Node:
        _value : int|str|None = None
        _next_node : Self|None = None

    INDEX_MSG : ClassVar[str] = "L'index est en dehors de la liste"
    EMPTY_MSG : ClassVar[str] = "La liste est vide"
    _tail : TNode|None = None
    _head : TNode|None = None
    _length : int = 0
        
    def _is_empty(self, error:int|bool|None=None) -> NoReturn|bool:
        if error is None: return self._length == 0
        if self._length == 0: raise IndexError(Llist.EMPTY_MSG) if type(error) is int else ValueError(Llist.EMPTY_MSG)
        else: return None
        
    def _is_overflow(self, index:int) -> NoReturn|None:
        if not (0 <= index < self._length): 
            raise ValueError(Llist.INDEX_MSG)
        
    def append(self, elem_to_append:int|str) -> None:
        """Permet d'ajouter un élément à la fin de la liste"""
        
        node = self._Node(elem_to_append)

        if self._is_empty():
            self._head = self._tail = node
        else:
            self._tail._next_node = self._tail = node
            
        self._length += 1
        
    def insert(self, index:int, elem_to_insert:int|str) -> None:
        """insère l'élement "elem_to_insert" à l'index "index" donné"""
        self._is_empty(index)
        self._is_overflow(index)
            
        def recursion_insert(node=self._head, recursion_index=0):
            if recursion_index == index:
                node._next_node, node._value, =self._Node(node._value, node._next_node), elem_to_insert
                return 
            recursion_insert(node._next_node, recursion_index + 1)
            
        if index == self._length - 1:
            self._tail._next_node, self._tail._value = self._Node(self._tail._value), elem_to_insert
            self._tail = self._tail._next_node
        else: 
            recursion_insert()
            
        self._length += 1
    
    def remove(self, elem_to_remove:int|str) -> None:
        """Retire un élément de valeur donnée s'il existe"""
        self.remove_at(self.index_of(elem_to_remove)) if not self._is_empty() else ...
            
    def remove_at(self, index:int) -> None:
        """Retire un élément à l'index donnée"""
        self._is_empty(index)
        self._is_overflow(index)
        
        def recursion_remove_at(node=self._head, recursion_index=0):
            if recursion_index == index:
                node._next_node = node._next_node._next_node
                return 
            return recursion_remove_at(node._next_node, recursion_index + 1)
        
        if index < 0:
            self._is_overflow(abs(index) - 1)
            index = self._length + index
        else:
            recursion_remove_at()
            
        self._length -= 1
    
    def at_index(self, index:int) -> int|str:
        """Renvoie la valeur à l'index donné"""
        self._is_empty(index)
        
        def recursion_at_index(node=self._head, recursion_index=0):
            if index == recursion_index:
                return node._value
            return recursion_at_index(node._next_node, recursion_index + 1)
        
        
        if index < 0:
            index = self._length + index 
            
        self._is_overflow(index)
        
        if index == self._length - 1:
            return self._tail._value
            
        return recursion_at_index()
    
    def index_of(self, elem:int|str) -> int:
        """
        Renvoie l'index du premier élément rencontré
        -1 si elem n'est pas présent dans la liste
        """
        self._is_empty(False)
        
        def recursion_index_of(node=self._head, index=0):
            if node._value == elem:
                return index
            next_node = node._next_node
            return recursion_index_of(next_node, index + 1) if next_node else -1
        
        return recursion_index_of()
            
    def is_unique(self) -> bool:
        """Vérifie que la liste ne contient pas de doublons"""
        self._is_empty(False)
        
        def recursion_is_unique(node=self._head, value_list=[]):
            if not node:
                return True
            else:
                if node._value in value_list:
                    return False
                value_list.append(node._value)
                return recursion_is_unique(node._next_node, value_list)
        
            
        if self._head == self._tail and self._length > 1: return False
        else : return recursion_is_unique()
                    
    def reversed(self) -> None:
        """Inverse la liste"""
        self._is_empty(False)

        def recursion_reversed(node=self._head, previous=None):
            if not node:
                self._head, self._tail = self._tail, self._head
                return
            node._next_node, previous, node = previous, node, node._next_node
            recursion_reversed(node, previous)
            
        recursion_reversed()
  
    def contains(self, elem:int|str) -> bool:
        """Vérifie que elem est présent dans la liste"""
        return self._tail == elem or self.index_of(elem) >= 0
    
    def transform_list(self) -> list:
        def recursion_transform_list(node=self._head, list_value=[]):
            if not node:
                return list_value
            list_value.append(node._value)
            return recursion_transform_list(node._next_node, list_value)
        
        return recursion_transform_list()
        
    def __len__(self) -> int:
        return self._length
    
    def __str__(self) -> str:
        return f"{self.transform_list()}" 
     
    
if __name__ == "__main__":
    llist = Llist()
    print(llist) # []

    llist.append(3)
    llist.append(10)
    llist.append(30)
    print(len(llist)) # 3
    print(llist) # [3, 10, 30]

    llist.insert(1, 50)
    print(llist) # [3, 50, 10, 30]

    llist.remove_at(0)
    print(llist) # [50, 10, 30]

    print(llist.contains(10)) # True
    print(llist.contains(87)) # False

    print(llist.index_of(10)) # 1
    print(llist.index_of(87)) # -1

    print(llist.at_index(1)) # 10
    print(llist.at_index(-2)) # 10

    print(llist.is_unique()) # True
    llist.append(50)
    print(llist) # [50, 10, 30, 50]
    print(llist.is_unique()) # False

    llist.append(20)
    llist.append(100)
    llist.append(80)
    print(llist) # [50, 10, 30, 50, 20, 100, 80]
    print(llist._head._value)
    print(llist._tail._value)
    llist.reversed()
    print(llist) # [80, 100, 20, 50, 30, 10, 50]
    print(llist._head._value)
    print(llist._tail._value)
    print(llist._tail._next_node)