from bitarray import bitarray
from fibonaccicodeq3 import fib_encode
import sys
from huffman import encode_huffman,Node


def run_length_encoding(text:str,huffman_encodings:list,fl:list):
    """
    Given huffman encodings list, and text, perform run length encoding
    
    """
    run_length=1
    encode_string=[]    
    for i in range(1,len(text)):
        if text[i]==text[i-1]:
            run_length+=1
            if i==len(text)-1: #last char so need to add to encoding
                order=ord(text[i-1])-36
                encode_string.append(huffman_encodings[order]) #append the huffman encodings to the string
                rle=fib_encode(run_length,fl)
                encode_string.append(rle) #append the run length as fib_encode
        else:
            #run length end, so append the huffman encodigs and the run length
            order=ord(text[i-1])-36
            encode_string.append(huffman_encodings[order])
            rle=fib_encode(run_length,fl)
            encode_string.append(rle)
            run_length=1
    return "".join(encode_string)
    


def find_character_freq(text:str):
    
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

    binary_stream=[] #bitstream to be outputted
    fl=[1,2] #fibonacci list

    length_encode=fib_encode(length,fl)

    #if empty string, only encode length
    if length<=1:
        return length_encode
    else:
        binary_stream.append(length_encode)

        nodes=find_character_freq(text)
        uniq_chars=len(nodes)
        uniq_chars_encode=fib_encode(uniq_chars,fl) #encode number of uniq char

        binary_stream.append(uniq_chars_encode)


        char_encodings=[] #encodings of the character of bwt
        huffman_encodings=encode_huffman(text,nodes) #create huffman list

        for node in nodes:
            c=node.char
            char_encodings.append(format(ord(c),"07b")) #ascii encoding
            encode_length=len(huffman_encodings[ord(c)-36]) # length of huffman encoding of char

            char_encodings.append(fib_encode(encode_length,fl)) #encoded legnth of huffman
            char_encodings.append(huffman_encodings[ord(c)-36]) #encode the actual huffman encoding

        binary_stream.append("".join(char_encodings))

        binary_stream.append(run_length_encoding(text,huffman_encodings,fl)) #append the run length encoding 
        return "".join(binary_stream)

def output_to_bin(binary_string):
    
    with open("encodedBWT.bin","wb") as f:
        stream=bitarray(binary_string)
        stream.tofile(f)




if __name__=="__main__":
    bwt=sys.argv[1]
    bin_string=encode_bwt(bwt)
    output_to_bin(bin_string)