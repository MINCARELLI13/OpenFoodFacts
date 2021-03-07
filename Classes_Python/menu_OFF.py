# coding: utf-8
import config

print()

def select_category():
    for i in range(1,6):
        print(i, '-', config.categories[i-1] )
    print()

    cat = int(input('Sélectionnez une catégorie : '))
    while cat not in range(1,6):
        cat = int(input('Sélectionnez une catégorie (1 à 5) : '))

    print()
    print(cat)
    print()



actions = {
        '1': 'Choisir une des catégories de produits',
        '2': 'Afficher les produits substitués',
        '3': 'Réinitialiser la base de données',
        '4': 'Quitter le programme'
        }

[print(key, '- ', actions[key]) for key in actions.keys()]
print()

action = str(input('Sélectionnez une action : '))

while action not in ['1', '2', '3', '4']:
    action = str(input('Sélectionnez une action (1 à 4) : '))

print()
print('--')

# print(actions[action])
if action == '1':
    select_category()

