# Objective

Learn how to run or operate airflow

# Instructions
Before anything else, check if there's any new updates by [syncing new updates to your private repository](https://gitlab.com/startupcampus.be/startup-campus-backend#sync-repository). Do this everytime you are notified that there are new updates.

Run this command to create .env file 
```
cd startup-campus-backend/airflow
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

then run this command to run database migrations and create the first user account
```
docker-compose up airflow-init
```

After initialization is complete, you should see a message like this:

```
airflow-init_1       | Upgrades done
airflow-init_1       | Admin user airflow created
airflow-init_1       | 2.4.1
start_airflow-init_1 exited with code 0
```

now you can start the airflow service with this command:
```
docker-compose up
```

you can start by accessing webserver at localhost:8080

default username and password are:
username: airflow
password: airflow


