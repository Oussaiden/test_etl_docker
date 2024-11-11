import pg8000
import sqlite3
import pandas as pd
import os

# Connexion à la base de données locale pour récupérer la structure enregistrée
db_path = os.getenv('DB_PATH', '/data/struture.db')

schema=os.getenv('DB_SCHEMA')

connPst = pg8000.connect(
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT')
)

connSQL = sqlite3.connect(db_path)
cursorSQL = connSQL.cursor()

# Vérifier si la table existe
cursorSQL.execute("SELECT name FROM sqlite_master WHERE type='table' AND name= 'table_structure';")
result = cursorSQL.fetchone()

if result is None:
    print(f"La table table_structure n'existe pas. Création de la table.")
    create_table_query = f'''
    CREATE TABLE table_structure (
    table_name TEXT,
    column_name TEXT,
    data_type TEXT,
    character_maximum_length REAL,
    constraint_type TEXT,
    is_BI INTEGER CHECK(is_BI IN (0, 1))
    )
    '''
    cursorSQL.execute(create_table_query)
    connSQL.commit()
    
    print(f"Table table_structure créée avec succès.")

    cursorPst = connPst.cursor()
    query_structure = f"""
                   SELECT 
                   c.TABLE_NAME, 
                   c.COLUMN_NAME, 
                   c.DATA_TYPE, 
                   c.CHARACTER_MAXIMUM_LENGTH,
                   CASE 
                       WHEN kcu.CONSTRAINT_NAME IS NOT NULL THEN 'PRIMARY KEY' 
                       ELSE '' 
                   END AS CONSTRAINT_TYPE
               FROM 
                   INFORMATION_SCHEMA.COLUMNS c
               LEFT JOIN 
                   INFORMATION_SCHEMA.KEY_COLUMN_USAGE kcu 
               ON 
                   c.TABLE_SCHEMA = kcu.TABLE_SCHEMA 
                   AND c.TABLE_NAME = kcu.TABLE_NAME 
                   AND c.COLUMN_NAME = kcu.COLUMN_NAME
               WHERE 
                   c.TABLE_SCHEMA = '{schema}'
               ORDER BY 
                   c.TABLE_NAME, 
                   c.ORDINAL_POSITION;
               """
    cursorPst.execute(query_structure)
    results = cursorPst.fetchall()
    


    # Insérer les résultats dans la table
    for row in results:
        cursorSQL.execute('''
            INSERT INTO table_structure (table_name, column_name, data_type, 
                          character_maximum_length, constraint_type,is_BI)
            VALUES (?, ?, ?, ?, ?,0)
        ''', row)

    connSQL.commit()
    connSQL.close()
    print(f"Maj import données succès.")