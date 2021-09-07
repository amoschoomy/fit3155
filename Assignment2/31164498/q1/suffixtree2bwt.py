import sys
from typing import List, Text

"""
Name: Amos Choo Jia Shern
ID: 31164498

"""

from ukkonen import SuffixTree,Node

def read_file(txt_file):
    """
    Read file
    
    """
    with open (txt_file,"r",encoding="utf-8") as f:
        txt=f.read()
    return txt

def write_tofile(bwt:str):
    """
    Write to file
    """
    with open("output_bwt.txt","w",encoding="utf-8") as f:
        f.write(bwt)

def bwt(text:str):
    st=SuffixTree(Node(),text)
    st.build()
    suffix_array=st.build_suffix_array()
    print(suffix_array)
    print(len(suffix_array))
    print(text)
    result=[None]*(len(text))
    for i in range(len(text)):
        # print(suffix_array[i])
        if suffix_array[i]==0:
            result[i]="$"
        else:
            result[i]=text[suffix_array[i]-1]
        print(result[i])
    print(result)
    return result




if __name__=="__main__":
    txt_file=sys.argv[1]
    txt=read_file(txt_file)
    bwt(txt)

        