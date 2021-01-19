# Easy Tidy B - API

This is the API of Easy Tidy Business App. This API contains certain routes which will be accessed by the easyTidyB-Frontend app. 

### Frameworks and libraries used:
- Flask
- MySQL-connector

### App complementations:
This app objective is to be accessed by a frontend whose code is on the [easyTidyB-Frontend repository](https://github.com/fabiosaac12/easyTidyB-Frontend):
This API depends on a MySQL database, whose code is on the [easyTidyB-DB repository](https://github.com/fabiosaac12/easyTidyB-DB):

### How to clone this repository and start using this app locally:
1. Open the terminal
2. `git clone https://github.com/fabiosaac12/easyTidyB-API` --> to clone the repository
3. `cd easyTidyB-API` --> to move to the generated folder
4. `pip install -r requirements.txt` --> to install all the required modules
5. Set the necessary environment variables in the init.sh file
6. `./init.sh` --> executing that file will start the API server on port 9000 with the pre-established environment variables
