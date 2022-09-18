from flask import Flask, g, jsonify
from api.dao.conexao import Conexao
import sqlite3
import json


class DespesasDAO(object):
    def adicionar_despesas(self, descricao, valor, data_compra, tipo_pagamento, categoria):
        conn = Conexao()
        g.conn = conn.conectar()
        query = """ INSERT INTO despesas(valor, data_compra, descricao, tipo_pagamento_id, categoria_id) VALUES (?,?,?,?,?)"""
        g.conn.execute(query, (valor, data_compra,
                       descricao, tipo_pagamento, categoria))
        g.conn.commit()

    def atualizar_despesas(self, id, descricao, valor, data_compra, tipo_pagamento, categoria):
        conn = Conexao()
        g.conn = conn.conectar()
        query = """ UPDATE despesas SET valor=?, data_compra=?, descricao=?, tipo_pagamento_id=?, categoria_id=? WHERE id=?"""
        g.conn.execute(query, (valor, data_compra,
                       descricao, tipo_pagamento, categoria, id))
        g.conn.commit()

    def consultar(self):
        try:
            conn = Conexao()
            con = conn.conectar()
            con.row_factory = sqlite3.Row
            cursor = con.cursor()
            query = """ SELECT * FROM despesas"""
            cursor.execute(query)
            resultado = [{'id': row[0], 'valor':row[1], 'data_compra':row[2], 'descricao':row[3], 'tipo_pagamento_id': row[4], 'categoria_id':row[5]}
                         for row in cursor.fetchall()]

            # return jsonify(resultado)
            return jsonify({"data": resultado, "sucess": True})
        except:
            return jsonify({"data": "null", "sucess": False})

    def consultar_id(self, id):
        try:
            conn = Conexao()
            con = conn.conectar()
            con.row_factory = sqlite3.Row
            cursor = con.cursor()
            query = """ SELECT * FROM despesas WHERE id = {}""".format(id)
            cursor.execute(query)
            resultado = [{'id': row[0], 'valor':row[1], 'data_compra':row[2], 'descricao':row[3], 'tipo_pagamento_id': row[4], 'categoria_id':row[5]}
                         for row in cursor.fetchall()]
            return jsonify({"data": resultado, "sucess": True})
        except:
            return jsonify({"data": "null", "sucess": False})

    def deletar_despesa(self, id):
        try:
            conn = Conexao()
            g.conn = conn.conectar()
           
            query = """DELETE FROM despesas WHERE id={}""".format(id)
            
            g.conn.execute(query)
            g.conn.commit()
            return jsonify({"data": "Despesa apagada", "sucess": True})
        except:
            return jsonify({"data": "Id não encontrado", "sucess": False})
