"""
Interface Utilisateur pour l'Analyseur de Chaînes Élémentaires
Module Interface - user_interface.py

Université de Yaoundé I
Département d'Informatique - Licence 2
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import json
from graph_analyzer import GraphAnalyzer
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx

class GraphUI:
    """Interface utilisateur graphique pour l'analyseur de graphes"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Analyseur de Chaînes Élémentaires - Université de Yaoundé I")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        self.analyzer = GraphAnalyzer()
        self.current_path = None
        
        self.setup_ui()
        self.show_guide()
    
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configuration du titre
        title_label = ttk.Label(main_frame, text="Analyseur de Chaînes Élémentaires", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Frame pour la saisie du graphe
        input_frame = ttk.LabelFrame(main_frame, text="Saisie du Graphe", padding="10")
        input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Boutons de saisie
        ttk.Button(input_frame, text="Saisir Matrice d'Adjacence", 
                  command=self.input_matrix).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(input_frame, text="Saisir Liste d'Adjacence", 
                  command=self.input_adjacency_list).grid(row=0, column=1, padx=(0, 10))
        ttk.Button(input_frame, text="Charger depuis Fichier", 
                  command=self.load_from_file).grid(row=0, column=2)
        
        # Frame pour l'analyse
        analysis_frame = ttk.LabelFrame(main_frame, text="Analyse des Chaînes", padding="10")
        analysis_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Sélection des sommets
        ttk.Label(analysis_frame, text="Sommet de départ:").grid(row=0, column=0)
        self.start_var = tk.StringVar()
        self.start_combo = ttk.Combobox(analysis_frame, textvariable=self.start_var, width=10)
        self.start_combo.grid(row=0, column=1, padx=(5, 15))
        
        ttk.Label(analysis_frame, text="Sommet d'arrivée:").grid(row=0, column=2)
        self.end_var = tk.StringVar()
        self.end_combo = ttk.Combobox(analysis_frame, textvariable=self.end_var, width=10)
        self.end_combo.grid(row=0, column=3, padx=(5, 15))
        
        # Boutons d'analyse
        ttk.Button(analysis_frame, text="Trouver Chaîne Élémentaire", 
                  command=self.find_chain).grid(row=0, column=4, padx=(0, 10))
        ttk.Button(analysis_frame, text="Toutes les Chaînes", 
                  command=self.find_all_chains).grid(row=0, column=5)
        
        # Frame pour les résultats
        results_frame = ttk.LabelFrame(main_frame, text="Résultats", padding="10")
        results_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        self.results_text = scrolledtext.ScrolledText(results_frame, height=15, width=60)
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Frame pour la visualisation
        viz_frame = ttk.LabelFrame(main_frame, text="Visualisation", padding="10")
        viz_frame.grid(row=3, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Canvas pour matplotlib
        self.fig, self.ax = plt.subplots(figsize=(6, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, viz_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0)
        
        # Boutons d'action
        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=4, column=0, columnspan=3, pady=(10, 0))
        
        ttk.Button(action_frame, text="Afficher Propriétés du Graphe", 
                  command=self.show_properties).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(action_frame, text="Sauvegarder Visualisation", 
                  command=self.save_visualization).grid(row=0, column=1, padx=(0, 10))
        ttk.Button(action_frame, text="Aide", 
                  command=self.show_guide).grid(row=0, column=2)
        
        # Configuration de redimensionnement
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
    def show_guide(self):
        """Affiche le guide d'utilisation"""
        guide_text = """
GUIDE D'UTILISATION - ANALYSEUR DE CHAÎNES ÉLÉMENTAIRES

1. SAISIE DU GRAPHE:
   • Matrice d'Adjacence: Entrez une matrice carrée (ex: [[0,1,1],[1,0,1],[1,1,0]])
   • Liste d'Adjacence: Entrez un dictionnaire (ex: {0:[1,2], 1:[0,2], 2:[0,1]})
   • Fichier: Chargez un fichier JSON contenant la représentation du graphe

2. ANALYSE:
   • Sélectionnez les sommets de départ et d'arrivée
   • Cliquez sur "Trouver Chaîne Élémentaire" pour une chaîne
   • Cliquez sur "Toutes les Chaînes" pour tous les chemins possibles

3. VISUALISATION:
   • Le graphe s'affiche automatiquement avec la chaîne en surbrillance
   • Les nœuds du chemin apparaissent en rouge
   • Les arêtes du chemin sont mises en évidence

4. PROPRIÉTÉS:
   • Consultez les propriétés du graphe (connexité, densité, etc.)
   • Sauvegardez la visualisation en image

Une chaîne élémentaire est un chemin où chaque sommet n'apparaît qu'une seule fois.
        """
        
        messagebox.showinfo("Guide d'utilisation", guide_text)
    
    def input_matrix(self):
        """Interface pour saisir une matrice d'adjacence"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Saisir Matrice d'Adjacence")
        dialog.geometry("400x300")
        
        ttk.Label(dialog, text="Entrez la matrice d'adjacence (format: [[0,1,0],[1,0,1],[0,1,0]]):").pack(pady=10)
        
        text_widget = scrolledtext.ScrolledText(dialog, height=10, width=50)
        text_widget.pack(pady=10)
        
        def validate_and_load():
            try:
                matrix_str = text_widget.get("1.0", tk.END).strip()
                matrix = eval(matrix_str)
                
                # Validation
                if not isinstance(matrix, list) or not all(isinstance(row, list) for row in matrix):
                    raise ValueError("Format de matrice invalide")
                
                n = len(matrix)
                if not all(len(row) == n for row in matrix):
                    raise ValueError("La matrice doit être carrée")
                
                self.analyzer.load_from_matrix(matrix)
                self.update_combo_boxes()
                self.update_visualization()
                self.results_text.delete("1.0", tk.END)
                self.results_text.insert(tk.END, "Graphe chargé avec succès à partir de la matrice d'adjacence!\n\n")
                self.analyzer.print_graph_info()
                dialog.destroy()
                
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors du chargement: {str(e)}")
        
        ttk.Button(dialog, text="Charger", command=validate_and_load).pack(pady=10)
    
    def input_adjacency_list(self):
        """Interface pour saisir une liste d'adjacence"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Saisir Liste d'Adjacence")
        dialog.geometry("400x300")
        
        ttk.Label(dialog, text="Entrez la liste d'adjacence (format: {0:[1,2], 1:[0,2], 2:[0,1]}):").pack(pady=10)
        
        text_widget = scrolledtext.ScrolledText(dialog, height=10, width=50)
        text_widget.pack(pady=10)
        
        def validate_and_load():
            try:
                adj_str = text_widget.get("1.0", tk.END).strip()
                adj_list = eval(adj_str)
                
                if not isinstance(adj_list, dict):
                    raise ValueError("La liste d'adjacence doit être un dictionnaire")
                
                self.analyzer.load_from_adjacency_list(adj_list)
                self.update_combo_boxes()
                self.update_visualization()
                self.results_text.delete("1.0", tk.END)
                self.results_text.insert(tk.END, "Graphe chargé avec succès à partir de la liste d'adjacence!\n\n")
                dialog.destroy()
                
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors du chargement: {str(e)}")
        
        ttk.Button(dialog, text="Charger", command=validate_and_load).pack(pady=10)
    
    def load_from_file(self):
        """Charge un graphe depuis un fichier JSON"""
        filename = filedialog.askopenfilename(
            title="Charger un graphe",
            filetypes=[("Fichiers JSON", "*.json"), ("Tous les fichiers", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    data = json.load(f)
                
                if 'matrix' in data:
                    self.analyzer.load_from_matrix(data['matrix'])
                elif 'adjacency_list' in data:
                    self.analyzer.load_from_adjacency_list(data['adjacency_list'])
                else:
                    raise ValueError("Format de fichier non reconnu")
                
                self.update_combo_boxes()
                self.update_visualization()
                self.results_text.delete("1.0", tk.END)
                self.results_text.insert(tk.END, f"Graphe chargé depuis {filename}\n\n")
                
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors du chargement: {str(e)}")
    
    def update_combo_boxes(self):
        """Met à jour les combobox avec les sommets disponibles"""
        vertices = list(range(self.analyzer.num_vertices))
        self.start_combo['values'] = vertices
        self.end_combo['values'] = vertices
    
    def find_chain(self):
        """Trouve une chaîne élémentaire entre deux sommets"""
        if not self.analyzer.nx_graph:
            messagebox.showerror("Erreur", "Veuillez d'abord charger un graphe!")
            return
        
        try:
            start = int(self.start_var.get())
            end = int(self.end_var.get())
            
            exists, path = self.analyzer.find_elementary_chain(start, end)
            
            self.results_text.delete("1.0", tk.END)
            if exists:
                self.results_text.insert(tk.END, f"CHAÎNE ÉLÉMENTAIRE TROUVÉE!\n")
                self.results_text.insert(tk.END, f"De {start} vers {end}: {' → '.join(map(str, path))}\n")
                self.results_text.insert(tk.END, f"Longueur: {len(path) - 1} arêtes\n\n")
                self.current_path = path
                self.update_visualization(highlight_path=path)
            else:
                self.results_text.insert(tk.END, f"AUCUNE CHAÎNE TROUVÉE!\n")
                self.results_text.insert(tk.END, f"Il n'existe pas de chaîne élémentaire entre {start} et {end}\n\n")
                self.current_path = None
                self.update_visualization()
                
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez sélectionner des sommets valides!")
    
    def find_all_chains(self):
        """Trouve toutes les chaînes élémentaires entre deux sommets"""
        if not self.analyzer.nx_graph:
            messagebox.showerror("Erreur", "Veuillez d'abord charger un graphe!")
            return
        
        try:
            start = int(self.start_var.get())
            end = int(self.end_var.get())
            
            all_paths = self.analyzer.find_all_elementary_chains(start, end)
            
            self.results_text.delete("1.0", tk.END)
            if all_paths:
                self.results_text.insert(tk.END, f"TOUTES LES CHAÎNES ÉLÉMENTAIRES TROUVÉES!\n")
                self.results_text.insert(tk.END, f"Entre {start} et {end}:\n\n")
                
                for i, path in enumerate(all_paths, 1):
                    self.results_text.insert(tk.END, f"Chaîne {i}: {' → '.join(map(str, path))}\n")
                    self.results_text.insert(tk.END, f"Longueur: {len(path) - 1} arêtes\n\n")
                
                # Mettre en surbrillance la première chaîne
                self.current_path = all_paths[0]
                self.update_visualization(highlight_path=all_paths[0])
            else:
                self.results_text.insert(tk.END, f"AUCUNE CHAÎNE TROUVÉE!\n")
                self.results_text.insert(tk.END, f"Il n'existe pas de chaîne élémentaire entre {start} et {end}\n\n")
                self.current_path = None
                self.update_visualization()
                
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez sélectionner des sommets valides!")
    
    def update_visualization(self, highlight_path=None):
        """Met à jour la visualisation du graphe"""
        if not self.analyzer.nx_graph:
            return
        
        self.ax.clear()
        
        pos = nx.spring_layout(self.analyzer.nx_graph, seed=42)
        
        # Dessiner le graphe de base
        nx.draw_networkx_nodes(self.analyzer.nx_graph, pos, ax=self.ax,
                              node_color='lightblue', node_size=500, alpha=0.7)
        nx.draw_networkx_edges(self.analyzer.nx_graph, pos, ax=self.ax,
                              edge_color='gray', alpha=0.5, width=1)
        
        # Mettre en surbrillance le chemin
        if highlight_path and len(highlight_path) > 1:
            nx.draw_networkx_nodes(self.analyzer.nx_graph, pos, ax=self.ax,
                                 nodelist=highlight_path, node_color='red', 
                                 node_size=700, alpha=0.8)
            
            path_edges = [(highlight_path[i], highlight_path[i+1]) 
                         for i in range(len(highlight_path)-1)]
            nx.draw_networkx_edges(self.analyzer.nx_graph, pos, ax=self.ax,
                                 edgelist=path_edges, edge_color='red', 
                                 width=3, alpha=0.8)
        
        nx.draw_networkx_labels(self.analyzer.nx_graph, pos, ax=self.ax,
                               font_size=12, font_weight='bold')
        
        self.ax.set_title("Visualisation du Graphe")
        self.ax.axis('off')
        self.canvas.draw()
    
    def show_properties(self):
        """Affiche les propriétés du graphe"""
        if not self.analyzer.nx_graph:
            messagebox.showerror("Erreur", "Veuillez d'abord charger un graphe!")
            return
        
        props = self.analyzer.get_graph_properties()
        
        prop_text = f"""PROPRIÉTÉS DU GRAPHE:

Nombre de sommets: {props['nombre_sommets']}
Nombre d'arêtes: {props['nombre_aretes']}
Densité: {props['densite']:.3f}
Connexe: {props['est_connexe']}
Diamètre: {props['diametre']}

Composantes connexes: {len(props['composantes_connexes'])}
"""
        
        self.results_text.delete("1.0", tk.END)
        self.results_text.insert(tk.END, prop_text)
    
    def save_visualization(self):
        """Sauvegarde la visualisation"""
        if not self.analyzer.nx_graph:
            messagebox.showerror("Erreur", "Aucun graphe à sauvegarder!")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Sauvegarder la visualisation",
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("PDF", "*.pdf"), ("SVG", "*.svg")]
        )
        
        if filename:
            self.fig.savefig(filename, dpi=300, bbox_inches='tight')
            messagebox.showinfo("Succès", f"Visualisation sauvegardée: {filename}")
    
    def run(self):
        """Lance l'application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = GraphUI()
    app.run()
