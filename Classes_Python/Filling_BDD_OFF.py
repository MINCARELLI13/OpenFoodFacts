import requests
import mysql.connector
import config
from Create_Tables_BDD_OFF import Tables_BDD_OFF    # ligne à supprimer !!!

print()

# !!!  Supprimer ces 3 lignes avant la présentation  !!!
# Tables = Tables_BDD_OFF()
# Tables.drop_all_tables_BDD_OFF()
# Tables.create_all_tables_BDD_OFF()

class Filling_of_BDD_OFF:
    """ Creation and loading of the tables of the database BDD_OFF """

    # def __init__(self, cnx, cursor):
    def __init__(self):
        """ connection to SQL """
        # Tables_BDD_OFF.__init__(self, cnx, cursor)
        self.Tables = Tables_BDD_OFF()
        self.Categories_id = {}
        self.reinitialisation_of_tables()
        self.insertion_fields_of_Category()
        self.research_id_of_categories()
        self.filling_table_Product()
        # self.cnx = self.Tables.cnx
        # self.cursor = self.Tables.cursor


    def reinitialisation_of_tables(self):
        """ Drop all tables of database BDD_OFF and recreate them """
        self.Tables.drop_all_tables_BDD_OFF()
        self.Tables.create_all_tables_BDD_OFF()

    def insertion_fields_of_Category(self):
        """ Insertion of the types of categories in database BDD_OFF
        (Snacks salés, Gâteaux, Sodas...) """
        for catg in config.categories:
            query = f"INSERT INTO Category (name) VALUES ('{catg}')"
            self.Tables.cursor.execute(query)
            self.Tables.cnx.commit()

    def research_id_of_categories(self):
        """ researching id's of 'Category' table of BDD_OFF
        In reception : nothing
        In return    : return a dictionnary like
        {'Snacks':1, 'Gâteaux':2, 'Sodas':3, 'Glace':4, 'Plats':5}
        """
        query = f"SELECT id, name FROM Category"
        self.Tables.cursor.execute(query)
        for (cat_id, cat_name) in self.Tables.cursor:
        # print('CATEGORY-Cat_Id :', cat_name, ', id :', cat_id)
            self.Categories_id[cat_name] = cat_id
        # print('     Categories_id :',Categories_id)

    def filling_table_Product(self):
        """ For each category of products
        makes a request to OpenFoodFacts API
        and fills the 'Product' table of BDD_OFF """

        for catg in config.categories:
        # print('CATEGORY =', catg)
            parameters_request_API = {
                'action': 'process', 'tagtype_0': 'categories',
                'tag_contains_0': 'contains', 'tag_0': catg,
                'fields': ','.join(config.fields_of_products),
                'page_size': config.products_nb, 'json': 'true'}

            req = requests.get(config.url, params=parameters_request_API)
            # selects only useful informations on products
            infos_of_products = req.json().get('products')
            # print(infos_of_products)


        # selects only usables informations
            for info in infos_of_products:
                try:
                # print(info['url'])
                    if info['url'] \
                        and info['product_name_fr'] \
                        and info['brands'] \
                        and info['nutrition_grade_fr'] \
                        and info['ingredients_text_fr'] \
                        and info['stores'] \
                        and ('Chargement' not in info['product_name_fr'][0:10]):
                        # print('Début de remplissage')
                            # URL_nb = str(product['url']).replace("'", " ")
                            Nom = str(info['product_name_fr']).replace("'", " ")
                            Marque = str(info['brands']).replace("'", " ")
                            Nutriscore = str(info['nutrition_grade_fr']).replace("'", " ")
                            # Ingredients = str(product['ingredients_text_fr']).replace("'", " ")
                            Magasins = str(info['stores']).replace("'", " ")
                            cat = self.Categories_id[catg]
        #                    query = f"SELECT id FROM Category"
        #                    for cat_id in cursor:
        #                        print('CATEGORY :', catg, ', id :', cat_id)

                            URL_nb = 'https'
                            # Nom = 'moi'
                            # Marque = 'Havelard'
                            # Nutriscore = 'D'
                            Ingredients = 'eau et sel (pour le goût)'
                            # Magasins = 'maison'
                            # cat = 1

                        # print('URL:', URL_nb, '; Nom:', Nom, ' ;Marque:', Marque, ' ;Nutriscore:', Nutriscore) # , ' ;Ingrédients:', Ingredients, ' ; Magasins:', Magasins)

                            # insertion of products of category in "BDD_OFF.Product"
                            query = f"INSERT INTO Product ( \
                                    name, brand,url, nutriscore, \
                                    ingredients, stores, category_id) \
                                    VALUES ('{Nom}', '{Marque}', \
                                    '{URL_nb}', '{Nutriscore}', \
                                    '{Ingredients}',' {Magasins}', '{cat}')"
                            self.Tables.cursor.execute(query)
                            self.Tables.cnx.commit()

                except KeyError as msg:
                    pass
                    # !!!  à supprimer avant la présentation  !!!
                    print("     Il manque la clé", msg)


if __name__=='__main__':
    Tables = Tables_BDD_OFF()
    Tables.drop_all_tables_BDD_OFF()
    Tables.create_all_tables_BDD_OFF()
