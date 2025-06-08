"""
Programme Principal - Analyseur de Chaînes Élémentaires dans les Graphes
main.py

Université de Yaoundé I
Département d'Informatique - Licence 2
Supervisé par Dr Manga MAXWELL

Membres:
- DIZE TCHEMOU MIGUEL CAREY
- SAGUEN KAMDEM CHERYL RONALD  
- SIGNE FONGANG WILFRIED BRANDON

Ce programme permet de:
1. Lire un graphe via une matrice d'adjacence ou une liste d'adjacence
2. Vérifier l'existence de chaînes élémentaires entre deux sommets
3. Visualiser le graphe avec mise en surbrillance des chaînes trouvées
4. Analyser les propriétés du graphe
"""

import sys
import os
from graph_analyzer import GraphAnalyzer
from user_interface import GraphUI
import matplotlib.pyplot as plt

def demo_console():
    """Démonstration en mode console"""
    print("="*80)
    print("ANALYSEUR DE CHAÎNES ÉLÉMENTAIRES - MODE CONSOLE")
    print("Université de Yaoundé I - Département d'Informatique")
    print("="*80)
    
    # Exemple de graphe prédéfini
    exemple_matrice = [
        [0, 1, 1, 0, 0],
        [1, 0, 1, 1, 0],
        [1, 1, 0, 1, 1],
        [0, 1, 1, 0, 1],
        [0, 0, 1, 1, 0]
    ]
    
    analyzer = GraphAnalyzer()
    analyzer.load_from_matrix(exemple_matrice)
    
    print("Graphe d'exemple chargé:")
    analyzer.print_graph_info()
    
    print("\n" + "="*60)
    print("RECHERCHE DE CHAÎNES ÉLÉMENTAIRES")
    print("="*60)
    
    # Tests de chaînes élémentaires
    test_cases = [(0, 4), (1, 3), (0, 2), (2, 4)]
    
    for start, end in test_cases:
        print(f"\nRecherche de chaîne de {start} vers {end}:")
        exists, path = analyzer.find_elementary_chain(start, end)
        
        if exists:
            print(f"✓ Chaîne trouvée: {' → '.join(map(str, path))}")
            print(f"  Longueur: {len(path) - 1} arêtes")
            
            # Trouver toutes les chaînes
            all_paths = analyzer.find_all_elementary_chains(start, end)
            if len(all_paths) > 1:
                print(f"  Nombre total de chaînes: {len(all_paths)}")
                for i, p in enumerate(all_paths[:3], 1):  # Afficher max 3 chaînes
                    print(f"    Chaîne {i}: {' → '.join(map(str, p))}")
                if len(all_paths) > 3:
                    print(f"    ... et {len(all_paths) - 3} autres")
        else:
            print("✗ Aucune chaîne élémentaire trouvée")
    
    # Visualisation
    print(f"\n{'='*60}")
    print("VISUALISATION DU GRAPHE")
    print("="*60)
    
    try:
        # Visualiser avec une chaîne en surbrillance
        exists, path = analyzer.find_elementary_chain(0, 4)
        if exists:
            analyzer.visualize_graph(highlight_path=path, save_path="demo_graph.png")
            print("Graphe visualisé et sauvegardé dans 'demo_graph.png'")
        else:
            analyzer.visualize_graph(save_path="demo_graph.png")
            print("Graphe visualisé et sauvegardé dans 'demo_graph.png'")
    except Exception as e:
        print(f"Erreur lors de la visualisation: {e}")
    
    print("\nDémonstration terminée!")

