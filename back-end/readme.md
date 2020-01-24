# Backend Readme
## Getting Started
I am using python 3.8 for this implementation and running Windows 10.

###Setup a virtual python environment in the back-end folder
Start by moving to the location of the repository, mine is located in: **E:\Users\Edward\Documents\GitHub\coding-test\back-end** You will have to change this location!
```
cd E:\Users\Edward\Documents\GitHub\coding-test\back-end
```
Create the virtual environment
```
C:\Users\Edward\AppData\Local\Programs\Python\Python38-32\python.exe -m venv venv
```
Activate the virtual environment
```
.\venv\Scripts\activate.bat
```
Install the requirements
```
pip install -r requirements.txt
```
Copy the json file into the back-end folder and create a copy for the testing
```
copy ..\stores.json .\stores.json && copy ..\stores.json .\stores-test.json
```
Generate the documentation
```
docs\make.bat html
```
Run the tests
```
coverage run -m pytest && coverage report -m
```
Start up the application
```
python main.py
```

##Requirements
- Create a new Python-based application (any framework is fine, we prefer Flask)
- Render the list of stores from the stores.json file in alphabetical order through a backend template
- Use postcodes.io to get the latitude and longitude for each postcode and render them next to each store location in the template
- Build the functionality that allows you to return a list of stores in any given radius of any given postcode in the UK ordered from north to south and unit test it - no need to render anything