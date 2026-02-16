"""
Interface simple pour s'entraîner sur des cas ZBLL spécifiques
"""

import kociemba
import pycuber as pc
from collections import Counter
import random
from zbll_algorithms_database import ZBLL_ALGORITHMS
from zbls_algorithms_database import ZBLS_ALGORITHMS

# Système de parsing intégré
def expand_move(move: str) -> str:
    """Convertit un mouvement avancé en mouvements standards"""
    if len(move) <= 1:
        base = move
        suffix = ''
    else:
        if move[-1] in ["'", "2"]:
            base = move[:-1]
            suffix = move[-1]
        else:
            base = move
            suffix = ''
    
    equivalents = {
        'r': "R M'", 'l': "L M", 'u': "U E'", 'd': "D E",
        'f': "F S", 'b': "B S'",
        'M': "L' R", 'E': "D' U", 'S': "F' B",
        'x': "R L' M'", 'y': "U D' E'", 'z': "F B' S'"
    }
    
    if base not in equivalents:
        return move
    
    sequence = equivalents[base]
    
    if suffix == "'":
        # Inverser toute la séquence
        moves = sequence.split()
        inverted = []
        for move in reversed(moves):
            if move.endswith("2"):
                inverted.append(move)
            elif move.endswith("'"):
                inverted.append(move[:-1])
            else:
                inverted.append(move + "'")
        return " ".join(inverted)
    elif suffix == "2":
        return f"{sequence} {sequence}"
    else:
        return sequence

def expand_algorithm(alg: str) -> str:
    """Convertit un algorithme complet en mouvements standards"""
    if not alg.strip():
        return alg
    
    moves = alg.split()
    expanded_moves = []
    
    for move in moves:
        expanded = expand_move(move)
        expanded_moves.append(expanded)
    
    return " ".join(expanded_moves)

def list_all_cases():
    """Liste tous les cas ZBLL disponibles"""
    cases = []
    for family_name in ZBLL_ALGORITHMS.keys():
        cases.append(family_name)
    return cases

def get_zbll_by_case(case_name):
    """Récupère tous les algorithmes pour un cas ZBLL donné"""
    if case_name not in ZBLL_ALGORITHMS:
        return []
    
    algorithms = []
    family = ZBLL_ALGORITHMS[case_name]
    
    for subcase_name, subcase in family.items():
        for variation_name, variation in subcase.items():
            if variation.get('algorithm'):
                algorithms.append({
                    'name': f"{variation['name']}",
                    'algorithm': variation['algorithm'],
                    'description': variation.get('description', '')
                })
    
    return algorithms


def invert_alg(alg):
    """Inverse un algorithme"""
    moves = alg.split()
    inverted = []

    for move in reversed(moves):
        if move.endswith("2"):
            inverted.append(move)
        elif move.endswith("'"):
            inverted.append(move[:-1])
        else:
            inverted.append(move + "'")

    return " ".join(inverted)

def cube_to_kociemba_safe(c):
    """Conversion sécurisée du cube PyCuber vers Kociemba"""
    color_map = {
        'white': 'U',
        'yellow': 'D', 
        'green': 'F',
        'blue': 'B',
        'red': 'R',
        'orange': 'L'
    }
    
    faces_order = ['U', 'R', 'F', 'D', 'L', 'B']
    result = ""
    
    for face in faces_order:
        face_obj = c.get_face(face)
        for row in face_obj:
            for sticker in row:
                colour = sticker.colour
                if colour in color_map:
                    result += color_map[colour]
                else:
                    colour_upper = colour.upper()
                    if colour_upper in ['U', 'D', 'R', 'L', 'F', 'B']:
                        result += colour_upper
                    else:
                        raise ValueError(f"Couleur invalide: {colour}")
    
    return result

def validate_state_safe(state):
    """Validation robuste de l'état"""
    if len(state) != 54:
        return False, f"Longueur incorrecte: {len(state)}"
    
    expected = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
    if Counter(state) == Counter(expected):
        return True, "Valide"
    else:
        return False, "Comptes de couleurs incorrects"

