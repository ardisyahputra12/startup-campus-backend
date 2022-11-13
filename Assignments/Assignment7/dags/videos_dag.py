"""
In this file, you will need to
- create DAG as mention in README

[TO DO & TIPS]
- you can use PythonOperator for creating dags operator
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from importing_data.views import create_table_views, copy_views
from importing_data.users import create_table_users, copy_users
from importing_data.videos import create_table_videos, copy_videos
from importing_data.categories import create_table_categories, copy_categories


from transforming_data.most_active_users import create_table_most_active_users, insert_most_active_users
from transforming_data.most_watched_videos import create_table_most_watched_videos, insert_most_watched_videos
from transforming_data.least_watched_categories import create_table_least_watched_categories, insert_least_watched_categories


# create_table_users()
# create_table_categories()
# create_table_videos()
# create_table_views()

# create_table_least_watched_categories()
# create_table_most_watched_videos()
# create_table_most_active_users()

# copy_users()
# copy_categories()
# copy_videos()
# copy_views()

# insert_least_watched_categories()
# insert_most_watched_videos()
# insert_most_active_users()

# create your dag and task here
with DAG(
    "Assignment-7",
    description = "BE03054 - Ardi Saputra - Assignment7",
    start_date = datetime(2022, 11, 11),
    catchup = False,
    tags = ["latest"],
) as dag:
    t1 = PythonOperator(
        task_id = "copy_views",
        python_callable = copy_views,
        do_xcom_push = True,
    )

    t2 = PythonOperator(
        task_id = "copy_categories",
        python_callable = copy_categories,
        do_xcom_push = True,
    )

    t3 = PythonOperator(
        task_id = "copy_users",
        python_callable = copy_users,
        do_xcom_push = True,
    )

    t4 = PythonOperator(
        task_id = "copy_videos",
        python_callable = copy_videos,
        do_xcom_push = True,
    )

    t5 = PythonOperator(
        task_id = "insert_least_watched_categories",
        python_callable = insert_least_watched_categories,
        do_xcom_push = True,
    )

    t6 = PythonOperator(
        task_id = "insert_most_active_users",
        python_callable = insert_most_active_users,
        do_xcom_push = True,
    )

    t7 = PythonOperator(
        task_id = "insert_most_watched_videos",
        python_callable = insert_most_watched_videos,
        do_xcom_push = True,
    )

    t1 >> [t2, t3, t4]
    t2 >> [t5]
    t3 >> [t6]
    t4 >> [t5, t7]