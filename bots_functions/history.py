from sql import DB_function

class history:
    def __init__(self):
        self.db_func = DB_function()

    def get_history(self, user_id):
        query = 'SELECT recently_0, recently_1, recently_2, recently_3, recently_4, recently_5, recently_6, recently_7, recently_8, recently_9 FROM user_info where ID=\'' + user_id + '\''
        res = self.db_func.DB_query(query)
        output = []
        for i in range(len(res)):
            if (res[i] is not None):
                output.append(res[i])
        return output

    def add_history(self, user_id, restaurant_name):
        query = 'SELECT counter FROM user_info WHERE ID=\'' + user_id + '\''
        counter = self.db_func.DB_query(query)
        counter = int(counter[0])
        add_query = 'UPDATE user_info SET recently_' + str(counter) + '=\'' + restaurant_name + '\' WHERE ID=\'' + user_id + '\''
        counter = (counter + 1) % 10
        counter_query = 'UPDATE user_info SET counter=\'' + str(counter) + '\' WHERE ID=\'' + user_id + '\''
        self.db_func.DB_insert(add_query)
        self.db_func.DB_insert(counter_query)
        self.db_func.DB_commit()