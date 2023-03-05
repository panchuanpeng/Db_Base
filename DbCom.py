import sqlite3


class Cdb:
    def __init__(self, dbname):
        self.dbName = dbname
        self.conn = None
        self.cursor = None
        self.__connect()

    def __connect(self):
        try:
            self.conn = sqlite3.connect(self.dbName)
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(f"conn db err! error is {e}")

    @staticmethod
    def change_tuple(params):
        if len(params) != 0:
            try:
                params = tuple(params[0])
            except TypeError:
                pass
        return params

    def exec_query(self, sql, *params):
        try:
            params = self.change_tuple(params)
            self.cursor.execute(sql, params)
            values = self.cursor.fetchall()
        except Exception as e:
            print(f"exec_query error,error is {e},sql is=", sql)
            return None
        return values

    def exec_cmd(self, sql, *params):
        try:
            params = self.change_tuple(params)
            self.cursor.execute(sql, params)
            self.conn.commit()
        except Exception as e:
            print(f"exec_cmd error,error is {e},sql is=", sql)

    def exec_cmd_many(self, sql, *params):
        try:
            params = self.change_tuple(params)
            self.cursor.executemany(sql, params)
            self.conn.commit()
        except Exception as e:
            print(f"exec_cmd_many error,error is {e},sql is=", sql)

    def close_connect(self):
        try:
            self.cursor.close()
            self.conn.close()
        except Exception as e:
            print(f"close db err! error is {e}")

    def InitTable(self, tb, items):
        """
        :param tb: 表名
        :param items: 表头的列表
        :return: None
        """
        self.__connect()
        item_sql = " varchar(200),".join(items) + " varchar(200)"
        sql = f"create table if not exists {tb}(id integer primary key autoincrement not null,{item_sql})"
        self.exec_cmd(sql)
        self.close_connect()

    def DeleteTable(self, tb):
        """
        :param tb: 表名
        :return: None
        """
        self.__connect()
        sql = f"drop table {tb}"
        self.exec_cmd(sql)
        self.close_connect()

    def AddData(self, tb, items, datas):
        """
        :param tb: 表名
        :param items: 表头的列表
        :param datas: 数据的列表
        :return: None
        """
        self.__connect()
        sql1 = f"insert into {tb}({','.join(items)}) values ({'?,'*(len(items)-1)+'?'})"
        self.exec_cmd(sql1, datas)
        self.close_connect()

    def AddDataMany(self, tb, items, datas):
        """
        :param tb: 表名
        :param items: 表头的列表
        :param datas: 数据的列表
        :return: None
        """
        self.__connect()
        sql1 = f"insert into {tb}({','.join(items)}) values ({'?,'*(len(items)-1)+'?'})"
        self.exec_cmd_many(sql1, datas)
        self.close_connect()

    def DeleteData(self, tb, items, datas):
        """
        :param tb: 表名
        :param items: 索引
        :param datas: 值,一个元组（1，）
        :return: None
        """
        self.__connect()
        sql1 = f"delete from {tb} where {items}=?"
        self.exec_cmd(sql1, datas)
        self.close_connect()

    def EditData(self, tb, items, datas, key_item, key_value):
        """
        :param tb: 表名
        :param items: 表头的列表
        :param datas: 值,一个元组（1，）
        :param key_item: 查询关键字
        :param key_value: 关键字的值
        :return: None
        """
        self.__connect()
        sql1 = f"update {tb} set {'=?,'.join(items)}=? where {key_item}=?"
        self.exec_cmd(sql1, datas + [key_value])
        self.close_connect()

    def GetData(self, tb):
        """
        :param tb: 表名
        :return: 表内的所有数据，二维列表
        """
        self.__connect()
        sql1 = f"pragma table_info({tb})"
        res = self.exec_query(sql1)
        res = [[t[1] for t in res]]
        sql2 = f"select * from {tb}"
        res = res + self.exec_query(sql2)
        self.close_connect()
        return res


if __name__ == "__main__":
    pass
    DbName = "test.db"
    tb_name = "test"
    item = ["A1", "B1", "C1", "D1", "E1"]
    data = ["A1", "B6", "C1", "D1", "E1"]
    cdb = Cdb(DbName)
    cdb.InitTable(tb_name, item)
    cdb.AddData(tb_name, item, data)
    data1 = [["A1", "B6", "C1", "D1", "E1"],["A1", "B6", "C1", "D1", "E1"],["A1", "B6", "C1", "D1", "E1"],["A1", "B6", "C1", "D1", "E1"]]
    cdb.AddDataMany(tb_name, item, data1)
    # cdb.DeleteData(tb_name, "id", 1)
    # cdb.EditData(tb_name, item, data, "id", 2)
    # cdb.DeleteTable(tb_name)
    print(cdb.GetData(tb_name))
