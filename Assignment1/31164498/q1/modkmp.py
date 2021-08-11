import sys
from typing import List

def read_file(txt_file,pat_file):
    with open (txt_file,"r",encoding="utf-8") as f:
        txt=f.read()
    with open(pat_file,"r",encoding="utf-8") as f:
        pat=f.read()
    return txt,pat

def write_tofile(occurences:List[int]):
    with open("output_modkmp.txt","w",encoding="utf-8") as f:
        if not occurences:
            f.close()
            return
        f.write(str(occurences[0]+1))
        for i in range(1,len(occurences)):
            f.write("\n")
            f.write(str(occurences[i]+1))


def kmp_mod(pattern,text):
    return []


if __name__=="__main__":
    txt_file=sys.argv[1]
    pat_file=sys.argv[2]
    text,pattern=read_file(txt_file,pat_file)
    occurences=kmp_mod("pattern","text")

    write_tofile(occurences)



