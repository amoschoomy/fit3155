from bitarray import bitarray
import sys
from fibonaccicodeq3 import fib_decode
from huffman import HuffmanTree


#NOTE: Optimise fibonacci encoding to not recompute fibonacci every time

def retrieve_bitstring(bin_file):
    with open(bin_file,"rb") as f:
        x=bitarray()
        bitarray.fromfile(x,f)
    return x

def decode_bit(barray):
    bit_ptr=0
    fl=[1,2]
    bwt_length,bit_ptr=fib_decode(barray,bit_ptr,fl)
    uniq_char,bit_ptr=fib_decode(barray,bit_ptr,fl)
    tree=HuffmanTree()
    for _ in range(uniq_char):
        asc_chr=""
        for i in range(7):
            asc_chr+=str(barray[bit_ptr+i])
        char=chr(int(asc_chr,2))
        bit_ptr+=7
        code_length,bit_ptr=fib_decode(barray,bit_ptr,fl)
        tree.add_code(barray,bit_ptr,code_length,char)
        bit_ptr+=code_length
    result=[]

    total_length=0
    while total_length<bwt_length:
        char,bit_ptr=tree.traverse(barray,bit_ptr)
        run_length,bit_ptr=fib_decode(barray,bit_ptr,fl)
        total_length+=run_length
        for _ in range(run_length):
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