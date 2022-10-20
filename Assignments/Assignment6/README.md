# Objective

To test your ability to dockerize and deploy flask app.

# Instructions

## Setup

Before anything else, check if there's any new updates by [syncing new updates to your private repository](https://gitlab.com/startupcampus.be/startup-campus-backend#sync-repository). Do this everytime you are notified that there are new updates.

Then create a new Merge Request for this assigment by following these steps:
- Go to your repo homepage (`https://gitlab.com/<your_gitlab_username>/startup-campus-backend`)
- From the left sidepanel, go to `Repository > Branches`
- Click `New Branch` button on the top right
- Input `assignment-6` on the Branch name, make sure you are creating from `main` branch and then click `Create branch`
- Wait until redirected to a new page with a notification that you just pushed to your new branch, click `Create merge request`
- In the `New merge request` page
  - Check **Squash commits ...** option on the bottom
  - Feel free to leave everything else as is
  - Click `Create Merge Request`

and you should be done! 

You can now start working on your local machine by clicking  `Code > Check out branch` from the new Merge Request page.

## Pre-work

- Make sure you already install docker and docker-compose

## Definition

In this assignment, you will try to do the following :
- dockerize flask app inside the folder "./app"
- create docker image using dockerfile with this information:
    - for base image, you can use python:3.9-slim-buster
    - the working directory will be at ./app
    - you should install all the library inside "requirements.txt"

- create docker-compose file to run the application in docker with this information:
    - you should create 2 container, for the flask app and db
    - flask app should be deployed within port 5000
    - flask app container name should be "library"
    - db will be deployed within port 5432 
    - db will be use postgresql image
    - db container name should be "library-db"
    - both db and flask app must be accessible from outside your vm
- deploy this application using docker in cloud, u can use gcp compute engine vm instance
- you should publish your flask image to docker hub: https://docs.docker.com/docker-hub/#step-5-build-and-push-a-container-image-to-docker-hub-from-your-computer

Notes:
- for those who using GCP, you should open both port 5000 and 5432, for more information: https://cloud.google.com/vpc/docs/using-firewalls



If you encounter any issues understanding the problem statement, feel free to ask and reach out to your mentors!

## Grading

Your grade will be mainly deducd by the amount of test cases you manage to pass across the whole problem sets. See Testing on how to check your live grades.

Mentors will also check your codes (in the Merge Request) to ensure no cheating attempts is performed.

## Testing

To test locally, go to the relative path for assignment 6
```
cd
cd startup-campus-backend/Assigments/Assignment6
```

then run
```
docker-compose up
```

- you will be able to access your app via curl to localhost:5000
- you will be able to access your postgres db with this command:
```
docker exec -it library-db -U users -d library-db
```

## Submission

Push your changes to the branch (created via Merge Request) and simply **copy paste the Merge Request URL** into the corresponding **Assignment folder** in your **Google Classroom** account.