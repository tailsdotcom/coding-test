# Backend Readme
## Getting Started
I am using python 3.8 for this implementation and running on Windows 10.

###Setup a virtual python environment in the back-end folder
Start by moving to the location of the repository, mine is located in: **E:\Users\Edward\Documents\GitHub\coding-test\back-end** You will have to change this location!
```
cd E:\Users\Edward\Documents\GitHub\coding-test\back-end
```
###Create the virtual environment
```
C:\Users\Edward\AppData\Local\Programs\Python\Python38-32\python.exe -m venv venv
```
###Activate the virtual environment
```
.\venv\Scripts\activate.bat
```
###Install the requirements
```
pip install -r requirements.txt
```
###Copy the json file into the back-end folder and create a copy for the testing
```
copy ..\stores.json .\stores.json
```
###Run the tests for coverage and branches
```
coverage run --source=middleware --branch -m pytest && coverage report -m
```
###Run the tests for coverage
```
coverage run --source=middleware -m pytest && coverage report -m
```
###See the pylint score of the application
```
pylint -j 0 main.py middleware\middleware.py middleware\errors.py middleware\helper_methods.py
```
###Generate the Documentation
```
docs\make.bat html
```
The documentation is located in: **docs/_build/html/index.html**
###Start up the application
```
python main.py
```
##View the application
To view the application running go to: [http://localhost:5000](http://localhost:5000)
- Running `GET /sorted/name` will render the stores list in alphabetical order by name
- Running `GET /sorted/postcode` will render the stores list in alphabetical order by postcode
- Running `GET /postcode/` will fetch the latitude and longitude from postcodes.io and update the stores list
- Running `GET /postcode/{postcode}/{max_distance}` will return a list of stores ordered by North/South that have the distance from the submitted postcode and within the maximum specified distance. `GET /postcode/` must be run before this step to fetch latitude and longitudes!

##Coverage & Quality
Line coverage is: 86%
Line and Branch coverage is: 82%
pylint score is: 9.25

##Overall thoughts and improvements
- Postcodes.io returns more than longitude and latitude and writing more code to better analyse the quality of the api request would be better
- I handled as many errors as reasonable for the time-frame, i then boiled them down into two errors, internal and input. This could be better but again for the time-frame I was happy to condense into two general errors.
- The code as a whole is generally unit tested. Main.py is missing tests but as it only acted as a Flask endpoint it seemed less important as I manually tested all routes in the browser. For the time-frame I am happy with the coverage as it also tests a lot of error conditions and edge cases.
- The documentation could always be better, I tried to cover a range to generally show the style I like to use.
- The general architecture should allow for scalability as helper functions that may be used widely are separated as well as all functions render to endpoints allowing internal API calls if necessary.
- I think implementing the haversine formula was probably unnecessary.
- I like that this is probably okay to go into production as most failures are covered and documentation is okay.
- There has been no attempt to optimise the performance of the code as ensuring a correct and repeatable output was deemed more important.
- There are a lot of optimisations that should be put into nearest_store_lookup.
- It was probably unnecessary to implement single_search_postcodes_io as bulk_search_postcodes_io can take a single postcode
- I like the function names and variables as they are descriptive and tell you what the variable is.
- I liked that GU19 5DG is now a terminated postcode as it allowed quicker testing. [https://api.postcodes.io/terminated_postcodes/GU195DG](https://api.postcodes.io/terminated_postcodes/GU15DG)
- There is no built in functionality to handle terminated postcodes.
- I found the last requirement was the toughest as it required multiple smaller functions to happen.
- To improve the test you could ask the candidate to generate documentation.
- I would have liked to used the logging module built into python but it would have required more time.
- I used pylint and [black](https://black.readthedocs.io/en/stable/) throughout to ensure PEP-8 compliance .

##Requirements
- Create a new Python-based application (any framework is fine, we prefer Flask)
- Render the list of stores from the stores.json file in alphabetical order through a backend template
- Use postcodes.io to get the latitude and longitude for each postcode and render them next to each store location in the template
- Build the functionality that allows you to return a list of stores in any given radius of any given postcode in the UK ordered from north to south and unit test it - no need to render anything