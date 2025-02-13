# Computer Science Capstone 2020
# High Impact Experience Project

   This is the official GitHub repo for the Southwestern University 2020 Capstone, High Impact Experiences Project.

## Description

Southwestern University students participate in a variety of High Impact Experiences (HIEs), including first-year seminars, study abroad programs, academic internships, community engaged-learning, SCOPE, and senior seminar projects. Since HIEs are strong indicators of student success, data about student participation is tracked and utilized by numerous departments on campus. The goal of this Computer Science Capstone project is to move away from manual processing by individuals knowledgeable about the data, to an internal web tool that provides an easy way for staff to interact with the data about thousands of students. Currently, the data about these experiences is stored in several decentralized databases. While our project will not have direct access to these databases, it will be used to gather the information from these disparate sources. The tool will allow for quick manipulation of the data for querying using MySQL in conjunction with Google Cloud Platform, readily visualizing information about existing data using Bokeh, and Python Flask for the backend. Ultimately, this tool will increase the readability of the information, facilitate updating and adding information, and shorten the time needed to perform data analysis. 

## Getting Started

### Dependencies

* Anaconda
* Flask
* Flask-sqlalchemy
* Flask-cors
* Some flavour of relational database, MySQL or SQLite recommended
* Angular

### Installation and Running Program

* Fork or download the repository
* Install dependancies for Flask and Angular
* Inside "instance" folder, change database URI info and create new secret key
* If using custom data, please consult the [Develpers Manual](https://docs.google.com/document/d/11v9bZ9jAxd6rLdgNfTPL05XJn2khUwS5kAbbUEdu1mc/edit?usp=sharing)
* From folder, run command from CLI
```
flask run
```
* Server should start on [localhost:5000](http://localhost:5000/)
* Due to routing issues, a file testWithFrontEnd.py is included which can be run as a normal python executable

## Help

* [Developers Manual](https://docs.google.com/document/d/11v9bZ9jAxd6rLdgNfTPL05XJn2khUwS5kAbbUEdu1mc/edit?usp=sharing)

## Authors

Matt Sanford: [[email](Mattsanford@protonmail.com)]

Hazel Hedrick

Darwin Johnson

Victoria Negus

Alice Quintanilla: [[email](alice.quintanilla98@gmail.com)]

## Acknowledgments

### People

* Dr. Barbara Anthony
* Dr. Sarah Brackmann
* Dr. Williams
* Hal Hoeppner
