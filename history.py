from sql import DB_function

def get_history(user_id):
    res = DB_function.DB_query('SELECT recently FROM user_info WHERE ID=\'' + user_id + '\'')
    history = res.split(' ')
    return history

def add_history(user_id, restaurant_name):
    counter = DB_function.DB_query('SELECT counter FROM user_info WHERE ID=\'' + user_id + '\'')
    res = DB_function.DB_query('SELECT recently FROM user_info WHERE ID=\'' + user_id + '\'')
    history = res.split(' ')
    history[counter] = restaurant_name
    put_back = ''
    for i in range(len(history)):
        put_back += history[i]
    counter = (counter + 1) % 10
    DB_function.DB_insert('UPDATE user_info SET recently=\'' + put_back + '\' WHERE ID=\'' + user_id + '\';')
    DB_function.DB_insert('UPDATE user_info SET counter=\'' + counter + '\' WHERE ID=\'' + user_id + '\';')
    DB_function.DB_commit()