def get_random_u_move():
    """Génère un mouvement U aléatoire (U, U' ou U2)"""
    return random.choice(['U', "U'", 'U2'])

def get_random_zbls_algorithm():
    """Récupère un algorithme ZBLS aléatoire"""
    available_algs = []
    
    for family_name, family in ZBLS_ALGORITHMS.items():
        for case_name, case_data in family.items():
            if case_data.get('algorithm'):  # Vérifier si l'algorithme n'est pas vide
                available_algs.append({
                    'name': case_name,
                    'algorithm': case_data['algorithm'],
                    'family': family_name
                })
    
    if available_algs:
        return random.choice(available_algs)
    else:
        return {'name': 'Default', 'algorithm': 'F R\' F\' R', 'family': 'Default'}

def get_random_zbll_algorithm():
    """Récupère un algorithme ZBLL aléatoire"""
    available_algs = []
    
    for family_name, family in ZBLL_ALGORITHMS.items():
        for subcase_name, subcase in family.items():
            for variation_name, variation in subcase.items():
                if variation.get('algorithm'):
                    available_algs.append({
                        'name': f"{family_name}-{subcase_name}-{variation['name']}",
                        'algorithm': variation['algorithm'],
                        'family': family_name,
                        'subcase': subcase_name,
                        'variation': variation['name']
                    })
    
    if available_algs:
        return random.choice(available_algs)
    else:
        return {'name': 'T-Default', 'algorithm': 'R U R2 F R F2 r\' F r F R U R\' U R U2 R\'', 'family': 'T', 'subcase': 'Default', 'variation': 'Default'}

def generate_training_scramble_random():
    """Génère un scramble pour des cas ZBLS et ZBLL aléatoires"""
    zbls_alg_data = get_random_zbls_algorithm()
    zbll_alg_data = get_random_zbll_algorithm()
    
    zbls_alg = zbls_alg_data['algorithm']
    zbll_alg = zbll_alg_data['algorithm']
    
    print(f"Génération pour: ZBLS {zbls_alg_data['name']} - ZBLL {zbll_alg_data['name']}")
    
    # Générer les mouvements U aléatoires
    random_u_before = get_random_u_move()
    random_u_after = get_random_u_move()
    print(f"Mouvement U avant ZBLS: {random_u_before}")
    print(f"Mouvement U avant ZBLL: {random_u_after}")
    
    try:
        # Inverser les algorithmes
        inverted_zbll = invert_alg(zbll_alg)
        inverted_zbls = invert_alg(zbls_alg)
        
        # Étendre les algorithmes inversés
        expanded_zbll = expand_algorithm(inverted_zbll)
        expanded_zbls = expand_algorithm(inverted_zbls)
        
        # Construire l'état
        cube = pc.Cube()
        cube("z2")  # Orienter le cube
        
        # Ajouter un mouvement U aléatoire avant le ZBLS
        cube(random_u_before)
        
        cube(zbls_alg)  # Appliquer ZBLS
        
        # Ajouter un mouvement U aléatoire avant la ZBLL
        cube(random_u_after)
        
        cube(zbll_alg)  # Puis appliquer ZBLL
        
        # Convertir et valider
        state = cube_to_kociemba_safe(cube)
        is_valid, message = validate_state_safe(state)
        
        if not is_valid:
            raise Exception(f"État invalide: {message}")
        
        # Générer le scramble (solution pour revenir à l'état résolu)
        solution = kociemba.solve(state)
        scramble = solution  # Pas besoin d'inverser, kociemba donne déjà le scramble
        
        return {
            'scramble': scramble,
            'zbll': zbll_alg,
            'zbll_name': zbll_alg_data['name'],
            'zbls': zbls_alg,
            'zbls_name': zbls_alg_data['name'],
            'u_before_zbls': random_u_before,
            'u_before_zbll': random_u_after,
            'success': True
        }
        
    except Exception as e:
        return {
            'scramble': None,
            'error': str(e),
            'zbll': zbll_alg,
            'zbll_name': zbll_alg_data['name'],
            'zbls': zbls_alg,
            'zbls_name': zbls_alg_data['name'],
            'success': False
        }

