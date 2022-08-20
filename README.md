# Startup Campus - Backend

Backend repository for Startup Campus

## Initial setup

Follow these instruction to start using this repository:

- [ ] Create your own private repository by [forking this repository](###fork-repository)
- [ ] [Clone from your new repository](###clone-repository)
- [ ] [Install Python 3.9](###python-installation)
- [ ] Create [virtual environment](###virtual-environment)

***

## Assignments

All assignments will be pushed into the **Assignments** folder, each with its own subfolder. Follow the instructions in each assignment folder (or read the corresponding *README.md*)

*** 

## Projects

All assignments will be pushed into the **Projects** folder, each with its own subfolder. Follow the instructions in each project folder (or **read** the corresponding *README.md*)

***

# Appendix

## Fork repository

TODO: image how to fork

Don't forget to set the visibility to public so mentors can access your repo for grading purposes!

## Clone repository

In your local machine, run the following
```
cd <base_folder_path>
git clone https://gitlab.com/<your_gitlab_username>/startup-campus-backend.git
```
then authenticate with your Gitlab credentials.

## Sync repository

[Original repository](https://gitlab.com/startupcampus.be/startup-campus-backend) will be periodically updated and you will need to manually sync new changes from your forked, private repository.

In your local machine, set the upstream to original repository
```
cd <base_folder_path>
git remote add upstream https://gitlab.com/startupcampus.be/startup-campus-backend.git

```

then checkout to `main` branch and pull new changes from upstream to your remote repository
```
git checkout main
git pull upstream main
```

New changes (if any) should now be on your local machine. Finally, push these changes back to the `main` branch on your private repository
```
git push origin main
```

## Python installation

To install python 3.9, [follow this instruction](https://linuxhint.com/install-python-ubuntu-22-04/).

After completing the installation, check that Python is already installed by running
```
which python3.9
```

Then, you need to install [pip](https://pypi.org/project/pip/) which will be used to install other useful Python packages
```
sudo apt install python3.9-distutils
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3.9 get-pip.py

# clean up the installation file
rm get-pip.py
```

Finally, check that the pip is installed by running
```
which pip3.9
```

## Virtual environment

After installing Python, **enable virtual environment** to *isolate your working environment* as you might use different set of Python packages and versions for other projects.

First, run the following
```
apt-get install python3-venv
python3.9 -m pip install virtualenv
```
Then choose **a name for your environment**. For instance, if the environment name is `startup-campus-backend` then run the following
```
cd <working_folder_path>
python3.9 -m venv startup-campus-backend
```

To start using your new environment, run the following command
```
source <environment_name>/bin/activate
```
If it's successfull, you will see `[environment_name]` on the left side 

![](/images/verify-venv-activation.png)

Make sure that you are using this environment when you are working on your assignments locally.

To stop using virtual environment, just run
```
deactvate
```
and check that the prefix `[environment_name]` is now gone as well.