![Logo](https://www.verkehrshaus.ch/fileadmin/user_upload/Header_Webseite__Plani.jpg)


# Planetarium

This project was created specifically for a planetarium. It makes it easy to operate planetarium via this api.


## 👩‍💻 _Installation & Run_
### 🧠 Set up the environment 

### 📝 Set enviroment variable
- Copy and rename the **.env.sample** file to **.env** 
- Open the .env file and edit the environment variables 
- Save the .env file securely 
- Make sure the .env file is in .gitignore

 On Windows:
```python
python -m venv venv 
venv\Scripts\activate
 ```

 On UNIX or macOS:
```python
python3 -m venv venv 
source venv/bin/activate
 ```

### 🗃️ Install requirements 
```python
docker-compose up --build
```


### 👥 Create a superuser (optional)
If you want to perform all available features, create a superuser account in a new terminal:
```python
docker exec -it py-dockerize-cinema-db-1 /bin/sh
python manage.py createsuperuser
```

### 😄 Go to site [http://localhost:8000/](http://localhost:8000/)


## 📰 Feature
- **1** JWT Authentication
- **2** Uploading files
- **3** Fake data for test API
- **4** Swagger documentation
- **5** Docker
- **6** Telegram Bot
- **7** Redis as cache handler


## 📝 Contributing
If you want to contribute to the project, please follow these steps:
    1. Fork the repository.
    2. Create a new branch for your feature or bug fix.
    3. Make the necessary changes and commit them.
    4. Submit a pull request.

## 😋 _Enjoy it!_