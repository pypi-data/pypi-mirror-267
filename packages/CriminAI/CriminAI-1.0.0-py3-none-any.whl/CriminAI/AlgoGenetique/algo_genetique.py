import random
import numpy as np

# Fonction pour appliquer du bruit à chaque vecteur
def add_noise(vector, noise_factor):
    """
    Ajoute du bruit à un vecteur en lui ajoutant une petite valeur aléatoire à chaque coordonnée.

    Args:
        vector (list(float)): Le vecteur auquel on veut appliquer du bruit.
        noise_factor (float): Le facteur de bruit que l'on souhaite appliquer lors de la génération de nouvelles coordonnées.

    Returns:
        list(float): Le vecteur avec un peu de bruit appliqué.
    """   
    noisy_vector = [coord + np.random.normal(0, noise_factor) for coord in vector]
    return noisy_vector


# Fonction pour initialiser une population de vecteurs avec un bruit à partir d'un vecteur initial
def create_new_photos(nombre_photos, base_vector, noise_factor):
    """
    Cette fonction prend en entrée un vecteur et génère plusieurs nouveaux vecteurs en appliquant un bruit aléatoire à chacune de ses coordonnées.

    Args:
        nombre_photos (float): Le nombre de photos que l'on veut générer.
        base_vector (list(float)): Le vecteur à partir duquel on veut générer une nouvelle population.
        noise_factor (float): Le facteur de bruit que l'on souhaite appliquer lors de la génération de nouvelles coordonnées.

    Returns:
        list(list(float)): Les coordonnées générées des nouvelles photos.
    """
    coordonnees_photos = []
    for _ in range(nombre_photos):
        new_vector = [add_noise(base_vector, noise_factor)]
        coordonnees_photos.append(new_vector)
    return coordonnees_photos

# Methode 1 : calcule le vecteur de coordonnées des centroides des vecteurs fournis puis génère une population de vecteurs
def photos_methode_centroide(nombre_photos, vectors, noise_factor=1):
    """
    Cette fonction génère les coordonnées de nouvelles photos à partir d'un vecteur de vecteurs de coordonnées.
    Dans cette fonction, les coordonnées des nouvelles photos sont générées en calculant le centroïde des vecteurs de la liste, puis en lui appliquant un bruit autant de fois que le nombre de photos que l'on souhaite générer.

    Args:
        nombre_photos (float): Le nombre de photos que l'on veut générer.
        vectors (list(list(float))): Les vecteurs de coordonnées sur lesquels appliquer l'algorithme génétique et générer la nouvelle population
        noise_factor (float, optional): Le facteur de bruit que l'on souhaite appliquer lors de la génération de nouvelles coordonnées. Vaut 1 par défaut.

    Returns:
        list(list(float)): Les coordonnées générées des nouvelles photos.
    """
    if len(vectors) == 0:
        return None  # Retourner None si la liste de vecteurs est vide
    dimensions = len(vectors[0])  # Nombre de dimensions
    centroid_vector = [0] * dimensions  # Initialiser le vecteur centroïde à zéro
    num_vectors = len(vectors)  # Nombre de vecteurs
    for vector in vectors:
        for i in range(dimensions):
            centroid_vector[i] += vector[i]  # Ajouter les coordonnées de chaque vecteur
    centroid_vector = [coord / num_vectors for coord in centroid_vector]  # Calculer la moyenne

    coords_photos = create_new_photos(nombre_photos, centroid_vector, noise_factor)
    return coords_photos

# Methode 2 : crée un nouveau vecteur composé des coordonnées de tous les vecteurs de manière aléatoire puis génère une population de vecteurs
def photos_methode_crossover(nombre_photos, vectors, noise_factor=1):
    """
    Cette fonction génère les coordonnées de nouvelles photos à partir d'un vecteur de vecteurs de coordonnées.
    Dans cette fonction, les coordonnées des nouvelles photos sont générées en croisant aléatoirement les coordonnées des vecteurs de la liste dans un seul vecteur puis en lui appliquant un bruit, autant de fois que le nombre de photos que l'on souhaite générer.

    Args:
        nombre_photos (float): Le nombre de photos que l'on veut générer.
        vectors (list(list(float))): Les vecteurs de coordonnées sur lesquels appliquer l'algorithme génétique et générer la nouvelle population
        noise_factor (float, optional): Le facteur de bruit que l'on souhaite appliquer lors de la génération de nouvelles coordonnées. Vaut 1 par défaut.

    Returns:
        list(list(float)): Les coordonnées générées des nouvelles photos.
    """
    new_vector = []
    for i in range(len(vectors[0])):
        coord = random.randint(0, len(vectors)-1)
        new_vector.append(vectors[coord][i])

    coords_photos = create_new_photos(nombre_photos, new_vector, noise_factor)
    return coords_photos

# Methode 3 : applique le bruit sur chacun des vecteurs avant le regroupement
def photos_methode_noise(nombre_photos, vectors, noise_factor=1):
    """
    Cette fonction génère les coordonnées de nouvelles photos à partir d'un vecteur de vecteurs de coordonnées.
    Dans cette fonction, les coordonnées des nouvelles photos sont générées en appliquant simplement du bruit sur les vecteurs d'entrée.

    Args:
        nombre_photos (float): Le nombre de photos que l'on veut générer.
        vectors (list(list(float))): Les vecteurs de coordonnées sur lesquels appliquer l'algorithme génétique et générer la nouvelle population
        noise_factor (float, optional): Le facteur de bruit que l'on souhaite appliquer lors de la génération de nouvelles coordonnées. Vaut 1 par défaut.

    Returns:
        list(list(float)): Les coordonnées générées des nouvelles photos.
    """
    # Appliquer du bruit à chaque vecteur
    noisy_vectors = [add_noise(vector, noise_factor) for vector in vectors]
    
    # Générer une population de nouveaux vecteurs à partir des vecteurs bruités
    new_vectors_population = []
    for _ in range(nombre_photos):
        # Pour chaque vecteur bruité, créer un nouveau vecteur en ajoutant un peu de bruit supplémentaire
        new_vector = [coord + np.random.normal(0, noise_factor) for coord in noisy_vectors[random.randint(0, len(noisy_vectors)-1)]]
        new_vectors_population.append(new_vector)
    
    return new_vectors_population

if __name__ == "__main__":
    vector_1 = [10,20,30,40,50,60]
    vector_2 = [7,73,42,901,52,6]
    vector_3 = [17,74,63,716,893,42]
    vector_4 = [643,27,10,4,746,123]
    vector_list = [vector_1,vector_2,vector_3,vector_4]

    vector_method1 = photos_methode_centroide(10, vector_list)
    vector_method2 = photos_methode_crossover(10, vector_list)
    vector_method3 = photos_methode_noise(10, vector_list)

    print(vector_method1)
    print(vector_method2)
    print(vector_method3)
