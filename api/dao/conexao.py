from flask import Flask, g
import sqlite3

DB_URL = "data/database.db"

class Conexao(object):
    def conectar(self):
        self.con = sqlite3.connect(DB_URL)
        print("Conectado com sucesso")
        return self.con

        
    def desconectar(self):
        if g.conn is not None:
            g.conn.close()
            print("Desconectado com sucesso")
        else:
            self.conn.close()
            print("Desconectado com sucesso")