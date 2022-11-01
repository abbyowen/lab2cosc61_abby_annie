# COSC 61 Lab 2, Part d
## Abigail Owen and Annabel Revers

### .sql files
See README.md from Lab 2, Part c submission. Here, they are used to create tables triggers when first opening the management system and upon reset.

### author_operations.py
This file contains functions that handle operations within for the author role accoring to the System Specifications provided.

### editor_operations.py
This file contains functions that handles operations within for the editor role accoring to the System Specifications provided.

### reviewer_operations.py
This file contains functions that handles operations within for the reviewer role accoring to the System Specifications provided.

### ManUser.py
This file contains our manuscript database user object. It has getters and setters for both user id and role.

### cli.py
This file contains our command-line interface. It establishes a connection with mysql and hten reads the user's input from the command line. It checks for a user's permissions before allowing them to complete the requested action. It also checks the number of arguments given for a command. To run our program and use the manuscript system, run `python3 cli.py` in a command shell. 

### startup.py
This file contains the code to create our tables, triggers, views, and insert our testing data. Before running our command line interface, run `python3 startup.py` in a command shell to create all of our necessary information. **As we noted in Slack, we had a hard time resettng our triggers and views from mysql connector. It is perhaps better to run our sql files in MySQLWorkbench before running the system and after a reset.**






