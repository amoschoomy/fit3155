from heapq import heappush,heappop,heapify
class Node:
    def __init__(self,char,freq) -> None:
        self.char=char
        self.freq=freq
        self.left=None
        self.right=None

    
    def __lt__(self,other):
        if self.freq==other.freq:
            return len(self.char)<len(other.char)
        else:
            return self.freq<other.freq

def reverse_huffman(huffman_encodings):
    for e in range(len(huffman_encodings)):
        if len(huffman_encodings[e])!=0:
            huffman_encodings[e]="".join(huffman_encodings[e][::-1])
    return huffman_encodings

def encode_huffman(text:str,node_list):


    heapify(node_list)
    encoding=[[] for _ in range(127-36)] 
    
    while len(node_list)>1: #ensure two pops are done
        node1=heappop(node_list)
        node2=heappop(node_list)
        new_node=Node(node1.char+node2.char,node1.freq+node2.freq)
        for c in node1.char:
            node1ord=ord(c)-36
            encoding[node1ord].append("0")
        for c in node2.char:
            node2ord=ord(c)-36
            encoding[node2ord].append("1")
        heappush(node_list,new_node)
    
    encoding=reverse_huffman(encoding)
    return encoding