from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "pegpag-crud"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost:3306/mydb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column("id_Usuario", db.Integer, primary_key=True)
    nome = db.Column("Us_Nome", db.String(100), nullable=False)
    email = db.Column("Us_Email", db.String(100), nullable=False)
    cpf = db.Column("Us_CPF", db.String(20))
    end = db.Column("Us_End", db.String(150))
    senha = db.Column("Us_Senha", db.String(100), nullable=False)

class Categoria(db.Model):
    __tablename__ = "categoria"
    id = db.Column("id_categoria", db.Integer, primary_key=True)
    descricao = db.Column("cat_descricao", db.String(45), nullable=False)

class Anuncio(db.Model):
    __tablename__ = "anuncio"
    id = db.Column("id_anuncio", db.Integer, primary_key=True)
    titulo = db.Column("anu_titulo", db.String(35), nullable=False)
    descricao = db.Column("anu_descricao", db.String(250))
    valor = db.Column("anu_valor", db.Float, nullable=False)
    qtde = db.Column("anu_qtde", db.Integer, nullable=False)
    oferta = db.Column("anu_oferta", db.String(3))
    categoria_id = db.Column("id_categoria", db.Integer, db.ForeignKey("categoria.id_categoria"))
    usuario_id = db.Column("id_Usuario", db.Integer, db.ForeignKey("usuarios.id_Usuario"))

class Favorito(db.Model):
    __tablename__ = "favorito"
    id = db.Column("id_favorito", db.Integer, primary_key=True)
    anuncio_id = db.Column("id_anuncio", db.Integer, db.ForeignKey("anuncio.id_anuncio"), nullable=False)
    usuario_id = db.Column("id_Usuario", db.Integer, db.ForeignKey("usuarios.id_Usuario"), nullable=False)

class Pergunta(db.Model):
    __tablename__ = "pergunta"
    id = db.Column("id_pergunta", db.Integer, primary_key=True)
    pergunta = db.Column("Per_Pergunta", db.String(350), nullable=False)
    resposta = db.Column("Per_Resposta", db.String(350))
    anuncio_id = db.Column("id_anuncio", db.Integer, db.ForeignKey("anuncio.id_anuncio"))
    usuario_id = db.Column("id_Usuario", db.Integer, db.ForeignKey("usuarios.id_Usuario"))

class Compra(db.Model):
    __tablename__ = "compra"
    id = db.Column("id_compra", db.Integer, primary_key=True)
    qtde = db.Column("com_qtde", db.Integer, nullable=False)
    valor = db.Column("com_valor", db.Float, nullable=False)
    total = db.Column("com_total", db.Float, nullable=False)
    anuncio_id = db.Column("anuncio_id_anuncio", db.Integer, db.ForeignKey("anuncio.id_anuncio"))
    usuario_id = db.Column("id_Usuario", db.Integer, db.ForeignKey("usuarios.id_Usuario"))

@app.errorhandler(404)
def pagina_nao_encontrada(error):
    return render_template("pagnaoencontrada.html", titulo="Página não encontrada"), 404

@app.route("/")
def index():
    return render_template("index.html")

# USUARIOS
@app.route("/usuario")
def usuario():
    return render_template("usuario.html", usuarios=Usuario.query.order_by(Usuario.id.desc()).all(), titulo="Cadastro de Usuario")

@app.post("/usuario/criar")
def criarusuario():
    obj = Usuario(nome=request.form.get("nome"), email=request.form.get("email"), cpf=request.form.get("cpf"), end=request.form.get("end"), senha=request.form.get("senha"))
    db.session.add(obj); db.session.commit(); flash("Usuário cadastrado com sucesso.")
    return redirect(url_for("usuario"))

@app.route("/usuario/editar/<int:id>", methods=["GET","POST"])
def editarusuario(id):
    obj = Usuario.query.get_or_404(id)
    if request.method == "POST":
        obj.nome=request.form.get("nome"); obj.email=request.form.get("email"); obj.cpf=request.form.get("cpf"); obj.end=request.form.get("end"); obj.senha=request.form.get("senha")
        db.session.commit(); flash("Usuário alterado com sucesso."); return redirect(url_for("usuario"))
    return render_template("perfil.html", usuario=obj, titulo="Alterar usuário")

@app.post("/usuario/deletar/<int:id>")
def deletarusuario(id):
    db.session.delete(Usuario.query.get_or_404(id)); db.session.commit(); flash("Usuário excluído com sucesso.")
    return redirect(url_for("usuario"))

@app.route("/usuario/detalhar/<int:id>")
def buscarusuario(id):
    obj=Usuario.query.get_or_404(id)
    return render_template("crud_detalhe.html", titulo="Detalhar usuário", entidade="Usuário", campos=[("ID",obj.id),("Nome",obj.nome),("E-mail",obj.email),("CPF",obj.cpf),("Endereço",obj.end)])

