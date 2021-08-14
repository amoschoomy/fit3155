import sys
from typing import List

def read_file(txt_file,pat_file):
    """
    Read file
    
    """
    with open (txt_file,"r",encoding="utf-8") as f:
        txt=f.read()
    with open(pat_file,"r",encoding="utf-8") as f:
        pat=f.read()
    return txt,pat

def write_tofile(occurences:List[int]):
    """
    Write to file
    """
    with open("output_modkmp.txt","w",encoding="utf-8") as f:
        if not occurences:
            f.close()
            return
        f.write(str(occurences[0]+1))
        for i in range(1,len(occurences)):
            f.write("\n")
            f.write(str(occurences[i]+1))

def zalgo(word:str):
    """
    Z-algorithm for pattern matching
    Generate and return zarray

    Time Complexity: O(len(word))

    
    """
    zarray=[0]*len(word)

    zarray[0]=len(word) #first position holds no info
    left,right=0,0
    for i in range(1,len(word)):

        #Case 1: explicit comparison
        if i>right:
            count=explicit_comparison(word,i,0) #start from i
            if count>0:
                #update count
                zarray[i]=count
                left=i
                right=i+count-1
        else: #Case 2, inside z box
            k=i-left
            remaining=right-i+1
            #Case 2a, value of previous zbox lesseer than remaining
            if zarray[k]<remaining:
                zarray[i]=zarray[k] #use the previous zbox value

            #Case 2b
            elif zarray[k]>remaining:
                zarray[i]=remaining

            else: #zarray[k]==remaining: Case 2c, need to explicit compare
                count=explicit_comparison(word,right+1,remaining) #start from right+1
                zarray[i]=zarray[k]+count
                if count>0:
                    right=remaining-1
                    left=i
    return zarray

def explicit_comparison(pattern,start1,start2):
    """
    Explicit comparison
    given two indexes
    
    """
    count=0
    for i in range(start1,len(pattern)):
        if pattern[i]!=pattern[start2]:
            break
        start2+=1
        count+=1
    return count

def shared_prefix(pattern,zarray):
    """
    Shared prefix array
    Algorithm from Lecture notes

    """
    m=len(pattern)
    sp=[0]*m
    for j in range(m-1,0,-1):
        i=j+zarray[j]-1
        sp[i]=zarray[j]
    return sp

def spix(pattern,zarray):
    """
    spix matrix
    
    """

    m=len(pattern)
    matrix=[[0 for i in range(m)] for j in range(256)]
    for j in range(m-1,0,-1):
        i=j+zarray[j]-1
        x=zarray[j]+1 #mismatch position
        if x<m:
            matrix[ord(pattern[x])][i]=zarray[j]
    return matrix

    


def kmp_mod(pattern,text):
    """
    
    Modded kmp to use SPi(x) when a mismatch occurs
    Time complexity: O(m+n)
    """
    zarray=zalgo(pattern)
    sp=shared_prefix(pattern,zarray)#preprocess
    spix_array=spix(pattern,zarray)

    i=0
    n=len(text)
    m=len(pattern)
    matches=[]
    resume=0
    while i+m<=n:
        j=0
        mismatch=False

        while j<m:
            if pattern[j]!=text[i+j]: #explicit comparison from position i+j and i
                mismatch=True
                break


            elif j<resume: #galil optimsiation, skip comparison till resume
                j=resume
                print("activated galil")
            j+=1


        if not mismatch: #if full match happens
            matches.append(i)
            shift=m-sp[m-1] #shift according to the formula
            print(shift,"full pattern shift")


        else: #mismatch happens
            if j==0: #at first position, move by one
                shift=1
            else:
                # shift=j-sp[j] # replace with spix
                shift=j-spix_array[ord(text[i+j])][j]
                if shift>1: 
                    resume=spix_array[ord(text[i+j])][j] #move resume
                print("modshift",shift)
            # print(shift,"mismatch shift")
        i+=max(shift,1)
        print("new i",i)
    return matches


if __name__=="__main__":

    # txt_file=sys.argv[1]
    # pat_file=sys.argv[2]
    # text,pattern=read_file(txt_file,pat_file)
    # occurences=kmp_mod(pattern,text)
    pass
    # write_tofile(occurences)
    # print(kmp_mod("abba","bbaababaababbababbaabba"))
    # print(kmp_mod("ooo","oolloloolloolooolooooool"))
    print(kmp_mod("moo","oommmoomomommomoommoo"))
    print(zalgo("dadax"))


print(ord(" "))
