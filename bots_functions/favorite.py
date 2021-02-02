from sql import DB_function

class my_favorite:
    def __init__(self):
        # self.user_id = user_id
        self.db_func = DB_function()


    def get_favorite(self, user_id):
        query = 'SELECT favorite FROM user_favorite WHERE ID=\'' + user_id + '\''
        res = self.db_func.DB_query(query)
        return res

    def add_favorite(self, user_id, restaurant_name):
        query = 'SELECT favorite FROM user_favorite WHERE ID=\'' + user_id + '\''
        res = self.db_func.DB_query(query)
        if (restaurant_name in res):
            return (restaurant_name + '已在最愛中~')
        else:
            insert_query = 'INSERT INTO user_favorite (ID, favorite) VALUES (\'' + user_id + '\', \'' + restaurant_name + '\')'
            self.db_func.DB_insert(insert_query)
            self.db_func.DB_commit()
            return ('已將' + restaurant_name + '加入最愛中!!')