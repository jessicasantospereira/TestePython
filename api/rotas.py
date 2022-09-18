from urllib import response
from flask import Flask, render_template, request, url_for, jsonify, redirect
from api.dao.despesasDAO import DespesasDAO
import json
import requests

despesas = DespesasDAO()

def home():
    data = despesas.consultar()
    dados = json.loads(data.data)
    if(dados['sucess'] == True):
        for item in dados['data']:
            if(item['categoria_id'] == 1):
                item['categoria_id'] = 'Custos fixos'
            elif(item['categoria_id'] == 2):
                item['categoria_id'] = 'Alimentação'
            elif(item['categoria_id'] == 3):
                item['categoria_id'] = 'Transporte'
            else:
                 item['categoria_id'] = 'Medicamentos'
            
            if(item['tipo_pagamento_id'] == 1):
                item['tipo_pagamento_id'] = 'Dinheiro'
            elif(item['tipo_pagamento_id'] == 2):
                item['tipo_pagamento_id'] = 'Débito'
            elif(item['tipo_pagamento_id'] == 3):
                item['tipo_pagamento_id'] = 'Crédito'
            else:
                item['tipo_pagamento_id'] = 'Pix'
            
    return render_template("home.html", data = dados['data'])

def cadastrar():
    if request.method=="POST":
        descricao = request.form['descricao']
        valor = request.form['valor']
        data_compra = request.form['data_compra']
        tipo_pagamento = request.form['tipo_pagamento']
        categoria = request.form['categoria']
        
        despesas.adicionar_despesas(descricao, valor, data_compra, tipo_pagamento, categoria)
        return redirect(url_for("api.home"))
    return render_template("cadastrar.html")

def editar(id):
    data = despesas.consultar_id(id)
    dados = json.loads(data.data)
    if request.method=="POST":
        id = id
        descricao = request.form['descricao']
        valor = request.form['valor']
        data_compra = request.form['data_compra']
        tipo_pagamento = request.form['tipo_pagamento']
        categoria = request.form['categoria']
        
        despesas.atualizar_despesas(id,descricao, valor, data_compra, tipo_pagamento, categoria)    
        return redirect(url_for("api.home"))
    
    return render_template("editar.html", data=dados['data'])

def deletar(id):
    data = despesas.deletar_despesa(id)
    dados = json.loads(data.data)

    return redirect(url_for("api.home"))
    