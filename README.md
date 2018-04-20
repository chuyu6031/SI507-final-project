# SI507-final-project

## Brief Intro
This program includes 99 design principles written by various companies or authors.
The data was crawled from the source listed below and presented using flask.
The users can filter/search for different principles using author name or keywords.

## Data sources
[Design Principles DTW](https://www.designprinciplesftw.com)

There are three pages with 99 design principles on website.
All principles’ title, author, source and details are crawled using Beautiful Soup.
There isn't any other API keys or client secrets needed to obtain the data from this website.

## Required Module
Please install all modules listed in *requirements.txt* to run the program successfully.

## Code Structure
- data crawling and database established: *final_project_data.py*
- key functions to process data: *model.py*
  - find_principle_by_author
  - find_principle_by_keyword
- uniitest of database and key functions: *final_project_test.py*
- flask: *app.py, templates, and static*

## User Guide
1. Make sure you already install all modules in *requirements.txt*.
2. Open your terminal and go to the correct directory.
3. Run *app.py* in terminal.
4. You will see these lines after successfulling running *app.py* file.

 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 324-859-096
 
5. Copy the url(http://127.0.0.1:5000/) and paste it into your browser.
6. Enjoy design principles!
