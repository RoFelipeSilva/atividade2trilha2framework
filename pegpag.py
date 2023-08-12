from flask import Flask, make_response
from markupsafe import escape
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask import url_for
from flask import redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:9577@localhost:3306/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column('id_Usuario', db.Integer, primary_key=True)
    nome = db.Column('Us_Nome', db.String(100))
    email = db.Column('Us_Email', db.String(100))
    cpf = db.Column('Us_CPF', db.Integer)
    end = db.Column('Us_End', db.String(150))
    senha = db.Column('Us_Senha', db.String(10))

    def __init__(self, nome, email, cpf, end, senha):
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.end = end
        self.senha = senha

class Categoria(db.Model):
    __tablename__ = "categoria"
    id = db.Column('id_categoria', db.Integer, primary_key=True)
    descricao = db.Column('cat_descricao', db.String(45))
    
    def __init__ (self, descricao):
        self.descricao = descricao

class Anuncio(db.Model):
    __tablename__ = "anuncio"
    id = db.Column('id_anuncio', db.Integer, primary_key=True)
    titulo = db.Column('anu_titulo', db.String(35))
    descricao = db.Column('anu_descricao', db.String(250))
    valor = db.Column('anu_valor', db.Float)
    qtde = db.Column('anu_qtde', db.Integer)
    oferta = db.Column('anu_oferta', db.String(3))
    categoria_id = db.Column('id_categoria',db.Integer, db.ForeignKey("categoria.id_categoria"))
    usuario_id = db.Column('id_Usuario',db.Integer, db.ForeignKey("usuarios.id_Usuario"))

    def __init__(self, titulo, descricao, valor, qtde, oferta, categoria_id, usuario_id):
        self.titulo = titulo
        self.descricao = descricao
        self.valor = valor
        self.qtde = qtde
        self.oferta = oferta
        self.categoria_id = categoria_id
        self.usuario_id = usuario_id

class Favorito(db.Model):
    __tablename__ = "favorito"
    id = db.Column('id_favorito', db.Integer, primary_key=True)
    categoria_id = db.Column('id_anuncio',db.Integer, db.ForeignKey("categoria.id_anuncio"))
    usuario_id = db.Column('id_Usuario',db.Integer, db.ForeignKey("usuarios.id_Usuario"))

class Pergunta(db.Model):
    __tablename_= "pergunta"
    id = db.Column('id_pergunta', db.Integer, primary_key=True)
    per_pergunta = db.Column('Per_Pergunta', db.String(350))
    per_resposta = db.Column('Per_Resposta', db.String(350))
    categoria_id = db.Column('id_anuncio',db.Integer, db.ForeignKey("anuncio.id_anuncio"))
    usuario_id = db.Column('id_Usuario',db.Integer, db.ForeignKey("usuarios.id_Usuario"))

    def __init__(self, pergunta, resposta, id_anuncio, id_usuario):
        self.pergunta = pergunta
        self.resposta = resposta
        self.anuncio_id = id_anuncio
        self.usuario_id = id_usuario

class Compra(db.Model):
    __tablename__ = "compra"
    id = db.Column('id_compra', db.Integer, primary_key=True)
    qtde = db.Column('com_qtde', db.Integer)
    valor = db.Column('com_valor', db.Float)
    total = db.Column('com_total', db.Float)
    anuncio_id = db.Column('anuncio_id_anuncio',db.Integer, db.ForeignKey("anuncio.id_anuncio"))
    usuario_id = db.Column('id_Usuario',db.Integer, db.ForeignKey("usuarios.id_Usuario"))

    def __init__(self, qtde, valor, total, anuncio_id, usuario_id):
        self.qtde = qtde
        self.valor = valor
        self.total = total
        self.anuncio_id = anuncio_id
        self.usuario_id = usuario_id

@app.errorhandler(404)
def paginanaoencontrada(error):
    return render_template('pagnaoencontrada.html', titulo = "Página não encontrada")
        

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/usuario")
def usuario():
    return render_template('usuario.html', usuarios = Usuario.query.all(), 
    titulo="Cadastro de Usuario")

@app.route("/usuario/meuperfil")
def meuperfil():
    return render_template('meuperfil.html', título="Meu perfil ")

@app.route("/usuario/criar", methods=['POST'])
def criarusuario():
    usuario = Usuario(request.form.get('nome'), request.form.get('email'), 
    request.form.get('cpf'), request.form.get('end'), request.form.get('senha'))
    db.session.add(usuario)
    db.session.commit()
    return redirect(url_for('usuario'))

@app.route("/usuario/detalhar/<int:id>")
def buscarusuario(id):
    usuario = Usuario.query.get(id)
    return usuario.nome

@app.route("/usuario/editar/<int:id>", methods=['GET','POST'])
def editarusuario(id):
    usuario = Usuario.query.get(id)
    if request.method == 'POST':
        usuario.nome = request.form.get('nome')
        usuario.email = request.form.get('email')
        usuario.cpf = request.form.get('cpf')
        usuario.end = request.form.get('end')
        usuario.senha = request.form.get('senha')
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('usuario'))

    return render_template('perfil.html', usuario = usuario, titulo="Alterar")

@app.route("/usuario/deletar/<int:id>")
def deletarusuario(id):
    usuario = Usuario.query.get(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('usuario'))

