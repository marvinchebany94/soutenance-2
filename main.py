#coding:utf-8
import sys
from fonction import test_url,directories_exist,scraping_all_site

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
    commande = sys.argv[1]

#On regarde si la commande est une url ou -all
if commande == "-all":
    print("Tu vas telecharger tout le site.")
    scraping_all_site()
else:
    print("On va voir si ton url est valide ou non.")
    directories_exist()
    test_url(commande)


