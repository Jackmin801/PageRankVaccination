import random

class Graph():
    def __init__(self,N):
        self.nodes = N
        self.edges = 0
        self.adj = [set() for i in range(N)]
        self.deg = [0]*N
        self.directed = False

    def __repr__(self):
        return str(self.adj)

    def _directed_connect(self,p,q):
        """ Connect p -> q """
        if q in self.adj[p]:
            return False
        else:
            self.adj[p].add(q)
            self.deg[p] += 1
            self.edges += 1
            return True

    def _undirected_connect(self,p,q):
        """ Connect p <-> q """
        if q in self.adj[p] and p in self.adj[q]:
            return False
        else:
            self._directed_connect(p,q)
            self._directed_connect(q,p)
            return True

    def connect(self,p,q):
        """
        Connect p and q
        Behavior depends on directed attribute
        """
        if self.directed:
            self._directed_connect(p,q)
        else:
            self._undirected_connect(p,q)

    def print_edges(self):
        for node,children in enumerate(self.adj):
            for child in children:
                print(str(node)+","+str(child))

    def print_adj(self):
        for children in self.adj:
            print(' '.join(map(str,children)))

    def connect_tree(self):
        """ Connect a tree through the nodes """
        A = [i for i in range(self.nodes)]
        random.shuffle(A)
        for upper,node in enumerate(A[1:],0):
            target = A[random.randint(0,upper)]
            self.connect(node,target)

    def random_grandchild(self,p):
        """ Search for a grandchild. If none found, return -1 """
        children = random.sample(self.adj[p],self.deg[p])
        for child in children:
            grandchildren = self.adj[child] - self.adj[p] - {p}
            if grandchildren:
                return random.sample(grandchildren,1)[0]
        return -1

    def connect_grandchild(self,p):
        """ Connect p to a grandchild """
        target = self.random_grandchild(p)
        if target == -1:
            return False
        return self.connect(p,target)

def main():
    graph = Graph(10)
    print(graph)
    graph.connect_tree()
    print(graph)
    graph.connect_grandchild(0)
    print(graph)

if __name__ == "__main__":
    main()

