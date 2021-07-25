#coding:utf-8
import sys
from fonction import test_url,directories_exist,scraping_all_site, category_or_book,find_category,count_page,\
    books_url, book_scraping, category_directory_creating

"""
Ce script va prendre en compte le paramétre qui sera donné au lancement.
Le script peut réaliser 3 choses :
    -scraper un seul livre
    -scraper tous les livres d'une catégorie précisée
    -scraper tout le site grâce à la commande -all
"""

try:
    """
    On vérifie l'existence d'un argument passé au script.
    """
    sys.argv[1]
except:
    print("Tu dois entrer une url ou bien la commande -all pour télécharger tout le site.")
    sys.exit()
#on regarde s'il y a plus qu'un seul argument
if len(sys.argv) != 2:
    print("Tu dois entrer seulement un argument")
    sys.exit()
else:
    """
    On crée une variable qui prendra la valeur de l'argument passé après le script
    """
    url_or_commande = sys.argv[1]

if url_or_commande == "-all":
    print("Tu vas telecharger tout le site.")
    all_categories_url = scraping_all_site()
    for link in all_categories_url:
        test_url(link)
        url = test_url(link)
        url_type = category_or_book(link)
        category = find_category(link)
        category_already_registred = category_directory_creating(category)
        if category_already_registred == "no":
            liste_url_page = count_page(link)
            print(liste_url_page)
            for page in liste_url_page:
                books_url(page)
                liste_url = books_url(page)
                for book in liste_url:
                    book_scraping(book, url_type)
        else:
            pass
else:
    print("On va voir si ton url est valide ou non.")
    directories_exist()
    test_url(url_or_commande)
    url = test_url(url_or_commande)
    url_type = category_or_book(url)
    if url_type == "category":
        category = find_category(url)
        category_already_registred = category_directory_creating(category)
        if category_already_registred == "no":
            liste_url_page = count_page(url)
            print(liste_url_page)
            for page in liste_url_page:
                liste_url = books_url(page)
                for book in liste_url:
                    book_scraping(book, "category")
        else:
            pass
    else:
        book_scraping(url, url_type)


