# coding: utf-8
import mysql.connector
import config

class Tables_BDD_OFF:

    def __init__(self):
        self.cnx = mysql.connector.connect(
            user = config.user,
            password = config.password,
            host = config.host,
            database = config.database
            )
        self.cursor = self.cnx.cursor()

    def drop_all_tables_BDD_OFF(self):
        """ drop tables Category, Product and Substitutes if exist """
        # deactivates the FOREIGN_KEYs to permit to drop all tables
        query = " SET FOREIGN_KEY_CHECKS = 0 "
        self.cursor.execute(query)
        # drop Product table of BDD_OFF database
        query = " DROP TABLE IF EXISTS BDD_OFF.Product "
        self.cursor.execute(query)
        # drop Category table of BDD_OFF database
        query = " DROP TABLE IF EXISTS BDD_OFF.Category "
        self.cursor.execute(query)
        # drop Substitutes table of BDD_OFF database
        query = " DROP TABLE IF EXISTS BDD_OFF.Substitutes "
        self.cursor.execute(query)
        # reactivates the FOREIGN_KEYs after drop of all tables
        query = " SET FOREIGN_KEY_CHECKS = 1 "
        self.cursor.execute(query)

    def create_all_tables_BDD_OFF(self):
        """ creation of tables Category, Product and Substitutes """
        # creation of Category TABLE
        query = " CREATE TABLE Category (id INT AUTO_INCREMENT, \
            name VARCHAR(100) NOT NULL, \
            PRIMARY KEY (id) ) \
            ENGINE = InnoDB "
        self.cursor.execute(query)                      

        # creation of Product TABLE
        query = " CREATE TABLE IF NOT EXISTS BDD_OFF.Product ( \
            id INT NOT NULL AUTO_INCREMENT, \
            name VARCHAR(100) NOT NULL, \
            brand VARCHAR(100) NOT NULL, \
            url VARCHAR(100) NOT NULL, \
            nutriscore CHAR(1) NOT NULL, \
            ingredients VARCHAR(500) NULL DEFAULT NULL, \
            stores VARCHAR(150) NULL DEFAULT NULL, \
            category_id INT NOT NULL, \
            PRIMARY KEY (id), \
            INDEX fk_Product_category_id (category_id ASC) VISIBLE, \
            CONSTRAINT fk_Product_category_id \
            FOREIGN KEY (category_id) \
            REFERENCES BDD_OFF.Category (id) \
            ON DELETE NO ACTION \
            ON UPDATE NO ACTION) \
            ENGINE = InnoDB "
        self.cursor.execute(query)

        # creation of Substitutes TABLE
        query = " CREATE TABLE IF NOT EXISTS BDD_OFF.Substitutes ( \
            original_id INT NOT NULL, \
            substitut_id INT NOT NULL, \
            PRIMARY KEY (original_id, substitut_id), \
            CONSTRAINT fk_Substitutes_original_id \
            FOREIGN KEY (original_id) \
            REFERENCES BDD_OFF.Product (id) \
            ON DELETE NO ACTION \
            ON UPDATE NO ACTION, \
            CONSTRAINT fk_Substitutes_substitut_id \
            FOREIGN KEY (substitut_id) \
            REFERENCES BDD_OFF.Product (id) \
            ON DELETE NO ACTION \
            ON UPDATE NO ACTION) \
            ENGINE = InnoDB "
        self.cursor.execute(query)


if __name__ == '__main__':
    Tables = Tables_BDD_OFF()
    response_products = Tables.display_products(5)
    for product in response_products:
        print(product)
    print()

