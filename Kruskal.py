import networkx as nx
import matplotlib.pyplot as plt

class Grafo:
    def __init__(self, G):
        self.G = G
        self.vertices = list(G.nodes)
        self.V = len(self.vertices)
        self.arestas = []

    # Adiciona as arestas do grafo em um formato que possa ser processado pelo algoritmo de Kruskal
    def preparar_arestas(self):
        for u, v, data in self.G.edges(data=True):
            self.arestas.append((u, v, data['weight']))

    # Função para encontrar o conjunto de um elemento i
    def find(self, parent, i):
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])

    # Função que une dois conjuntos de x e y
    def union(self, parent, rank, x, y):
        x_root = self.find(parent, x)
        y_root = self.find(parent, y)

        # Anexa o menor rank sob a raiz do maior rank
        if rank[x_root] < rank[y_root]:
            parent[x_root] = y_root
        elif rank[x_root] > rank[y_root]:
            parent[y_root] = x_root
        else:
            # Se os ranks forem iguais, faça um deles a raiz e incremente seu rank por um
            parent[y_root] = x_root
            rank[x_root] += 1

    # Função principal para encontrar a árvore geradora mínima usando o algoritmo de Kruskal
    def kruskal(self):
        result = []  # Este será o armazenamento final para a AGM
        i, e = 0, 0  # índice da próxima aresta a ser adicionada ao resultado

        # Classifica todas as arestas em ordem crescente de peso
        self.arestas = sorted(self.arestas, key=lambda item: item[2])

        parent = []
        rank = []

        # Inicializa parent e rank
        for node in range(self.V):
            parent.append(node)
            rank.append(0)

        # Número de arestas a serem tomadas é igual ao número de vértices - 1
        while e < self.V - 1:
            u, v, w = self.arestas[i]
            i += 1
            x = self.find(parent, self.vertices.index(u))
            y = self.find(parent, self.vertices.index(v))

            # Se incluir esta aresta não cria um ciclo, inclua-a no resultado e incremente o índice de aresta
            if x != y:
                e += 1
                result.append((u, v, w))
                self.union(parent, rank, x, y)

        # Criar um novo grafo para a AGM
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

# Desenhar o grafo original
plt.figure(figsize=(10, 5))
plt.subplot(121)
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True,node_color='skyblue',node_size=450,font_size=10,font_weight='bold')
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.title('Grafo Original')

# Desenhar a árvore geradora mínima
plt.subplot(122)
pos = nx.spring_layout(AGM)
nx.draw(AGM, pos, with_labels=True,node_color='skyblue',node_size=450,font_size=10,font_weight='bold')
labels = nx.get_edge_attributes(AGM, 'weight')
nx.draw_networkx_edge_labels(AGM, pos, edge_labels=labels)
plt.title('Árvore Geradora Mínima (Kruskal)')

# Mostrar os gráficos
plt.tight_layout()
plt.show()
