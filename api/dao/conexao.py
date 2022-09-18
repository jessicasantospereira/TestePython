from flask import Flask
import sqlite3

DB_URL = "data/database.db"

class Conexao(object):
    def conectar(self):
        self.conn = sqlite3.connect(DB_URL)
        return self.conn
