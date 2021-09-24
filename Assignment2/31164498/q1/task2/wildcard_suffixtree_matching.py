import sys
from typing import List
from ukkonen import SuffixTree,Node,Edge

"""
Name: Amos Choo Jia Shern
ID: 31164498

"""


def read_file(txt_file,pat_file):
    """
    Read file
    
    """
    with open (txt_file,"r",encoding="utf-8") as f:
        txt=f.read()
    with open (pat_file,"r",encoding="utf-8") as f:
        pat=f.read()
    return txt,pat

def write_tofile(occurences:List[int]):
    """
    Write to file
    """
    with open("output_wildcard_matching.txt","w",encoding="utf-8") as f:
        if not occurences:
            f.close()
            return
        #This line of code is referenced from 
        # https://monash.au.panopto.com/Panopto/Pages/Viewer.aspx?id=c11e7654-565b-415b-a7d9-ad7f0090bc75&start=0    
        f.write(str(occurences[0]+1))
        for i in range(1,len(occurences)):
            f.write("\n")
            f.write(str(occurences[i]+1))





def pattern_find(pattern:str,word:str):
    """
    
    Find pattern using suffix tree
    
    
    """
    word+="$"
    suffix_tree=SuffixTree(Node(),word)
    suffix_tree.build()
    nodes=[]
    root=suffix_tree.root
    word=suffix_tree.word
    aux_pattern_find(pattern,root,None,0,-1,word,nodes)
    occurences=[]
    for node in nodes:
        suffix_tree.inorder(node,occurences) #inorder traversal -> code in ukkonen file
    return occurences
    
def aux_pattern_find(pattern:str,node:Node,edge:Edge,i:int,count:int,word:str,nodes:List):

    #base case, pattern done matching
    if i==len(pattern):
        if edge is not None and i<edge.get_end():
            node=edge.node
        nodes.append(node)

    else:

        if pattern[i]!="?" and edge is None: #not a wild card and not inside an edge -> enter an edge
            edge=node.edges[ord(pattern[i])-36]
            if edge is not None:
                if edge.start+1>edge.get_end(): # exceeded edge end, so dont traverse insinde the edge anymore and go to edge node
                    aux_pattern_find(pattern,edge.node,None,i+1,-1,word,nodes)
                else:
                    aux_pattern_find(pattern,node,edge,i+1,edge.start+1,word,nodes)


        elif pattern[i]=="?" and edge is None: #wildcard match, traverse through all edges from the node, only happen when it is exactly at the node

            for k in range(127-36):
                if node.edges[k] is not None:
                    if node.edges[k].start+1>node.edges[k].get_end():
                        aux_pattern_find(pattern,node.edges[k].node,None,i+1,-1,word,nodes)
                    else:
                        aux_pattern_find(pattern,node,node.edges[k],i+1,node.edges[k].start+1,word,nodes)


        elif edge is not None: #if pattern matching happen in between edges
            if pattern[i]==word[count] or pattern[i]=="?": #continue traverse the edge
                if count>=edge.get_end(): #if reached the end, go to next node
                    node=edge.node
                    edge=None
                    aux_pattern_find(pattern,node,edge,i+1,-1,word,nodes)
                else:
                    aux_pattern_find(pattern,node,edge,i+1,count+1,word,nodes)
            
if __name__=="__main__":
    txt_file=sys.argv[1]
    pattern_file=sys.argv[2]
    txt,pattern=read_file(txt_file,pattern_file)
    occurences=pattern_find(pattern,txt)
    write_tofile(occurences)





            
