from typing import List


class End: #global end variable // only use em at ukkonen leaf
    def __init__(self) -> None:
        self.end=-1 #start from -1, as it increments at the start of every
    
    def increment(self):
        self.end+=1
    def get(self):
        return self.end


class Edge:
    def __init__(self,node,start,end) -> None:
        self.start=start
        self.end=end
        self.node=node #edge linking to which node?
    
    def get_end(self):
        if isinstance(self.end,End):
            return self.end.get()
        else:
            return self.end



class Node:
    def __init__(self) -> None:
        self.edges=[None]*256 #to traverse the tree
        self.suffix_link=None#suffix link, set to root after creation
        self.id=None #suffix id, only at leaf
    
    def add_suffix_id(self,index):
        self.id=index #add suffix id
    
    def add_edge(self,char,edge:Edge):
        # Add or Replace edges
        # If None == add
        # If got already == replace
        self.edges[ord(char)]=edge
    

class Active:
    #Active class
    def __init__(self,root:Node) -> None:
        self.node=root 
        self.length=0 # length 0 == traverse directly from active node
        self.edge=None


class SuffixTree:
    def __init__(self,root,word) -> None:
        self.root=root
        self.word=word
    
    def build(self): #build suffix tree
        ukkonen(self.root,self.word)
    
    def traverse(self):
        #IN order traversal?? maybe
        suffix_array=[]
        self.inorder(self.root,suffix_array)
        print(suffix_array)
    
    def inorder(self,node:Node,suffix_array:List):
        if node.id is not None:
            suffix_array.append(node.id)
        else:
            for i in range(256):
                if node.edges[i] is not None:
                    self.inorder(node.edges[i].node,suffix_array)






def ukkonen(root:Node,pattern:str):
    """
    O(N) complete Ukkonen algorithm
    2 passes maximum needed to compute Suffix Tree

    4 tricks , 3 rules

    Rule 1 supplemented by a leave always a leave

    Traverse a tree use skip count trick and suffix link in O(1) time

    Rule 2 is branching 
    Rule 3 is do nothing -- converted to showstopper trick


    
    
    """
    i,j=0,0
    pattern+="$" #add terminal
    n=len(pattern)
    end=End() #end class
    active=Active(root) #active class, active node at start always root
    while i<n:
        previous_node=None #reset previous node at every new phase i
        end.increment() # increment global end
        
        while j<=i: # add suffixes to tree from j...i
        

            #Calculate skip count val 
            if active.edge is not None:
                skip_count=active.edge.start+active.length
            else:
                skip_count=active.length

            #Do extension directly from the active node - enabled by active length 0
            if (active.node is root or active.node.edges[ord(pattern[i])] is None) and (active.length==0):

                if active.node.edges[ord(pattern[i])] is None:
                    #rule 2 extension
                    new_node=Node()
                    new_edge=Edge(new_node,j,end)
                    active.node.add_edge(pattern[i],new_edge)
                    new_node.add_suffix_id(j)

                    if i==j: #move both pointers and start new phase
                        i+=1
                        j+=1
                        break
                    else:

                        j+=1 #stay in same phase

                        #Follow suffix link
                        #Do not change active length if follow suffix link
                        if active.node is not root:
                            active.node=active.node.suffix_link
                            if active.edge is not None:
                                active.edge=active.node.edges[ord(pattern[active.edge.start])] #new Active edge will follow the char of the old active edge 
                        else: #if at root, decrement active length, change active edge
                            active.length-=1
                            active.edge=active.node.edges[ord(pattern[j])]
                        
                else:
                    #rule 3 showstopper, increment active length, move to new phase
                    i+=1
                    active.edge=active.node.edges[ord(pattern[j])]
                    active.length+=1 

                    # move active node and edge if active length exceeded the maximum end of the current active edge
                    if active.length>active.edge.get_end():
                        active.length=0
                        active.node=active.edge.node
                        active.edge=active.node.edges[ord(pattern[i])]
                    break    


            elif (pattern[i]!=pattern[skip_count] and active.length!=0): #using skip count instead to compare, enaled by active length present>0
                #Mismatch found

                start=active.edge.start #start of active edge

                    
                if skip_count==active.edge.get_end(): 
                    #if reached the end edge of that node, branch and create a new node
                    #new node will be at terminal
                    new_node=Node()
                    new_edge=Edge(new_node,j,end)
                    active.node.add_edge(pattern[i],new_edge)
                    new_node.add_suffix_id(j)  

                else: 
                    # iF in between edges
                    new_node=Node() #create new intermediate node
                    new_node.suffix_link=root #every intermediate suffix link ==root
                    active.edge.start=skip_count #change active edge start -- to be skip count
                    new_node.add_edge(pattern[active.edge.start],active.edge) #new node now connect to active edge instead
                    new_edge=Edge(new_node,start,start+active.length-1) #new edge that will link to new node
                    active.node.add_edge(pattern[start],new_edge) #active node now connected to new node using new edge

                    #A branch will also be created at index [i,end]
                    new_branch_node=Node()
                    new_branch_node.add_suffix_id(j)
                    new_branch_edge=Edge(new_branch_node,i,end)
                    new_node.add_edge(pattern[i],new_branch_edge)

                    if previous_node is None: #same phahse, if no previous internal node, make it the previous now
                        previous_node=new_node
                    else:
                        previous_node.suffix_link=new_node
                        previous_node=new_node 

                #Finish doing extension        
                if i==j:
                    i+=1
                    j+=1
                    if active.length!=0:
                        active.length-=1
                    active.edge=active.node.edges[ord(pattern[j])]
                    break

                else:
                    j+=1

                    if active.node is not root: #Follow suffix link and do not decrement active length
                        
                        active.node=active.node.suffix_link
                        active.edge=active.node.edges[ord(pattern[start])]

                        #Move active node and active edge if already exceed end of current of active edge
                        if active.length>active.edge.get_end():
                            active.node=active.edge.node
                            active.length=0
                            active.edge=active.node.edges[ord(pattern[i])]

                    else:

                        active.length-=1
                        active.edge=active.node.edges[ord(pattern[j])]

                        if active.edge is not None:
                            if active.length>active.edge.get_end():
                                active.node=active.edge.node
                                active.length=0
                                active.edge=active.node.edges[ord(pattern[i])]

            else:
                #rule 3 showstopper, increment i, start new phase immediately
                i+=1
                if active.edge is  None:
                    active.edge=active.node.edges[ord(pattern[j])]
                active.length+=1
                if active.length>active.edge.get_end():
                    active.length=0
                    active.node=active.edge.node
                    active.edge=active.node.edges[ord(pattern[i])]

                break
    return root #optional? maybe since we doing in class
     
st=SuffixTree(Node(),"abcabxabcyab")
st.build()
st.traverse()