def generate_training_scramble(zbll_alg: str, zbls_alg: str = None):
    """
    Génère un scramble pour un cas ZBLL spécifique
    
    Args:
        zbll_alg: Algorithme ZBLL à entraîner
        zbls_alg: Algorithme ZBLS (si None, utilise un algorithme aléatoire de la base)
    
    Returns:
        Scramble et informations
    """
    # Si aucun ZBLS n'est spécifié, en prendre un aléatoire dans la base
    if zbls_alg is None:
        zbls_data = get_random_zbls_algorithm()
        zbls_alg = zbls_data['algorithm']
        zbls_name = zbls_data['name']
    else:
        zbls_name = "Manuel"
    
    print(f"Génération pour: {zbll_alg} (ZBLS: {zbls_name})")
    
    # Générer les mouvements U aléatoires
    random_u_before = get_random_u_move()
    random_u_after = get_random_u_move()
    print(f"Mouvement U avant ZBLS: {random_u_before}")
    print(f"Mouvement U avant ZBLL: {random_u_after}")
    
    try:
        # Inverser les algorithmes
        inverted_zbll = invert_alg(zbll_alg)
        inverted_zbls = invert_alg(zbls_alg)
        
        # Étendre les algorithmes inversés
        expanded_zbll = expand_algorithm(inverted_zbll)
        expanded_zbls = expand_algorithm(inverted_zbls)
        
        # Construire l'état
        cube = pc.Cube()
        cube("z2")  # Orienter le cube
        
        # Ajouter un mouvement U aléatoire avant le ZBLS
        cube(random_u_before)
        
        cube(zbls_alg)  # Appliquer ZBLS
        
        # Ajouter un mouvement U aléatoire avant la ZBLL
        cube(random_u_after)
        
        cube(zbll_alg)  # Puis appliquer ZBLL
        
        # Convertir et valider
        state = cube_to_kociemba_safe(cube)
        is_valid, message = validate_state_safe(state)
        
        if not is_valid:
            raise Exception(f"État invalide: {message}")
        
        # Générer le scramble (solution pour revenir à l'état résolu)
        solution = kociemba.solve(state)
        scramble = solution  # Pas besoin d'inverser, kociemba donne déjà le scramble
        
        return {
            'scramble': scramble,
            'zbll': zbll_alg,
            'zbls': zbls_alg,
            'zbls_name': zbls_name,
            'u_before_zbls': random_u_before,
            'u_before_zbll': random_u_after,
            'success': True
        }
        
    except Exception as e:
        return {
            'scramble': None,
            'error': str(e),
            'zbll': zbll_alg,
            'zbls': zbls_alg,
            'zbls_name': zbls_name,
            'success': False
        }

def interactive_menu():
    """Menu interactif pour choisir les cas ZBLL"""
    print("=== ZBLL Trainer ===\n")
    
    # Afficher les cas disponibles
    cases = list_all_cases()
    print("Cas ZBLL disponibles:")
    for i, case in enumerate(cases, 1):
        algs = get_zbll_by_case(case)
        print(f"  {i}. {case} ({len(algs)} algorithmes)")
    
    # Choisir le cas
    while True:
        try:
            choice = input(f"\nChoisissez un cas (1-{len(cases)}) ou 'q' pour quitter: ")
            
            if choice.lower() == 'q':
                print("Au revoir!")
                return
            
            case_index = int(choice) - 1
            if 0 <= case_index < len(cases):
                selected_case = cases[case_index]
                break
            else:
                print("Choix invalide. Réessayez.")
        except ValueError:
            print("Entrée invalide. Réessayez.")
    
    # Afficher les algorithmes pour le cas choisi
    algs = get_zbll_by_case(selected_case)
    print(f"\nAlgorithmes {selected_case}:")
    for i, alg in enumerate(algs, 1):
        print(f"  {i}. {alg['name']}: {alg['algorithm']}")
        if alg['description']:
            print(f"     {alg['description']}")
    
    # Choisir l'algorithme
    while True:
        try:
            choice = input(f"\nChoisissez un algorithme (1-{len(algs)}) ou 'q' pour quitter: ")
            
            if choice.lower() == 'q':
                print("Au revoir!")
                return
            
            alg_index = int(choice) - 1
            if 0 <= alg_index < len(algs):
                selected_alg = algs[alg_index]
                break
            else:
                print("Choix invalide. Réessayez.")
        except ValueError:
            print("Entrée invalide. Réessayez.")
    
    # Générer le scramble
    print(f"\nGénération du scramble pour {selected_alg['name']}...")
    result = generate_training_scramble(selected_alg['algorithm'])
    
    if result['success']:
        print(f"\n✅ Scramble généré:")
        print(f"   {result['scramble']}")
        print(f"\nInstructions:")
        print(f"1. Applique le scramble ci-dessus")
        print(f"2. Résous avec ZBLS: F R' F' R")
        print(f"3. Résous avec ZBLL: {selected_alg['algorithm']}")
    else:
        print(f"\n❌ Erreur: {result['error']}")

