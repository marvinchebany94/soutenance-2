#coding:utf-8
import requests
import sys,os,csv
import urllib.request
from PIL import Image
from bs4 import BeautifulSoup

#sert pour la première fonction test_url
url_basique = 'http://books.toscrape.com/'

#Variable qui donne le current path
current_path = sys.argv[0]
current_path = os.path.dirname(current_path)

#creation de liste vide pour savoir si la catégorie a déjà été créée
global category_already_exists
category_already_exists = []

liste_url = []

#Verification de l'url
def test_url(url_to_test):
    """


    :param url_to_test:
    :return:
    """
    if "https://books.toscrape.com/" in url_to_test or url_basique in url_to_test:

        #Global r pour que la variable r soit reprise en dehors de la fonction
        global r
        r = requests.get(url_to_test)
        if r.status_code == 200:
            print("L'url fonctionne.")
        else:
            print("l'url n'est pas valide.")
            sys.exit()
    else:
        print("L'url ne correspond pas à celles du site.")
        sys.exit()

    global url
    url = url_to_test
    global liste_url

    #on va voir si l'url provient d'un livre, ou d'une catégorie
    if 'category' in url_to_test:
        print("La page correspond à une liste de plusieurs livres")

        find_category(url_to_test)
        books_url(url_to_test)
        count_page(url_to_test)
        for book in liste_url:
            book_scraping(book, "category")

    else:
        print("L'url correspond à un livre seulement.")
        book_scraping(url_to_test, "book")

    # on vide la liste d'url au cas ou la personne scrap tout le site entier
    liste_url = []
#vérification des repertoires obligatoires au bon fonctionnement
def directories_exist():
    if os.path.exists(current_path+"\\book"):
        print("Le repertoire book existe.")
    else:
        print("Le repertoire book n'existe pas, le script le crée pour vous.")
        os.mkdir(current_path+"\\book")

    if os.path.exists(current_path+"\\catégorie"):
        print("Le repertoire catégorie existe.")
    else:
        print("Le repertoire catégorie& n'existe pas, le script le crée pour vous.")
        os.mkdir(current_path+"\\catégorie")

#dans le cas ou l'url provient d'une page de catégorie, on prendra l'url de tous les livres de la page
def books_url(url_to_test):
    #On note l'url de base à placer devant les href
    url_base = "https://books.toscrape.com/catalogue/"
    req = requests.get(url_to_test)
    #on crée un object soup avec la variable R qui a été crée dans la fonction test_url
    soup = BeautifulSoup(req.content, features="html.parser")

    #on va chercher l'endroit ou se trouve toutes les url des livres de la catégorie
    url_endroit = soup.find('ol')
    urls = url_endroit.findAll('a')
    #on va faire une boucle pour chaque livre présent dans la catégorie et noter l'url dans une liste
    global liste_url
    for url in urls:
        #comme les urls apparaissent deux fois on crée une variable qui les recupere, si l'url est dedans elle sera
        #ignorée
        url = url_base+url['href'][9:]
        if url not in liste_url:
            url_liste = url
            #On commence à la 8eme position car avant il y ../../..
            print(url)
            liste_url.append(url)
        else:
            continue
    print("\n")
#On voit si notre page posséde plusieurs pages ou non
def count_page(page_to_count):
    #on recupére le nombre de page
    req = requests.get(page_to_count)
    soup = BeautifulSoup(req.content, features="html.parser")
    try:
        resultat = soup.find('li', class_='current').text
        resultat = resultat.split()
        resultat = int(resultat[3])
        print(resultat)
        print('\n')

        # On reprend l'url et on change la fin de celle-ci pour atteindre les autres pages
        i = 1
        url__ = url[0:-10]
        while i < resultat:
            i += 1
            url_finale = url__ + "page-" + str(i) + ".html"
            books_url(url_finale)
    except:
        print("La catégorie ne contient pas plusieurs pages.")
        books_url(page_to_count)

#on va trouver la catégorie de la page
def find_category(url_to_scrap):
    req = requests.get(url_to_scrap)
    soup = BeautifulSoup(req.content, features="html.parser")
    global category_
    #category_ = soup.findAll('a')[3].text
    category_ = soup.find("h1").text
    print("la catégorie est : {}".format(category_))

    #on va voir si la catégorie est déjà enregistrée dans l'ordinateur
    if os.path.exists(current_path+"\\catégorie\\"+category_):

        print("Tu as déjà enregistré cette catégorie.")
        sys.exit()

    else:
        try:
            os.mkdir(current_path+"\\catégorie\\"+category_)
        except:
            print("Ton dossier n'a pas été créé.")
            sys.exit()

