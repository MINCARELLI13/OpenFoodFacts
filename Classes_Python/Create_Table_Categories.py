import mysql.connector
import config

print()

cnx = mysql.connector.connect(user = config.user,
                            password = config.password,
                            host = config.host,
                            database = config.database)

cursor = cnx.cursor()
""" creation of Category TABLE """
query = " CREATE TABLE Category (id INT AUTO_INCREMENT, \
                                name VARCHAR(100) NOT NULL, \
                                PRIMARY KEY (id) ) \
                                ENGINE = InnoDB "
cursor.execute(query)

""" insertion of the five selected categories """
for category_name in config.categories:
    print(category_name)
    query = (
        f" INSERT INTO Category (name) "
        f" VALUES ('{category_name}') "
    )
    cursor.execute(query)
    cnx.commit()


