# soutenance-2
Script pour scraper un site de livre.

Ce script python va servir à scraper le site web suivant : https://books.toscrape.com/index.html
Qu'est ce que le scraping ? Ce terme désigne le fait d'extraire du contenu d'un site web de manière automatique via l'éxécution d'un script.

! Ce script fonctionne exclusivement avec windows !

Démarrage :

Le fichier contient 4 fichiers, 2 fichiers python : main.py et fonction.py,  puis un fichier README et requirements.txt
Avant de lancer le script veillez à avoir télécharger python (voici une url pour le telecharger : https://www.python.org/downloads/ (prenez la dérnière version)

Le fichier requirments.txt est le fichier qui contient tous les modules utilisés par les scripts, sans ceux-là le script ne marche pas.
	Ouvrez l'invite de commande (écrivez cmd dans la barre de recherche en bas à gauche)
	
	Placez vous dans le répértoire ou se trouve les scripts (commande dir pour voir les répértoires présents, et cd pour se placer dedans)
	
	Une fois dedans faites python -m pip install -r requirements.txt (La commande va telecharger tous les modules obligatoires au bon fonctionnement du script)

Maintenant tous les modules ont été installé, il ne vous reste plus qu'à découvrir l'utilisation du script

Utilisation du script:

Le script que l'on utilise est main.py, fonction.py contient seulement les fonctions servant à scraper etc. 
Le script a 3 utilisations différentes : 
	-permet de scraper un livre seulement 
	-permet de scraper toute une catégorie + chaque livre
	-permet de scraper le site en entier
