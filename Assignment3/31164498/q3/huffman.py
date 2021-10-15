from heapq import heappush,heappop,heapify



"""
Amos Choo Jia Shern
31164998

"""

class HuffmanTree():
    def __init__(self) -> None:
        self.root=Node()
    
    def add_code(self,bits,ptr,length,char):
        """
        Add huffman code to the tree by traversing the tree
        
        """

        current=self.root
        
        for i in range(ptr,ptr+length): #ptr+length cos we pass in the whole bitarray

            bit=bits[i]
            if bit==0:
                if current.left is None:
                    current.left=Node()
                    current=current.left
                else:
                    current=current.left

                #if finish the bitstring, add a char to the node    
                if i==(ptr+length-1):
                    if current is None:
                        current=Node()
                    current.char=char

            else: #Right sided node for bit 1
                if current.right is None:
                    current.right=Node()
                    current=current.right
                else:
                    current=current.right

                if i==(ptr+length-1):
                    if current is None:
                        current=Node()
                    current.char=char


    def traverse(self,bits,ptr):
        """
        Traverse the tree following the bits until you get a char at a node
        
        """
        current=self.root
        for i in range(ptr,len(bits)):
            if current.char is not None:
                return current.char,i
            else:
                if bits[i]==1:
                    current=current.right
                else:
                    current=current.left


class Node:
    def __init__(self,char=None,freq=None) -> None:
        self.char=char
        self.freq=freq
        self.left=None
        self.right=None

    
    def __lt__(self,other): #comparator for min heap
        if self.freq==other.freq:
            return len(self.char)<len(other.char) #if same freq, priortise the least length
        else:
            return self.freq<other.freq


def reverse_huffman(huffman_encodings):
    """
    O(1) append so need to O(n) reverse, take the opportunity to convert into string too
    """
    for e in range(len(huffman_encodings)):
        if len(huffman_encodings[e])!=0:
            huffman_encodings[e]="".join(huffman_encodings[e][::-1])
    return huffman_encodings

def encode_huffman(text:str,node_list):

    """
    Convert nodes into huffman list
    """
    heapify(node_list) #convert into heap the node list
    encoding=[[] for _ in range(127-36)] 
    
    while len(node_list)>1: #ensure two pops are done
        node1=heappop(node_list)
        node2=heappop(node_list)
        new_node=Node(node1.char+node2.char,node1.freq+node2.freq)

        for c in node1.char: #append to the encoding of the char for each char in the node
            node1ord=ord(c)-36
            encoding[node1ord].append("0")
        for c in node2.char:
            node2ord=ord(c)-36
            encoding[node2ord].append("1")
        heappush(node_list,new_node)
    
    encoding=reverse_huffman(encoding) #reverse the encoding before return
    return encoding