from application import mysql, session
from JinxChain import JinxChain,Block

class Table():
    def __init__(self, table_name, *args):
        self.table = table_name
        self.columns = "(%s)" % ",".join(args)
        self.columnsList = args

        if check_newtable(table_name):
            create_data = ""
            for column in self.columnsList:
                create_data += "%s varchar(100)," % column

            cur = mysql.connection.cursor()
            cur.execute("CREATE TABLE %s(%s)" %
                        (self.table, create_data[:len(create_data)-1]))
            cur.close()

    def get_all(self):
        cursor = mysql.connection.cursor()
        result = cursor.execute("SELECT * FROM %s" % self.table)
        data = cursor.fetchall()
        return data

    def get_one(self, search, value):
        data = {}
        cursor = mysql.connection.cursor()
        result = cursor.execute("SELECT * FROM %s WHERE %s = \"%s\"" %
                                (self.table, search, value))
        if result > 0:
            data = cursor.fetchone()
        cursor.close()
        return data

    def delete_one(self, search, value):
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE from %s where %s = \"%s\"" %
                       (self.table, search, value))
        mysql.connection.commit()
        cursor.close()

    def delete_all(self):
        self.drop()
        self.__init__(self.table, *self.columnsList)

    def drop(self):
        cur = mysql.connection.cursor()
        cur.execute("DROP TABLE %s" % self.table)
        cur.close()

    def insert(self, *args):
        data = ""
        for arg in args:
            data += "\"%s\"," % (arg)

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO %s%s VALUES(%s)" %
                       (self.table, self.columns, data[:len(data)-1]))
        mysql.connection.commit()
        cursor.close()


def check_newtable(table_name):
    cursor = mysql.connection.cursor()
    try:
        result = cursor.execute("SELECT * from %s" % table_name)
        cursor.close()
    except:
        return True
    return False

def isnewuser(username):

    users = Table("users", "name", "email", "username", "password")
    data = users.get_all()
    usernames = [user.get('username') for user in data]

    return False if username in usernames else True


def get_jinxchain():
    blockchain = JinxChain()
    blockchain_sql = Table("blockchain","number","hash","previous","tran","nonce")
    for b in blockchain_sql.get_all():
        blockchain.add_block(Block(int(b.get('number')),b.get('previous'), b.get('tran'),int(b.get('nonce'))))
    
    return blockchain

def sync_jinxchain(blockchain):
    blockchain_sql = Table("blockchain", "number", "hash", "previous", "tran", "nonce")
    blockchain_sql.delete_all()

    for block in blockchain.chain:
        blockchain_sql.insert(str(block.number), block.hash(), block.previous_hash, block.tran, block.nonce)


    