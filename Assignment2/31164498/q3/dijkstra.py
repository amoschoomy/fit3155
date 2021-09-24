from fibonacci_heap import FibHeap,Node
from math import inf
import sys

"""
Name: Amos Choo Jia Shern
ID: 31164498

"""

class Edge:
    """
    Edge class

    """
    def __init__(self,u:int,v:int,w:float) -> None:

        """
        Init method

        Big O Time Complexity: O(1)
        Aux Space Complexity: O(1)
        """
        #access vertex through vertex id
        self.u=u
        self.v=v
        self.weight=w
    
    def __str__(self) -> str:

        return "("+str(self.u)+","+str(self.v)+")"+", Weight: "+str(self.weight)

class Vertex:
    """
    Vertex class
    """
    def __init__(self,val) -> None:
        """
        Init method

        Big O Time Complexity: O(1)
        Aux Space Complexity: O(1)
        """
        self.id=val
        self.edges=[]
        self.visited=False
        self.node=None

    def add_edge(self,edge:Edge):
        """
        
        add edge object to edges list
        
        Init method

        Big O Time Complexity: O(1)
        Aux Space Complexity: O(1)
        
        """

        self.edges.append(edge)


    def __str__(self) -> str:

        res=str(self.id)
        for edge in self.edges:
            res+=" Edges: "+str(edge)
        return res



class Graph:
    """
    Graph class
    """
    def __init__(self,no_vertices:int,directed=True) -> None:

        """
        Init method, default is a directed graph

        Big O Time Complexity: O(V) whre V is the number of vertices in graph
        Aux Space Complexity: O(V) where V is the number of vertices in graph

        """
        self.vertices=[Vertex(i)for i in range(no_vertices)] #Adjacency list representation
        self.edges_in_graph=[]
        self.no_vertices=no_vertices
        self.directed=directed

    
    def add_edge_to_graph(self,edge:Edge):
        """
        Add Edge object to graph

        Big O Time Complexity: O(1)
        Aux Space Complexity: O(1)

        """
        current_vertex=self.vertices[edge.u]
        current_vertex.add_edge(edge)
        self.edges_in_graph.append(edge)
        

        #if not directed, swap the edge u and v and add it
        if not self.directed:
            current_vertex=self.vertices[edge.v]
            reversed_edge=Edge(edge.v,edge.u,edge.weight)
            current_vertex.add_edge(reversed_edge)
            self.edges_in_graph.append(reversed_edge)
    
    def add_vertex_to_graph(self):
        """
        Add vertex to graph

        Big O Time Complexity: O(1)
        Aux Space Complexity: O(1)
        """
        self.vertices.append(Vertex(len(self.vertices)))

    def reset_visits(self):
        """
        Reset visit status in the graph

        Big O Time Complexity: O(V)
        Aux Space Complexity: O(1)
        """
        for vertex in self.vertices:
            vertex.visited=False
    
    def __str__(self) -> str:


        res=""
        for vertice in self.vertices:
            res+="Vertex: "+str(vertice)+"\n"
        return res




def djikstra(graph:Graph,source:int):
    """
   
   Dijkstra algorithm using Fibonacci heap

    """


    #Initialisation of min heap, predeccesor array and distance arrray along with the source value
    fib_heap=FibHeap()
    distance=[inf]*graph.no_vertices
    distance[source]=0
    # pred=[-1]*graph.no_vertices


    #Add into fib heap
    for vertex_id in range(len(graph.vertices)):
        node=Node(vertex_id,distance[vertex_id])
        graph.vertices[vertex_id].node=node
        fib_heap.insert(node)


    
    while not fib_heap.is_empty():
        node=fib_heap.extract_min()
        vertex=graph.vertices[node.key]
        vertex.visited=True

        #Relax adjacent edges of the popped vertex
        for edge in vertex.edges:
            vertex_v=graph.vertices[edge.v]
            weight=edge.weight
            #Only vertex are not visited will be seen
            if not vertex_v.visited:
                if distance[edge.u]+weight<distance[edge.v]:
                    distance[edge.v]=distance[edge.u]+weight
                    # pred[edge.v]=edge.u
                    v_node=vertex_v.node
                    fib_heap.decrease_key(v_node,distance[edge.u]+weight) #update the new heap index position
                   
    return distance

def compute(no_vertice,lst_of_edges):
    """
    Run djikstra given lst of edges
    """
    graph=Graph(no_vertice,False)
    for edge in lst_of_edges:
        graph.add_edge_to_graph(edge)
    distance=djikstra(graph,0)
    return distance

def read_file(graph_file):
    
    with open(graph_file,"r",encoding="UTF-8") as f:
        no_vertice,no_of_edges=f.readline().split(" ")
        no_of_edges=int(no_of_edges)
        no_vertice=int(no_vertice)
        edges=[]
        for _ in range(no_of_edges):
            u,v,w=f.readline().split(" ")
            u,v,w=int(u),int(v),int(w)
            edges.append(Edge(u,v,w))
        return no_vertice,edges

def write_tofile(distance):
    with open("output_dijkstra.txt","w",encoding="UTF-8") as f:
        f.write("0 0")
        for i in range(1,len(distance)):
            f.write("\n")
            f.write("{vertex} {distance}".format(vertex=i,distance=distance[i]))


if __name__=="__main__":
    g=sys.argv[1]
    v,e=read_file(g)
    distance=compute(v,e)
    write_tofile(distance)
