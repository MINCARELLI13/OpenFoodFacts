# coding: utf-8

print()

""" Categories proposed to users """
categories = ['Snacks salés', 'Gâteaux', 'Sodas', 'Desserts glacés', 'Plats préparés']

# number of products to load per category
products_nb = 10

""" user of MySQL """
user = 'root'

""" password of connexion to SQL """
password = '123ab456'

""" host of connexion to SQL """
host = 'localhost'
 
""" database used """
database = 'BDD_OFF'

""" begin of URL of API """
url = 'https://fr.openfoodfacts.org/cgi/search.pl'

""" fields of the products to load """
fields_of_products = ('url', 'product_name_fr',
                    'brands', 'nutrition_grade_fr',
                    'ingredients_text_fr', 'stores')

name_of_product_fields = ('nom', 'marque', 'url', 'nutriscore', 'ingrédients', 'magasins')
