from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder=".")
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
def pagina_nao_encontrada(error): return render_template("paginanaoencontrada.html", titulo="Página não encontrada"), 404
@app.route("/")
def index(): return render_template("index.html")

@app.route("/usuario")
def usuario(): return render_template("usuario.html", usuarios=Usuario.query.order_by(Usuario.id.desc()).all(), titulo="Cadastro de Usuario")
@app.post("/usuario/criar")
def criarusuario():
    db.session.add(Usuario(request.form.get("nome"),request.form.get("email"),request.form.get("cpf"),request.form.get("end") or request.form.get("endereco"),request.form.get("senha"))); db.session.commit(); flash("Usuário cadastrado com sucesso."); return redirect(url_for("usuario"))
@app.route("/usuario/editar/<int:id>",methods=["GET","POST"])
def editarusuario(id):
    obj=Usuario.query.get_or_404(id)
    if request.method=="POST": obj.nome=request.form.get("nome"); obj.email=request.form.get("email"); obj.cpf=request.form.get("cpf"); obj.end=request.form.get("end") or request.form.get("endereco"); obj.senha=request.form.get("senha"); db.session.commit(); flash("Usuário alterado com sucesso."); return redirect(url_for("usuario"))
    return render_template("perfil.html",usuario=obj,titulo="Alterar usuário")
@app.post("/usuario/deletar/<int:id>")
def deletarusuario(id): db.session.delete(Usuario.query.get_or_404(id)); db.session.commit(); flash("Usuário excluído com sucesso."); return redirect(url_for("usuario"))
@app.route("/usuario/detalhar/<int:id>")
def buscarusuario(id):
    o=Usuario.query.get_or_404(id); return render_template("crud_detalhe.html",titulo="Detalhar usuário",entidade="Usuário",campos=[("ID",o.id),("Nome",o.nome),("E-mail",o.email),("CPF",o.cpf),("Endereço",o.end)])

@app.route("/config")
def config(): return render_template("config.html",titulo="Configurações")
@app.route("/config/categorias")
def categorias(): return render_template("categorias.html",categorias=Categoria.query.order_by(Categoria.id.desc()).all(),titulo="Categorias")
@app.post("/config/cadcategorias")
def cadcategorias(): db.session.add(Categoria(request.form.get("descricao"))); db.session.commit(); flash("Categoria cadastrada com sucesso."); return redirect(url_for("categorias"))
@app.route("/config/editar/<int:id>",methods=["GET","POST"])
def editarcategoria(id):
    o=Categoria.query.get_or_404(id)
    if request.method=="POST": o.descricao=request.form.get("descricao"); db.session.commit(); flash("Categoria alterada com sucesso."); return redirect(url_for("categorias"))
    return render_template("editcategoria.html",categoria=o,titulo="Alterar categoria")
@app.post("/config/deletar/<int:id>")
def deletarcategoria(id): db.session.delete(Categoria.query.get_or_404(id)); db.session.commit(); flash("Categoria excluída com sucesso."); return redirect(url_for("categorias"))
@app.route("/config/detalhar/<int:id>")
def buscarcategoria(id):
    o=Categoria.query.get_or_404(id); return render_template("crud_detalhe.html",titulo="Detalhar categoria",entidade="Categoria",campos=[("ID",o.id),("Descrição",o.descricao)])

@app.route("/anuncio")
def anuncio(): return render_template("anuncio.html",anuncios=Anuncio.query.order_by(Anuncio.id.desc()).all(),categorias=Categoria.query.all(),titulo="Anúncios")
@app.post("/anuncio/cadanuncio")
def cadanuncio():
    o=Anuncio(request.form.get("titulo"),request.form.get("descricao"),float(request.form.get("valor") or 0),int(request.form.get("qtde") or 0),request.form.get("oferta"),request.form.get("categoria_id"),request.form.get("usuario_id")); db.session.add(o); db.session.commit(); flash("Anúncio cadastrado com sucesso."); return redirect(url_for("anuncio"))
@app.route("/anuncio/editar/<int:id>",methods=["GET","POST"])
def editaranuncio(id):
    o=Anuncio.query.get_or_404(id)
    if request.method=="POST": o.titulo=request.form.get("titulo"); o.descricao=request.form.get("descricao"); o.valor=float(request.form.get("valor") or 0); o.qtde=int(request.form.get("qtde") or 0); o.oferta=request.form.get("oferta"); o.categoria_id=request.form.get("categoria_id"); o.usuario_id=request.form.get("usuario_id"); db.session.commit(); flash("Anúncio alterado com sucesso."); return redirect(url_for("anuncio"))
    return render_template("editanuncio.html",anuncio=o,categorias=Categoria.query.all(),titulo="Alterar anúncio")
@app.post("/anuncio/deletar/<int:id>")
def deletaranuncio(id): db.session.delete(Anuncio.query.get_or_404(id)); db.session.commit(); flash("Anúncio excluído com sucesso."); return redirect(url_for("anuncio"))
@app.route("/anuncio/detalhar/<int:id>")
def buscaranuncio(id):
    o=Anuncio.query.get_or_404(id); return render_template("crud_detalhe.html",titulo="Detalhar anúncio",entidade="Anúncio",campos=[("ID",o.id),("Título",o.titulo),("Descrição",o.descricao),("Valor",o.valor),("Quantidade",o.qtde),("Oferta",o.oferta)])