#on va créer la fonction qui va scraper les url
def book_scraping(book_url, category_or_book):

    # on cree un object soup pour parser le code html
    if category_or_book == "book":
        soup = BeautifulSoup(r.content, features="html.parser")
    else:
        req = requests.get(book_url)
        soup = BeautifulSoup(req.content, features="html.parser")

    # On va maintenant créer la recherche pour chaque infos demandées et créer une liste avec tous les elements

    product_page_url = book_url
    universal_product_code = soup.findAll('td')[0].text

    global title
    title = soup.find('h1').text

    price_including_taxe = soup.findAll('td')[2].text
    price_including_taxe = price_including_taxe[1:]

    price_exluding_taxe = soup.findAll('td')[3].text
    price_exluding_taxe = price_exluding_taxe[1:]

    number_available = soup.findAll('td')[5].text
    number_available = number_scrap(number_available)

    product_description = soup.findAll('p')[3].text
    category = soup.findAll('a')[3].text

    review_rating = soup.findAll('p')[2]
    review_rating = note_book(review_rating)

    url_basique = 'http://books.toscrape.com/'

    image_url = soup.find('img')
    image_url = image_url['src'][6:]
    image_url_ = url_basique + image_url

    if category_or_book == "book":
        path = current_path + "\\book\\"
        dir = path + clean_title(book_url)

        try:
            os.mkdir(dir)
        except FileExistsError:
            print("Probleme lors de la creation du repertoire, le fichier existe déjà.")
            sys.exit()
    else:
        path = current_path + "\\catégorie\\"
        dir = path + category

    if category_or_book == "book":
        fichier = dir + '\\' + 'livre.csv'
    else:
        fichier = dir + '\\' + category + '.csv'
    # On crée le fichier csv
    with open(fichier, 'a', newline='', encoding="utf-8") as f:

        # on crée les colonnes avec les noms indiqués
        fieldnames = ['product_page_url', 'universal_product_code', 'title', 'price_including_taxe',
                      'price_excluding_taxe', 'number_available', 'product_description', 'category',
                      'image_url', 'review_rating']

        writer = csv.DictWriter(f, fieldnames=fieldnames)
        #si la catégorie est dans la liste, on ne crée plus de colonnes
        if category not in category_already_exists:
            writer.writeheader()
        else:
            pass

        # on va mettre le nom de la catégorie dans la variable des catégories déjà créés
        category_already_exists.append(category)

        writer.writerow(
            {'product_page_url': book_url, 'universal_product_code': universal_product_code, 'title': title,
             'price_including_taxe': price_including_taxe, 'price_excluding_taxe': price_exluding_taxe,
             'number_available': number_available, 'product_description': product_description,
             'category': category, 'image_url': image_url_,
             'review_rating': review_rating})

    img = Image.open(requests.get(image_url_, stream=True).raw)
    if category_or_book == 'book':
        fichier_img = dir + '\\' + 'image.jpg'
    else:
        fichier_img = dir + '\\' + universal_product_code + '.jpg'

    urllib.request.urlretrieve(image_url_, fichier_img)
    print('''
        Votre livre a bien été enregistré ainsi que sa page de couverture.
        Retrouvez le fichier csv et la couverture à l'endroit suivant : {}
        '''.format(dir))

#fonction qui va enlever les caracteres spéciaux des titres
def clean_title(url_to_take_title):

    title = url_to_take_title.split('/')
    title = title[4:][0]
    title = title.split('_')[0]
    title = title.split('-')
    title_clean = ' '.join(title)
    print(title_clean)

    return title_clean

def number_scrap(obj_soup):
    #on crée un algorithme qui va verifier chaque caractére de l'object soupe
    #s'il n'y a pas de nombre, il passe, s'il voit un chiffre il l'ajoute dans une variable afin d'avoir seulement
    #le nombre de livre restant

    #La variable contenant le nombre de livres disponibles. (Sous forme de liste qu'on va joindre à la fin)
    number_available = []
    for caractere in obj_soup:
        if caractere.isnumeric():
            number_available.extend(caractere)
        else:
            continue
    number_available = ''.join(number_available)
    return number_available

def note_book(obj_soup):
    #On crée un algoright qui va scraper tous les paragraphes, la note se trouve dans le paragraphe 3
    #La note est écrite en lettre et en anglais, on va donc vérifier que one/two/three/four/five
    #se trouve bien dans le texte, et pour chacun de ses mots on assignera un chiffre
    obj_soup = str(obj_soup)
    if 'One' in obj_soup:
        note = 1
    elif 'Two' in obj_soup:
        note = 2
    elif 'Three' in obj_soup:
        note = 3
    elif 'Four' in obj_soup:
        note = 4
    elif 'Five' in obj_soup:
        note = 5
    else:
        note = "Aucune note n'a été trouvée"
    return note

def scraping_all_site():
    obj_req = requests.get("https://books.toscrape.com/index.html")
    soup = BeautifulSoup(obj_req.content, features="html.parser")
    url_categories = soup.find("ul", class_="nav nav-list")
    url_categories = url_categories.findAll("li")
    for url_categorie in url_categories:
        url_finale = url_basique + url_categorie.a['href']
        if 'books_1' not in url_finale:
            test_url(url_finale)
        else:
            pass