"""
    This is DB Function.
    Using MySQL.
    CRUD ... Create / Read / Update / Delete
"""
import MySQLdb
import random

DB_NAME = ""
TABLE_NAME = ""

class DBManager():
    # 生成された画像を保存
    def create(self):
        pass

    # 過去の作成物を表示するのに利用(ランダムに)
    def read_random_part(self):
        conn = MySQLdb.connect(
                user='',
                passwd='',
                host='',
                db=DB_NAME
                )
        cur = conn.cursor()
        # データの総数を入手
        sql = "select count(*) from {}".format(TABLE_NAME)
        cur.execute(sql)
        n = cur.fetchall()
        # random関数で総数以下の数値を20個ぐらい生成
        res_num = set()
        while len(list) < 20:
            res_num.add(random.randint(1, n))
        # 生成した数番目のデータを取得する
        res_data = []
        for _ in range(20):
            sql = "select count(*) from {} where {}".format(TABLE_NAME, res_num.pop())
            cur.execute(sql)
            res_data.append(cur.fetchall())

        conn.close()
