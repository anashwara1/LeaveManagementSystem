# LeaveManagementSystem


#cloning the project from github

1)Copy Repository URL:

-Go to the GitHub repository of our project
-Click on the "Code" button.
-Copy the URL (HTTPS or SSH) that is displayed.

2)open terminal:

-open your terminal or command prompt

3)Navigate to Desired Directory:

-Use the cd command to navigate to the directory where you want to clone the repository.

4)Clone the Repository:

-Use the git clone command followed by the URL you copied earlier.
   example: git clone <repository_url>

5)Wait for the Cloning Process:

-Git will now download the entire repository to your local machine.

#To make sure we have the latest version of pip, run the following command:
 python -m pip install --upgrade pip

#Creating a virtual environment 
 
1)Open a terminal or command prompt.

2)Navigate to the root directory of your Django project.

3)Run the following command to create a virtual environment named venv:  python -m venv venv

#activation of virtual environment

-set the path and write this command : venv\Scripts\activate

#now its time to install all the dependencies using requirements.txt file containing all the dependencies:
   
    pip install -r requirements.txt      


#create a ".env" text file where you will storing the environment variables 

->you can find a .env sample file in the repository, you can take it as reference and set the variables to access your database.

#Now you need to migrate the models to database: use these commands

-> python manage.py makemigrations
     python manage.py migrate   

#Next step is to create a superuser :

-> python manage.py createsuperuser........................
    enter the details for the respective fields.............
 And now you are ready to login and access the admin side and add employees

# To run the server
-> python manage.py runserver

Now the server gets started 












