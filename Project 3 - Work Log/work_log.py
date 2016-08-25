"""
Develop a terminal application for logging what work someone did on a certain day.
The script should ask for:
    a date
    a task name
    how much time was spent on the task
    and any general notes about the task.
Record each of these items into a row of a CSV file along with a date.

Provide a way for a user to find all of the tasks that were done
on a certain date
or that match a search string (either as a regular expression or a plain text search).

Print a report of this information to the screen, including the
    date,
    title of task,
    time spent, and
    general notes.
"""

import datetime
# import csv
import re
import math
import sys

def sort_list_of_dates(datelist):
    dates = [datetime.datetime.strptime(ts, "%m/%d/%Y") for ts in datelist]
    dates.sort()
    sorted_list = [datetime.datetime.strftime(ts, "%m/%d/%Y") for ts in dates]
    return sorted_list

def press_enter_to_continue():
    while True:
        print("")
        input_ = input("Press Enter to continue")
        if input_ == "":
            break


class WorkLog():

    welcome_text = "\n*** WELCOME TO WORK LOG *** \n If you want to add new entry, type Add. \n If you want to Lookup" \
                   " older entries type lookup \n Type Quit to exit the program."
    tasks_log_file = 'tasks_log.csv'

    def task_or_lookup(self):
        print(self.welcome_text)
        while True:
            user_choice = input(">  ")
            if user_choice.lower() == 'add':
                self.add_task()
            elif user_choice.lower() == 'lookup':
                self.lookup_selection()
            elif user_choice.lower() == 'quit':
                sys.exit()


    def add_task(self):
        print("\n*** Add task ***")
        print("You can type Quit anytime to cancel the task adding")
        print("")

        date_input = '00/00/0000 00:00'
        taskname_input = ''
        spend_time_input = ''

        # ask for date
        task_string = ""
        while True:
            date_input = input("What date and time task has been started? Give the date in form MM/DD/YYYY HH:MM \n > ")
            # 07/22/1988 12:35
            if date_input.lower() == 'quit':
                self.task_or_lookup()
            try:
                datetime.datetime.strptime(date_input, "%m/%d/%Y %H:%M")
            except ValueError:
                print("{} isn't valid date format".format(date_input))
                print("")
            else:
                task_string += date_input + ","
                break

        # ask for a task name
        while True:
            taskname_input = input("Type your task name: \n > ")
            if taskname_input == "":
                print("No empty task names allowed.")
            elif taskname_input.lower() == 'quit':
                self.task_or_lookup()
            else:
                task_string += taskname_input + ","
                break

        while True:
            spend_time_input = input("How many minutes you spend on task? \n > ")

            if spend_time_input.lower() == "quit":
                self.task_or_lookup()
            try:
                spend_time_input = int(spend_time_input)
            except ValueError:
                print("{} is not a number.".format(spend_time_input))
            else:
                task_string += str(spend_time_input) + ","
                break

        notes_input = input("Give additional notes to task. Press enter if no notes. \n > ")

        if notes_input.lower() == 'quit':
            self.task_or_lookup()

        task_string += notes_input + ","

        # Confirm Task
        print("")
        print("*** Confirm Task ***")
        print("Task start date: {} \n"
              "Task name: {} \n"
              "Time spend: {} minutes\n"
              "Notes: {}"
              "\n"
              "Log Task? Type (Y)es or (N)o".format(
            date_input,taskname_input, spend_time_input, notes_input
        ))

        while True:
            confirm_input = input("> ")
            if confirm_input.lower() == 'y':
                self.write_task_to_log(task_string)
                print("")
                print("Task Added")
                print("")
                self.task_or_lookup()
            elif confirm_input.lower() == 'n':
                print("")
                print("Task Cancelled!")
                print("")
                self.add_task()

    def lookup_selection(self):
        print("\n*** Task Lookup ***")
        print("If you want to find task by \n"
              "Date: Type Date \n"
              "Time spent: Type Time \n"
              "Exact search: Type Search \n"
              "Pattern: Type Pattern \n")
        print("Type Quit to Exit Task Lookup.")
        while True:
            user_input = input("> ")
            if user_input.lower() == 'quit':
                self.task_or_lookup()
            elif user_input.lower() == 'date':
                self.find_by_date()
            elif user_input.lower() == 'time':
                self.find_by_time_spend()
            elif user_input.lower() == 'search':
                self.find_by_search()
            elif user_input.lower() == 'pattern':
                self.find_by_pattern()
            else:
                print("{} was invalid input.".format(user_input))

    def read_tasks_to_dic(self, file):

        work_log = file
        # find dates and puts them to dictionary:

        line = re.compile(r'''
                    (?P<date>(?P<month> \w+)/(?P<day> \w+)/(?P<year> \w+))\W
                    (?P<task_time> \w+\:\w+)\,
                    (?P<task_name> [\w\ ]*)\,
                    (?P<task_length> \w+)\,
                    (?P<task_notes> [\w\ \.\!]*)\,$
                    ''', re.M | re.X)

        list_of_tasks = []
        for match in line.finditer(work_log):
            # print(match)
            # print(match.groupdict())
            list_of_tasks.append(match.groupdict())

        return list_of_tasks

    def print_task(self, task_dict):
        print("Work done: " + task_dict['date'])
        print("Task name: " + task_dict['task_name'])
        print("Task started: " + task_dict['task_time'])
        print("Task took: " + task_dict['task_length'] + " minutes")
        print("Additional notes: " + task_dict['task_notes'])
        print()

        #{'task_length': '120', 'task_name': 'Driver', 'year': '2016', 'date': '01/10/2016', 'month': '01',
        # 'task_time': '13:00', 'task_notes': 'Drived boss to lunch', 'day': '10'}

    def find_by_date(self):
        '''
        Presents list of task dates and user can type which date to check tasks
        '''
        print("*** Find by Date ***\n")

        list_of_tasks = self.read_tasks_to_dic(self.open_file())
        # print(list_of_tasks)

        # remove duplicates and put the dates in order
        list_of_tasks_dates = []

        print("Choose The Date from the list by typing that date in same format")
        for task in list_of_tasks:
            if task['date'] not in list_of_tasks_dates:
                list_of_tasks_dates.append(task['date'])

        list_of_tasks_dates = sort_list_of_dates(list_of_tasks_dates)
        for date in list_of_tasks_dates:
            print("\t" + date)

        matched_tasks = []

        while True:
            user_choice = input("> ")
            if user_choice in list_of_tasks_dates:
                for task in list_of_tasks:
                    if task['date'] == user_choice:
                        matched_tasks.append(task)
                break
            else:
                print("Not valid date.")

        # print(matched_tasks)
        # print tasks
        print("Tasks for that date: \n")
        for task in matched_tasks:
            self.print_task(task)
            print("")

        press_enter_to_continue()
        self.lookup_selection()

    def find_by_time_spend(self):
        ''' find entries within a range of time spent on a task'''
        print("*** Find by Time ***\n")

        list_of_tasks = self.read_tasks_to_dic(self.open_file())

        while True:
            lower_bound = input("Type lower bound of time (minutes) spend on task."
                                        "\nIf no lower bound, press Enter \n > ")

            upper_bound = input("Type upper bound of time (minutes) spend on task. "
                                "\nIf no upper bound press Enter\n > ")
            try:
                if lower_bound == "":
                    lower_bound = 0
                else:
                    lower_bound = int(lower_bound)
                if upper_bound == "":
                    upper_bound = math.inf
                    search_string_value = "infinity"
                else:
                    upper_bound = int(upper_bound)
                    search_string_value = str(upper_bound)
                    if int(lower_bound) > int(upper_bound):
                        print("\nLower bound is greated than upper bound. Try again.\n")
                        continue
            except ValueError:
                print("Not valid time ranges. Give only the value.\n")
            else:
                break
        print("You are searching times in range "
              "" + str(lower_bound) + " minutes" + " - " + search_string_value + " minutes.")

        press_enter_to_continue()

        matched_tasks = []

        print("\n\n** Here are tasks for that time range.\n **")
        for task in list_of_tasks:
            time = int(task['task_length'])
            # print(str(time))
            if time <= upper_bound and time > lower_bound:
                matched_tasks.append(task)

        for task in matched_tasks:
            self.print_task(task)
        print("\n** End of list **")

        press_enter_to_continue()
        self.lookup_selection()

    def find_by_search(self):
        '''
        As a user of the script, if finding by an exact string,
        I should be allowed to enter a string and then be presented with
        entries containing that string in the task name or notes.
        :return:
        '''
        print("*** Find by exact search ***\n")

        search_string = input("What you want to search?\n > ")

        matched_tasks_string = ""
        with open(self.tasks_log_file) as log_file:
            for line in log_file:
                if search_string in line:
                    matched_tasks_string += line + "\n"
        # print(matched_tasks_string)

        matched_tasks = self.read_tasks_to_dic(matched_tasks_string)

        print("** Search results **\n")
        for task in matched_tasks:
            self.print_task(task)
        press_enter_to_continue()
        self.lookup_selection()

    def find_by_pattern(self):
        '''
        As a user of the script, if finding by a pattern,
        I should be allowed to enter a regular expression and
        then be presented with entries matching that pattern in their task name or notes.
        '''
        print("*** Find by Pattern ***\n")

        user_re = input("Give regular expression to search.\n > ")
        log_file = self.open_file()
        line = re.findall(user_re, log_file)
        # print(line)

        matched_tasks_string = ""
        with open(self.tasks_log_file) as log_file:
            for match in line:
                for lines in log_file:
                    if match in lines:
                        matched_tasks_string += lines + "\n"
        matched_tasks = self.read_tasks_to_dic(matched_tasks_string)
        # print(matched_tasks)

        # no DRY here
        print("** Search results **\n")
        for task in matched_tasks:
            self.print_task(task)
        press_enter_to_continue()
        self.lookup_selection()

    def write_task_to_log(self, string):
        with open(self.tasks_log_file, 'a') as csvfile:
            csvfile.write(string + "\n")

    def open_file(self):

        names_file = open(self.tasks_log_file, encoding="utf-8")
        data = names_file.read()
        names_file.close()

        return data

    def clear_screen(self):
        print("\033c", end="")

WorkLog().task_or_lookup()

# work = WorkLog()
# work.add_task()
# work.lookup_selection()
# work.task_or_lookup()
# work.find_by_date()
# work.find_by_time_spend()
# work.find_by_search()
# work.find_by_pattern()