from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

produto = []

@app.route("/")
def index():
    return render_template("index.html", produto=produto)

@app.route('/', methods=['POST'])
def codigo_ean():
    try:
        df = pd.read_excel('EstoqueMatriz.xlsx')
        codigo = request.form.get('codigo')
        
        cod = codigo
        sp = int(cod[1:7])
        su = cod [7:13]
        dt = df.loc[df['Código'] == sp]

        if not dt.empty:
            line = dt.index[0]

            '''calculo atraves do preço de venda'''
            pa = float(df.at[line, "estoque atual"])
            pv = float(df.at[line,"Preço Unitário de Venda"])
            su2 = float(su)

            ppp = su2 / pv
            pet = float(ppp / 1000)
            peso_redondo = round(pet, 3)
            np = pa + peso_redondo        

            df.at[line, "estoque atual"] = np
            descricao = df.at[line, "Descrição"]
            estoque = df.at[line, "estoque atual"]

            '''Salvando o novo valor de estoque valor'''
            df.to_excel('EstoqueMatriz.xlsx', index = False)

            produto.append({"descricao": descricao, "peso":estoque})
            return render_template("index.html", produto=produto)
        else:
            print('Produto Não Encontrado')
            return render_template("index.html",produto=produto)
    except:
        return format('<h1>Erro</h1>')
    
    
@app.route('/manual', methods=['POST'])
def manual():
    try:
        df = pd.read_excel('EstoqueMatriz.xlsx')

        codigo = request.form.get('codigo')
        peso = request.form.get('peso')

        cod = int(codigo)
        pes = float(peso)    
        dt = df.loc[df['Código'] == cod]

        if not dt.empty:
            line = dt.index[0]
            print('\n\n', df.at[line, "estoque atual"])

            # Atualizando o estoque atual com o novo peso
            floa = float(df.at[line, "estoque atual"])
            pess = floa + pes
            df.at[line, "estoque atual"] = pess
            descricao = df.at[line, "Descrição"]
            estoque = df.at[line, "estoque atual"]

        # Salvando o novo valor de estoque valor
            df.to_excel('EstoqueMatriz.xlsx', index = False)
            descricao = df.at[line, "Descrição"]
            estoque = df.at[line, "estoque atual"]

            produto.append({"descricao": descricao, "peso":estoque})
            return render_template("index.html", produto=produto)
        else:
            print('Produto Não Encontrado')
            return render_template("index.html", produto=produto)
    except:
        return format('<h1>Erro</h1>')

@app.route('/correcao', methods=['POST'])
def correcao():
    try:
        df = pd.read_excel('EstoqueMatriz.xlsx')

        codigo = request.form.get('codigo')
        peso = request.form.get('peso')

        cod = int(codigo)
        pes = float(peso)    
        dt = df.loc[df['Código'] == cod]

        if not dt.empty:
            line = dt.index[0]
            print('\n\n', df.at[line, "estoque atual"])

            # Atualizando o estoque atual com o novo peso
            floa = float(df.at[line, "estoque atual"])
            pess = floa - pes
            df.at[line, "estoque atual"] = pess
            descricao = df.at[line, "Descrição"]
            estoque = df.at[line, "estoque atual"]

        # Salvando o novo valor de estoque valor
            df.to_excel('EstoqueMatriz.xlsx', index = False)
            descricao = df.at[line, "Descrição"]
            estoque = df.at[line, "estoque atual"]

            produto.append({"descricao": descricao, "peso":estoque})
            return render_template("index.html", produto=produto)
        else:
            print('Produto Não Encontrado')
            return render_template("index.html", produto=produto)
    except:
        return format('<h1>Erro</h1>')
    
@app.route('/zerar', methods=['POST'])
def zerar():
    try:
        global produto
        produto = []  # Zera a lista de histórico
        return render_template("index.html", produto=produto)
    except:
        return format('<h1>Erro</h1>')

@app.route('/zerar_planilha', methods=['POST'])
def zerar_planilha():
    try:
        df = pd.read_excel('EstoqueMatriz.xlsx')
   
        dt = df.loc[df["estoque atual"] > 0]

        if not dt.empty:
            print(dt["estoque atual"])
            df.loc[df["estoque atual"] > 0, "estoque atual"] = 0
            
            # Salvando o novo valor de estoque valor   
            df.to_excel('EstoqueMatriz.xlsx', index = False)

            return render_template("index.html")
        else:
            print('Produto Não Encontrado')
            return render_template("index.html", produto=produto)
    except:
        return format('<h1>Erro</h1>')

if __name__ == "__main__":
    app.run(debug=True)