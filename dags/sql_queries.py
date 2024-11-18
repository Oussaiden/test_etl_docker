# sql_queries.py

# Requête de sélection
SELECT_ALL = """
SELECT * FROM article;
"""

# Requête d'insertion
INSERT_DATA = """
INSERT INTO your_table (col1, col2, col3) VALUES (%s, %s, %s);
"""

# Requête de vérification de structure
CHECK_TABLE_STRUCTURE = """
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'your_table';
"""

# Requête d'une autre opération
ANOTHER_QUERY = """
UPDATE your_table SET col1 = 'value' WHERE col2 = 'condition';
"""

# Dictionnaire pour organiser les requêtes (facultatif)
QUERIES = {
    "select_all": SELECT_ALL,
    "insert_data": INSERT_DATA,
    "check_structure": CHECK_TABLE_STRUCTURE,
    "update_data": ANOTHER_QUERY,
}
