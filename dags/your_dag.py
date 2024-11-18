from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

from sql_queries import QUERIES  # Importation des requêtes

# Fonction Python pour exécuter une requête SQL
def execute_query(query_name, **kwargs):
    
    hook = PostgresHook(postgres_conn_id='your_postgres_connection')
    sql_query = QUERIES[query_name]  # Récupération de la requête à partir du fichier
    hook.run(sql_query)  # Exécution de la requête

# Définir le DAG
default_args = {
    'owner': 'airflow',
    'retries': 1,
}
with DAG(
    dag_id='example_dag',
    default_args=default_args,
    schedule_interval='@daily',
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:

    # Task qui exécute une requête de sélection
    task_select = PythonOperator(
        task_id='select_all_data',
        python_callable=execute_query,
        op_kwargs={'query_name': 'select_all'},  # Nom de la requête
    )

    # Task qui exécute une mise à jour
    task_update = PythonOperator(
        task_id='update_data',
        python_callable=execute_query,
        op_kwargs={'query_name': 'select_all'},  # Nom de la requête
    )

    task_select >> task_update