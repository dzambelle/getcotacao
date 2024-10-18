# What is it?
Python code to get:
  - stock information 
    - BR from B3 site
    - USA from yahoo finance 
  - financial index in Brazil 
    - SELIC from Brazilian central bank
    - IPCA from Brazilian central bank
    - TESOURO DIRETO
  - daily USD / BRL quote from Brazilian central bank

# Database
  - MySQL (not add here since you can use the code and create your own db to save the data)

# How it works
  - Code can be trigger from a cron job to run every 15"minutes and save the information on the database.
  - it call the getcotacao.py (main file) who will call all the others
  - readfile.py handles the read of the ini file (you must setup it) and log file location
  
