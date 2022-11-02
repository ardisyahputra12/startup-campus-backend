"""
In this file, you will need to
- create DAG as mention in README

[TO DO & TIPS]
- you can use PythonOperator for creating dags operator
"""

from airflow import DAG
from datetime import datetime, timedelta

from importing_data.views import copy_views
from importing_data.users import copy_users
from importing_data.videos import copy_videos
from importing_data.categories import copy_categories


from transforming_data.most_active_users import insert_most_active_users
from transforming_data.most_watched_videos import insert_most_watched_videos
from transforming_data.least_watched_categories import insert_least_watched_categories


# create your dag and task here
