## Instructions d'installation du logiciel

    1) Ouvrir un terminal 
    2) Aller dans le dossier où on veut mettre l’application
    3) Créer un environnement virtuel : python3 -m venv CriminAI
    4) Aller dans l’environnement virtuel : cd CriminAI
    5) Activer l’environnement virtuel : source bin/activate
    6) Créer un fichier avec l’extension .py : touch appli.py (par exemple, le nom peut changer ; il ne faut juste pas que le nom soit le même que celui du package, à savoir CriminAI.py)
    7) L’ouvrir et écrire ces deux lignes : 
    from CriminAI import mainWindow
    mainWindow()
    8) Enregistrer et fermer le fichier.
    9) Dans le terminal, taper /Applications/Python et faire tab pour que le terminal autocomplète avec la bonne version de Python, puis ajouter /Install\ Certificates.command
    Cela donne par exemple pour Python 3.12 : /Applications/Python\ 3.12/Install\ Certificates.command
    10) Puis installer le package via PyPi : pip install CriminAI
    11) Enfin, lancer l'application : python3 appli.py (pour notre cas, adapter le nom en fonction)