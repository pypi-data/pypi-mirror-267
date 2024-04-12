# Algorithme génétique appliqué à l'entrée/sortie de l'autoencodeur variationnel pour la génération d'images

Le processus de sélection du logiciel CriminAI est effectué par l'algorithme génétique. Le principe utilisé est le suivant : l'autoencodeur fournit et travaille sur des données qui prennent la forme de vecteurs numériques à n dimensions. Les images sélectionnées par l'utilisateur sont donc chacunes représentées par un vecteur de coordonnées. L'algorithme génétique vient tout d'abord regrouper les vecteurs correspondant aux images sélectionnées par l'utilisateur à l'aide de différentes méthodes dont le choix est géré par l'utilisateur lui-même. Une fois regroupés en un seul vecteur de coordonnées, l'algorithme applique un bruit sur les coordonnées afin de générer une population, c'est-à-dire de nouveaux vecteurs correspondant à de nouvelles images, qui sont proches du vecteur et donc de l'image résultante du regroupement.
'
## Méthodes de regroupement :

### Méthode 1 : Centroïde

Les nouvelles images sont créées en calculant le centroïde de la liste de vecteurs donnée en paramètre, puis en appliquant un bruit aléatoire sur chaque coordonnée de ce centroïde pour obtenir un nombre de nouvelles images défini dans les paramètres de la méthode.

### Méthode 2 : Crossover

Les nouvelles images sont créées en générant un vecteur de coordonnées prises aléatoirement de la liste de vecteurs donnée en paramètre, puis en appliquant un bruit aléatoire sur chaque coordonnée de ce centroïde pour obtenir un nombre de nouvelles images défini dans les paramètres de la méthode.

### Méthode 3 : Bruit avant génération

Les nouvelles images sont créées en générant simplement du bruit autour des images sélectionnées.