from heapq import heapify,heappush,heappop
from bitarray import bitarray
from fibonaccicodeq3 import fib_encode

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
    
    encoding=reverse_huffman(encoding)
    return encoding

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


def run_length_encoding(text:str,huffman_encodings:list):
    run_length=1
    encode_string=[]
    for i in range(1,len(text)):
        if text[i]==text[i-1]:
            run_length+=1
            if i==len(text)-1:
                order=ord(text[i-1])-36
                encode_string.append(huffman_encodings[order])
                rle=fib_encode(run_length)
                encode_string.append(rle)
        else:
            order=ord(text[i-1])-36
            encode_string.append(huffman_encodings[order])
            rle=fib_encode(run_length)
            encode_string.append(rle)
            run_length=1
    return "".join(encode_string)
    

def reverse_huffman(huffman_encodings):
    for e in range(len(huffman_encodings)):
        huffman_encodings[e]="".join(huffman_encodings[e][::-1])
    return huffman_encodings


def encode_bwt(text:str):
    length=len(text)
    binary_stream=[]
    length_encode=fib_encode(length)
    binary_stream.append(length_encode)
    nodes=find_character_freq(text)
    uniq_chars=len(nodes)
    uniq_chars_encode=fib_encode(uniq_chars)
    binary_stream.append(uniq_chars_encode)


    char_encodings=[]
    huffman_encodings=encode_huffman(text)
    for node in nodes:
        c=node.char
        char_encodings.append(format(ord(c),"0b"))
        encode_length=len(huffman_encodings[ord(c)-36])
        char_encodings.append(fib_encode(encode_length))
        char_encodings.append(huffman_encodings[ord(c)-36])
    binary_stream.append("".join(char_encodings))
    binary_stream.append(run_length_encoding(text,huffman_encodings))
    binary_string="".join(binary_stream)
    output_to_bin(binary_string)

def output_to_bin(binary_string):
    with open("encodedBWT.bin","wb") as f:
        stream=bitarray(binary_string)
        stream.tofile(f)



# with open("dx.bin","wb") as f:
#     x=bitarray("10")
#     y=bitarray("11101011")
#     x.tofile(f)
#     y.tofile(f)
if __name__=="__main__":
    encode_bwt("b$aaaaaaaaaa")