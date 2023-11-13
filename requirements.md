# Software Requirements Specification (SRS)

Number: 1
--------------------------
Statement: Software must remember a list of tasks, that can be added to and edited by the user.

Evaluation Method: Will be satisfied if the user can have 10 separate tasks, and each can then be edited and deleted.

Dependency: None

Priority: Essential

Requirement revision history: None


Number: 2
--------------------------
Statement: Software must remember tasks through a system shutdown.

Evaluation Method: Reboot the system running the program to see if it will retain data on reboot.

Dependency: None

Priority: Essential

Requirement revision history: None

Number: 3
--------------------------
Statement: Software must support separate users.

Evaluation Method: 3 unique users can log in to the software with different usernames and passwords.

Dependency: None

Priority: Essential

Requirement revision history: None


Number: 4
--------------------------
Statement: Software will notify users increasingly often of their deadlines as they approach.

Evaluation Method: Measure how often the user is alerted on a specific deadline. If the interval changes signifigantly (more than a few minutes), success.

Dependency: None

Priority: Essential

Requirement revision history: None


Number: 5
--------------------------
Statement: Software will run on Windows 10.

Evaluation Method: Run on a computer running an installation of Windows 10.

Dependency: None

Priority: Essenstial

Requirement revision history: None


Number: 6
--------------------------
Statement: Software will be able to be told which window is "on task" and will sound an alarm if you are off task for a specified amount of time. 

Evaluation Method: Select a browser window to be "on task", select another window then see if we get an alarm after 15 minutes. Do the same with the window selected.

Dependency: 5

Priority: High

Requirement revision history: None


Number: 7
--------------------------
Statement: Software should recommend subtasks to help break up tasks into more manageable pieces.

Evaluation Method: A button should be included that will use ChatGPT to take a task as written and suggest 3 separate new subtasks.

Dependency: None

Priority: If time permits
Requirement revision history:None
