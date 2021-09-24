from math import inf, log2

"""
Name: Amos Choo Jia Shern
ID: 31164498

"""

class Node:
    def __init__(self, key, distance=None) -> None:
        self.key = key
        self.distance = distance  # data
        self.degree = 0  # how many children
        self.mark = False  # node marked?
        self.parent = None  # parent of node - only one per node
        # any one children - so can traverse other children through their siblings
        self.children = None
        self.left = self  # left sibling
        self.right = self  # right sibling
    

class FibHeap:
    """
    Initialise Fibonacci Heap


    """

    def __init__(self, node=None) -> None:
        self.minimum = node  # minimum node stored here
        # maintain total number of nodes in heap
        self.total_nodes = 0 if node is None else 1

    def is_empty(self):
        return self.total_nodes == 0

    def get_min(self):
        """
        Look at minimum at the heap

        """
        if self.minimum is None:
            raise ValueError("No node found")
        return self.minimum
    
    def merge(self, heap):
        """
        Merge two Fh

        Code referenced and adapted from FIT3155 lecture notes(Taylor) Week 6 pg6

        """

        self.get_min().left.right = heap.get_min().right
        heap.get_min().right.left = self.get_min().left
        heap.get_min().right = self.get_min()
        self.get_min().left = heap.get_min()

        if self.get_min().distance > heap.get_min().distance:
            self.minimum = heap.get_min()

    def insert(self, node: Node):
        """
        Insert a node into the heap


        """

        if self.minimum is None:  # no min, empty heap so set directly
            self.minimum = node
            self.total_nodes += 1
        else:
            new_heap = FibHeap(node)
            new_heap.minimum = node
            self.merge(new_heap)
            self.total_nodes += 1

    
        # # merge a node with the doubly linked root list


    
    def extract_min(self):

        minimum = self.minimum
        if minimum.children is not None:
            end= minimum.children.left #end at children left
            node=minimum.children
            temp_right=node.right

            while True: #go through all children siblings and merge them into the root
                temp_right=node.right
                next_left=node
                self.merge_to_root(node)
                node.parent = None
                node = temp_right
                if next_left is end:
                    break

        minimum.left.right = minimum.right #connect left sibling to right sibling vice versa
        minimum.right.left = minimum.left

        
        self.total_nodes -= 1 # old minimum no longer at the heap, decrement them, and find new min

        if minimum is minimum.right: #since its linking to itself, if right sibling also the same node,
            #means no more minimum
            self.minimum= None

        else:
            self.minimum = minimum.right #set temp min to the right
        if self.minimum is not None: 
            self.consolidate() #only consolidate when at least one node at heap, otherwise math error
        return minimum


    def merge_to_root(self, node:Node):

        """
        Merge a node into the root,
        extract min and for cutting usage

        Code adapted and modified from FIT3155 lecture notes Week 6 (Taylor) pg6
        
        """
        self.get_min().left.right = node
        node.left = self.get_min().left
        node.right = self.get_min()
        self.get_min().left = node
    

    def consolidate(self):

        degree_array = [None] * (int(log2((self.total_nodes))+2)) #+2 for zero based indexing

        node = self.get_min()
        end = node.left

        while True: #consolidate along the root

            deg = node.degree
            next = node.right
            next_left = next.left
            while degree_array[deg] is not None:  # make sure only one deg per heap

                if degree_array[deg].distance>node.distance:
                    node = self.merge_node_into_parent(node, degree_array[deg]) #merge to increase degree
                else:
                    node = self.merge_node_into_parent(degree_array[deg], node) #merge to increase

                degree_array[deg] = None
                deg += 1 #go to next degree

            # node either by merging or ori go into the degree
            degree_array[deg] = node

            if node.distance <= self.get_min().distance:  # if found new minimum update self.minimum
                self.minimum = node
            node = next  # move to right sibling
            if next_left is end:  # finish interating through all nodes at root
                break


    def merge_node_into_parent(self, parent: Node, node: Node):
        """
        Merge node into parent, for consolidate purpose

        """

        # Node no longer connected with its sibling vice versa
        # remove the middle node bwtween the sibling

        if node is self.minimum: #if node is minimum, move minimum to the right
            self.minimum=node.right

        #Severe sibling links, link back to itself    
        node.left.right = node.right
        node.right.left = node.left
        node.left = node
        node.right = node

        if parent.children is None:
            parent.children = node

        else:

            # Connect the node to the children by adjusting the links
            # Code adapted and modified from FIT3155 lecture notes(Taylor) Week 6
            parent.children.left.right = node
            node.left = parent.children.left
            node.right = parent.children
            parent.children.left = node

        parent.degree += 1  # parent degree increase by 1
        node.parent = parent
        node.mark = False #unmark them
        return parent



    def decrease_key(self, node:Node, val):
        """
        
        Decrease key given a new value
        """
 
        parent = node.parent
        if parent is None or parent.distance <= val:  # still maintain property leave it - Case 1
            node.distance = val
        
        else:
            if not parent.mark:
                self.unlink_node_and_parent(parent,node)  # if parent is unmarked -- Case 2A
                self.promote_and_unmark(node)
                parent.mark = True
                parent.degree -= 1
                node.distance = val
            else:
                node.distance=val
                while True: #Case 2B - cascading cut -> keep cutting until find unmarked/reach root
                    self.unlink_node_and_parent(parent,node)
                    self.promote_and_unmark(node)
                    parent.degree -= 1

                    if not parent.mark:
                        parent.mark=True
                        break
                    elif parent.parent is None:
                        break
                    node=parent
                    parent=node.parent

        if val < self.minimum.distance:
            self.minimum = node

    def unlink_node_and_parent(self, parent, node):
        """
        Unlink node and parent, used at cutting

        """

        if parent.children is parent.children.right: #if children its own sibling, means no more child since its self linking
            parent.children = None

        elif parent.children is node: #if directly at children, give to right sibling of children
            parent.children = node.right
            node.right.parent = parent

        #connect left to right each other
        node.left.right = node.right
        node.right.left = node.left


    def promote_and_unmark(self,node):
        """
        Promote to root, and unmark it

        """
        self.merge_to_root(node)
        node.parent=None
        node.mark=False
 
    def delete(self, node):
        """
        Not needed, not tested, leaving it for potential future use
        
        """
        self.decrease_key(node, -inf)
        self.extract_min()
