import mysql.connector

class Database:
    def __init__(self, user=None, password=None, database=None, host="127.0.0.1", port="3306"):
        print(user)
        print(password)
        if user is None:
            print("Por favor, entre com usuario e senha!")
            exit(-1)
        if password is None:
            print("Por favor, entre com usuario e senha!")
            exit(-1)            
        self.conn = mysql.connector.connect(
            user=user,
            passwd=password,
            database=database,
            host=host,
            port=port
        )
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS BMF_values;")
        self.cursor.execute("USE BMF_values;")
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS all_data ("
            "  IDENTIFICADOR VARCHAR(64) NOT NULL,"
            "  DATA DATETIME NOT NULL,"
            "  DERIVATIVO VARCHAR(64) NOT NULL,"
            "  PARTICIPANTE VARCHAR(64) NOT NULL,"
            "  LONGCONTRACTS DECIMAL(10,4) NOT NULL,"
            "  LONG_ DECIMAL(5,2) NOT NULL,"
            "  SHORTCONTRACTS DECIMAL(10,4) NOT NULL,"
            "  SHORT_ DECIMAL(5,2) NOT NULL,"
            "  SALDO DECIMAL(10,4) NOT NULL,"
            "  PRIMARY KEY(IDENTIFICADOR)"    
            ");")

    def insert_into_all_data(self, all_data):
        add_all_data = (
            "INSERT IGNORE INTO all_data "
            "(IDENTIFICADOR, DATA, DERIVATIVO, PARTICIPANTE, LONGCONTRACTS, LONG%, SHORTCONTRACTS, SHORT%, SALDO) "
            "VALUES (%(id)s, %(date)s, %(derivative)s, %(participant)s, %(longcontracts)s, %(long)s, %(shortcontracts)s, %(short)s, %(balance)s)")
        self.cursor.execute(add_all_data, all_data)
        self.conn.commit()