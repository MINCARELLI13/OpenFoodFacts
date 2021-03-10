# coding: utf-8
import os
import config
from filling_BDD_OFF import Filling_of_BDD_OFF
from create_Tables_BDD_OFF import Tables_BDD_OFF
from requests_BDD_OFF import Requests

print()

class Menu(Tables_BDD_OFF):
    """ offers a menu with 4 possible actions """

    def __init__(self):
        Tables_BDD_OFF.__init__(self)
        self.request = Requests()
        # 4 possible actions from 1 to 4
        self.action_chosen = self.select_action()

    def select_action(self):
        """ asks to select one action among 4 proposed """
        actions = {
                '1': 'Rechercher un produit',
                '2': 'Afficher les produits substitués',
                '3': 'Réinitialiser la base de données',
                '4': 'Quitter le programme'
                }

        # displays the 4 possible actions
        os.system('CLS')
        [print(key, '- ', actions[key]) for key in actions.keys()]
        print()

        # waits for the chosen action by user
        action = str(input('Sélectionnez une action : '))
        while action not in ['1', '2', '3', '4']:
            os.system('CLS')
            [print(key, '- ', actions[key]) for key in actions.keys()]
            print()
            action = str(input('Sélectionnez une action (1 à 4) : '))
        
        self.action_chosen = action
        return self.execute_action()
    
    def execute_action(self):
        """ executes action choosed in the 'select_action' procedure """ 
        actions = {
                '1': self.select_category,
                '2': self.display_substituts,
                '3': self.reinitialisation_BDD_OFF,
                '4': self.quit_program
                }
        return actions[self.action_chosen]()

    def select_category(self):
        """ asks to select one category of products
            among 5 proposed """
        os.system('CLS')
        print("Choix d'une catégorie de produits")
        print()
        # displays the choise of 5 categories for select
        [print(i, '-', config.categories[i-1]) for i in range(1, 6)]
        print()

        cat = int(input('Sélectionnez une catégorie : '))
        # asks to select one category of products among 5 proposed
        while cat not in range(1,6):
            os.system('CLS')
            print("Choix d'une catégorie de produits")
            print()
            [print(i, '-', config.categories[i-1]) for i in range(1, 6)]
            print()
            cat = int(input('Sélectionnez une catégorie (1 à 5) : '))
        print()
        self.display_products(cat)
        # return cat

    def display_products(self, catg_id):
        """ displays finded products of choosed category """
        os.system('CLS')
        print('Affichage des produits trouvés pour la catégorie "',
            config.categories[catg_id-1],'" :')
        print()
        query = f" SELECT * FROM Product WHERE Product.category_id='{catg_id}' "
        self.cursor.execute(query)
        # displaying of products
        response_products = self.cursor.fetchall()
        increment = 0
        for product in response_products:
            increment += 1
            print(increment, '-', product)
        print()
        choice_product = int(input("Sélectionnez un produit (ou '0' pour quitter) : "))
        while choice_product not in range(0,increment+1):
            os.system('CLS')
            print('Affichage des produits trouvés pour la catégorie "',
                config.categories[catg_id-1],'" :')
            print()
            increment = 0
            for product in response_products:
                increment += 1
                print(increment, '-', product)
            print()
            choice_product = int(input("Sélectionnez un produit (ou '0' pour quitter) : "))
        print('Choice_product :', choice_product)
        if choice_product == 0:
            self.quit_program()            
        else:
            os.system('CLS')
            print('Affichage du produit sélectionné pour la catégorie "',
                    config.categories[catg_id-1],'" :')
            print()
            for i in range(1,7):
                print('  ',config.name_of_product_fields[i-1], ' :',
                    response_products[choice_product-1][i])
            print()
            choice_substitut = int(input("Sélectionnez une option"
                    " (1- chercher un substitut;"
                    " 2- retour au menu principal;"
                    " 3- quitter l'application) : "))
            while choice_substitut not in range(1,4):
                os.system('CLS')
                print('Affichage du produit sélectionné pour la catégorie "',
                        config.categories[catg_id-1],'" :')
                print()
                for i in range(1,7):
                    print('  ',config.name_of_product_fields[i-1], ' :',
                        response_products[choice_product-1][i])
                print()
                choice_substitut = int(input("Sélectionnez une option"
                    " (1-chercher un substitut;"
                    " 2-retour au menu principal;"
                    " 3-quitter l'application) : "))
                print()
            print()
            if choice_substitut == 3:
                os.system('CLS')
                print('Arrêt du programme demandé...')
                print()
                quit()
            elif choice_substitut == 2:
                os.system('CLS')
                self.select_action()
            else:
                os.system('CLS')
                response_substituts = self.request.find_substituts(catg_id)
                # selection of the useful substituts
                response_substituts = self.select_useful_substituts(
                    response_substituts, response_products[choice_product-1][4])
                print(response_substituts)
                # displays the product to substitut
                print('Produit à remplacer par un substitut :')
                for i in range(1,7):
                    print('  ',config.name_of_product_fields[i-1], ' :',
                        response_products[choice_product-1][i])
                print()
                # displays the substituts of product
                print('Substituts trouvés pour le produit ci-dessus :')
                increment = 0
                for response_substitut in response_substituts:
                    increment += 1
                    print(increment, '-', response_substitut)
                print()
                # proposes to select a substitut to record
                choice_record = int(input("Sélectionnez un substitut à enregistrer (ou '0' pour revenir au menu) : "))
                print('len(response_substituts) :', len(response_substituts))
                while choice_record not in range(0,len(response_substituts)+1):
                    os.system('CLS')
                    print('len(response_substituts) :', len(response_substituts))
                    # displays the substituts of product
                    print('Substituts trouvés pour le produit ci-dessus :')
                    increment = 0
                    for response_substitut in response_substituts:
                        increment += 1
                        print(increment, '-', response_substitut)
                    print()
                    choice_record = int(input("Sélectionnez un substitut"
                            " à enregistrer (ou '0' pour revenir au menu) : "))
                print('Choice_record :', choice_record)
                if choice_record == 0:
                    os.system('CLS')
                    self.select_action()
                else:
                    os.system('CLS')
                    # displays the product to substitut
                    print('Produit à remplacer par un substitut :')
                    for i in range(1,7):
                        print('  ',config.name_of_product_fields[i-1], ' :',
                            response_products[choice_product-1][i])
                    print()
                    # displays the substitut of product
                    print('Affichage du substitut sélectionné pour le produit ci-dessus :')
                    for i in range(1,7):
                        print('  ',config.name_of_product_fields[i-1], ' :',
                            response_substituts[choice_record-1][i])
                    print()
                    # proposes to record a substitut
                    choice_Yes_No = input("Voulez-vous enregistrer ce substitut ? (O/N) : ").upper()
                    while choice_Yes_No not in ['O', 'N']:
                        os.system('CLS')
                        # displays the product to substitut
                        print('Produit à remplacer par un substitut :')
                        for i in range(1,7):
                            print('  ',config.name_of_product_fields[i-1], ' :',
                                response_products[choice_product-1][i])
                        print()
                        # displays the substitut of product
                        print('Affichage du substitut sélectionné pour le produit ci-dessus :')
                        for i in range(1,7):
                            print('  ',config.name_of_product_fields[i-1], ' :',
                                response_substituts[choice_record-1][i])
                        print()
                        choice_Yes_No = input("Voulez-vous enregistrer ce substitut ? (O/N) : ").upper()
                    print('Choice_Yes_No :', choice_Yes_No)

                    



    def display_substituts(self):
        """ displays the recorded substituts """
        print('     def display_substituts()')

    def reinitialisation_BDD_OFF(self):
        """ reinitializes the database BDD_OFF """
        print()
        print('Réinitialisation de la base de données en cours...')
        return Filling_of_BDD_OFF()

    def quit_program(self):
        """ end of program """
        os.system('CLS')
        print('Arrêt du programme demandé...')
        print()
        quit()
    
    def select_useful_substituts(self, substituts_list, nutri_test):
        """ selects substitutes whose nutriscore is lower than a nutriscore test """
        results_list = []
        for data in substituts_list:
            if data[4] < nutri_test:
                results_list.append(data)
        return results_list


if __name__=='__main__':
    os.system('CLS')
    menu = Menu()
    print()

