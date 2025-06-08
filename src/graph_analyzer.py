"""
Analyseur de Chaînes Élémentaires dans les Graphes
Module Principal - graph_analyzer.py

Université de Yaoundé I
Département d'Informatique - Licence 2
Supervisé par Dr Manga MAXWELL

Membres:
- DIZE TCHEMOU MIGUEL CAREY
- SAGUEN KAMDEM CHERYL RONALD  
- SIGNE FONGANG WILFRIED BRANDON
"""

import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict, deque
import numpy as np

class GraphAnalyzer:
    """Classe principale pour l'analyse des graphes et la recherche de chaînes élémentaires"""
    
    def __init__(self):
        self.graph = None
        self.nx_graph = None
        self.adjacency_matrix = None
        self.adjacency_list = None
        self.num_vertices = 0
        
    def load_from_matrix(self, matrix):
        """
        Charge un graphe à partir d'une matrice d'adjacence
        
        Args:
            matrix: Liste de listes ou array numpy représentant la matrice d'adjacence
        """
        self.adjacency_matrix = np.array(matrix)
        self.num_vertices = len(matrix)
        
        # Conversion en liste d'adjacence
        self.adjacency_list = defaultdict(list)
        for i in range(self.num_vertices):
            for j in range(self.num_vertices):
                if matrix[i][j] != 0:
                    self.adjacency_list[i].append(j)
        
        # Création du graphe NetworkX pour la visualisation
        self._create_networkx_graph()
        
    def load_from_adjacency_list(self, adj_list):
        """
        Charge un graphe à partir d'une liste d'adjacence
        
        Args:
            adj_list: Dictionnaire {sommet: [liste_des_voisins]}
        """
        self.adjacency_list = defaultdict(list, adj_list)
        self.num_vertices = max(max(adj_list.keys()), max([max(v) for v in adj_list.values() if v])) + 1
        
        # Conversion en matrice d'adjacence
        self.adjacency_matrix = np.zeros((self.num_vertices, self.num_vertices), dtype=int)
        for vertex, neighbors in adj_list.items():
            for neighbor in neighbors:
                self.adjacency_matrix[vertex][neighbor] = 1
        
        # Création du graphe NetworkX
        self._create_networkx_graph()
        
    def _create_networkx_graph(self):
        """Crée un graphe NetworkX à partir de la liste d'adjacence"""
        self.nx_graph = nx.Graph()
        for vertex in range(self.num_vertices):
            self.nx_graph.add_node(vertex)
        
        for vertex, neighbors in self.adjacency_list.items():
            for neighbor in neighbors:
                self.nx_graph.add_edge(vertex, neighbor)
    
    def find_elementary_chain(self, start, end):
        """
        Trouve une chaîne élémentaire entre deux sommets en utilisant BFS
        
        Args:
            start: Sommet de départ
            end: Sommet d'arrivée
            
        Returns:
            tuple: (chemin_trouvé, liste_des_sommets_du_chemin)
        """
        if start == end:
            return True, [start]
        
        # BFS pour trouver le chemin le plus court
        queue = deque([(start, [start])])
        visited = set([start])
        
        while queue:
            current_vertex, path = queue.popleft()
            
            for neighbor in self.adjacency_list[current_vertex]:
                if neighbor == end:
                    return True, path + [neighbor]
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return False, []
    
    def find_all_elementary_chains(self, start, end):
        """
        Trouve toutes les chaînes élémentaires entre deux sommets
        
        Args:
            start: Sommet de départ
            end: Sommet d'arrivée
            
        Returns:
            list: Liste de tous les chemins élémentaires
        """
        all_paths = []
        
        def dfs_paths(current, target, path, visited):
            if current == target:
                all_paths.append(path[:])
                return
            
            for neighbor in self.adjacency_list[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    path.append(neighbor)
                    dfs_paths(neighbor, target, path, visited)
                    path.pop()
                    visited.remove(neighbor)
        
        if start == end:
            return [[start]]
        
        visited = set([start])
        dfs_paths(start, end, [start], visited)
        return all_paths
    
    def visualize_graph(self, highlight_path=None, save_path=None):
        """
        Visualise le graphe avec mise en surbrillance optionnelle d'un chemin
        
        Args:
            highlight_path: Liste des sommets du chemin à mettre en surbrillance
            save_path: Chemin pour sauvegarder l'image
        """
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(self.nx_graph, seed=42)
        
        # Dessiner tous les nœuds et arêtes en gris clair
        nx.draw_networkx_nodes(self.nx_graph, pos, node_color='lightblue', 
                              node_size=800, alpha=0.7)
        nx.draw_networkx_edges(self.nx_graph, pos, edge_color='gray', 
                              alpha=0.5, width=1)
        
        # Mettre en surbrillance le chemin si fourni
        if highlight_path and len(highlight_path) > 1:
            # Nœuds du chemin en rouge
            nx.draw_networkx_nodes(self.nx_graph, pos, 
                                 nodelist=highlight_path, 
                                 node_color='red', node_size=1000, alpha=0.8)
            
            # Arêtes du chemin en rouge
            path_edges = [(highlight_path[i], highlight_path[i+1]) 
                         for i in range(len(highlight_path)-1)]
            nx.draw_networkx_edges(self.nx_graph, pos, 
                                 edgelist=path_edges, 
                                 edge_color='red', width=3, alpha=0.8)
        
        # Étiquettes des nœuds
        nx.draw_networkx_labels(self.nx_graph, pos, font_size=16, font_weight='bold')
        
        plt.title("Visualisation du Graphe avec Chaîne Élémentaire", 
                 fontsize=16, fontweight='bold')
        plt.axis('off')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.tight_layout()
        plt.show()
    
    def get_graph_properties(self):
        """
        Retourne les propriétés du graphe
        
        Returns:
            dict: Dictionnaire contenant les propriétés du graphe
        """
        if not self.nx_graph:
            return {}
        
        return {
            'nombre_sommets': self.num_vertices,
            'nombre_aretes': self.nx_graph.number_of_edges(),
            'densite': nx.density(self.nx_graph),
            'est_connexe': nx.is_connected(self.nx_graph),
            'composantes_connexes': list(nx.connected_components(self.nx_graph)),
            'diametre': nx.diameter(self.nx_graph) if nx.is_connected(self.nx_graph) else 'Non défini (graphe non connexe)'
        }
    
    def print_graph_info(self):
        """Affiche les informations du graphe"""
        print("=" * 60)
        print("INFORMATIONS SUR LE GRAPHE")
        print("=" * 60)
        
        print(f"Nombre de sommets: {self.num_vertices}")
        print(f"Nombre d'arêtes: {self.nx_graph.number_of_edges()}")
        
        print("\nMatrice d'adjacence:")
        print(self.adjacency_matrix)
        
        print("\nListe d'adjacence:")
        for vertex in range(self.num_vertices):
            neighbors = self.adjacency_list[vertex]
            print(f"Sommet {vertex}: {neighbors}")
        
        props = self.get_graph_properties()
        print(f"\nDensité: {props['densite']:.3f}")
        print(f"Connexe: {props['est_connexe']}")
        
        if not props['est_connexe']:
            print(f"Composantes connexes: {len(props['composantes_connexes'])}")
        else:
            print(f"Diamètre: {props['diametre']}")
