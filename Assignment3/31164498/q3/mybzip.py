from bitarray import bitarray
from fibonaccicodeq3 import fib_encode
import sys
from huffman import encode_huffman


class Node:
    def __init__(self,char,freq) -> None:
        self.char=char
        self.freq=freq

    
    def __lt__(self,other):
        if self.freq==other.freq:
            return len(self.char)<len(other.char)
        else:
            return self.freq<other.freq



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
    


def find_character_freq(text:str):
    """
    Change to list instead dict

    """
    nodes=[]
    table=[0]*(127-36)
    for char in text:
        table[ord(char)-36]+=1
    for c in range(len(table)):
        if table[c]!=0:
            nodes.append(Node(chr(c+36),table[c]))
    return nodes

def encode_bwt(text:str):
    length=len(text)
    binary_stream=[]
    length_encode=fib_encode(length)
    if length<=1:
        return length_encode
    else:
        binary_stream.append(length_encode)
        nodes=find_character_freq(text)
        uniq_chars=len(nodes)
        uniq_chars_encode=fib_encode(uniq_chars)
        binary_stream.append(uniq_chars_encode)


        char_encodings=[]
        huffman_encodings=encode_huffman(text,nodes)
        for node in nodes:
            c=node.char
            char_encodings.append(format(ord(c),"07b"))
            encode_length=len(huffman_encodings[ord(c)-36])
            char_encodings.append(fib_encode(encode_length))
            char_encodings.append(huffman_encodings[ord(c)-36])
        binary_stream.append("".join(char_encodings))
        binary_stream.append(run_length_encoding(text,huffman_encodings))
        binary_string="".join(binary_stream)
        return binary_string

def output_to_bin(binary_string):
    with open("encodedBWT.bin","wb") as f:
        stream=bitarray(binary_string)
        stream.tofile(f)




if __name__=="__main__":
    bwt=sys.argv[1]
    bin_string=encode_bwt(bwt)
    output_to_bin(bin_string)