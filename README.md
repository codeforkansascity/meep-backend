# meep-backend

## Setup

### Unix
  1. Install python
     ```
     sudo apt-get install python3
     ```
  2. clone the master branch
  3. create a virtual environment in the project root directory
  4. activate the virtual environment ```source venv/bin/activate```
  5. pip install requiremnets ```pip install -r requirements.txt```
  6. create a sqlite database ```touch dev.db```
  7. set dev database environment variable ```export DEV_DATABASE_URL=sqlite:///dev.db```
  8. create ```sqlite3 dev.db```  
  9. create and populate tables ```python db_operations.py reset``` 
  10. check to see if it created the tables ```.tables```
  11. try to display data from a table ```select * from projects;``` you should see a list of projects display
  
  12. set flask environment variable to development
    ```
    export FLASK_ENV=development
    ```
  13. run the app
    ```
    flask run
    ```
  14. test to see if it worked: in a browser, type localhost:5000/projects you should see some json containing project data
  
  
  

### Windows
  1. Install python
  2. Install pip
  3. Install virtualenv
  4. clone the master branch
  5. create a virtual environment in the project root directory
  6. activate the virtual environment ```venv\Scripts\activate```
  7. pip install requirements ```pip install -r requirements.txt```
  8. In mysql, create a new database named 'meep_dev'.
  9. Add a user called 'meep' to this database. 
  10. Create a password 'meep' for the user 'meep'.
  
