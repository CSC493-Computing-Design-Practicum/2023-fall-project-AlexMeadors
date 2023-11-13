# Main Project

## Method: Main
Runs on program startup
Runs Tkinter Setup for the "root" object
Runs Show Login Screen
Tracks root, the focus window, and time "off task"
Loops running Track Focus Window once every 10 seconds
If time off task is more than 5 minutes, will run System Notification

## Method: Tkinter Setup
Runs from Main
Sets up the main tkinter object we need, root
Returns root

## Method: Login to Database
Uses the login obtained from the login screen to create a connection to the MySQL database
Runs when the user presses the login button on the login screen
Returns success or error, with a failed login giving the user another chance to log in

## Method: Send to Database
Sends a message to the database
Returns Nothing
Used in all other database methods

## Method: Read from Database
Retrieves data from the database
Used in Search Database
Returns the query results

## Method: Search Database
Sends a query to the database and then gets the results
Returns the results from Read from Database
Uses Send to Database and Read from Database as helper functions

## Method: Add to Database
Sends a query to the database adding a task
Uses Send to Database as a helper function

## Method: Remove from Database
Sends a query to the database removing a task
Uses Send to Database as a helper function

## Method: Edit Database
Sends a query to the data base editing a task
Uses Send to Database as a helper function

## Method: Set Task Window
Triggered on button press / Event handler
Can set what the "on task" window is, updates it in the main
Returns new on task window to main

## Method: Track Focus Window
Checks what your in focus window is. If it is not the "on task" window, update the time off task in the main
Returns the new time off task to the main

## Method: System Notification
Shows a Windows system notification to get the users attention.
Runs from the main when off task too long

## Method: Show Login Screen
Displays the login screen
Takes root from the main, runs at program start
Has a button that runs Login to Database, which will connect the program to the database

## Method: Show Task Screen
Shows our list of tasks, with buttons for adding, removing, and editing tasks
Has buttons that runs Add to Database, Remove from Database, and one that shows the Task Edit Screen

## Method: Show Task Edit Screen
Runs when the user selects a task and then chooses to edit it.
Takes the information of the task, sets it all within text boxes so the user can edit it
Runs Edit Database once the user clicks the submit button, then goes back to the Show Task Screen
