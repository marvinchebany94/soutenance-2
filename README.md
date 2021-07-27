# soutenance-2
Script pour scraper un site de livre.

Ce script python va servir à scraper le site web suivant : https://books.toscrape.com/index.html

Qu'est ce que le scraping ? Ce terme désigne le fait d'extraire du contenu d'un site web de manière automatique via l'éxécution d'un script.

! La présentation sera faite sur windows !

Démarrage :

Le fichier contient 4 fichiers, 2 fichiers python : book_scraper.py et fonctions.py,  puis un fichier README et requirements.txt
Avant de lancer le script veillez à avoir télécharger python (voici une url pour le telecharger : https://www.python.org/downloads/ (prenez la dérnière version)

Le fichier requirments.txt est le fichier qui contient tous les modules utilisés par les scripts, sans ceux-là le script ne marche pas.

Le fichier README sert à comprendre comment utiliser le script.

On va maintenant télécharger le dossier entier via github. Le dossier sera un .zip, on va donc décompresser le dossier, puis le placer sur notre bureau.

	Ouvrez l'invite de commandes (écrivez cmd dans la barre de recherche en bas à gauche)
	
	Placez vous dans le répértoire ou se trouve les scripts (commande dir pour voir les répértoires présents, et cd pour se placer dedans)
	
	On crée notre environnement virtuel :
	
	python -m venv env (env est le nom de notre environnement)
	
	On active notre environnement :
	
	cd env/Scripts
	
	activate.bat ou activate
	
	Normalement avant le chemin de notre fichier il y aura (env)
	
	Le script ne peut pas marcher car il manque les modules, afin de les télécharger nous faisons cela :
	
	python -m pip install -r requirements.txt 

Maintenant tous les modules ont été installé, il ne vous reste plus qu'à découvrir l'utilisation du script

Utilisation du script:

! Veillez à entrer seulement 1 seul argument après le nom du script ou le script ne fonctionnera pas !

Le script que l'on utilise est book_scraper.py, fonctions.py contient seulement les fonctions servant à scraper etc. 
Le script a 3 utilisations différentes : 

	-permet de scraper un livre seulement
	
	-permet de scraper toute une catégorie + chaque livre
	
	-permet de scraper le site en entier
	
Pour scraper l'url d'un livre :

	-On ouvre l'invite de commandes (cmd)
	
	-on se place dans le dossier ayant les 2 scripts python
	
	- chemin/main.py https://books.toscrape.com/catalogue/civilization-and-its-discontents_140/index.html
	
	-Le script se lance et va créer un fichier portant le nom du livre dans le répértoire book, dans ce dossier 
		il y aura l'image (image.jpg) + un fichier csv livre.scv
		
Pour scraper l'url d'une catégorie entière : 

	-On ouvre l'invite de commandes (cmd)
	
	-on se place dans le dossier ayant les 2 scripts python
	
	- chemin/main.py https://books.toscrape.com/catalogue/category/books/psychology_26/index.html
	
	- Le script se lance et va créer un dossier portant la catégorie dans le répértoire catégorie, dans ce dossier il y aura les images (Les images auront le code universel du livre) + un fichier csv portant le nom de la catégorie

Pour scraper le site entier :

	-On ouvre l'invite de commandes (cmd)
	
	-on se place dans le dossier ayant les 2 scripts python
	
	- chemin/main.py -all
	
	-Le script se lance et va créer un dossier pour chaque catégorie comportant un fichier csv avec le nom de la catégorie, ainsi que toutes les images de la catégorie avec comme nom le code universel du livre.
	
	
