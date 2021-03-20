# coding: utf-8
import os
import config
from filling_BDD_OFF import Filling_of_BDD_OFF
from create_Tables_BDD_OFF import Tables_BDD_OFF
from requests_BDD_OFF import Requests

print()

class Menu(Tables_BDD_OFF):
    """ offers all menus for managing app """

    def __init__(self):
        Tables_BDD_OFF.__init__(self)
        self.request = Requests()
        self.fill = Filling_of_BDD_OFF()
        self.selected_category_id = 99999
        self.selected_product = []
        self.selected_substitute = []
        self.main_menu()


    def get_a_choice(self, question, dico_choices):
        """ ask a 'question' and wait for a choice among several in 'dico_choices' """
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
        choice = self.get_a_choice(question, actions)
        # executes action choosed
        actions = {
                '1': self.select_category_menu,
                '2': self.display_substituts_list,
                '3': self.reinitialisation_BDD_OFF,
                '4': self.quit_program
                }
        return actions[choice]()


    def select_category_menu(self):
        """ asks to select one category of products
            among 5 proposed """
        question = "Sélectionnez une catégorie de produits : "
        self.selected_category_id = self.get_a_choice(question, config.categories)
        # choice_catg = self.get_a_choice(question, config.categories)
        print()
        self.display_products()
        # self.display_products(choice_catg)

    def select_product_menu(self, products_list):
        """ displays finded products of choosed category """
        os.system('CLS')
        # loading of all products from a category
        dico_choices = {}
        increment = 1
        for product in products_list:
            dico_choices[str(increment)] = "{} de '{}' (nutriscore {}) : {}.".format(
                                            product[1], product[2], product[4], product[5])
            increment += 1
        question = "Sélectionnez un produit : "
        return int(self.get_a_choice(question, dico_choices))

    def find_substituts_menu(self):
        os.system('CLS')
        print('Affichage du produit sélectionné pour la catégorie "',
                config.categories[self.selected_category_id],'" :')
        print()
        for i in range(1, 7):
            print('  ',config.name_of_product_fields[i-1], ' :',
                self.selected_product[i])
        print()
        choice_find_substitut = int(input("Sélectionnez une option"
                " (1- chercher un substitut;"
                " 2- retour au menu principal;"
                " 3- quitter l'application) : ") or 0)
        while choice_find_substitut not in range(1,4):
            os.system('CLS')
            print('Affichage du produit sélectionné pour la catégorie "',
                    config.categories[self.selected_category_id],'" :')
            print()
            for i in range(1,7):
                print('  ',config.name_of_product_fields[i-1], ' :',
                    self.selected_product[i])
            print()
            choice_find_substitut = int(input("Sélectionnez une option"
                " (1- chercher un substitut;"
                " 2- retour au menu principal;"
                " 3- quitter l'application) : ") or 0)
            print()
        print()
        return choice_find_substitut

    def select_substituts_menu(self, substitutes_list):
        """ asks to select one substitut among all proposed """
        os.system('CLS')   
        # displays the product to substitut
        print('Produit à remplacer par un substitut :')
        for i in range(1,7):
            print('  ',config.name_of_product_fields[i-1], ' :',
                self.selected_product[i])
        print()
        # displays the substituts of product
        print('Substituts trouvés pour le produit ci-dessus :')
        increment = 0
        # for response_substitut in substitutes_list:
        for substitute in substitutes_list :
            increment += 1
            substitute_details = "{} de '{}' (nutriscore {}) : {}.".format(
                    substitute[1], substitute[2], substitute[4], substitute[5])
            print(increment, '-', substitute_details)
        print()
        # proposes to select a substitut to record
        choice_record = int(input("Sélectionnez un substitut (ou '0' pour revenir au menu) : ") or 9999)
        # print('len(response_substituts) :', len(substitutes_list))
        while choice_record not in range(0,len(substitutes_list)+1):
            os.system('CLS')
            # displays the product to substitut
            print('Produit à remplacer par un substitut :')
            for i in range(1,7):
                print('  ',config.name_of_product_fields[i-1], ' :',
                    self.selected_product[i])
            print()
            # displays the substituts of product
            print('Substituts trouvés pour le produit ci-dessus :')
            increment = 0
            for substitute in substitutes_list:
                increment += 1
                substitute_details = "{} de '{}' (nutriscore {}) : {}.".format(
                        substitute[1], substitute[2], substitute[4], substitute[5])
                print(increment, '-', substitute_details)
            print()
            choice_record = int(input("Sélectionnez un substitut"
                    " (ou '0' pour revenir au menu) : ") or 99999)
        return choice_record
    
    def display_substitute(self):
        # loads substitutes from database
        response_substituts = self.request.find_substituts(self.selected_category_id)
        # selects only useful substituts and puts them in' response_substituts'
        response_substituts = self.cleaning_of_substitutes(response_substituts)
        # selection of a substitute of the product
        choice_substitut = self.select_substituts_menu(response_substituts)
        # substitute elements stored in 'selected_substitute'
        self.selected_substitute = response_substituts[choice_substitut-1]
        # if user choose to back at the main menu
        if choice_substitut == 0:
            self.main_menu()
        # if user choose the number of a substitute
        else:
            # asks if the user wants to save the substitute corresponding to the product 
            choice_Yes_No = self.record_substitut_menu()
            # if the user wants to save the substitute
            if choice_Yes_No == 'O':
                # check if the pair (produit_id, substitut_id) has not already been recorded in the database
                if not self.request.exist_duplicate_in_Category(self.selected_product[0],
                                                                self.selected_substitute[0]):
                    # records the pair (produit_id, substitut_id) in the database
                    self.fill.filling_table_Substitutes(self.selected_product[0],
                                                    self.selected_substitute[0])
                # if the pair (produit_id, substitut_id) has already been recorded in the database
                else:
                    choice_Yes_No = self.another_substitute_menu()
                    # if the user choose to search another substitute              
                    if choice_Yes_No == 'O':
                        os.system('CLS')
                        self.display_substitute()
                    # if the user want quit app
                    else:
                        self.quit_program()
            # if the user don't wants to save the substitute
            else:
                os.system('CLS')
                self.main_menu()


    def record_substitut_menu(self):
        """ asks if user wants to record subtitute choosed """
        os.system('CLS')
        # displays the product to substitut
        print('Produit à remplacer par un substitut :')
        for i in range(1,7):
            print('  ',config.name_of_product_fields[i-1], ' :',
                self.selected_product[i])
        print()
        # displays the substitut of product
        print('Affichage du substitut sélectionné pour le produit ci-dessus :')
        for i in range(1,7):
            print('  ',config.name_of_product_fields[i-1], ' :',
                self.selected_substitute[i])
        print()
        # proposes to record a substitut
        choice_Yes_No = input("Voulez-vous enregistrer ce substitut ? (O/N) : ").upper()
        while choice_Yes_No not in ['O', 'N']:
            os.system('CLS')
            # displays the product to substitut
            print('Produit à remplacer par un substitut :')
            for i in range(1,7):
                print('  ',config.name_of_product_fields[i-1], ' :',
                    self.selected_product[i])
            print()
            # displays the substitut of product
            print('Affichage du substitut sélectionné pour le produit ci-dessus :')
            for i in range(1,7):
                print('  ',config.name_of_product_fields[i-1], ' :',
                    self.selected_substitute[i])
            print()
            choice_Yes_No = input("Voulez-vous enregistrer ce substitut ? (O/N) : ").upper()
        return choice_Yes_No


    def cleaning_of_substitutes(self, substitutes_list):
        # selects only substituts with nurtigrade <= nutrigrade of product
        substitutes_list = self.select_useful_substituts(
                            substitutes_list,
                            self.selected_product[4])
        # for remove the substitute identical to the product
        for i in range(len(substitutes_list)):
            # print("response_substituts[i] :", substitutes_list[i], len(substitutes_list))
            # if a substitute is identical to the product 
            if substitutes_list[i][0] == self.selected_product[0]:
                substitut_index = i
        # removes the substitute identical to the product 
        del substitutes_list[substitut_index]
        return substitutes_list

    def another_substitute_menu(self):
        """ asks for search new substitute in case of
            the pair (produit_id, substitut_id) has
            already been recorded in the database
        """
        os.system('CLS')
        print('\t ATTENTION : le substitut sélectionné a déjà été enregistré pour ce produit !')
        print()
        # displays the product to substitut
        print('Produit à remplacer par un substitut :', end=' ')
        print(self.selected_product[1], end=' ')
        print('(', self.selected_product[2], ')')
        print()
        # displays the substitut of product
        print('Substitut sélectionné :', end=' ')
        print(self.selected_substitute[1], end=' ')
        print('(', self.selected_substitute[2], ')')
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
                        self.selected_product[i])
            print()
            choice_Yes_No = input("Voulez-vous rechercher un autre substitut au produit ? (O/N) : ").upper()
        return choice_Yes_No

    def display_products(self):
        """ displays finded products of choosed category """
        # loads products of selected category
        response_products = self.request.find_products_on_Category(self.selected_category_id)
        # selection of a product
        choice_product = self.select_product_menu(response_products)
        # the elements of the selected product are stored in 'selected_product' 
        self.selected_product = response_products[choice_product-1]
        # asks if user want to see the substitutes at a product
        choice_find_substitut = self.find_substituts_menu()
        os.system('CLS')
        # if user chose to quit app
        if choice_find_substitut == 3:
            self.quit_program()
        # if user choose to back main menu
        elif choice_find_substitut == 2:
            self.main_menu()
        # if user choose to find some substituts at product
        else:
            self.display_substitute()
            

    def display_substituts_list(self):
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
        response = input("Etes-vous sûr de vouloir réinitialiser la base de données BDD_OFF ? (O/N) ").upper()
        if response == "O":
            print('Réinitialisation de la base de données en cours...')
            self.fill.reinitialisation_of_tables()
            self.fill.filling_table_Category()
            self.fill.filling_table_Product()
            print()
            print('Base de données réinitialisée')
        else:
            self.main_menu()

    def quit_program(self):
        """ end of program """
        os.system('CLS')
        print('Arrêt du programme demandé...')
        print()
        quit()
    
    def select_useful_substituts(self, substitutes_list, nutri_test):
        """ selects substitutes whose nutriscore is lower than a nutriscore test """
        # print("select_useful_substituts :", nutri_test)
        results_list = []
        for data in substitutes_list:
            if data[4] <= nutri_test:
                results_list.append(data)
        # print("results_list :", results_list)
        # input("")
        return results_list


if __name__=='__main__':
    os.system('CLS')
    menu = Menu()
    print()