@app.route("/anuncio/comprar")
def comprar(): return render_template("comprar.html",anuncios=Anuncio.query.all(),categorias=Categoria.query.all(),titulo="Comprar")
@app.route("/anuncio/vender")
def vender(): return render_template("vender.html",anuncios=Anuncio.query.all(),categorias=Categoria.query.all(),titulo="Vender")

@app.route("/anuncio/perguntar")
def perguntas(): return render_template("perguntar.html",perguntas=Pergunta.query.order_by(Pergunta.id.desc()).all(),anuncios=Anuncio.query.all(),usuarios=Usuario.query.all(),titulo="Perguntas")
@app.post("/anuncio/cadpergunta")
def cadpergunta(): db.session.add(Pergunta(request.form.get("pergunta"),request.form.get("resposta"),request.form.get("anuncio_id"),request.form.get("usuario_id"))); db.session.commit(); flash("Pergunta cadastrada com sucesso."); return redirect(url_for("perguntas"))
@app.route("/anuncio/pergunta/editar/<int:id>",methods=["GET","POST"])
def editarpergunta(id):
    o=Pergunta.query.get_or_404(id)
    if request.method=="POST": o.pergunta=request.form.get("pergunta"); o.resposta=request.form.get("resposta"); o.anuncio_id=request.form.get("anuncio_id"); o.usuario_id=request.form.get("usuario_id"); db.session.commit(); flash("Pergunta alterada com sucesso."); return redirect(url_for("perguntas"))
    return render_template("pergunta_form.html",pergunta=o,anuncios=Anuncio.query.all(),usuarios=Usuario.query.all(),titulo="Alterar pergunta")
@app.post("/anuncio/pergunta/deletar/<int:id>")
def deletarpergunta(id): db.session.delete(Pergunta.query.get_or_404(id)); db.session.commit(); flash("Pergunta excluída com sucesso."); return redirect(url_for("perguntas"))

@app.route("/anuncio/favoritos")
def favoritos(): return render_template("favoritos.html",favoritos=Favorito.query.order_by(Favorito.id.desc()).all(),anuncios=Anuncio.query.all(),usuarios=Usuario.query.all(),titulo="Favoritos")
@app.post("/anuncio/favoritos/criar")
def criarfavorito(): db.session.add(Favorito(request.form.get("anuncio_id"),request.form.get("usuario_id"))); db.session.commit(); flash("Favorito cadastrado com sucesso."); return redirect(url_for("favoritos"))
@app.route("/anuncio/favoritos/editar/<int:id>",methods=["GET","POST"])
def editarfavorito(id):
    o=Favorito.query.get_or_404(id)
    if request.method=="POST": o.anuncio_id=request.form.get("anuncio_id"); o.usuario_id=request.form.get("usuario_id"); db.session.commit(); flash("Favorito alterado com sucesso."); return redirect(url_for("favoritos"))
    return render_template("favorito_form.html",favorito=o,titulo="Alterar favorito")
@app.post("/anuncio/favoritos/deletar/<int:id>")
def deletarfavorito(id): db.session.delete(Favorito.query.get_or_404(id)); db.session.commit(); flash("Favorito excluído com sucesso."); return redirect(url_for("favoritos"))

@app.route("/compras")
def compras(): return render_template("compras.html",compras=Compra.query.order_by(Compra.id.desc()).all(),anuncios=Anuncio.query.all(),usuarios=Usuario.query.all(),titulo="Compras")
@app.post("/compras/criar")
def criarcompra():
    q=int(request.form.get("qtde") or 0); v=float(request.form.get("valor") or 0); t=float(request.form.get("total") or q*v); db.session.add(Compra(q,v,t,request.form.get("anuncio_id"),request.form.get("usuario_id"))); db.session.commit(); flash("Compra cadastrada com sucesso."); return redirect(url_for("compras"))
@app.route("/compras/editar/<int:id>",methods=["GET","POST"])
def editarcompra(id):
    o=Compra.query.get_or_404(id)
    if request.method=="POST": o.qtde=int(request.form.get("qtde") or 0); o.valor=float(request.form.get("valor") or 0); o.total=float(request.form.get("total") or o.qtde*o.valor); o.anuncio_id=request.form.get("anuncio_id"); o.usuario_id=request.form.get("usuario_id"); db.session.commit(); flash("Compra alterada com sucesso."); return redirect(url_for("compras"))
    return render_template("compra_form.html",compra=o,titulo="Alterar compra")
@app.post("/compras/deletar/<int:id>")
def deletarcompra(id): db.session.delete(Compra.query.get_or_404(id)); db.session.commit(); flash("Compra excluída com sucesso."); return redirect(url_for("compras"))

@app.route("/ofertas")
def ofertas(): return render_template("ofertas.html",titulo="Ofertas",anuncios=Anuncio.query.all(),categorias=Categoria.query.all())
@app.route("/relatorios")
def relatorios(): return render_template("relatorios.html")
@app.route("/relatorios/vendas")
def relVendas(): return render_template("relvendas.html",titulo="Relatório de vendas")
@app.route("/relatorios/compras")
def relCompras(): return render_template("relcompras.html",titulo="Relatório de compras")
@app.route("/cad/faleconosco")
def faleconosco(): return render_template("faleconosco.html",titulo="Fale Conosco")
@app.post("/cad/cadmsg")
def cadmsg(): return request.form
@app.route("/quemsomos")
def quemsomos(): return render_template("quemsomos.html",titulo="Quem somos")

if __name__=="__main__":
    with app.app_context(): db.create_all()
    app.run(debug=True)
