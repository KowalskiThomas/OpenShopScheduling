from random import randint
from copy import deepcopy
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

durees = [
    1,
    2,
    3,
    4,
    5
]

nbrEleves = 3
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

def construireEDT(solution):
    def estDisponibleEleve(eleve, heure, temps):
        for epreuve, heureEpreuve in eleve.items():
            if heure == -1:
                continue
            
            if heure <= heureEpreuve and heure + temps + pause > heureEpreuve:
                return False
            elif heure >= heureEpreuve and heureEpreuve + durees[epreuve] + pause > heure:
                return False

        return True

    def estDisponibleJury(jury, heure):
        numeroJury, orauxJury = jury["Numero"], jury["Oraux"]

        for oral, heureOral in orauxJury.items():
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

def perturbation(solution):
    solution = deepcopy(solution)

    indice = randint(0, len(solution) - 1)

    sousListe = solution[indice]
    sousIndice = randint(0, len(sousListe) - 2)
    sousListe[sousIndice], sousListe[sousIndice + 1] = sousListe[sousIndice + 1], sousListe[sousIndice]

    solution[indice] = sousListe

    return solution

def critere(solution, solutionPerturbee):
    print("test")

def solutionInitiale():
    sol = [[i for i in range(len(durees))]]
    
    for _ in range(len(durees)):
        sol += [[j for j in range(len(eleves))]]

    return sol

def afficher(patches, margin = 8):    
    plt.rcdefaults()
    fig, ax = plt.subplots()
    for p in patches:
        ax.add_patch(p)
    maxMachines = max(rect.get_y() for rect in patches) + 1
    maxJobs = max(rect.get_x() + margin for rect in patches)
    plt.axis([0, maxJobs, 0, maxMachines])
    plt.show()

def afficherEDT(EDT):
    patches = list()
    colors = ["black", "darksalmon", "DarkKhaki", "DarkViolet", "red", "blue", "green", "cyan", "magenta", "yellow", "black", "IndianRed", "Pink", "Lavender", "DarkOrange", "GreenYellow", "Teal", "SteelBlue", "MidnightBlue", "Maroon", "DimGray"]
    
    for i, prof in enumerate(EDT):
        if i == 0:
            continue
        for eleve, heure in prof.items():
            
            rekt = mpatches.Rectangle((heure, i), durees[i], 1, color = colors[eleve], ec = "black")
        
            patches.append(rekt)
        
    afficher(patches)

solution = solutionInitiale()
print(solution)
solution2 = perturbation(solution)
construireEDT(solution2)

print("Jurys")
print(jurys)
print("Eleves")
print(eleves)