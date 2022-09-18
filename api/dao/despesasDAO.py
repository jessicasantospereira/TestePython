from flask import Flask, g, jsonify
from api.dao.conexao import Conexao
import sqlite3
import json
from datetime import datetime 
from calendar import monthrange


class DespesasDAO(object):
    def adicionar_despesas(self, descricao, valor, data_compra, tipo_pagamento, categoria):
        conn = Conexao()
        con = conn.conectar()
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        query = """ INSERT INTO despesas(valor, data_compra, descricao, tipo_pagamento_id, categoria_id) VALUES (?,?,?,?,?)"""
        resposta = cursor.execute(query, (valor, data_compra,descricao, tipo_pagamento, categoria))
        con.commit()
        if(resposta != ''):
            ultimo= """SELECT * FROM despesas ORDER BY id DESC LIMIT 1"""
            cursor.execute(ultimo)
            resultado = [{'id': row[0], 'valor':row[1], 'data_compra':row[2], 'descricao':row[3], 'tipo_pagamento_id': row[4], 'categoria_id':row[5]}
                            for row in cursor.fetchall()]
            con.close()
            return jsonify({"data": resultado, "sucess": True})
        else:
            return jsonify({"data": 'Nenhum resultado encontrado', "sucess": False})
        

    def atualizar_despesas(self, id, descricao, valor, data_compra, tipo_pagamento, categoria):
        conn = Conexao()
        con = conn.conectar()
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        query = """ UPDATE despesas SET valor=?, data_compra=?, descricao=?, tipo_pagamento_id=?, categoria_id=? WHERE id=?"""
        resposta = cursor.execute(query, (valor, data_compra,descricao, tipo_pagamento, categoria, id))
        con.commit()
        if(resposta != ''):
            ultimo= """SELECT * FROM despesas WHERE id={}""".format(id)
            cursor.execute(ultimo)
            resultado = [{'id': row[0], 'valor':row[1], 'data_compra':row[2], 'descricao':row[3], 'tipo_pagamento_id': row[4], 'categoria_id':row[5]}
                            for row in cursor.fetchall()]
            print(resultado)
            return jsonify({"data": resultado, "sucess": True})
        else:
            return jsonify({"data": 'Nenhum valor atualizado', "sucess": False})

    def consultar(self):
        self.data = datetime.now()
        self.mes = self.data.month
        self.ano = self.data.year
        if(self.mes >= 10):
            self.dia_1 = str(self.ano) + '-' + str(self.mes) + '-01'
            self.ultimo_dia = str(self.ano) + '-' + str(self.mes) + '-'+ str(monthrange(self.ano, self.mes)[1])
        else:
            self.dia_1 = str(self.ano) + '-0' + str(self.mes) + '-01'
            self.ultimo_dia = str(self.ano) + '-0' + str(self.mes) + '-'+ str(monthrange(self.ano, self.mes)[1])

        try:
            conn = Conexao()
            con = conn.conectar()
            con.row_factory = sqlite3.Row
            cursor = con.cursor()
            query = "SELECT * FROM despesas WHERE data_compra BETWEEN '"+self.dia_1+"' AND '"+self.ultimo_dia+"'"
            cursor.execute(query)
            resultado = [{'id': row[0], 'valor':row[1], 'data_compra':row[2], 'descricao':row[3], 'tipo_pagamento_id': row[4], 'categoria_id':row[5]}
                         for row in cursor.fetchall()]
            con.close()
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
            con.close()
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
            g.conn.close()
            return jsonify({"data": "Despesa apagada", "sucess": True})
        except:
            return jsonify({"data": "Id não encontrado", "sucess": False})
