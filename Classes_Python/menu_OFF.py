# coding: utf-8
print()
 
print('1- Choisir une catégorie de produits')
print('2- Afficher les produits substitués')
print('3- Réinitialiser la base de données')
print('4- Quitter le programme')
print()

option = str(input('Sélectionnez une action :'))

while option not in ['1', '2', '3', '4']:
    option = str(input('Sélectionnez une action :'))


print('Option...', option)
print()

