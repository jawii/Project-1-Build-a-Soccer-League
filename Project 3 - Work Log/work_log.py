'''
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
'''

import datetime
import csv


class WorkLog():

    welcome_text = "\n*** WELCOME TO WORK LOG *** \n If you want to add new entry, type Add. \n If you want to Lookup" \
                   " older entries type lookup \n"
    tasks_log_file = 'tasks_log.csv'

    def task_or_lookup(self):
        print(self.welcome_text)
        while True:
            user_choice = input(">  ")
            if user_choice.lower() == 'add':
                self.add_task()
            elif user_choice.lower() == 'lookup':
                print("Lookup")
                break
        # TODO Add something to exit the program

    def add_task(self):
        print("*** Add task ***")
        print("You can type Quit anytime to cancel the task adding")
        print("")

        date_input = '00/00/0000 00:00'
        taskname_input = ''

        # ask for date
        task_string = ""
        while True:
            date_input = input("What date and time task has been started? Give the date in form MM/DD/YYYY HH:MM \n > ")
            # 07/22/1988 12:35
            try:
                datetime.datetime.strptime(date_input, "%m/%d/%Y %H:%M")
            except ValueError:
                print("{} isn't valid date format".format(date_input))
                print("")
            else:
                if date_input.lower() == 'quit':
                    self.task_or_lookup()
                task_string += date_input
                break

        # ask for a task name
        while True:
            taskname_input = input("Type your task name: \n > ")
            if taskname_input == "":
                print("No empty task names allowed.")
            elif taskname_input.lower() == 'quit':
                self.task_or_lookup()
            else:
                task_string += " " + taskname_input
                break

        #TODO ask for time spend on task
        spend_time_input = 0
        #TODO ask for general notes about the task
        notes_input = ""

        # Cofirm Task
        print("")
        print("*** Confirm Task ***")
        print("Task start date: {} \n"
              "Task name: {} \n"
              "Time spend: {}\n"
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


    def write_task_to_log(self, string):
        with open(self.tasks_log_file, 'a') as csvfile:
            csvfile.write(string + "\n")

    def task_lookup(self):
        pass

    def clear_screen(self):
        print("\033c", end="")

# WorkLog().task_or_lookup()

work = WorkLog()
work.add_task()
# 07/22/1988 12:35