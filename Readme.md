
# University Apis Application
## Overview

 - University Apis Application is a **CRUD** Apis Application for the universities.
 - This application also consists of a **Search/Filter** Api for the universities.
 
 ## Requirements
 
 - **Python 3.8.2**
 - **Mysql 8.0.20**
 - **Git 2.25.1**
 
## Installation and Setup
	
- ### Cloning the Github Repository
	 Clone the github repository by running the following command:
	 
		git clone https://github.com/sahildiwan94/universityCRUD.git

 - ### Creating and Activating a Virtual Environment
	 Create a new Virtual Environment by running the following command:
       

		 python3 -m venv env_name
	Activate the  Virtual Environment by running the following command:
       

		 source env_name/bin/activate
		 		
- ### Installing Dependancies
	 Install all the dependancies  by running the following command from the root directory:
       

		pip3 install -r requirements.txt
		
- ### Database Setup
	 Create a new Mysql Database (logging into the mysql shell or by phpMyadmin) by the following command:
	 
       

		create database database_name
	 Grant all privileges on that database to the user (logging into the mysql shell or by phpMyadmin) by the following command:
	 
       

		grant all privileges on database_name.* to 'username'@'localhost';
	Add the database configuration in  `settings.py` file:
	

		DATABASES = {
		    'default': {
		        'ENGINE': 'django.db.backends.mysql',
		        'NAME': 'database_name',
		        'USER': 'username',
		        'PASSWORD':'password',
		        'HOST':'localhost',
		        'PORT': 3306,
		    }
		 }
	Migrate the database tables to the database by running the following commands from the root directory
	

		 python3 manage.py makemigrations
		 python3 manage.py migrate

- ### Create a Superuser for using the django admin site
	 Create a new superuser by running the following command from the root directory
	 

		 python3 manage.py createsuperuser
		 
## Running the Application Server
	
Run the following command from the root directory:
	 
	python3 manage.py runserver 0.0.0.0:8000(port number)


## Api Documentation

University Apis Application consists of the following 7 Apis:

 - On Heroku : host = `https://university-apis-sahil-diwan.herokuapp.com`
 - On Local : host = localhost
 
1.  ### List of Countries
	 **Url** : host/countries
	**Type** : GET
	 **Description** : This is a GET Api for the listing of countries.These country codes are used in creaion/updation of a university.
	 **Request** : No Request Parameters.
	 **Response** :
	 **HTTP Status Code** - 200 OK 
		
		 {
		    "message": "Countries Listed",
		    "data": [
			    {"code": "AF",
			     "name": "Afghanistan"},
			     ............
			]
		 }
2.  ### Create University
	 **Url** : host/universities
	**Type** : POST
	 **Description** : This is a POST Api for the creation of a university.
	 **Request** : 
	 
		 name: VESIT (University name must be of max 150 characters)
		 domain: ves.ac.in (University domain must be of max 100 characters)
		 country: IN (A valid country of University code taken from list of countries Api response)
		 web_page: https://ves.ac.in/vesit/ (University Web page url)

			 
	 **Response** : 
	 
	 **HTTP Status Code** - 201 Created 
		
		 {
		    "message": "University Created",
		    "data": 
			    {"id": 18,
			    "name": "VESIT",
			    "domain": "ves.ac.in",
			    "web_page": "https://ves.ac.in/vesit/",
			    "country": "India",
			    "createdAt": "2020-07-25 07:29",
			    "alpha_two_code": "IN""}
		 }
3.  ###  University List
	 **Url** : host/universities
	**Type** : GET
	 **Description** : This is a GET Api for the listing of the universities.
	 **Query Params** : 
	 
		 page: 1 (Page no,if not given all objects will be listed.)
		 page_size: 10 (Page size,default=10)
		 ordering: IN (Ordering can take the following values(createdAt,-createdAt,name,-name
			       default=-createdAt(latest entry on top),
			       '--)
		 domain: .edu (Filter by end part of  domain)
		 country: IN (Filter by country code)
		 search: v (Search by university name)

			 
	 **Response** : 
	 
	 **HTTP Status Code** - 200 Ok 
		
		 {
		    "message": "Universities Listed",
		    "data": [
			    {"id": 18,
			    "name": "VESIT",
			    "domain": "ves.ac.in",
			    "web_page": "https://ves.ac.in/vesit/",
			    "country": "India",
			    "createdAt": "2020-07-25 07:29",
			    "alpha_two_code": "IN""},
			     ............
			]
		 }

4.  ###  University Retrieve
	 **Url** : host/universities/university_id
	**Type** : GET
	 **Description** : This is a GET Api for the retrieval of a university.
	 **Query Params** : No Query Params
	 **Response** : 
	 
	 **HTTP Status Code** - 200 Ok 
		
		 {
		    "message": "University Retrieved",
		    "data": 
			    {"id": 18,
			    "name": "VESIT",
			    "domain": "ves.ac.in",
			    "web_page": "https://ves.ac.in/vesit/",
			    "country": "India",
			    "createdAt": "2020-07-25 07:29",
			    "alpha_two_code": "IN""}
		 }
		 
5.  ### Update University
	 **Url** : host/universities/university_id
	**Type** : PUT
	 **Description** : This is a PUT Api for the updation of a university.
	 **Request** : 
	 
		 name: VESIT (University name must be of max 150 characters)
		 domain: ves.ac.in (University domain must be of max 100 characters)
		 country: IN (A valid country of University code taken from list of countries Api response)
		 web_page: https://ves.ac.in/vesit/ (University Web page url)

			 
	 **Response** : 
	 
	 **HTTP Status Code** - 200 Ok 
		
		 {
		    "message": "University Updated",
		    "data": 
			    {"id": 18,
			    "name": "VESIT",
			    "domain": "ves.ac.in",
			    "web_page": "https://ves.ac.in/vesit/",
			    "country": "India",
			    "createdAt": "2020-07-25 07:29",
			    "alpha_two_code": "IN""}
		 }

6.  ###  University Delete
	 **Url** : host/universities/university_id
	**Type** : DELETE
	 **Description** : This is a DELETE Api for thesoft deletion of a university.
	 **Query Params** : No Query Params
	 **Response** : 
	 
	 **HTTP Status Code** - 200 Ok 
		
		 {
		    "message": "University Deleted",
		    "data": {}
		 } 

7.  ###  University Search
	 **Url** : host/universities/search
	**Type** : GET
	 **Description** : This is a GET Api to search/filter universities.
	 **Query Params** : 
	 
		 page: 1 (Page no,if not given all objects will be listed.)
		 page_size: 10 (Page size,default=10)
		 ordering: IN (Ordering can take the following values(createdAt,-createdAt,name,-name
			       default=-createdAt(latest entry on top),
			       '--)
		 domain: .edu (Filter by end part of  domain)
		 country: IN (Filter by country code)
		 search: v (Search by university name)

			 
	 **Response** : 
	 
	 **HTTP Status Code** - 200 Ok 
		
		 {
		    "message": "Universities Listed",
		    "data": [
			    {"id": 18,
			    "name": "VESIT",
			    "domain": "ves.ac.in",
			    "web_page": "https://ves.ac.in/vesit/",
			    "country": "India",
			    "createdAt": "2020-07-25 07:29",
			    "alpha_two_code": "IN""},
			     ............
			]
		 }

* **Please refer to the postman collection of these Apis for testing which is located in `docs/university_apis.json`**

