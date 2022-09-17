# Objective

To test your ability to create SQL queries according to requirements and use Python to execute the queries. 

# Instructions

## Setup

Before anything else, check if there's any new updates by [syncing new updates to your private repository](https://gitlab.com/startupcampus.be/startup-campus-backend#sync-repository). Do this everytime you are notified that there are new updates.

Then create a new Merge Request for this assigment by following these steps:
- Go to your repo homepage (`https://gitlab.com/<your_gitlab_username>/startup-campus-backend`)
- From the left sidepanel, go to `Repository > Branches`
- Click `New Branch` button on the top right
- Input `assignment-3` on the Branch name, make sure you are creating from `main` branch and then click `Create branch`
- Wait until redirected to a new page with a notification that you just pushed to your new branch, click `Create merge request`
- In the `New merge request` page
  - Check **Squash commits ...** option on the bottom
  - Feel free to leave everything else as is
  - Click `Create Merge Request`

and you should be done! 

You can now start working on your local machine by clicking  `Code > Check out branch` from the new Merge Request page.

## Definition

In this assignment, you will try to do the following in Python:
- connect to a remote database (PostgreSQL) 
- create SELECT queries to read selected data according to given requirements
- create a local database (via SQLite)
- move selected data from remote database into local database

You will implement the main logic into the functions provided

Simply remove the `pass` statement within the function context and start coding.
```py
def function_to_implement(...)
    # your code here
    ...
```

If you encounter any issues understanding the problem statement, feel free to ask and reach out to your mentors!

## Grading

Your grade will be mainly deducd by the amount of test cases you manage to pass across the whole problem sets. See Testing on how to check your live grades.

Mentors will also check your codes (in the Merge Request) to ensure no cheating attempts is performed.

## Testing

To test locally, go to the relative path for assignment 3
```
cd
cd startup-campus-backend/Assigments/Assignment3
```

then run
```
python3.9 -m grader
```
you will be able to see details regarding the performance of your code and overall grade for this assignment.

## Submission

Push your changes to the branch (created via Merge Request) and simply **copy paste the Merge Request URL** into the corresponding **Assignment folder** in your **Google Classroom** account.