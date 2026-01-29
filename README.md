# Simplex Solver - Deux Phases et Grand M

Une application web moderne pour résoudre des problèmes de programmation linéaire en utilisant deux méthodes du simplexe:
- **Méthode du Grand M**
- **Simplexe Deux Phases**

## Installation

### Prérequis
- Python 3.7+
- pip

### Étapes d'installation

1. **Créer un environnement virtuel (optionnel mais recommandé)**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

## Lancement de l'application

```bash
python app.py
```

L'application sera accessible à l'adresse: **http://localhost:5000**

## Utilisation

1. **Page d'accueil**: Sélectionnez la méthode (Grand M ou Deux Phases), le nombre de variables et de contraintes
2. **Page de saisie**: Entrez les coefficients de la fonction objectif et les contraintes
3. **Page de résultats**: Consultez la solution optimale et la valeur de Z

## Structure du projet

```
├── app.py                    # Application Flask et logique du simplexe
├── requirements.txt          # Dépendances Python
├── static/
│   ├── styles.css           # Styles généraux
│   ├── fonction.css         # Styles de la page de saisie
│   └── resultat.css         # Styles de la page de résultats
└── templates/
    ├── index.html           # Page d'accueil
    ├── fonction.html        # Page de saisie
    └── resultat.html        # Page de résultats
```

## Méthodes implémentées

### Méthode du Grand M
- Ajoute une pénalité M très grande aux variables artificielles
- Plus simple à implémenter
- Peut avoir des problèmes de stabilité numérique avec certains problèmes

### Méthode à Deux Phases
- Phase 1: Minimiser la somme des variables artificielles
- Phase 2: Résoudre le problème original avec la solution de base réalisable trouvée
- Plus robuste numériquement
- Meilleure pour les problèmes avec des variables artificielles

## Exemple d'utilisation

**Maximiser**: Z = 3x₁ + 2x₂

**Sous les contraintes**:
- x₁ + x₂ ≤ 4
- 2x₁ + x₂ ≤ 5
- x₁, x₂ ≥ 0

## Auteur
SimplexPHP 2025
