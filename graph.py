class Nodel:
    def __init__(self, value):#Stores a Node object in its value attribute, has next attribute to be implemented into the queue for BFS
        self.value = value  
        self.next = None 
    
    def __str__(self):
        return "Node({})".format(self.value) 

    __repr__ = __str__

class Queue:#Basic Queue used for BFS
  def __init__(self):
      self.head=None
      self.tail=None
      self.map=[]

  def __str__(self):
      temp=self.head
      out=[]
      while temp:
          out.append(str(temp.value))
          temp=temp.next
      out=' -> '.join(out)
      return f'Head:{self.head}\nTail:{self.tail}\nQueue:{out}'

  __repr__=__str__

  def isEmpty(self):
      if self.head==None:
          return True
      return False

  def replace(self,value):
    if self.isEmpty():
      self.head=value
      self.tail=value

  def clear(self):
    self.head=None
    self.tail=None     

  def enqueue(self, value):#adds node to beginning of the queue
      current=self.head#temp value storing the front of the queue
      newval=Nodel(value)
      if self.isEmpty():#it is an empty queue
          self.head=newval
          self.tail=newval
      else:
          if len(self)==1:#If there is only one existing member of the queue
              self.head.next=newval
          else:
              self.tail.next=newval
              self.tail=newval
              
  def dequeue(self):#removes element from queue, while simultaneously storing its value and returning it.
      if self.isEmpty():
          return None
      else:
          a=self.head
          self.head=self.head.next
          if self.head==None:
            self.tail=None
          a.next=None
      return a.value

  def decrease_key(self):
    self.map_rebuilder()
    self.rebuild_queue()

  def map_rebuilder(self):
    self.map=sorted(self.map,key=lambda i: i.distance,reverse=False)
    
  def rebuild_queue(self):
    self.clear()
    for i in self.map:
      self.enqueue(i)

  def __len__(self):
      x=1
      current=self.head
      while current!=None:
          current=current.next
          x=x+1
      return x

class lengthed_edge:
  def __init__(self,v1,v2,length,directed=True):
    self.length=length
    self.v1=v1
    self.v2=v2
    self.directed=directed#might need to get rid of this

class node:
  def __init__(self,name):
    self.name = name
    self.count = []#may not be needed
    self.pre=0 #pre number in DFS traversal
    self.post=0#post number in DFS traversal
    self.visited=False
    self.adjacent = []
    self.prev=None
    self.distance=10000#used to store the amount of edges it takes to get to this node from a specified ancestor node. Tempory value.
    self.node_edges=[]
  def __str__(self):
        return "{}".format(self.name) 

  __repr__ = __str__

  def buildlist(self):
    self.count.append(self.pre)
    self.count.append(self.post)
   
