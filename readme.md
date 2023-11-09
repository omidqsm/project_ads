# SETUP MANUAL
## requirements
- **docker** and **docker compose**
- a VPN connection to avoid any connection errors when installing stuff

## steps
- connect to your VPN
- open a terminal window in the project folder
- run ```docker compose up --build```
- open **localhost:8000/docs/** in your browser
- use **"/auth/signup/"** to register your credentials
- use **"/auth/login/"** to retrieve an auth-token from the server
- click **authorize** button on top-right corner of the page and user your
token to login and authorize in the system
- now you can do CRUD operations on **advertisements** and **comments**

that's it!

## How to run tests?
- start an interactive terminal in the running app container
- run following commands
  - ```pipenv shell```
  - ```python manage.py test```

## notes
- this project is written in django rest framework