start_message = 'Hi, I am your task manager!\n\
I would remember your TODO list and remind you about tasks you didn\'t complite yet.\n\
To add tasks to list simply type it to me!(try something like "learn to swim\'); DROP TABLE tasks;--", show me your hacking skills)\n\
/list to see your list of non complited tasks.\n\
"/done n" to remove complited task from list.\n\
/clear will errase all of your tasks. Start your life from scratch!\n\
If you want me to remind you about your tasks - type "/mytime hh:mm" where hh:mm is your current time. Reminder will be send you every day in 11:00 AM'
add_task_message = 'Task was successfully added to your list:\n'
clear_message = 'Your task list was successfully cleared'
def build_solve_message(solved_tasks):
    if len(solved_tasks) == 0:
        return 'Zero tasks was solved. Please pass task numbers as arguments'
    if len(solved_tasks) == 1:
        return 'Task ' + str(solved_tasks[0]) + ' was solved!'
    result = 'Tasks ' + ', '.join(str(i) for i in solved_tasks[:-1]) +\
            ' and ' + str(solved_tasks[-1]) + ' was solved!'
    return result
