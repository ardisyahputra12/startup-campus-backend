# Objective

To test your ability to create simple API endpoints using Flask.

# Instructions

## Setup

Before anything else, check if there's any new updates by [syncing new updates to your private repository](https://gitlab.com/startupcampus.be/startup-campus-backend#sync-repository). Do this everytime you are notified that there are new updates.

Then create a new Merge Request for this assigment by following these steps:
- Go to your repo homepage (`https://gitlab.com/<your_gitlab_username>/startup-campus-backend`)
- From the left sidepanel, go to `Repository > Branches`
- Click `New Branch` button on the top right
- Input `assignment-4` on the Branch name, make sure you are creating from `main` branch and then click `Create branch`
- Wait until redirected to a new page with a notification that you just pushed to your new branch, click `Create merge request`
- In the `New merge request` page
  - Check **Squash commits ...** option on the bottom
  - Feel free to leave everything else as is
  - Click `Create Merge Request`

and you should be done! 

You can now start working on your local machine by clicking  `Code > Check out branch` from the new Merge Request page.

## Pre-work

- Activate your virtual environment before running any Python file
- After activation, re-install the necessary packages by running 
```
cd to root_folder
pip3.9 install -r requirements.txt
```

## Definition

In this assignment, you will try to do the following in Python:
- read and understand endpoint requirements
- implement the endpoints based on the requirements

Implement all endpoints in **p1.py, p2.py, p3.py, p4.py**

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

To test locally, go to the relative path for assignment 4
```
cd
cd startup-campus-backend/Assigments/Assignment4
```

then run
```
python3.9 grader.py
```
you will be able to see details regarding the performance of your code and overall grade for this assignment.

## Submission

Push your changes to the branch (created via Merge Request) and simply **copy paste the Merge Request URL** into the corresponding **Assignment folder** in your **Google Classroom** account.