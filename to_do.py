import re
import pandas as pd
import numpy as np

"""
add_task() function:
designed to add a new task to the to-do list stored in a Pandas DataFrame (todo_df) 
Parameters:
- todo_df: existing to-do list stored in a DataFrame
- task_descrp: string containing the details of the task
"""
def add_task(todo_df, task_descrp):

    #creates new df with a new task
    new_task = pd.DataFrame({'Task': [task_descrp]})

    #link (concatenate) new task df with existing to-do df
    todo_df = pd.concat([todo_df, new_task], ignore_index=True)

    #printing message saying task has been added to to-do list
    print(f'Task "{task_descrp}" added to the to-do list.')

    #return updated to-do dataframe
    return todo_df

"""
split_task_decrp(): split a task description into a list of words
Parameters:
- task: task description that is being split 
"""
def split_task_descrp(task):

    #using split() method to split task into list of words
    words = task.split()

    #return list of words
    return words

"""
escape_special_charc(): Use a backslash to escape a special character in the task description
Parameters:
- task: task description that is being processed
"""
def escape_special_charc(task):
    
    #replace the single quote with escaped single quotes
        #this is needed in case special characters are used
    escaped_task = task.replace('\'', '\\\'')

    #returns modified task description
    return escaped_task

"""
use_raw_string(): Use a raw string to avoid needing to use backslashes
Parameters:
- task: the task description
"""
def use_raw_string(task):
   
    #link(concat) task with raw string prefix
    raw_task = r"Raw string: " + task
    return raw_task

"""
check_task_pattern(): Use a regular expression to check if a task matches a certain pattern
Parameters:
- task: the task description that needs to be checked
"""
def check_task_pattern(task):
    
    #specific pattern the string should match
    #includes upper/lowercase letters, digits, and special characters
    pattern = r'^[A-Za-z\s]+$'

    #checks if task matches pattern using re.match()
    #re.match(): checks if regular expression pattern matches the beginning of a string
    return re.match(pattern, task) is not None

"""
extract_task_info(): Use regular expressions with groupings to extract information from a task
Parameters:
- task: task description to extract info from
"""
def extract_task_info(task):
   
    #regular expression pattern with named capture groups
    #the named capture groups, action and task match some of the characters
    #action captured group matches the action of task
    #item captured group matched the item of the task
    match = re.match(r'^(?P<action>\w+) (?P<item>\w+)$', task)

    #check if there is a match
    if match:
        
        #extract info using the named capture groups
        action = match.group('action')
        item = match.group('item')
        print(f"Action: {action}, Item: {item}")
    
    #print message for invalid format
    else:
        print("Invalid task format.")

"""
vector_computate(): Use numpy to perform a vectorized computation on the to-do list df
Parameters:
- todo_df: to-do list dataframe
"""
def vector_computate(todo_df):

    #checks if 'Task_Length' column exists
    if 'Task_Length' not in todo_df.columns:
        print("\nTask lengths computation skipped. No tasks added.")
    
    else:
        #perform vectorized computation using NumPy
        #apply the len function to each element
        todo_df['Task_Length'] = np.vectorize(len)(todo_df['Task'])
        print("\nTask lengths computed using vectorized computation:")

        #print updated dataframe
        print(todo_df)

"""
read_csv_to_df(): Read in a CSV of data into a DataFrame using pandas.
Parameters:
- csv_filename: filename of the CSV file being read 
"""
def read_csv_to_df(csv_filename):
   
    try:
        #try to read data
        df = pd.read_csv(csv_filename)
        print("\nData loaded from CSV:")
        print(df)

    #if file is not found, produce error
    except FileNotFoundError:
        print(f"\nFile '{csv_filename}' not found. Creating an empty DataFrame.")

        #create empty dataframe with 'Task' column
        df = pd.DataFrame(columns=['Task'])

    #return dataframe (either the empty or loaded one)
    return df

"""
subset_dataframe(): Use pandas to get a subset of a DataFrame using a boolean condition.
Parameters:
- todo_df: to-do list input dataframe
"""
def subset_dataframe(todo_df):
    
    #subset dataframe where task length > 10
    subset_df = todo_df[todo_df['Task_Length'] > 10]

    #print subset
    print("\nSubset of DataFrame where Task_Length > 10:")
    print(subset_df)
    return subset_df

"""
write_to_csv(): Write data to a CSV using pandas.
Parameters:
- todo_df: dataframe to be written in CSV file
- csv_filename: filename of CSV file
"""
def write_to_csv(todo_df, csv_filename):
    
    #write dataframe to specified csv file
    todo_df.to_csv(csv_filename, index=False)
    print(f"\nData written to {csv_filename}")


"""
generate_todo_list(): Simple to-do list program that allows the user to enter tasks
Parameter: none
"""
def generate_todo_list():

    #initializing empty to-do list dataframe
    todo_df = pd.DataFrame(columns=['Task'])

    while True:
        #displaying current to-do list
        print("\n==== To-Do List ====")
        print(todo_df)

        #prompting user to enter tasks
        user_input = input("\nEnter a task (type 'exit' to quit): ")

        #if the user is done entering tasks, can quit the program
        if user_input.lower() == 'exit':
            print("\n==== Final To-Do List ====")
            print(todo_df)
            print("Exiting the to-do list program.")
            break

        #add the task to the to-do list
        todo_df = add_task(todo_df, user_input)

        #split task description into a list of words
        words = split_task_descrp(user_input)
        print(f"Task words: {words}")

        #escape special characters in the task description
        escaped_task = escape_special_charc(user_input)
        print(f"Escaped task: {escaped_task}")

        #use a raw string
        raw_task = use_raw_string(user_input)
        print(raw_task)

        #check if the task matches a certain pattern
        if check_task_pattern(user_input):
            print("Task format is valid.")

        #printing message if format is invalid 
        else:
            print("Task format is invalid.")

        #extract information from the task using regular expressions
        extract_task_info(user_input)

    #perform vectorized computation on the to-do list DataFrame
    vector_computate(todo_df)

    #read in a CSV file into a DataFrame
    csv_filename = 'todo_data.csv'
    todo_df_csv = read_csv_to_df(csv_filename)

    #get a subset of the DataFrame using a boolean condition
    subset_df = subset_dataframe(todo_df_csv)

    #write data to a CSV file
    write_to_csv(subset_df, 'subset_todo_data.csv')

#this code checks if the script is the main program
#if it is the main program, the code under the progam will run
#the function thats going to run is generate_todo_list() which will start the program
if __name__ == "__main__":
    generate_todo_list()