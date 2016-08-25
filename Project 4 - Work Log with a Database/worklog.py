'''
WorkLog that will allow employees to enter
their name,
time worked,
task worked on,
and general notes about the task into a database.

There should be a way to
    add a new entry
    list all entries for a particular employee
    list all entries that match a date or search term.

Print a report of this information to the screen, including
    the date
    title of task
    time spent
    employee
    and general notes.
'''
import sys
import os
import datetime

from peewee import *


db = SqliteDatabase('worklogs.db')

class Worklog(Model):
    worker = CharField()
    task_name = CharField()
    timestamp = DateTimeField()
    task_time = DateTimeField()
    notes = TextField()

    class Meta:
        database = db


def initialize():
    """Create database and the table if they don't exist"""
    db.connect()
    db.create_tables([Worklog], safe=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    ''' Prints Start Screen and Add Task or Lookup Task selection'''
    welcome_text = "\n*** WELCOME TO WORK LOG *** \n If you want to add new entry, type Add. \n If you want to Lookup" \
                   " older entries type lookup \n Type Quit to exit the program."
    print(welcome_text)
    while True:
        user_choice = input(">  ")
        if user_choice.lower() == 'add':
            clear_screen()
            add_task()
        elif user_choice.lower() == 'lookup':
            clear_screen()
            lookup_selection()
        elif user_choice.lower() == 'quit':
            clear_screen()
            sys.exit()


def add_task():
    '''
    Asks for
        name
        a task name
        a number of minutes spent working on it
        and any additional notes I want to record
    And creates task with them
    '''
    print("\n*** Add task ***")
    print("You can type Quit anytime to cancel the task adding")
    print("")
    worker = ask_worker_name()
    task_name = ask_task_name()
    timestamp = ask_work_date()
    task_time = ask_for_time_spend_on_task()
    notes = ask_for_notes_to_task()

    #Create Task Or Cancel?
    print("")
    print("*** Confirm Task ***")
    print("Task start date: {} \n"
          "Task name: {} \n"
          "Time spend: {} minutes\n"
          "Notes: {}"
          "\n"
          "Log Task? Type (Y)es or (N)o".format(
        timestamp, task_name, task_time, notes
    ))

    while True:
        confirm_input = input("> ")
        if confirm_input.lower() == 'y':
            Worklog.create(worker=worker,
                           task_name=task_name,
                           timestamp=timestamp,
                           task_time=task_time,
                           notes=notes)
            print("")
            print("Task Added")
            print("")
            main()
        elif confirm_input.lower() == 'n':
            print("")
            print("Task Cancelled!")
            print("")
            clear_screen()
            add_task()


def ask_worker_name():
    worker_name = ""
    while worker_name == "":
        worker_name = input("Give the workers name:\n > ")
    return worker_name


def ask_task_name():
    while True:
        taskname = input("Type your task name.\n > ")
        if taskname == "":
            print("No empty task names allowed.")
        elif taskname.lower() == 'quit':
            main()
        else:
            return taskname


def ask_work_date():
    while True:
        date_input = input("What date and time task has been started."
                           " Give the date in form MM/DD/YYYY HH:MM\n > ")
        # 07/22/1988 12:35
        if date_input.lower() == 'quit':
            main()
        try:
            datetime.datetime.strptime(date_input, "%m/%d/%Y %H:%M")
        except ValueError:
            print("{} isn't valid date format".format(date_input))
            print("")
        else:
            return datetime.datetime.strptime(date_input, "%m/%d/%Y %H:%M")


def ask_for_time_spend_on_task():
    while True:
        spend_time_input = input("How many minutes you spend on task \n >  ")

        if spend_time_input.lower() == "quit":
            main()
        try:
            spend_time_input = int(spend_time_input)
        except ValueError:
            print("{} is not a number.".format(spend_time_input))
        else:
            return spend_time_input


def ask_for_notes_to_task():
    notes_input = input("Give additional notes to task. Press enter if no notes. \n > ")
    if notes_input.lower() == 'quit':
        main()
    return notes_input


def lookup_selection():
    '''find by employee, find by date, find by search term.'''
    print("\n*** Task Lookup ***")
    print("If you want to find task\n"
          "By Employee: Type E \n"
          "By date: Type D \n"
          "By Search: Type S")
    print("Type Quit to Exit Task Lookup.")
    while True:
        user_input = input("> ")
        if user_input.lower() == 'quit':
            main()
        elif user_input.lower() == 'd':
            find_task_by_date()
        elif user_input.lower() == 'e':
            find_task_by_employee()
        elif user_input.lower() == 's':
            find_task_by_search()
        else:
            print("{} was invalid input.".format(user_input))


def find_task_by_date():
    '''presents a list of dates with entries and be able to choose one to see entries from.'''
    print("*** Find by Date ***\n")
    user_choice = ""
    dates = add_task_dates_to_dict()
    # print(dates)
    print("Type number to select the date to look tasks for")
    for keys, value in dates.items():
        print(str(keys + 1) + ") " + value + " \t\t(" + str(how_many_dates_matched(value)) + " logs)")

    while True:
        user_choice = input("> ")
        try:
            int(user_choice)
            if int(user_choice) > len(dates) or int(user_choice) <= 0:
                raise ValueError
        except ValueError:
            print("Not valid choice.")
        else:
            break

    user_choice = int(user_choice) - 1

    # look for date with that and print them
    worklogs = Worklog.select()
    for log in worklogs:
        if log.timestamp.strftime('%A %b %d %Y')==dates[user_choice]:
            print_log(log)


def add_task_dates_to_dict():
    ''' return list of dates with'''
    log_dates = {}
    worklogs = Worklog.select().order_by(Worklog.timestamp.desc())
    no_duplicate_dates = []
    # remove duplicates
    for log in worklogs:
        no_duplicate_dates.append(log.timestamp.strftime('%A %b %d %Y'))

    no_duplicate_dates = set(no_duplicate_dates)
    no_duplicate_dates = list(no_duplicate_dates)

    for key, date in enumerate(no_duplicate_dates):
        log_dates[key] = date

    return log_dates


def print_log(log):
    print("="*len("Work day: " + log.timestamp.strftime('%A %B %d, %Y %I:%M%p')))
    print("Worker: " + log.worker)
    print("Work day: " + log.timestamp.strftime('%A %B %d, %Y %I:%M%p'))
    print("Task: " + log.task_name)
    print("Task took: " + str(log.task_time))
    print("Additional notes: \n" + log.notes)
    print("=" * len("Work day: " + log.timestamp.strftime('%A %B %d, %Y %I:%M%p')))


def how_many_dates_matched(date):
    '''return how many logs are in same date'''
    # dates are in format '%A %b %d %Y'
    count = 0
    worklogs = Worklog.select()
    for log in worklogs:
        if log.timestamp.strftime('%A %b %d %Y') == date:
            count += 1
    return count


def find_task_by_employee():
    print("*** Find by employee *** \n")
    pass


def find_task_by_search():
    print("*** Find By Search *** \n")
    pass








if __name__ == '__main__':
    initialize()
    main()
    #find_task_by_date()

# print(ask_worker_name())
# print(ask_task_name())
# print(ask_work_date())

# main()