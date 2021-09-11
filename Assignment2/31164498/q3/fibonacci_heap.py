from math import inf, log


class Node:
    def __init__(self, key, distance=None) -> None:
        self.key = key
        self.vertex = None
        self.distance = distance  # data
        self.degree = 0  # how many children
        self.mark = False  # node marked?
        self.parent = None  # parent of node - only one per node
        # any one children - so can traverse other children through their siblings
        self.children = None
        self.left_sibling = self  # left sibling
        self.right_sibling = self  # right sibling


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

        self.get_min().left_sibling.right_sibling = heap.get_min().right_sibling
        heap.get_min().right_sibling.left_sibling = self.get_min().left_sibling
        heap.get_min().right_sibling = self.get_min()
        self.get_min().left_sibling = heap.get_min()

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

    def merge_node_into_root(self, node: Node):
        """
        Merge node into root , same thing as merging heap above but specific
        to node only without changing minimum

        Code referenced and adapted from FIT3155 lecture notes(Taylor) Week 6 pg6


        """
        if self.minimum is None:
            self.minimum = node
        else:
            self.get_min().left_sibling.right_sibling = node.right_sibling
            node.right_sibling.left_sibling = self.get_min().left_sibling
            node.right_sibling = self.get_min()
            self.get_min().left_sibling = node

    def merge_node_into_parent(self, parent: Node, node: Node):
        """
        Merge node into parent

        """

        # Node no longer connected with its sibling vice versa
        # remove the middle node bwtween the sibling
        node.left_sibling.right_sibling = node.right_sibling
        # remove the millde node between the sibling
        node.right_sibling.left_sibling = node.left_sibling
        node.left_sibling = node
        node.right_sibling = node

        if parent.children is None:
            parent.children = node
        else:
            # Connect the node to the children by adjusting the links
            # Code referenced and adapted from FIT3155 lecture notes(Taylor) Week 6 pg6
            node.left_sibling.right_sibling = parent.children.right_sibling
            parent.children.right_sibling.left_sibling = node.left_sibling
            parent.children.right_sibling = node
            node.left_sibling = parent.children

        parent.degree += 1  # parent degree increase by 1
        node.parent = parent
        node.mark = False
        return parent

    def extract_min(self):
        minimum_element = self.get_min()

        # Remove sibling links to and from the minimum element
        ls = minimum_element.left_sibling
        rs = minimum_element.right_sibling
        ls.right_sibling = rs
        rs.left_sibling = ls

        # if min sibling point to itself == no more min when removed
        if minimum_element is minimum_element.right_sibling:
            self.minimum = None
        else:
            self.minimum = rs  # set temp minimum to right sibling first

        # link to itself
        minimum_element.left_sibling = minimum_element
        minimum_element.right_sibling = minimum_element

        self.total_nodes -= 1  # Node no longer in the heap, decrease them

        if minimum_element.children is not None:  # only touch children if there exists

            children = minimum_element.children
            end = children.left_sibling

            # merge all children into root
            while True:
                next = children.right_sibling
                next_left = next.left_sibling
                children.parent = None
                self.merge_node_into_root(children)
                children = next
                if next_left is end:
                    break

        if self.minimum is not None:
            self.consolidate()  # only consolidate the heap if exists minimum element
        return minimum_element

    def consolidate(self):
        # +2 because 0 indexing
        degree_array = [None]*int(log(self.total_nodes)+2)
        node = self.get_min()
        end = node.left_sibling
        while True:
            if node.distance < self.get_min().distance:  # if found new minimum update self.minimum
                self.minimum = node
            deg = node.degree
            next = node.right_sibling
            next_left = next.left_sibling
            while degree_array[deg] is not None:  # make sure only one deg per heap
                if degree_array[deg].distance > node.distance:
                    # do that by increasing degree eg b0+b0=b1
                    node = self.merge_node_into_parent(node, degree_array[deg])
                else:
                    # do that by increasing degree eg b0+b0=b1
                    node = self.merge_node_into_parent(degree_array[deg], node)
                degree_array[deg] = None
                deg += 1
            # node either by merging or ori go into the degree
            degree_array[deg] = node
            node = next  # move to right sibling
            if next_left is end:  # finish interating through all children
                break

    def cut(self, node: Node):
        """
        Cut the links of the node and merge to root

        """

        node.left_sibling.right_sibling = node.right_sibling  # remove node from sibling
        node.right_sibling.left_sibling = node.left_sibling  # remove node from sibling
        node.right_sibling = node
        node.left_sibling = node
        self.merge_node_into_root(node)
        node.parent = None
        node.mark = False

    def decrease_key(self, node: Node, val):
        """
        Decreaase key of the node given node and val

        """
        parent = node.parent
        if parent is None or parent.distance < val:  # still maintain property leave it - Case 1
            node.distance = val

        else:
            if not parent.mark:  # if parent is unmarked -- Case 2A
                if parent.children is parent.children.right_sibling:
                    parent.children = None
                elif parent.children is node:
                    parent.children = node.right_sibling
                    node.right_sibling.parent = parent

                self.cut(node)
                parent.mark = True
                parent.degree -= 1
                node.distance = val

            else:  # if parent is marked, do cascading cut until reached root, or no more parent is marked
                # Case 2B
                while parent.mark and parent.parent is not None:
                    if parent.children is parent.children.right_sibling:
                        parent.children = None
                    elif parent.children is node:
                        parent.children = node.right_sibling
                        node.right_sibling.parent = parent
                    self.cut(node)
                    parent.degree -= 1
                    node = parent
                    parent = parent.parent
                node.distance = val
        if val < self.minimum.distance:
            self.minimum = node

    def delete(self, node):
        self.decrease_key(node, -inf)
        self.extract_min()