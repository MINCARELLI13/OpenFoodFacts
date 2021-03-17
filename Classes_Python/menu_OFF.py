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
        self.fill = Filling_of_BDD_OFF()
        # 4 possible actions from 1 to 4
        # self.action_chosen = self.main_menu()
        self.main_menu()

    def make_a_choice(self, question, dico_choices):
        """ ask a 'question' and wait for a choice among several """
        # displays the possible actions
        os.system('CLS')
        [print(key, '- ', dico_choices[key]) for key in dico_choices.keys()]
        print()
        # make liste of choices numbers : ['1', '2', '3', '4'...]
        choices_nb = []
        for i in range(1, len(dico_choices)+1):
            choices_nb.append(str(i))
        # waits for the chosen action by user
        action = str(input(question))
        question = question + '(1 à ' + str(len(choices_nb)) + ') : '
        while action not in choices_nb:
            os.system('CLS')
            [print(key, '- ', dico_choices[key]) for key in dico_choices.keys()]
            print()
            action = str(input(question))
        return action


    def main_menu(self):
        """ asks to select one action among 4 proposed """
        actions = {
                '1': 'Rechercher un produit',
                '2': 'Afficher les produits substitués',
                '3': 'Réinitialiser la base de données',
                '4': 'Quitter le programme'
                }
        question = "Sélectionnez une action : "
        choice = self.make_a_choice(question, actions)
        # executes action choosed
        actions = {
                '1': self.category_menu,
                '2': self.display_substituts,
                '3': self.reinitialisation_BDD_OFF,
                '4': self.quit_program
                }
        return actions[choice]()

    def category_menu(self):
        """ asks to select one category of products
            among 5 proposed """
        question = "Sélectionnez une catégorie de produits : "
        choice = self.make_a_choice(question, config.categories)
        print()
        self.display_products(choice)

    def display_products(self, catg_id):
        """ displays finded products of choosed category """
        os.system('CLS')
        # loading of all product from a category
        response_products = self.request.find_products_on_Category(catg_id)
        dico_choices = {}
        increment = 1
        for product in response_products:
            liste_of_products = [item for item in product]
            dico_choices[str(increment)] = ", ".join(liste_of_products)
            increment += 1
        question = "Sélectionnez un produit : "
        choice_product = int(self.make_a_choice(question, dico_choices))
        print()

        # selection of a product
        os.system('CLS')
        print('Affichage du produit sélectionné pour la catégorie "',
                config.categories[catg_id],'" :')
                # config.categories[catg_id-1],'" :')
        print()
        for i in range(0, 7):
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
            self.main_menu()
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
                self.main_menu()
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
                # print('Choice_Yes_No :', choice_Yes_No)
                if choice_Yes_No == 'O':
                    if not self.request.exist_duplicate_in_Category(response_products[choice_product-1][0],
                                                                    response_substituts[choice_record-1][0]):
                        self.fill.filling_table_Substitutes(response_products[choice_product-1][0],
                                                        response_substituts[choice_record-1][0])
                    else:
                        os.system('CLS')
                        print('\t ATTENTION : le substitut sélectionné a déjà été enregistré pour ce produit !')
                        print()
                        # displays the product to substitut
                        print('Produit à remplacer par un substitut :', end=' ')
                        print(response_products[choice_product-1][1], end=' ')
                        print('(', response_products[choice_product-1][2], ')')
                        print()
                        # displays the substitut of product
                        print('Substitut sélectionné :', end=' ')
                        print(response_substituts[choice_record-1][1], end=' ')
                        print('(', response_substituts[choice_record-1][2], ')')
                        print()
                        print()
                        # proposes to record a substitut
                        choice_Yes_No = ""
                        choice_Yes_No = input("Voulez-vous rechercher un autre substitut au produit ? (O/N) : ").upper()
                        while choice_Yes_No not in ['O', 'N']:
                            os.system('CLS')
                            # displays the product to substitut
                            for i in range(1,7):
                                print('  ',config.name_of_product_fields[i-1], ' :',
                                        response_products[choice_product-1][i])
                            print()
                            choice_Yes_No = input("Voulez-vous rechercher un autre substitut au produit ? (O/N) : ").upper()
                        if choice_Yes_No == 'O':
                            os.system('CLS')
                            self.main_menu()
                        else:
                            self.quit_program()
                else:
                    os.system('CLS')
                    self.main_menu()


    def display_substituts(self):
        """ displays the recorded substituts """
        os.system('CLS')
        print("\t Affichage des produits et de leurs substituts")
        print()
        substituts_id_result = self.request.load_substituts()
        for product_id in substituts_id_result:
            product = self.request.replace_id_by_name(product_id)
            print("* Substitut(s) au produit '", product, "':")
            for  substitut_id in substituts_id_result[product_id]:
                substitut = self.request.replace_id_by_name(substitut_id)
                print("\t -", substitut)
            print()

    def reinitialisation_BDD_OFF(self):
        """ reinitializes the database BDD_OFF """
        print()
        print('Réinitialisation de la base de données en cours...')
        self.fill.reinitialisation_of_tables()
        self.fill.filling_table_Category()
        self.fill.filling_table_Product()
        print()
        print('Base de données réinitialisée')

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

