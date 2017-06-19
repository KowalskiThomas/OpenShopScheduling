# Optimisation d'oraux de concours 

## Présentation 
Pour optimiser des emplois du temps d'oraux de concours, on peut utiliser cette adaptation de l'algorithme du recuit simulé utilisant le modèle introduit par Benjamin Rabdeau pour son optimisation par algorithme génétique.

## Fonctionnement
On souhaite optimiser une solution au problème d'ordonnancement *open-shop* suivant.
* *n* objets (*jobs*) qui représentent les candidats
* *p* machines qui représentent les jurys

Optimiser une solution à ce problème peut se faire en utilisant la représentation sous forme de graphes connus dans la littérature, mais aussi en utilisant un modèle sous forme de chromosomes. 
Dans celui-ci, on modélise une solution par *p + 1* chrosomes. Le premier correspond à l'ordre d'affectation des oraux aux jurys, les *p* suivants à l'ordre d'affectation des candidats pour chaque jury. 

Par exemple, un tel gène :

```
123 1234 4231 2314
```
Signifie 
``` 
123  : on créé les emplois du temps des jurys dans l'ordre 1, 2, 3
1234 : pour le premier jury, on affecte les élèves dans l'ordre 1, 2, 3, 4
1234 : pour le second jury, on affecte les élèves dans l'ordre 4, 3, 2, 1
1234 : pour le troisième jury, on affecte les élèves dans l'ordre 2, 3, 1, 4
```
Pour apporter une perturbation à une solution (nécessaire pour l'algorithme du recuit simulé) on prend un gène au hasard et on transpose deux allèles. Par exemple, 
```
123 12*34* 4231 2314
```
Peut devenir
```
123 12*43* 4231 2314
```
(Modification au niveau des étoiles.)
## Annexe : algorithme de reconstruction
Pour construire une solution à partir d'un chromosome, on utilise un algorithme glouton fonctionnant comme décrit ci-après. On divise le problème global en *p* problèmes locaux d'optimalité pour chaque jury. 
On "remplit" l'emploi du temps de chaque jury (dans l'ordre donné par le premier gène). 

Pour ce faire, on lit le gène correspondant au jury dont on souhaite construire l'emploi du temps et on place les candidats dans l'ordre que le gène donne. 
Pour assurer la consistence de la solution fournie (éviter que deux jurys soient avec le même élève en même temps, ou le deux élèves avec le même jury en même temps), on vérifie avant de placer un oral que l'élève et le jury ne sont pas "ailleurs" à cet instant dans les emplois du temps des autres jurys déjà affectéss. 

## Questions / Remarques
A adresser à Thomas Kowalski (thomaskowalski [at] outlook [dot] com)