class graph:
  def __init__(self,adjlist):
    self.top=[]#topological sort representation that is directly implemented into DFS
    self.adjlist = adjlist
    self.count = 0#clock used in BFS to help define pre and post ordering of visited nodes
    self.bfstraversal=[]#Representation of the visited nodes in BFS
    self.directed=True
    self.edges=[]
    
  def construct(self):#creates an adjacency list of each edge and should be called shortly after the creation of the graph
    if type(self.adjlist[list(self.adjlist.keys())[0]][0]) is tuple:#separate case for when we are accounting for length
      for i in self.adjlist:
        for j in self.adjlist[i]:
          temp=lengthed_edge(i,j[0],j[1])
          self.edges.append(temp)
          temp.v1.node_edges.append(temp)
    else:
      for i in self.adjlist:
        for j in self.adjlist[i]:
          i.adjacent.append(j)
    

  def evaledge(self,v1,v2):#works with implementation of DFS that takes a pre and post number to identify the type of edge
    u=v1.count#fix this for tree and front
    v=v2.count
    if len(u)<2 or len(v)<2:
      return "None\n"
    if (u[0]>v[0]) and (u[1]>v[1]):
      return "({}-->{})=Cross Edge\n".format(v1,v2)
    elif (u[0]>v[0]) and (v[1]>u[1]):
      return "({}-->{})=Back Edge\n".format(v1,v2)
    else:
      if (u[0]==v[0]-1) or (u[1]==1+v[1]):
        return "({}-->{})=Tree Edge\n".format(v1,v2)
      return "({}-->{})=Front Edge\n".format(v1,v2)
      
  def edgetype(self):#string representation of all of the edges
    finalstr=""
    for i in self.adjlist:
      for j in self.adjlist[i]:
        finalstr+=self.evaledge(i,j)
    return finalstr


  def dfs(self,start):
    self.count=self.count+1
    start.pre=self.count
    start.visited=True
    for i in start.adjacent:
      if i.visited==False:
        if i.pre<start.pre:
          print("{}>{}".format(i,start))
        self.dfs(i)
    self.count=self.count+1
    start.post=self.count
    self.top.append(start)
    start.buildlist()

  def dfs_call(self,start,finish,maxlen):
    for i in self.adjlist:
      i.visited=False
    start.distance=0
    return self.explore(start,finish,maxlen)

  def explore_min(self,start,finish,maxlen,maxdist):
    if start==finish:
      return start.distance
    start.visited=True
    for i in start.node_edges:
      #print(i.v1.distance)
      #print(i.v1)
      i.v2.distance=i.v1.distance+i.length
      if not i.v2.visited and i.length<maxlen:
        if i.v2.distance<maxdist:
          return self.explore_min(i.v2,finish,maxlen,maxdist)

  def dfs_call_min(self,start,finish,maxlen):
    for n in range(1000):
      for i in self.adjlist:
        i.visited=False
        i.distance=1000
      start.distance=0
      found=self.explore_min(start,finish,maxlen,n)
      if found!=None:
        return found

  def bfscall(self,start,bfq=Queue()):#resets all of the vertices's to unvisited then calls bfs
    for i in self.adjlist:
      i.visited = False
    self.bfs(start,bfq)

  def bfsfindcall(self,start,finish,bfq=Queue()):#resets all of the vertices's to unvisited then calls bfsfind to find a given vertex
    for i in self.adjlist:
      i.visited = False
    output=self.bfs_find(start,finish,bfq)
    for i in self.adjlist:
      i.distance = 0
    return output


  def bfs(self,start,bfq=Queue()):
    print(start)
    self.bfstraversal.append(start)
    start.visited = True
    for j in start.adjacent:
      if not j.visited:
        bfq.enqueue(j)#putting all the children in the queue to be explored later
    if not bfq.isEmpty():
      while bfq.head!=None:
        a=bfq.head
        bfq.dequeue()
        if a.value.visited==False:
          self.bfs(a.value,bfq)

    
  def bfs_find(self,start,finish,bfq=Queue()):#finds a specific vertex from a starting point and returns its distance using the bfs algorithm
    if start.name==finish.name:#base case
      return "{} found at depth:{}".format(finish,finish.distance)
    start.visited = True
    for j in start.adjacent:
      j.distance=start.distance+1
      if not j.visited:
        bfq.enqueue(j)#putting all the children in the queue to be explored later
    if not bfq.isEmpty():
      while bfq.head!=None:
        a=bfq.head
        bfq.dequeue()
        if a.value.visited==False:
          return self.bfs_find(a.value,finish,bfq)

  
  def dijikstra_call(self,start):
    if len(self.edges)==0:
      return None
    unvisited=Queue()
    for i in self.adjlist:#create unvisited queue and set all nodes to unvisited
      #i.visited=False
      unvisited.enqueue(i)
      unvisited.map.append(i)
      i.distance=10000
      i.prev=None
    start.distance=0
    #start.visited=True
    return self.dijikstra(start,unvisited)


  def dijikstra(self,start,pq):#finds the shortest path between two nodes
    while not pq.isEmpty():
      u=pq.dequeue()#take out first element as it has been visited
      pq.map.remove(u)#take it out from the map
      for i in u.node_edges:
        if i.v2.distance>=i.v1.distance+i.length:
          i.v2.distance=i.v1.distance+i.length
          i.v2.prev=i.v1
          pq.decrease_key()
    for j in self.adjlist:
      print("{}>>{}\n".format(j,j.distance))


  def bellmanford(self,start):
      for i in self.adjlist:
        i.distance=10000
        i.previous=None
      start.distance=0
      self.edges=sorted(self.edges,key=lambda i: i.length,reverse=False)
      for j in self.edges:
        temp=j.v1.distance+j.length
        if j.v2.distance>temp:
          j.v2.distance=temp
          j.v2.prev=j.v1
      l=[]
      for i in self.adjlist:
        l.append([i.distance,i])
      return l


  def run(self,start=None,finish=None):
    self.construct()
    print(self.bellmanford(start))
def main():
  H = node("H")
  A = node("A")
  B = node("B")
  C = node("C")
  D = node("D")
  E = node("E")
  F = node("F")
  G = node("G")
  I = node("I")
  #adj={A:[(B,1),(F,6)],B:[(D,1)],C:[(F,1)],D:[(C,2)],F:[(B,7)]}
  adj={A:[(B,-1),(D,1)],B:[(C,1)],C:[(E,7)],D:[(C,2),(E,2)],E:[]}
  #adj={A:[B,C],B:[D,G,H],C:[E,F],D:[F,I],E:[],F:[],G:[I],H:[],I:[C]}
  g = graph(adj)
  g.run(A,C)




if __name__ == '__main__':
  main()