# CATEGORIAS
@app.route("/config")
def config(): return render_template("config.html", titulo="Configurações")

@app.route("/config/categorias")
def categorias(): return render_template("categorias.html", categorias=Categoria.query.order_by(Categoria.id.desc()).all(), titulo="Categorias")

@app.post("/config/cadcategorias")
def cadcategorias():
    db.session.add(Categoria(request.form.get("descricao"))); db.session.commit(); flash("Categoria cadastrada com sucesso.")
    return redirect(url_for("categorias"))

@app.route("/config/editar/<int:id>", methods=["GET","POST"])
def editarcategoria(id):
    obj=Categoria.query.get_or_404(id)
    if request.method=="POST": obj.descricao=request.form.get("descricao"); db.session.commit(); flash("Categoria alterada com sucesso."); return redirect(url_for("categorias"))
    return render_template("editcategoria.html", categoria=obj, titulo="Alterar categoria")

@app.post("/config/deletar/<int:id>")
def deletarcategoria(id):
    db.session.delete(Categoria.query.get_or_404(id)); db.session.commit(); flash("Categoria excluída com sucesso."); return redirect(url_for("categorias"))

@app.route("/config/detalhar/<int:id>")
def buscarcategoria(id):
    obj=Categoria.query.get_or_404(id); return render_template("crud_detalhe.html", titulo="Detalhar categoria", entidade="Categoria", campos=[("ID",obj.id),("Descrição",obj.descricao)])

# ANUNCIOS
@app.route("/anuncio")
def anuncio(): return render_template("anuncio.html", anuncios=Anuncio.query.order_by(Anuncio.id.desc()).all(), categorias=Categoria.query.all(), titulo="Anúncios")

@app.post("/anuncio/cadanuncio")
def cadanuncio():
    obj=Anuncio(titulo=request.form.get("titulo"), descricao=request.form.get("descricao"), valor=float(request.form.get("valor") or 0), qtde=int(request.form.get("qtde") or 0), oferta=request.form.get("oferta"), categoria_id=request.form.get("categoria_id"), usuario_id=request.form.get("usuario_id")); db.session.add(obj); db.session.commit(); flash("Anúncio cadastrado com sucesso."); return redirect(url_for("anuncio"))

@app.route("/anuncio/editar/<int:id>", methods=["GET","POST"])
def editaranuncio(id):
    obj=Anuncio.query.get_or_404(id)
    if request.method=="POST":
        obj.titulo=request.form.get("titulo"); obj.descricao=request.form.get("descricao"); obj.valor=float(request.form.get("valor") or 0); obj.qtde=int(request.form.get("qtde") or 0); obj.oferta=request.form.get("oferta"); obj.categoria_id=request.form.get("categoria_id"); obj.usuario_id=request.form.get("usuario_id"); db.session.commit(); flash("Anúncio alterado com sucesso."); return redirect(url_for("anuncio"))
    return render_template("editanuncio.html", anuncio=obj, categorias=Categoria.query.all(), titulo="Alterar anúncio")

@app.post("/anuncio/deletar/<int:id>")
def deletaranuncio(id): db.session.delete(Anuncio.query.get_or_404(id)); db.session.commit(); flash("Anúncio excluído com sucesso."); return redirect(url_for("anuncio"))

@app.route("/anuncio/detalhar/<int:id>")
def buscaranuncio(id):
    obj=Anuncio.query.get_or_404(id); return render_template("crud_detalhe.html", titulo="Detalhar anúncio", entidade="Anúncio", campos=[("ID",obj.id),("Título",obj.titulo),("Descrição",obj.descricao),("Valor",obj.valor),("Quantidade",obj.qtde),("Oferta",obj.oferta),("ID categoria",obj.categoria_id),("ID usuário",obj.usuario_id)])

@app.route("/anuncio/comprar")
def comprar(): return render_template("comprar.html", anuncios=Anuncio.query.all(), categorias=Categoria.query.all(), titulo="Comprar")
@app.route("/anuncio/vender")
def vender(): return render_template("vender.html", anuncios=Anuncio.query.all(), categorias=Categoria.query.all(), titulo="Vender")

# PERGUNTAS
@app.route("/anuncio/perguntar")
def perguntas(): return render_template("perguntar.html", perguntas=Pergunta.query.order_by(Pergunta.id.desc()).all(), anuncios=Anuncio.query.all(), usuarios=Usuario.query.all(), titulo="Perguntas")
@app.post("/anuncio/cadpergunta")
def cadpergunta():
    obj=Pergunta(pergunta=request.form.get("pergunta"), resposta=request.form.get("resposta"), anuncio_id=request.form.get("anuncio_id"), usuario_id=request.form.get("usuario_id")); db.session.add(obj); db.session.commit(); flash("Pergunta cadastrada com sucesso."); return redirect(url_for("perguntas"))
