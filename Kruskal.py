import networkx as nx
import matplotlib.pyplot as plt

class Grafo:
    def __init__(self, G):
        self.G = G
        self.vertices = list(G.nodes)
        self.V = len(self.vertices)
        self.arestas = []

    def preparar_arestas(self):
        for u, v, data in self.G.edges(data=True):
            self.arestas.append((u, v, data['weight']))

    def find(self, parent, i):
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])

    def union(self, parent, rank, x, y):
        x_root = self.find(parent, x)
        y_root = self.find(parent, y)

        if rank[x_root] < rank[y_root]:
            parent[x_root] = y_root
        elif rank[x_root] > rank[y_root]:
            parent[y_root] = x_root
        else:
            parent[y_root] = x_root
            rank[x_root] += 1

    def kruskal(self):
        result = []  
        i, e = 0, 0  

        self.arestas = sorted(self.arestas, key=lambda item: item[2])

        parent = []
        rank = []

        for node in range(self.V):
            parent.append(node)
            rank.append(0)

        while e < self.V - 1:
            u, v, w = self.arestas[i]
            i += 1
            x = self.find(parent, self.vertices.index(u))
            y = self.find(parent, self.vertices.index(v))

            if x != y:
                e += 1
                result.append((u, v, w))
                self.union(parent, rank, x, y)

        AGM = nx.Graph()
        AGM.add_weighted_edges_from(result)

        return AGM


G = nx.Graph()
with open('grafo.txt','r') as file:
    for line in file:
        elements = line.split()
        source = elements[0]
        target = elements[1]
        weight = elements[2]
        G.add_edge(source,target,weight=weight)

grafo = Grafo(G)
grafo.preparar_arestas()
AGM = grafo.kruskal()

plt.figure(figsize=(10, 5))
plt.subplot(121)
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True,node_color='skyblue',node_size=450,font_size=10,font_weight='bold')
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.title('Grafo Original')

plt.subplot(122)
pos = nx.spring_layout(AGM)
nx.draw(AGM, pos, with_labels=True,node_color='skyblue',node_size=450,font_size=10,font_weight='bold')
labels = nx.get_edge_attributes(AGM, 'weight')
nx.draw_networkx_edge_labels(AGM, pos, edge_labels=labels)
plt.title('Árvore Geradora Mínima (Kruskal)')

plt.tight_layout()
plt.show()