def batch_training():
    """Génère plusieurs scrambles pour tous les cas"""
    print("=== Entraînement par lots ===\n")
    
    all_results = {}
    
    for case_type in list_all_cases():
        algs = get_zbll_by_case(case_type)
        case_results = []
        
        print(f"Génération des scrambles {case_type}...")
        
        for alg in algs:
            result = generate_training_scramble(alg['algorithm'])
            if result['success']:
                case_results.append({
                    'name': alg['name'],
                    'scramble': result['scramble']
                })
                print(f"  ✅ {alg['name']}: {result['scramble']}")
            else:
                print(f"  ❌ {alg['name']}: {result['error']}")
        
        all_results[case_type] = case_results
    
    # Sauvegarder les résultats
    with open('training_scrambles.txt', 'w') as f:
        for case_type, results in all_results.items():
            f.write(f"\n=== {case_type} ===\n")
            for result in results:
                f.write(f"{result['name']}: {result['scramble']}\n")
    
    print(f"\n✅ {sum(len(results) for results in all_results.values())} scrambles sauvegardés dans 'training_scrambles.txt'")

if __name__ == "__main__":
    print("ZBLL Trainer - Système d'entraînement personnel\n")
    
    while True:
        print("\n" + "="*40)
        print("MENU PRINCIPAL:")
        print("1. Mode interactif (choisir cas et algorithme)")
        print("2. Génération par lots (tous les cas)")
        print("3. Scramble aléatoire (ZBLS + ZBLL de la base)")
        print("4. Lister tous les algorithmes")
        print("5. Quitter")
        
        choice = input("\nVotre choix (1-5): ")
        
        if choice == "1":
            interactive_menu()
        elif choice == "2":
            batch_training()
        elif choice == "3":
            print("\n" + "-"*40)
            result = generate_training_scramble_random()
            
            if result['success']:
                print(f"\n✅ Scramble généré:")
                print(f"   {result['scramble']}")
                print(f"\nDétails:")
                print(f"   Mouvement U avant ZBLS: {result['u_before_zbls']}")
                print(f"   ZBLS: {result['zbls_name']} - {result['zbls']}")
                print(f"   Mouvement U avant ZBLL: {result['u_before_zbll']}")
                print(f"   ZBLL: {result['zbll_name']} - {result['zbll']}")
                print(f"\nInstructions:")
                print(f"   1. Applique le scramble ci-dessus")
                print(f"   2. Résous avec ZBLS: {result['zbls']}")
                print(f"   3. Résous avec ZBLL: {result['zbll']}")
            else:
                print(f"\n❌ Erreur: {result['error']}")
        elif choice == "4":
            print("\n=== Tous les algorithmes ZBLL ===")
            for case_type in list_all_cases():
                algs = get_zbll_by_case(case_type)
                print(f"\n{case_type}:")
                for alg in algs:
                    print(f"  {alg['name']}: {alg['algorithm']}")
        elif choice == "5":
            print("Au revoir!")
            break
        else:
            print("Choix invalide. Réessayez.")
