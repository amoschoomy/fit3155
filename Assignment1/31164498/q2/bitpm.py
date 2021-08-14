import sys
from typing import List




def read_file(txt_file,pat_file):
    with open (txt_file,"r",encoding="utf-8") as f:
        txt=f.read()
    with open(pat_file,"r",encoding="utf-8") as f:
        pat=f.read()
    return txt,pat

def write_tofile(occurences:List[int]):
    with open("output_bitpm.txt","w",encoding="utf-8") as f:
        if not occurences:
            f.close()
            return
        f.write(str(occurences[0]+1))
        for i in range(1,len(occurences)):
            f.write("\n")
            f.write(str(occurences[i]+1))


def delta_array(pattern):
    m=len(pattern)
    delta=[2**m-1]*(126-32)
    for i in range(m-1,-1,-1):
        order=ord(pattern[i])-32
        n=delta[order]
        delta[order]=n^(1<<i)
   
    return delta

def bitvectors(pattern,text,delta):
    vectors=[]
    m=len(pattern)
    vector=2**m-1
    if pattern[0]==text[0]: #bitvector of 0
        vector=vector^(1<<0)
    vectors.append(vector)

    for i in range(1,len(text)):
        order=ord(text[i])-32
        next_vector=((vector<<1)|delta[order])%2**m
        vectors.append(next_vector)
        vector=next_vector
    return vectors

def bitpm(pattern,text):
    d_array=delta_array(pattern)
    bitvector_list=bitvectors(pattern,text,d_array)
    result=[]
    m=len(pattern)
    for i in range(len(pattern)-1,len(text)):
        bitvector=bitvector_list[i]
        if bitvector<=((2**m)/2)-1: #if less than half, means ==zero
            result.append(i-m+1)
    return result



if __name__=="__main__":
    # txt_file=sys.argv[1]
    # pat_file=sys.argv[2]
    # text,pattern=read_file(txt_file,pat_file)
    # occurences=boyer_bitwise("pattern","text")

    # write_tofile(occurences)
    pass