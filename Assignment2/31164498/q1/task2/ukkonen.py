from typing import List


"""
Name: Amos Choo Jia Shern
ID: 31164498

"""

class End:  # global end variable // only use em at ukkonen leaf
    def __init__(self) -> None:
        self.end = -1  # start from -1, as it increments at the start of every

    def increment(self):
        self.end += 1

    def get(self):
        return self.end


class Edge:
    def __init__(self, node, start, end) -> None:
        self.start = start
        self.end = end
        self.node = node  # edge linking to which node?

    def get_end(self):
        if isinstance(self.end, End):
            return self.end.get()
        else:
            return self.end


class Node:
    def __init__(self) -> None:
        self.edges = [None]*(127-36)  # to traverse the tree
        self.suffix_link = None  # suffix link, set to root after creation
        self.id = None  # suffix id, only at leaf

    def add_suffix_id(self, index):
        self.id = index  # add suffix id

    def add_edge(self, char, edge: Edge):
        # Add or Replace edges
        # If None == add
        # If got already == replace
        self.edges[ord(char)-36] = edge


class Active:
    # Active class
    def __init__(self, root: Node) -> None:
        self.node = root
        self.length = -1  # length -1 == traverse directly from active node
        self.edge = None


class SuffixTree:
    def __init__(self, root, word) -> None:
        self.root = root
        self.word = word

    def build(self):  # build suffix tree
        ukkonen(self.root, self.word)

    def build_suffix_array(self):
        suffix_array = []
        self.inorder(self.root, suffix_array)
        return suffix_array

    def inorder(self, node: Node, store_id: List):
        """
        Inorder traversal yields suffix array

        """
        if node.id is not None:
            store_id.append(node.id)
        else:
            for i in range(127-36):
                if node.edges[i] is not None:
                    self.inorder(node.edges[i].node, store_id)


def ukkonen(root: Node, pattern: str):
    """
    O(N) complete Ukkonen algorithm
    2 passes maximum needed to compute Suffix Tree

    4 tricks , 3 rules

    Rule 1 supplemented by a leave always a leave

    Traverse a tree use skip count trick and suffix link in O(1) time

    Rule 2 is branching 
    Rule 3 is do nothing -- converted to showstopper trick




    """
    i, j = 0, 0
    root.suffix_link = root
    end = End()
    active = Active(root)
    n = len(pattern)
    while i < n:
        previous_node = None  # reset previous node at every new phase i
        end.increment()  # increment global end

        while j <= i:

            # Calc traversal steps from active edge if possibe
            if active.edge is not None:
                skip_count = active.edge.start+active.length+1
            else:
                skip_count = active.length

            # Perform traversal from active node directly
            if active.length == -1 and active.node.edges[ord(pattern[i])-36] is None:

                if active.node.edges[ord(pattern[i])-36] is None:
                    # Do a rule 2 extension
                    new_node = Node()
                    new_edge = Edge(new_node, i, end)
                    active.node.add_edge(pattern[i], new_edge)
                    new_node.add_suffix_id(j)

                    if i == j:  # move both pointers and start new phase
                        i += 1
                        j += 1
                        break
                    else:
                        j += 1
                        # Follow suffix link
                        # Do not change active length if follow suffix link
                        if active.node is not root:
                            active.node = active.node.suffix_link
                            active.edge = active.node.edges[ord(pattern[j])-36]

                            if active.edge is not None:
                                # Move to edge according to remaining suffix length if possible
                                if i-j > (active.edge.get_end()-active.edge.start):
                                    active.node = active.edge.node
                                    active.edge = active.node.edges[ord(
                                        pattern[i])-36]

            # Inside active edge, so compare using skip count
            elif (pattern[i] != pattern[skip_count] and active.length > -1 and active.edge is not None):

                # Rule 2 extension branching
                start = active.edge.start
                new_node = Node()  # create new intermediate node
                new_node.suffix_link = root  # every intermediate suffix link ==root
                active.edge.start = skip_count  # change active edge start
                # new node now connect to active edge instead
                new_node.add_edge(pattern[active.edge.start], active.edge)
                # new edge that will link to new node
                new_edge = Edge(new_node, start, start+active.length)
                # active node now connected to new node using new edge
                active.node.add_edge(pattern[start], new_edge)

                # A branch will also be created at index [i,end]
                new_branch_node = Node()
                new_branch_node.add_suffix_id(j)
                new_branch_edge = Edge(new_branch_node, i, end)
                new_node.add_edge(pattern[i], new_branch_edge)

                if previous_node is None:  # same phahse, if no previous internal node, make it the previous now
                    previous_node = new_node
                else:
                    previous_node.suffix_link = new_node
                    previous_node = new_node

                j += 1

                if active.node is not root:  # Follow suffix link and do not decrement active length

                    active.node = active.node.suffix_link

                    if active.node is not root:
                        active.edge = active.node.edges[ord(pattern[start])-36]
                    else:
                        # Track active edge location from root, move to new node from
                        # remaining suffixes length if possible
                        active.edge = active.node.edges[ord(pattern[j])-36]
                        if active.edge is not None:
                            if i-j > (active.edge.get_end()-active.edge.start):
                                active.node = active.edge.node
                                active.edge = active.node.edges[ord(
                                    pattern[j+1])-36]

                    # Move active node and active edge if already exceed end of current of active edge
                    if active.edge is not None:
                        if active.length >= (active.edge.get_end()-active.edge.start):
                            active.node = active.edge.node
                            active.length -= (active.edge.get_end() -
                                              active.edge.start+1)
                            active.edge = active.node.edges[ord(
                                pattern[j+1])-36]

                else:  # If active node is root, decrement it and go to new Active edge

                    active.length -= 1
                    active.edge = active.node.edges[ord(pattern[j])-36]

                    if active.edge is not None:
                        # if active length exceeded, go to new active node
                        if active.length >= (active.edge.get_end()-active.edge.start):
                            active.node = active.edge.node
                            val = (active.edge.get_end()-active.edge.start+1)
                            active.length -= val
                            active.edge = active.node.edges[ord(
                                pattern[j+1])-36]
            else:
                # rule 3 showstopper, increment i, start new phase immediately
                i += 1
                active.length += 1
                if active.edge is None:
                    active.edge = active.node.edges[ord(pattern[j])-36]

                if active.edge is not None:
                    # Move to new node, if exceeded end of active edge
                    if active.length >= (active.edge.get_end()-active.edge.start):
                        active.node = active.edge.node
                        active.length -= (active.edge.get_end() -
                                          active.edge.start+1)
                        active.edge = active.node.edges[ord(pattern[i])-36]
                break