def mode_interactif():
    """Mode interactif en console"""
    print("="*80)
    print("MODE INTERACTIF - ANALYSEUR DE CHAÎNES ÉLÉMENTAIRES")
    print("="*80)
    
    analyzer = GraphAnalyzer()
    
    while True:
        print("\nOptions disponibles:")
        print("1. Charger graphe depuis matrice d'adjacence")
        print("2. Charger graphe depuis liste d'adjacence")
        print("3. Analyser chaîne élémentaire")
        print("4. Trouver toutes les chaînes")
        print("5. Afficher propriétés du graphe")
        print("6. Visualiser le graphe")
        print("7. Lancer interface graphique")
        print("0. Quitter")
        
        choix = input("\nVotre choix: ").strip()
        
        if choix == "0":
            print("Au revoir!")
            break
        
        elif choix == "1":
            try:
                print("Entrez la matrice d'adjacence (format: [[0,1,0],[1,0,1],[0,1,0]]):")
                matrix_str = input().strip()
                matrix = eval(matrix_str)
                analyzer.load_from_matrix(matrix)
                print("✓ Graphe chargé avec succès!")
                analyzer.print_graph_info()
            except Exception as e:
                print(f"✗ Erreur: {e}")
        
        elif choix == "2":
            try:
                print("Entrez la liste d'adjacence (format: {0:[1,2], 1:[0,2], 2:[0,1]}):")
                adj_str = input().strip()
                adj_list = eval(adj_str)
                analyzer.load_from_adjacency_list(adj_list)
                print("✓ Graphe chargé avec succès!")
                analyzer.print_graph_info()
            except Exception as e:
                print(f"✗ Erreur: {e}")
        
        elif choix == "3":
            if not analyzer.nx_graph:
                print("✗ Veuillez d'abord charger un graphe!")
                continue
            
            try:
                start = int(input("Sommet de départ: "))
                end = int(input("Sommet d'arrivée: "))
                
                exists, path = analyzer.find_elementary_chain(start, end)
                
                if exists:
                    print(f"✓ Chaîne trouvée: {' → '.join(map(str, path))}")
                    print(f"  Longueur: {len(path) - 1} arêtes")
                else:
                    print("✗ Aucune chaîne élémentaire trouvée")
            except ValueError:
                print("✗ Veuillez entrer des nombres valides")
        
        elif choix == "4":
            if not analyzer.nx_graph:
                print("✗ Veuillez d'abord charger un graphe!")
                continue
            
            try:
                start = int(input("Sommet de départ: "))
                end = int(input("Sommet d'arrivée: "))
                
                all_paths = analyzer.find_all_elementary_chains(start, end)
                
                if all_paths:
                    print(f"✓ {len(all_paths)} chaîne(s) trouvée(s):")
                    for i, path in enumerate(all_paths, 1):
                        print(f"  {i}. {' → '.join(map(str, path))}")
                else:
                    print("✗ Aucune chaîne élémentaire trouvée")
            except ValueError:
                print("✗ Veuillez entrer des nombres valides")
        
        elif choix == "5":
            if not analyzer.nx_graph:
                print("✗ Veuillez d'abord charger un graphe!")
                continue
            
            props = analyzer.get_graph_properties()
            print("\nPROPRIÉTÉS DU GRAPHE:")
            print(f"Nombre de sommets: {props['nombre_sommets']}")
            print(f"Nombre d'arêtes: {props['nombre_aretes']}")
            print(f"Densité: {props['densite']:.3f}")
            print(f"Connexe: {props['est_connexe']}")
            print(f"Diamètre: {props['diametre']}")
        
        elif choix == "6":
            if not analyzer.nx_graph:
                print("✗ Veuillez d'abord charger un graphe!")
                continue
            
            try:
                analyzer.visualize_graph(save_path="graphe_visualisation.png")
                print("✓ Graphe visualisé et sauvegardé dans 'graphe_visualisation.png'")
            except Exception as e:
                print(f"✗ Erreur lors de la visualisation: {e}")
        
        elif choix == "7":
            print("Lancement de l'interface graphique...")
            try:
                app = GraphUI()
                app.run()
            except Exception as e:
                print(f"✗ Erreur lors du lancement de l'interface: {e}")
        
        else:
            print("✗ Choix invalide!")

def main():
    """Fonction principale"""
    print("ANALYSEUR DE CHAÎNES ÉLÉMENTAIRES DANS LES GRAPHES")
    print("Université de Yaoundé I - Département d'Informatique")
    print("Supervisé par Dr Manga MAXWELL")
    print("\nMembres du groupe:")
    print("- DIZE TCHEMOU MIGUEL CAREY")
    print("- SAGUEN KAMDEM CHERYL RONALD")
    print("- SIGNE FONGANG WILFRIED BRANDON")
    print("="*80)
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--demo":
            demo_console()
        elif sys.argv[1] == "--console":
            mode_interactif()
        elif sys.argv[1] == "--gui":
            try:
                app = GraphUI()
                app.run()
            except Exception as e:
                print(f"Erreur lors du lancement de l'interface graphique: {e}")
                print("Passage en mode console...")
                mode_interactif()
        else:
            print("Arguments disponibles:")
            print("  --demo    : Démonstration avec exemple")
            print("  --console : Mode interactif console")
            print("  --gui     : Interface graphique (défaut)")
    else:
        # Par défaut, lancer l'interface graphique
        try:
            app = GraphUI()
            app.run()
        except Exception as e:
            print(f"Erreur lors du lancement de l'interface graphique: {e}")
            print("Passage en mode console...")
            mode_interactif()

if __name__ == "__main__":
    main()
