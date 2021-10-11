from heapq import heapify,heappush,heappop
from bitarray import bitarray
class Node:
    def __init__(self,char,freq) -> None:
        self.char=char
        self.freq=freq

    
    def __lt__(self,other):
        if self.freq==other.freq:
            return len(self.char)<len(other.char)
        else:
            return self.freq<other.freq


def encode_huffman(text:str):


    node_list=find_character_freq(text)
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

    return encoding #NOTE: need to reverse when output to stream

def find_character_freq(text:str):
    """
    Change to list instead dict

    """
    nodes=[]
    table=dict()
    for char in text:
        if not table.get(char):
            table[char]=1
        else:
            table[char]+=1
    for key in table:
        nodes.append(Node(key,table[key]))
    return nodes


def encode_bwt(text:str):
    length=len(text)
    
    
# print(encode_huffman("b$aaaaaaaaaa"))


# # print(bitarray(chr("a")))
# print(bin(ord("a")))
# bitarray(97)
   