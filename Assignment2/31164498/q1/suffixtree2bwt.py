import sys
from typing import List

"""
Name: Amos Choo Jia Shern
ID: 31164498

"""

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

if __name__=="__main__":
    txt_file=sys.argv[1]
    txt=read_file(txt_file)
    print(txt)

        