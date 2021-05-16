import sqlite3
constrains = {"not null":"NOT NULL","unique":"UNIQUE","primary key":"PRIMARY KEY","check":"","default":"","auto":"AUTOINCREMENT"}

__DataBase__ = "api_database.db"

class Model():
    def __init__(self,table_name):
        self.table_name = table_name
        self.fields = []
        con = self.open()
        cur = con.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?",[self.table_name])
        count = cur.fetchall()
        print(count)
        if len(count) <= 0:
            self.exist = False
            print("not exist")
        else:
            self.exist = True
            desc = self.describe()
            for field in desc:
                self.fields.append(field[1])
            print("exist")
        con.close()

    def open(self):
        con = sqlite3.connect(__DataBase__)
        return con

    def migrate(self,struct):
        con = self.open()
        q = "CREATE TABLE {} ( ".format(self.table_name)
        for field in struct:
            q = q + field['name']+" "+field['type']+" "
            for const in field['constrains']:
                q = q + const +" "
            q  = q + " , "
            self.fields.append(field['name'])
        q = q[:-2]
        q = q + " );"
        # print(q)
        res = con.execute(q)
        con.close()
        # print(res)

    def get_all(self):
        con = self.open()
        q = "select * from {};".format(self.table_name)
        cur = con.cursor()
        cur.execute(q)
        row = cur.fetchall()
        cur.close()
        serial_data = self.serialize(row)
        print(serial_data)
        con.close()
        return serial_data

    def insert(self,data):
        con = self.open()
        k=""
        v = ""
        values = []
        for key,val in data.items():
            k = k + key+" , "
            v = v+"?,"
            values.append(val)
        k = k[:-2]
        v = v[:-1]
        q = "insert into {}({}) VALUES({});".format(self.table_name,k,v)
        print(q)
        res = con.execute(q,values)
        con.commit()
        con.close()
        print(res)

    def describe(self):
        con  = self.open()
        q = "PRAGMA table_info([{}]);".format(self.table_name)
        print(q)
        res = con.execute(q)
        result = res.fetchall()
        con.close()
        return result
    
    def serialize(self,q_data):
        serial_data = []
        for row in q_data:
            r = {}
            for i in range(len(row)):
                r[self.fields[i]] = row[i]
            serial_data.append(r)
        return serial_data

    def filter(self,filters):
        con = self.open()
        q = "select * from {} where ".format(self.table_name)
        values = []
        for key,val in filters.items():
            q = q + key + " = ? and "
            values.append(val)
        q = q[:-4] + " ;"
        cur = con.cursor()
        print("query : ",q)
        try:
            cur.execute(q,values)
            res = cur.fetchall()
            con.close()
            return self.serialize(res)
        except:
            return False

    def update(self,id,data):
        con = self.open()
        q = "update {} set ".format(self.table_name)
        values = []
        for key,val in data.items():
            q = q + key + " = ? , "
            values.append(val)
        q = q[:-2] + " where id = ?;"
        values.append(id)
        print("query : ",q)
        try:
            res = con.execute(q,values)
            print("result : ",res)
            con.commit()
            con.close()
            return True
        except:
            return False

    def delete(self,id):
        con = self.open()
        q = "delete from {} where id = ? ".format(self.table_name)
        try:
            con.execute(q,[id])
            con.commit()
            con.close()
            return True
        except:
            return False
