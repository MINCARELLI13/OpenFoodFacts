# coding: utf-8
# import mysql.connector
from create_Tables_BDD_OFF import Tables_BDD_OFF
import config

class Requests (Tables_BDD_OFF):
    """ contains all the requests to practice on database BDD_OFF """

    def __init__(self):
        Tables_BDD_OFF.__init__(self)
    
    def tri_bulles(self, my_liste, column):
        for i in range (len(my_liste)-1,0, -1):
            for j in range(i):
                if my_liste[j][column]>my_liste[j+1][column]:
                    my_liste[j], my_liste[j+1] = my_liste[j+1], my_liste[j]     # on inverse les éléments de la liste situés aux index j et j+1
        return my_liste

    def find_products_on_Category(self, catg_id):
        """ loads all products from category_id """
        query = f" SELECT * FROM Product WHERE Product.category_id='{catg_id}' "
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def find_substituts(self, category_id):
        """ finds substituts to a product """
        # print('Produits de substitution pour la catégorie', category_id)
        query = f"SELECT * FROM Product WHERE category_id='{category_id}'"
        self.cursor.execute(query)

        substituts_list = []
        increm = 0
        for curseur in self.cursor:
            product_description = []
            for item in curseur:
                product_description.append(item)
            substituts_list.append(product_description)
        
        # print('Subtituts_list :', substituts_list)
        substituts_list = self.tri_bulles(substituts_list, 4)
        return substituts_list

    def exist_duplicate_in_Category(self, origin_id, substit_id):
        """ finds if duplicate (origin_id, substitut_id) already exists in the Substitutes' table """
        query = f"SELECT original_id, substitut_id FROM Substitutes"
        self.cursor.execute(query)
        # search duplicate of (origin_id, substitut_id)
        presence = False
        for curseur in self.cursor:
            if curseur == (origin_id, substit_id):
                presence = True
        return presence
                   
