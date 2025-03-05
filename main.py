from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Classes
class Transportadora:
    def __init__(self, nome, emissao_co2):
        self.nome = nome
        self.emissao_co2 = emissao_co2  # Escala de 1 a 5

class Produtor:
    def __init__(self, nome, poluicao_producao):
        self.nome = nome
        self.poluicao_producao = poluicao_producao  # Escala de 1 a 5

class Produto:
    def __init__(self, nome, produtor, transportadora):
        self.nome = nome
        self.produtor = produtor
        self.transportadora = transportadora
        self.custo_poluicao = produtor.poluicao_producao + transportadora.emissao_co2  # Escala de 2 a 10

class Consumidor:
    def __init__(self, nome):
        self.nome = nome
        self.produtos_selecionados = []
    
    def calcular_poluicao_total(self):
        return sum(produto.custo_poluicao for produto in self.produtos_selecionados)

# Dados fictícios
transportadoras = [
    Transportadora("EcoTrans", 2),
    Transportadora("FastDelivery", 4)
]

produtores = [
    Produtor("Fazenda Verde", 2),
    Produtor("AgroVida", 3),
    Produtor("EcoFrutas", 4)
]

produtos = [
    Produto("Maçã", produtores[0], transportadoras[0]),
    Produto("Maçã", produtores[1], transportadoras[1]),
    Produto("Maçã", produtores[2], transportadoras[0]),
    Produto("Laranja", produtores[0], transportadoras[1]),
    Produto("Laranja", produtores[1], transportadoras[0]),
    Produto("Laranja", produtores[2], transportadoras[1]),
    Produto("Banana", produtores[0], transportadoras[0]),
    Produto("Banana", produtores[1], transportadoras[1]),
    Produto("Banana", produtores[2], transportadoras[0]),
]

consumidor = None

# Rotas
@app.route('/', methods=['GET', 'POST'])
def login():
    global consumidor
    if request.method == 'POST':
        nome = request.form['nome']
        consumidor = Consumidor(nome)
        return redirect(url_for('escolher_produtos'))
    return render_template('login.html')

@app.route('/escolher_produtos', methods=['GET', 'POST'])
def escolher_produtos():
    if request.method == 'POST':
        selecionados = request.form.getlist('produtos')
        for nome_produto in selecionados:
            produto = next((p for p in produtos if p.nome == nome_produto), None)
            if produto:
                consumidor.produtos_selecionados.append(produto)
        return redirect(url_for('resumo_compra'))
    return render_template('escolher_produtos.html', produtos=produtos)

@app.route('/resumo_compra')
def resumo_compra():
    total_poluicao = consumidor.calcular_poluicao_total()
    return render_template('resumo_compra.html', consumidor=consumidor, total_poluicao=total_poluicao)

if __name__ == '__main__':
    app.run(debug=True)
