from bitarray import bitarray
import sys
from fibonaccicodeq3 import fib_decode
from huffman import HuffmanTree


"""
Amos Choo Jia Shern
31164998

"""

def retrieve_bitstring(bin_file):
    with open(bin_file,"rb") as f:
        x=bitarray()
        bitarray.fromfile(x,f)
    return x

def decode_bit(barray):

    bit_ptr=0 #use a pointer to iterate through bitarray
    fl=[1,2] #fibonacci list

    bwt_length,bit_ptr=fib_decode(barray,bit_ptr,fl) #decode bwt length and return the new pointer

    if bwt_length==1: #empty string case
        return ""

    uniq_char,bit_ptr=fib_decode(barray,bit_ptr,fl) #decode uniq char and return the new pointer

    tree=HuffmanTree() #huffman tree to decode huffman encoding

    for _ in range(uniq_char):
        asc_chr=""
        for i in range(7):
            asc_chr+=str(barray[bit_ptr+i]) #ascii decoding of char
        char=chr(int(asc_chr,2))
        bit_ptr+=7

        code_length,bit_ptr=fib_decode(barray,bit_ptr,fl) #decode the code length of huffman
        tree.add_code(barray,bit_ptr,code_length,char) #add the code to tree
        bit_ptr+=code_length

    result=[]

    total_length=0
    while total_length<bwt_length: #decode run length encoding by traversing the tree
        char,bit_ptr=tree.traverse(barray,bit_ptr) #get that char from tree
        run_length,bit_ptr=fib_decode(barray,bit_ptr,fl) #get the runlength
        total_length+=run_length
        for _ in range(run_length): #append run lengths of char
            result.append(char)
    return "".join(result)

def write_to_file(bwt:str):
    with open("decodedBWT.txt","w",encoding="UTF-8") as f:
        f.write(bwt)

if __name__=="__main__":
    bf=sys.argv[1]
    x=retrieve_bitstring(bf)
    bwt_string=decode_bit(x)
    write_to_file(bwt_string)

