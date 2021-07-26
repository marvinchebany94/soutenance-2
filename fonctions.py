#coding:utf-8
import requests
import sys,os,csv
import urllib.request
from PIL import Image
from bs4 import BeautifulSoup

#sert pour la première fonction test_url
URL_HTTP = 'http://books.toscrape.com/'
URL_HTTPS = 'https://books.toscrape.com'

#Variable qui donne le current path
current_path = sys.argv[0]
current_path = os.path.dirname(current_path)

#creation de liste vide pour savoir si la catégorie a déjà été créée
global category_already_exists
category_already_exists = []

def test_url(url_to_test):
    """
    Cette fonction va servir à tester l'url qui a été passé en paramétre,
    :param url_to_test: On passe en paramétre l'url que l'on veut scraper.
    :return: La fonction retourne simplement l'url passé en paramétre
    """
    if URL_HTTPS in url_to_test or URL_HTTP in url_to_test:

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

    return url_to_test

def category_or_book(url):
    """
    La fonction vérifie si l'url correspond à un livre ou à une catégorie
    :param url: Le paramétre correspond à l'url que tu veux scraper
    :return: La fonction retourne "book" ou "category"
    """

    if 'category' in url:
        print("La page correspond à une liste de plusieurs livres")
        type_url = "category"

    else:
        print("L'url correspond à un livre seulement.")
        type_url = "book"

    return type_url

def directories_exist():
    """
    Cette fonction sert à vérifier que les répértoires book et catégorie existent.
    Si ce n'est pas le cas la fonction les crée pour nous.
    """
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

def books_url(url_to_test):
    """
    Cette fonction sert à récupérer toutes les url des livres correspondant à la catégorie
    souhaitée.
    Les url recupérées iront dans une liste nommée liste_url qui nous servira dans d'autres fonctions.
    :param url_to_test: Le paramétre attendu pour cette variable est l'url d'une page de catégorie.
    :return: La fonction retourne la liste liste_url qui a toutes les url de la catégorie
    """
    #On note l'url de base à placer devant les href
    url_base = "https://books.toscrape.com/catalogue/"
    req = requests.get(url_to_test)
    #on crée un object soup avec la variable R qui a été crée dans la fonction test_url
    soup = BeautifulSoup(req.content, features="html.parser")

    #on va chercher l'endroit ou se trouve toutes les url des livres de la catégorie
    url_endroit = soup.find('ol')
    urls = url_endroit.findAll('a')

    #La var liste_url est une liste qui contiendra toutes les url de la page
    liste_url = []

    #on va faire une boucle pour chaque livre présent dans la catégorie et noter l'url dans une liste
    for url in urls:
        #comme les urls apparaissent deux fois on crée une variable qui les recupere, si l'url est dedans elle sera
        #ignorée
        url = url_base + url['href'][9:]
        if url not in liste_url:

            #On commence à la 9eme position car avant il y ../../..
            liste_url.append(url)
        else:
            continue

    print("\n")
    return liste_url

def count_page(page_to_count):
    """
    Cette fonction sert à compter le nombre de page d'une catégorie.
    Pour chaque page trouvée la fonction books_url sera utilisée en lui passant l'url trouvée
    en paramétre.
    :param page_to_count: Le paramétre attendu pour cette fonction est une url menant à une page de catégorie.
    """
    #Liste qui contient les url d'une page catégorie
    liste_url_page = [page_to_count]

    #on recupére le nombre de page
    req = requests.get(page_to_count)
    soup = BeautifulSoup(req.content, features="html.parser")
    try:
        resultat = soup.find('li', class_='current').text
        resultat = resultat.split()
        resultat = int(resultat[3])
        print(resultat)
        print('\n')

        #on crée une liste liste_url_page qui contiendra les url des pages

        # On reprend l'url et on change la fin de celle-ci pour atteindre les autres pages
        i = 1
        url = page_to_count[0:-10]
        while i < resultat:
            i += 1
            url_finale = url + "page-" + str(i) + ".html"
            liste_url_page.append(url_finale)

    except:
        print("La catégorie ne contient pas plusieurs pages.")

    return liste_url_page


def find_category(url_to_scrap):
    """
    Cette fonction sert à trouver la catégorie d'une url de catégorie.
    :param url_to_scrap: Le paramétre correspond à une url de catégorie.
    :return: La fonction retourne le nom de la catégorie
    """
    req = requests.get(url_to_scrap)
    soup = BeautifulSoup(req.content, features="html.parser")

    category_ = soup.find("h1").text
    print("la catégorie est : {}".format(category_))
    return category_

