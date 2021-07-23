#coding:utf-8
import sys
from fonction_02 import test_url,directories_exist,scraping_all_site, category_or_book

#On vérifie qu'il y a bien un argument passé au script
try:
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

#On regarde si la commande est une url ou -all
if url_or_commande == "-all":
    print("Tu vas telecharger tout le site.")
    all_categories_url = scraping_all_site()
    for url in all_categories_url:
        category_or_book(url)
else:
    print("On va voir si ton url est valide ou non.")
    directories_exist()
    test_url(url_or_commande)
    url = test_url(url_or_commande)
    category_or_book(url)


