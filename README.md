# Persons-Script

A script created in Python that automatically uploads human data from a file to a database. Using commands we operate on 
data in the database (list of available commands below). It also allows you to add more people data using the API.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.
### Installing

Clone the repository

```
Open a terminal with the selected path where the project should be cloned
```
```
Type: git clone https://github.com/szypkiwonsz/Persons-Script.git
```

### Prerequisites
Python Version
```
3.8+
```

Libraries and Packages
```
Open terminal with choosen folder "Persons-Script>"
```

```
Type: pip install -r requirements.txt
```
---

### Running

How to run a script

```
Download or clone project
```
```
Install requirements
```
```
Open terminal with choosen folder "Persons-Script\persons>"
```
```
Type selected command
```
---
### Running tests

How to run tests
```
Do the same as for running the script
```
```
Open terminal with choosen folder "Persons-Script>"
```
```
Type: pytest
```
---
### Avaible commands
```
Each command must be executed in the terminal from a folder "persons-script\persons>"
```
---
Loads persons data from json file to the database

```
python script.py load-from-file
```
---
Shows the percentage of men and women in the database

```
python script.py people-percentage
```
---

Shows the average age of men women or all people in the database

```
python script.py average-age male ---> shows average age of men
```
```
python script.py average-age female ---> shows average age of women
```
```
python script.py average-age all ---> shows average age of all people
```
---

Shows the most common city/cities in the database and the number of appearances

```
python script.py most-common-cities N ---> specify number of cities to show as N
```
---

Shows the most common password/passwords in the database and the number of appearances

```
python script.py most-common-passwords N ---> specify number of passwords to show as N
```
---
Shows people born between the dates given as a parameter

```
python script.py range-dob first_date second_date ---> date format: YYYY-MM-DD
```
---
Shows the password with the most points

```
python script.py safest-password
```
---
Adds the selected number of people to the database

```
python script.py load-from-api N ---> specify number of people to add as N
```
---
## Built With

* [Python 3.8](https://www.python.org/) - The programming language used

## Authors

* **Jan Kacper Sawicki** - [szypkiwonsz](https://github.com/szypkiwonsz)

## Acknowledgments

* The script was made as a recruitment task for an internship