def category_directory_creating(category):
    """
    Cette fonction vérifie l'existence d'un dossier portant la catégorie passée en argument.
    :param category: Le paramétre correspond au nom de la catégorie que vous voulez vérifier.
    :return: La fonction retourne "yes" si la catégorie existe, "no" si la catégorie n'existe pas.
    """

    #on va voir si la catégorie est déjà enregistrée dans l'ordinateur
    if os.path.exists(current_path+"\\catégorie\\"+category):

        print("Tu as déjà enregistré cette catégorie.")
        #sys.exit()
        category_already_registred = "yes"
    else:
        category_already_registred = "no"
        try:
            os.mkdir(current_path+"\\catégorie\\"+category)
        except:
            print("Ton dossier n'a pas été créé.")
            sys.exit()
    return category_already_registred

def book_scraping(book_url, category_or_book):
    """
    Cette fonction va avoir plusieurs fonctions. Dans un premier temps elle va scraper
    le site en allant chercher plusieurs informations (tittre, prix, catégorie etc.)
    Elle va ensuite créer un fichier csv dans le répértoire correspondant à si l'url
    est une url de livre ou une url de catégorie.
    Puis pour finir elle va telecharger l'image et la placer dans le dossier correspondant à son livre.
    Pour chaque livre la fonction nous indiquera le chemin ou les fichiers se trouvent.
    :param book_url: Ce paramétre correspond à l'url d'un livre et non d'une catégorie.
    :param category_or_book: Ce paramétre servira a définir les dossiers ou arriveront les fichiers csv et jpg.
    Si le param est catégory les fichiers iront dans le dossier "catégorie" et seront dans un dossier
    portant le nom de la catégorie.
    Si le param est book, le fichier csv ira dans le dossier "book" dans un dossier portant le nom du livre.
    """
    # on cree un object soup pour parser le code html
    if category_or_book == "book":
        soup = BeautifulSoup(r.content, features="html.parser")
    else:
        req = requests.get(book_url)
        soup = BeautifulSoup(req.content, features="html.parser")

    # On va maintenant créer la recherche pour chaque infos demandées et créer une liste avec tous les elements

    product_page_url = book_url
    universal_product_code = soup.findAll('td')[0].text

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

    image_url = soup.find('img')
    image_url = image_url['src'][6:]
    image_url_ = URL_HTTP + image_url

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


def clean_title(url_to_take_title):
    """
    Cette fonction sert à récupérer le titre d'un livre sans caractéres spéciaux
    pour créer les dossiers/fichiers sans problème.
    :param url_to_take_title: Le paramétre doit être l'url d'un livre et non d'une catégorie.
    :return: La fonction retourne la variable title_clean qui correspond au titre du livre sans
    caractéres spéciaux.
    """
    title = url_to_take_title.split('/')
    title = title[4:][0]
    title = title.split('_')[0]
    title = title.split('-')
    title_clean = ' '.join(title)
    print(title_clean)

    return title_clean

def number_scrap(obj_soup):
    """
    on crée un algorithme qui va verifier chaque caractére de l'object soup,
    s'il n'y a pas de nombre, il passe, s'il voit un chiffre il l'ajoute dans une variable afin d'avoir seulement
    le nombre de livre restant.
    :param obj_soup: Le paramétre correspond à la variable soup crée dans la fonction book_scraping nommé
    number_available.
    :return: La fonction retourne une variable indiquant un chiffre (le nombre de livres disponibles)
    """
    #

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
    """
    On crée un algoright qui va scraper tous les paragraphes, la note se trouve dans le paragraphe 3.
    La note est écrite en lettre et en anglais, on va donc vérifier que one/two/three/four/five
    se trouve bien dans le texte, et pour chacun de ses mots on assignera un chiffre.
    :param obj_soup: Le paramétre correspond à la variable review_rating de la fonction book_scraping.
    :return: Retourne la variable note qui nous donne un chiffre allant de 1 à 5.
    """

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
    """
    Cette fonction sert à scraper les url des catégories de tout le site.
    Pour éviter de prendre en compte la 1ere url qui n'est pos une catégorie on vérifie si books_1 se trouve dedans.
    Si ce n'est pas le cas la fonction test_url se lance pour chaque url de catégorie trouvée.
    """
    obj_req = requests.get("https://books.toscrape.com/index.html")
    soup = BeautifulSoup(obj_req.content, features="html.parser")
    url_categories = soup.find("ul", class_="nav nav-list")
    url_categories = url_categories.findAll("li")

    #on crée une liste qui prendra toutes les url de catégorie du site
    all_categories_url = []
    for url_categorie in url_categories:
        url_finale = URL_HTTP + url_categorie.a['href']
        if 'books_1' not in url_finale:
            all_categories_url.append(url_finale)
        else:
            pass
    return all_categories_url