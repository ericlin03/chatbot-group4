from sql import DB_function

class my_favorite:
    def __init__(self):
        # self.user_id = user_id
        self.db_func = DB_function()

    def get_favorite(self, user_id):
        query = 'SELECT favorite FROM user_info WHERE ID=\'' + user_id + '\''
        result = self.db_func.DB_query(query)
        fav = result.split(' ')
        return fav
        
    def add_favorite(self, user_id, restaurant_name):
        # current_fav = get_favorite(user_id)
        # original_fav = ''
        # for i in range(len(current_fav)):
        #     original_fav += current_fav[i]
        original_fav = self.db_func.DB_query('SELECT favorite FROM user_info WHERE ID=\'' + user_id + '\'')
        print(original_fav)
        query = 'UPDATE user_info SET favorite=\'' + original_fav + ' ' + restaurant_name + '\' WHERE ID=\'' + user_id + '\';'
        self.db_func.DB_insert(query)
        self.db_func.DB_commit()
        return ('已把' + restaurant_name + '加入我的最愛中!!')