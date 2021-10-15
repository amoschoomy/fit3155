from bitarray import bitarray
from fibonaccicodeq3 import fib_encode
import sys
from huffman import encode_huffman,Node



"""
Amos Choo Jia Shern
31164998

"""

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
                if run_length>fl[-1]:
                    rle,fl=fib_encode(run_length,fl)
                else:
                    rle,fl=fib_encode(run_length)
                encode_string.append(rle) #append the run length as fib_encode
        else:
            #run length end, so append the huffman encodigs and the run length
            order=ord(text[i-1])-36
            encode_string.append(huffman_encodings[order])
            if run_length>fl[-1]:
                rle,fl=fib_encode(run_length,fl)
            else:
                rle,fl=fib_encode(run_length)
            encode_string.append(rle)
            run_length=1

            if i==len(text)-1: #last char so need to add last char to encoding also
                order=ord(text[i])-36
                encode_string.append(huffman_encodings[order]) #append the huffman encodings to the string
                if run_length>fl[-1]:
                    rle,fl=fib_encode(run_length,fl)
                else:
                    rle,fl=fib_encode(run_length)
                encode_string.append(rle) #append the run length as fib_encode
    return "".join(encode_string),fl
    


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


    #If fibonacci largest val in list exceeds the value to encode, need to redo fibonacci again,
    #since encoding depend on length of the fibonacci list, same process is repeated for all fib encoding you see later
    if length>fl[-1]:
        length_encode,fl=fib_encode(length,fl)
    else:
        length_encode,fl=fib_encode(length)

    #if empty string, only encode length
    if length<=1:
        return length_encode
    else:
        binary_stream.append(length_encode)
        nodes=find_character_freq(text)
        uniq_chars=len(nodes)
        if uniq_chars>fl[-1]:
            uniq_chars_encode,fl=fib_encode(uniq_chars,fl)
        else:
            uniq_chars_encode,fl=fib_encode(uniq_chars) #encode number of uniq char
        binary_stream.append(uniq_chars_encode)

        copy_nodes=nodes[:]
        char_encodings=[] #encodings of the character of bwt
        huffman_encodings=encode_huffman(text,copy_nodes) #create huffman list

        for node in nodes:
            c=node.char
            char_encodings.append(format(ord(c),"07b")) #ascii encoding
            encode_length=len(huffman_encodings[ord(c)-36]) # length of huffman encoding of char
            if encode_length>fl[-1]:
                c_encode,fl=fib_encode(encode_length,fl)
            else:
                c_encode,fl=fib_encode(encode_length)
            char_encodings.append(c_encode) #encoded legnth of huffman
            char_encodings.append(huffman_encodings[ord(c)-36]) #encode the actual huffman encoding

        binary_stream.append("".join(char_encodings))
        rle_string,fl=run_length_encoding(text,huffman_encodings,fl)
        binary_stream.append(rle_string) #append the run length encoding 
        return "".join(binary_stream)

def output_to_bin(binary_string):
    
    with open("encodedBWT.bin","wb") as f:
        stream=bitarray(binary_string)
        stream.tofile(f)




if __name__=="__main__":
    bwt=sys.argv[1]
    bin_string=encode_bwt(bwt)
    output_to_bin(bin_string)
