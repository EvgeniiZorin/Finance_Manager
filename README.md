# Finance_Manager
> ver 3.3.2

This is a program for calculating spendings based on a financial record. It creates summarisation graphs on different parameters. 

<!-- <img align="center" alt="Python" width="500px" src="https://github.com/EvgeniiZorin/Finance_Manager/blob/4e84b908a629222a0b3052c9d5ab64f5c574e43e/Finance_manager_demo.png"/> -->

![image alt text](https://github.com/EvgeniiZorin/Finance_Manager/blob/4e84b908a629222a0b3052c9d5ab64f5c574e43e/Finance_manager_demo.png)

You can view the application demo via the link below:

https://youtu.be/WE1XGUu19EM


## Input

A spendings file containing spendings in the following format (columns separated by tabs, at the end of each line there is a newline):
```tsv
Date         Category    Amount   Currency
01.09.2021   groceries   100      MXN
```
For the same month, the same categories can contain multiple recordings - these are summed up in the processing. For reference, please see `Finance_record.tsv`. 

## How to run

To run the program, execute the main script `Main.py`. This open up a GUI, with which you then choose a finance record file of your choice and then can utilise the available functionality. 

For best experience, this script could be converted to an `.exe` file by running the following command in the Python terminal:
```py
pyinstaller -w Main.py
```
I didn't include the `.exe` file because it is too large to store on the Github :(

## Functionality

This python script reads a specified spendings file (for example, `Finance_record.tsv`) with information on spendings by date and category, and outputs some interesting information on the spendings:

**Finance summary**:
- Print unique categories present in the chosen finance file; 
- Print the time frame for which the financial record is available;

**Visualisations**:
- Show total spendings per month (all-time);
- Show total spendings per month (in a specified year);
- Show spendings per month over a specified period; 
- Show spendings for a specified category over a specified period of time; 
