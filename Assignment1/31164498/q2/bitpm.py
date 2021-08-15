import sys
from typing import List



"""
Name: Amos Choo Jia Shern
ID: 31164498

"""


def read_file(txt_file,pat_file):
    """
    Read file function

    """
    with open (txt_file,"r",encoding="utf-8") as f:
        txt=f.read()
    with open(pat_file,"r",encoding="utf-8") as f:
        pat=f.read()
    return txt,pat

def write_tofile(occurences:List[int]):
    """
    Write to file function
    """
    with open("output_bitpm.txt","w",encoding="utf-8") as f:
        if not occurences:
            f.close()
            return
        #This line of code is referenced from 
        # https://monash.au.panopto.com/Panopto/Pages/Viewer.aspx?id=c11e7654-565b-415b-a7d9-ad7f0090bc75&start=0    
        f.write(str(occurences[0]+1))
        for i in range(1,len(occurences)):
            f.write("\n")
            f.write(str(occurences[i]+1))


def delta_array(pattern):
    """
    
    Precompute delta vector
    for each character in printable ascci
    Time complexity: O(len(pattern))

    
    """
    m=len(pattern)
    delta=[2**m-1]*(126-32) #2**m-1 == upper limit of bit length m:: in binary it means 1111....1

    #Now for each character in pattern, flip the bits to zero according to the position
    # in the delta array
    for i in range(m-1,-1,-1): #NOTE: go backwards as shown in example in pdf, but it should work going upwards too
        order=ord(pattern[i])-32 
        n=delta[order] 
        delta[order]=n^(1<<i) #flip the bits at ith position
   
    return delta

def bitvectors(pattern,text,delta):
    """
    Pre compute bitvectors for each position in the text

    Time complexity: O(len(text))

    
    """
    vectors=[]
    m=len(pattern)
    vector=2**m-1 # we can make an observation for bitvector 0, it will have no pattern prefix aligned
    # with the text, except for the LSB of the vector
    # So in binary it will be 11111....1111 initallly


    #So this is why we check first char of pattern and text
    #Which corrosponds to LSB of bitvector 0
    #and flip it if theres a match

    if pattern[0]==text[0]: #bitvector of 0
        vector=vector^(1<<0) 
    vectors.append(vector)

    #Now we have bit vector 0, we can just compute all of them
    # in O(1) using the formula
    #NOTE: Not sure we can skip computing bitvector 0 and jump
    #      to the first alignment of len(pattern) with text
    #      But safety purposes, just did
    for i in range(1,len(text)):
        order=ord(text[i])-32
        next_vector=((vector<<1)|delta[order])%2**m
        vectors.append(next_vector)
        vector=next_vector
    return vectors

def bitpm(pattern,text):
    """
    Actual bit pattern matching algo

    Time complexity: O(len(text)-len(pattern)-1)
    
    """
    #Preprocess
    d_array=delta_array(pattern)
    bitvector_list=bitvectors(pattern,text,d_array)


    result=[]
    m=len(pattern)
    # here i skip to len(pattern)-1, there wont be
    # full matches before the alignment anyway
    for i in range(len(pattern)-1,len(text)): 
        bitvector=bitvector_list[i]
        if bitvector<=((2**m)/2)-1: #if less than half, means ==zero==full match
            result.append(i-m+1)
    return result



if __name__=="__main__":
    txt_file=sys.argv[1]
    pat_file=sys.argv[2]
    text,pattern=read_file(txt_file,pat_file)
    occurences=bitpm(pattern,text)

    write_tofile(occurences)
    