@app.route("/anuncio/pergunta/editar/<int:id>", methods=["GET","POST"])
def editarpergunta(id):
    obj=Pergunta.query.get_or_404(id)
    if request.method=="POST": obj.pergunta=request.form.get("pergunta"); obj.resposta=request.form.get("resposta"); obj.anuncio_id=request.form.get("anuncio_id"); obj.usuario_id=request.form.get("usuario_id"); db.session.commit(); flash("Pergunta alterada com sucesso."); return redirect(url_for("perguntas"))
    return render_template("pergunta_form.html", pergunta=obj, anuncios=Anuncio.query.all(), usuarios=Usuario.query.all(), titulo="Alterar pergunta")
@app.post("/anuncio/pergunta/deletar/<int:id>")
def deletarpergunta(id): db.session.delete(Pergunta.query.get_or_404(id)); db.session.commit(); flash("Pergunta excluída com sucesso."); return redirect(url_for("perguntas"))

# FAVORITOS
@app.route("/anuncio/favoritos")
def favoritos(): return render_template("favoritos.html", favoritos=Favorito.query.order_by(Favorito.id.desc()).all(), anuncios=Anuncio.query.all(), usuarios=Usuario.query.all(), titulo="Favoritos")
@app.post("/anuncio/favoritos/criar")
def criarfavorito():
    db.session.add(Favorito(anuncio_id=request.form.get("anuncio_id"), usuario_id=request.form.get("usuario_id"))); db.session.commit(); flash("Favorito cadastrado com sucesso."); return redirect(url_for("favoritos"))
@app.route("/anuncio/favoritos/editar/<int:id>", methods=["GET","POST"])
def editarfavorito(id):
    obj=Favorito.query.get_or_404(id)
    if request.method=="POST": obj.anuncio_id=request.form.get("anuncio_id"); obj.usuario_id=request.form.get("usuario_id"); db.session.commit(); flash("Favorito alterado com sucesso."); return redirect(url_for("favoritos"))
    return render_template("favorito_form.html", favorito=obj, anuncios=Anuncio.query.all(), usuarios=Usuario.query.all(), titulo="Alterar favorito")
@app.post("/anuncio/favoritos/deletar/<int:id>")
def deletarfavorito(id): db.session.delete(Favorito.query.get_or_404(id)); db.session.commit(); flash("Favorito excluído com sucesso."); return redirect(url_for("favoritos"))

# COMPRAS
@app.route("/compras")
def compras(): return render_template("compras.html", compras=Compra.query.order_by(Compra.id.desc()).all(), anuncios=Anuncio.query.all(), usuarios=Usuario.query.all(), titulo="Compras")
@app.post("/compras/criar")
def criarcompra():
    qtde=int(request.form.get("qtde") or 0); valor=float(request.form.get("valor") or 0); total=float(request.form.get("total") or qtde*valor); db.session.add(Compra(qtde,valor,total,request.form.get("anuncio_id"),request.form.get("usuario_id"))); db.session.commit(); flash("Compra cadastrada com sucesso."); return redirect(url_for("compras"))
@app.route("/compras/editar/<int:id>", methods=["GET","POST"])
def editarcompra(id):
    obj=Compra.query.get_or_404(id)
    if request.method=="POST": obj.qtde=int(request.form.get("qtde") or 0); obj.valor=float(request.form.get("valor") or 0); obj.total=float(request.form.get("total") or obj.qtde*obj.valor); obj.anuncio_id=request.form.get("anuncio_id"); obj.usuario_id=request.form.get("usuario_id"); db.session.commit(); flash("Compra alterada com sucesso."); return redirect(url_for("compras"))
    return render_template("compra_form.html", compra=obj, anuncios=Anuncio.query.all(), usuarios=Usuario.query.all(), titulo="Alterar compra")
@app.post("/compras/deletar/<int:id>")
def deletarcompra(id): db.session.delete(Compra.query.get_or_404(id)); db.session.commit(); flash("Compra excluída com sucesso."); return redirect(url_for("compras"))

# OUTRAS PAGINAS
@app.route("/ofertas")
def ofertas(): return render_template("ofertas.html", titulo="Ofertas", anuncios=Anuncio.query.all(), categorias=Categoria.query.all())
@app.route("/relatorios")
def relatorios(): return render_template("relatorios.html")
@app.route("/relatorios/vendas")
def relVendas(): return render_template("relvendas.html", titulo="Relatório de vendas")
@app.route("/relatorios/compras")
def relCompras(): return render_template("relcompras.html", titulo="Relatório de compras")
@app.route("/cad/faleconosco")
def faleconosco(): return render_template("faleconosco.html", titulo="Fale Conosco")
@app.post("/cad/cadmsg")
def cadmsg(): return request.form
@app.route("/quemsomos")
def quemsomos(): return render_template("quemsomos.html", titulo="Quem somos")

if __name__ == "__main__":
    with app.app_context(): db.create_all()
    app.run(debug=True)
