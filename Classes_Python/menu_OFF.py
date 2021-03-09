# coding: utf-8
import os
import config

print()

class Menu:
    """ offers a menu with 4 possible actions """

    def __init__(self):
        # 4 possible actions from 1 to 4
        self.action_chosen = self.select_action()

    def select_action(self):
        """ asks to select one action among 4 proposed """
        actions = {
                '1': 'Choisir une des catégories de produits',
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
        return cat
    
    def display_substituts(self):
        """ displays the recorded substituts """
        print('     def display_substituts()')

    def reinitialisation_BDD_OFF(self):
        """ reinitializes the database BDD_OFF """
        print('     def reinitialisation_BDD_OFF')

    def quit_program(self):
        """ end of program """
        # print('     def quit_program()')
        print()
        quit()


if __name__=='__main__':
    menu = Menu()
    print()
    # print('menu.action_chosen :', menu.action_chosen)
    # print('menu.category_chosen :', menu.category_chosen)

