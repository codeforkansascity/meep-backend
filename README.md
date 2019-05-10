# meep-backend

## Setup

### Docker
  1. Install Docker
  2. Build docker image from dockerfile:
    ```
    docker build -t meep-backend:gunicorn src
    ```
  3. Create and run a container from the image:
    ```
    docker run -p 8001:8000 meep-backend:gunicorn
    ```
    or to allow live editing of the code in the container, do
    ```
    docker run -p 8001:8000 -v $(pwd)/src:/meep/api/src meep-backend:gunicorn
    ```
    
      - On windows, the command for live editing probably won't work. instead of ```$(pwd)/src``` on the left side of the           bind mount, you will have to provide an absolute path to the project folder that contains the Dockerfile (src at the         time of writing). After that, there is a chance that you will get a different error. Restart docker and try again. It         usually works on the second attempt. Please note that this is a temporary workaround while we find a less annoying way       to run the project on windows.  
  4. In a browser, try typing ```http://localhost:8001/locations``` to see
    if it worked.

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
  8. Open the database in sqlite with ```sqlite3 dev.db;``` check to see if it created the tables with ```.tables```
  9. try to display data from a table ```select * from projects;``` you should see a list of projects display

  10. set flask environment variable to development
    ```
    export FLASK_ENV=development
    ```
  11. Set flask app environment variable
    ```
    export FLASK_APP="src/app:create_app()"
    ```
  12. run the app
    ```
    flask run
    ```
  13. test to see if it worked: in a browser, type ```localhost:5000/projects``` you should see some json containing project data





### Windows
  1. Install python
  2. Install pip
  3. Install virtualenv
  4. clone the master branch
  5. create a virtual environment in the project root directory
  6. activate the virtual environment ```venv\Scripts\activate```
  7. pip install requirements ```pip install -r requirements.txt```
  8. set dev database environment variable ```set DEV_DATABASE_URL=sqlite:///dev.db```
  9. set flask environment variable to development
    ```
    set FLASK_ENV=development
    ```
  10. set flask app variable to point towards app.py
    ```
    set FLASK_APP=src\app.py
    ```
  11. run the app
    ```
    flask run
    ```
  11. test to see if it worked: in a browser, type ```localhost:5000/projects``` you should see some json containing project data
