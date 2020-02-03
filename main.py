import config
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import messages
import sqlite3

def add_task(update, context):
    connection = sqlite3.connect(config.db_path)
    cursor = connection.cursor()
    cursor.execute('INSERT INTO tasks (user_id,task) VALUES (?,?);',\
            (update.effective_user.id, update.message.text))
    connection.commit()
    connection.close()
    message = messages.add_task_message +\
            build_tasks_list(update.effective_user.id)
    context.bot.send_message(chat_id = update.effective_chat.id,\
            text = message)
    

def start(update, context):
    connection = sqlite3.connect(config.db_path)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users WHERE id=?;',\
            (update.effective_user.id,))
    if len(cursor.fetchall()) < 1:
        cursor.execute('INSERT INTO users VALUES (?,?,NULL);',\
                (update.effective_user.id, update.effective_chat.id))
    connection.commit()
    connection.close()
    context.bot.send_message(chat_id = update.effective_chat.id,\
                              text = messages.start_message)

def list_tasks(update, context):
    message = build_tasks_list(update.effective_user.id)
    if message == '':
        message = 'You have no tasks'
    else:
        message = 'Your tasks:\n' + message
    context.bot.send_message(chat_id = update.effective_chat.id,\
            text = message)

def build_tasks_list(user_id):
    tasks = get_tasks(user_id)
    return '\n'.join([str(i+1)+'. '+tasks[i] for i in range(len(tasks))])

def get_tasks(user_id):
    conn = sqlite3.connect(config.db_path)
    c = conn.cursor()
    c.execute('SELECT task FROM tasks WHERE user_id=?;', (user_id,))
    result = c.fetchall()
    conn.close()
    return [e[0] for e in result]

def solve(update, context):
    if len(context.args) == 0:
        context.bot.send_message(chat_id = update.effective_chat.id,\
                text = messages.build_solve_message([]))
        return
    connection = sqlite3.connect(config.db_path)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM tasks WHERE user_id=?;',\
            (update.effective_user.id,))
    result = cursor.fetchall()
    solved_tasks = []
    args = list(set(context.args))
    for a in args:
        number = check_int(a, len(result))
        if number == 0: continue
        solved_tasks.append(number)
        cursor.execute('DELETE FROM tasks WHERE id=?;', (result[number-1][0],))
    connection.commit()
    connection.close()
    solved_tasks.sort()
    tasks = build_tasks_list(update.effective_user.id)
    message = messages.build_solve_message(solved_tasks) 
    if tasks != '':
        message = message + '\nCurrent tasks:\n' + tasks
    else:
        message += '\nYou have no tasks'
    context.bot.send_message(chat_id = update.effective_chat.id,\
            text = message)

def check_int(a, maxQ):
    try:
        r = int(a)
        if r > maxQ or r < 1:
            return 0
        return r
    except:
        return 0

def clear(update, context):
    connection = sqlite3.connect(config.db_path)
    cursor = connection.cursor()
    cursor.execute('DELETE FROM tasks WHERE user_id=?;',\
            (update.effective_user.id,))
    connection.commit()
    connection.close()
    message = messages.clear_message + \
            build_tasks_list(update.effective_user.id)
    context.bot.send_message(chat_id = update.effective_chat.id,\
            text = message)

def main():
    updater = Updater(token=config.TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',\
                        level=logging.INFO)
    start_handler = CommandHandler('start', start)
    clear_handler = CommandHandler('clear', clear)
    solve_handler = CommandHandler('done', solve)
    list_handler = CommandHandler('list', list_tasks)
    message_handler = MessageHandler(Filters.text, add_task)
    dispatcher.add_handler(list_handler)
    dispatcher.add_handler(message_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(clear_handler)
    dispatcher.add_handler(solve_handler)
    updater.start_polling()


if __name__ == '__main__':
    main()