@app.route("/cad/perfil")
def perfil():
    return render_template('perfil.html')

# - - - - - - A N Ú N C I O S - - - - - - 

@app.route("/anuncio")
def anuncio():
    return render_template('anuncio.html', anuncios = Anuncio.query.all(), 
    categorias = Categoria.query.all(), titulo="Anuncio")

@app.route("/anuncio/comprar")
def comprar():
    return render_template('comprar.html', anuncios = Anuncio.query.all(), 
    categorias = Categoria.query.all(), titulo="Anuncio")

@app.route("/anuncio/vender")
def vender():
    return render_template('vender.html', anuncios = Anuncio.query.all(), 
    categorias = Categoria.query.all(), titulo="Anuncio")

@app.route("/anuncio/cadanuncio", methods=['POST'])
def cadanuncio():
    anuncio = Anuncio(request.form.get('titulo'), request.form.get('descricao'),
    request.form.get('valor'),request.form.get('qtde'),request.form.get('oferta'),
    request.form.get('categoria_id'), request.form.get('usuario_id'))
    db.session.add(anuncio)
    db.session.commit()
    return redirect(url_for('anuncio'))

@app.route("/anuncio/detalhar/<int:id>")
def buscaranuncio(id):
    anuncio = Anuncio.query.get(id)
    return anuncio.titulo

@app.route("/anuncio/editar/<int:id>", methods=['GET','POST'])
def editaranuncio(id):
    anuncio = Anuncio.query.get(id)
    if request.method == 'POST':
        anuncio.titulo = request.form.get('titulo')
        anuncio.descricao = request.form.get('descricao')
        anuncio.valor = request.form.get('valor')
        anuncio.qtde = request.form.get('qtde')
        anuncio.oferta = request.form.get('oferta')
        anuncio.categoria = request.form.get('categoria_id')
        db.session.add(anuncio)
        db.session.commit()
        return redirect(url_for('anuncio'))

    return render_template('editanuncio.html', anuncio = anuncio, titulo="Alterar")

@app.route("/anuncio/deletar/<int:id>")
def deletaranuncio(id):
    anuncio = Anuncio.query.get(id)
    db.session.delete(anuncio)
    db.session.commit()
    return redirect(url_for('anuncio'))
    
# - - - - - - - - A N Ú N C I O S   P E R G U N T A S - - - - - - - - -

@app.route("/anuncio/perguntar")
def perguntar():
    return render_template('perguntar.html', titulo="perguntar", 
    perguntas = Pergunta.query.all())

@app.route("/anuncio/cadpergunta", methods=['POST'])
def cadpergunta(id):
    pergunta = Anuncio(request.form.get('pergunta'))
    db.session.add(pergunta)
    db.session.commit()
    return redirect(url_for('pergunta'))


#- - - - - - - - F A V O R I T O S - - - - - - - - -

@app.route("/anuncio/favoritos")
def favoritos():
    return render_template('favoritos.html')



@app.route("/ofertas")
def ofertas():
    return render_template("ofertas.html", titulo="Ofertas", anuncios = Anuncio.query.all(), 
    categorias = Categoria.query.all(),)


# - - - - - - - CATEGORIAS - - - - - - -  

@app.route("/config")
def config():
    return render_template('config.html', titulo="Configurações")

@app.route("/config/categorias")
def categorias():
    return render_template('categorias.html', categorias = Categoria.query.all(), 
    titulo='Categoria')

@app.route("/config/cadcategorias", methods=['POST'])
def cadcategorias():
    categoria = Categoria(request.form.get('descricao'))
    db.session.add(categoria)
    db.session.commit()
    return redirect(url_for('categorias'))

@app.route("/config/detalhar/<int:id>")
def buscarcategoria(id):
    categoria = Categoria.query.get(id)
    return categoria.descricao

@app.route("/config/editar/<int:id>", methods=['GET','POST'])
def editarcategoria(id):
    categoria = Categoria.query.get(id)
    if request.method == 'POST':
        categoria.descricao = request.form.get('descricao')
        db.session.add(categoria)
        db.session.commit()
        return redirect(url_for('categorias'))

    return render_template('editcategoria.html', categoria = categoria, titulo="Categorias")

@app.route("/config/deletar/<int:id>")
def deletarcategoria(id):
    categoria = Categoria.query.get(id)
    db.session.delete(categoria)
    db.session.commit()
    return redirect(url_for('categorias'))


# - - - - - - R E L A T Ó R I O S - - - - - - -

@app.route("/relatorios")
def relatorios():
    return render_template('relatorios.html')

@app.route("/relatorios/vendas")
def relVendas():
    return render_template('relvendas.html', titulo="Relatório de vendas")

@app.route("/relatorios/compras")
def relCompras():
    return render_template('relcompras.html', titulo="Relatório de compras")

@app.route("/cad/faleconosco")
def faleconosco():
    return render_template('faleconosco.html', titulo="Fale Conosco")

@app.route("/cad/cadmsg", methods=['POST'])
def cadmsg():
    return request.form

@app.route("/quemsomos")
def quemsomos():
    return render_template('quemsomos.html', titulo="Quem somos")

if __name__ == 'pegpag.py':
    db.create_all()