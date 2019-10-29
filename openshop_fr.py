from random import randint, random
from copy import deepcopy
import numpy as np
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

durees = [
    1,
    2,
    3,
    4,
    5
]

nbrEleves = 4
pause = 1

eleves = [
    {
        i : -1 
        for i in range(len(durees))
    } 
    for j in range(nbrEleves)
    ]

jurys = [
    {
        "Numero" : j,
        "Oraux" : {
            i : -1 
            for i in range(len(eleves))
        }
    } 
    for j in range(len(durees))
    ]

def construireEDT(solution, jurysVides, elevesVides):
    '''
    Construit l'EDT induit par `solution` selon un algorithme glouton.
    
    `jurysVides` et `elevesVides` doit contenir des dictionnaires correspondants aux jurys et élèves à qui il faut assigner les oraux, vides (c'est à dire dont les heures des oraux sont toutes `-1`)
    
    *Aucun paramètre n'est modifié, afin qu'aucune copie des variables originales `jurysVides` et `elevesVides` n'aient à être faites en dehors de la fonction.*
    ''' 
    jurys = deepcopy(jurysVides)
    eleves = deepcopy(elevesVides)

    def estDisponibleEleve(eleve, heure, temps):
        '''
        Renvoie vrai si l'élève `eleve` est disponible à `heure` pendant au moins `temps + pause` unités de temps.
        ''' 
        for epreuve, heureEpreuve in eleve.items():
            if heureEpreuve == -1:
                continue
            
            if heure <= heureEpreuve and heure + temps + pause > heureEpreuve:
                return False
            elif heure >= heureEpreuve and heureEpreuve + durees[epreuve] + pause > heure:
                return False

        return True

    def estDisponibleJury(jury, heure):
        '''
        Renvoie vrai si `jury` est disponible à `heure` pendant autant d'unités de temps que son épreuve dure.
        '''
        numeroJury, orauxJury = jury["Numero"], jury["Oraux"]

        for _, heureOral in orauxJury.items():
            if heureOral == -1:
                continue

            if heure <= heureOral and heure + durees[numeroJury] > heureOral:
                return False
            elif heureOral <= heure and heureOral + durees[numeroJury] > heure:
                return False

        return True

    ordreJurys, *ordres = solution

    for j in ordreJurys:
        tousAssocies = False
        t = 0
        while not tousAssocies:
            tousAssocies = [jurys[j]["Oraux"][i] != -1 for i in range(nbrEleves)] == [True for i in range(nbrEleves)]
            place = False
            for eleve in ordres[j]:
                if jurys[j]["Oraux"][eleve] != -1:
                    continue

                if estDisponibleEleve(eleves[eleve], t, durees[j]):
                    if estDisponibleJury(jurys[j], t):
                        place = True
                        eleves[eleve][j] = t
                        jurys[j]["Oraux"][eleve] = t
                        break

            if not place:
                t += 1
            else:
                t += durees[j]        

    return jurys, eleves

def duree(jurys):
    '''
    Calcule la durée de l'emploi du temps représenté par la liste de jurys `jurys`.
    '''
    maxFin = 0
    for jury in jurys:
        numeroJury, oraux = jury["Numero"], jury["Oraux"]
        for numeroEleve, heureOral in oraux.items():
            if heureOral + durees[numeroJury] > maxFin:
                maxFin = heureOral + durees[numeroJury]

    return maxFin

def perturbation(solution):
    '''
    Effectue une perturbation sur `solution`.
    Pour cela, on choisit au hasard un des chromosomes (le modèle vient de l'algorithme génétique) et on inverse deux allèles à l'intérieur.

    __Exemple :__
    * `Avant : 123 1234 1234 1234`
    * `Après : 123 1243 1234 1234`

    Seul un chromosome est modifié, afin d'avoir une incidence limitée sur la solution.
    '''
    solution = deepcopy(solution)

    indice = randint(0, len(solution) - 1)

    sousListe = solution[indice]
    sousIndice = randint(0, len(sousListe) - 2)
    sousListe[sousIndice], sousListe[sousIndice + 1] = sousListe[sousIndice + 1], sousListe[sousIndice]

    solution[indice] = sousListe

    return solution

def critere(solution, solutionPerturbee, T, constante):
    '''
    Applique le critère de Metropolis avec la température `T` et la constante de Boltzmann `constante` et renvoie la solution qui doit être conservée (choix entre `solution` et `solutionPerturbee`).
    '''
    alea = random()

    edtSolution = construireEDT(solution, jurys, eleves)[0]
    edtSolutionPerturbee = construireEDT(solutionPerturbee, jurys, eleves)[0]

    diffMakespan = duree(edtSolutionPerturbee) - duree(edtSolution)

    if diffMakespan <= 0:
        return solutionPerturbee
    else:
        if alea < np.exp(-1 * diffMakespan / (constante * T)):
            return solutionPerturbee
        else:
            return solution

def solutionInitiale():
    '''
    Renvoie une solution initiale correspondant à une solution naïve :

    `12...p 12...n 12...n (p fois)`
    '''
    sol = [[i for i in range(len(durees))]]
    
    for _ in range(len(durees)):
        sol += [[j for j in range(len(eleves))]]

    return sol

def afficher(patches, margin = 8):
    '''
    Affiches les rectangles dans `patches` dans une fenêtre `MatPlotLib`.
    Cette fonction ne devrait pas être appelée directement mais à travers `afficherEDT`.
    '''
    plt.rcdefaults()
    fig, ax = plt.subplots()
    for p in patches:
        ax.add_patch(p)
    maxMachines = max(rect.get_y() for rect in patches) + 1
    maxJobs = max(rect.get_x() + margin for rect in patches)
    plt.axis([0, maxJobs, 0, maxMachines])
    plt.show()

def afficherEDT(EDT):
    '''
    Affiche l'emploi du temps `EDT` qui est en fait une liste de dictionnaires-jurys.
    '''
    patches = list()
    colors = ["black", "darksalmon", "DarkKhaki", "DarkViolet", "red", "blue", "green", "cyan", "magenta", "yellow", "black", "IndianRed", "Pink", "Lavender", "DarkOrange", "GreenYellow", "Teal", "SteelBlue", "MidnightBlue", "Maroon", "DimGray"]
    
    for i, prof in enumerate(EDT):
        prof = prof["Oraux"]
        for eleve, heure in prof.items():
            rekt = mpatches.Rectangle((heure, i), durees[i], 1, color = colors[eleve], ec = "black")
            patches.append(rekt)

    afficher(patches)

def recuitSimule(temperature = 1000,
                 decroissance = lambda x : x - 10,
                 constante = 100):
    '''
    Applique l'algorithme du recuit simulé avec la température initiale `temperature`, la loi de décroissance `decroissance` et la constante de Boltzmann `constante`.
    '''

    solution = solutionInitiale()
    while temperature > 10:
        solutionPrime = perturbation(solution)
        solution = critere(solution, solutionPrime, temperature, constante)
        temperature = decroissance(temperature)

    edt = construireEDT(solution, jurys, eleves)[0]
    return edt

# Pour garantir les meilleurs résultats possibles, on recommence plusieurs fois l'optimisation par recuit simulé.
recommencements = 100
minDuree = float('inf')
meilleureEDT = None
for i in range(recommencements):
    edt = recuitSimule()
    if duree(edt) < minDuree:
        meilleurEDT = edt

afficherEDT(meilleurEDT)
