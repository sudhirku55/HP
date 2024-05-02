PyTest Framework - Web Automation

Keywords:
  
    We have created 70+ keywords for web actions in basic_actions.py file. You can visit this file in Pages_HPX folder. 
   
    We can Inherit the "BasicActions" class into each page and each tests to use all those functions.
   
    Any New web action or web keyword creations is happens, should be written in BasicActions class.
   
   
POM Pattern:

    We have used Page Object Model pattern in this project.  
    
    Each web pages having each separate python file and each python file has each class for each pages.
    
    Each classes contains locators as well as actions of the respective page.
    
Inputs:

    It is a folder for basic configuration like selecting environment, browser, URL, fernet key, etc.,

Drivers:

    Firefox, Chrome, Edge drivers were stored for automation
    
Tests:

    Each page tests written in separate python file based on the requirements.
    
    Each page should contain run command for that respective file also for each test cases 
    
    Page pattern should be:
    
       """
       To run this test suite: pytest -k test_suite_name --html=reports.html
       Number of test covered by this test suite:  
                Pie: 2064, 2065, 3069  (Jira ID's)
              Stage: 2064, 2065, 3070
       """
       
       Class TestSuite:
        
          def testcase(self):
            
            """ 
            To Run this test case :  pytest -s testcase --html=reports.html
            Requirements covered:
                Pie: 2064
              stgae: 2065
            """
            
Utilities:
  
    Contains python files where we can write our needed python functions. for example: API requests, database operations, etc.,
    
    cryptography.exe - It is a application to encrypt and decrypt the password for our credentials
    
Reports:

    There three types of reports configured.
    
    1. HTML report using pytest-html
    2. screen recording as a video file
    3. log file (.log) which keyword called and argument details are presents
    
ReadMe:
 
    BasicActions.html file will explain the keyword and arguments structures and function details

Step-By-Step Procedure To Install:

    Python Installation:

        Go To: python.org

        Download the latest python

        Install the python (Note: Click "Add to Path" checkbox during installation")

    Project Cloning:

        Go To: https://github.azc.ext.hp.com/HP1EIT/HP1Auto

        Click "CODE" button highlighted in Green color and copy the link it is showing

        Navigate to the folder where you want to store the project in your laptop

        Open CMD in the folder and give command as following below:

            git clone  <link_copied>

            Ex:  git clone https://github.azc.ext.hp.com/HP1EIT/HP1Auto.git

    Running the test:

        Open pycharm and open the project folder in it

        Navigate the terminal command to "data" folder in project  
            
            CMD:  cd data

        Run the requirements.txt file using the following command

            pip install -r requirements.txt

        Navigate the terminal path to "test_hpone"

            cd ..
            cd test_hpone

        Use the command we have mentioned in the DOCSTRING for execution

    Database:

        To view the database data, go to : https://sqlitebrowser.org/ download the file

        Install the downloaded file and open the database using installed application

    
    Note: During Installation, Any Error/ Issue you're facing, please contact in teams vijayakumar.gopal@hp.com


Database Operations:

    Adding Data:
    
        To add the data in the database, go to database_operations.py file in utilities

        At the bottom of the file, you can see the function names as "add_data"

        Replace with your details and run that file

    Deleting Data:

        To add the data in the database, go to database_operations.py file in utilities

        At the bottom of the file, you can see the function names as "delete_data

        Fill the data which you want to delete and run the file
