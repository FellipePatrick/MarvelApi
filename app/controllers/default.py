from flask_login import login_required, login_user, logout_user
from app import app, db, login_manager
from flask import  render_template, flash, redirect, url_for
from app.models.forms import LoginForm, CreateUser, CreateTeam, CreateHero, Candidato, recuperar, Search
from app.models.agente import Agente
from app.models.tables import User, equipe, candidato, heroi
from translate import Translator

objeto = Agente()

@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()

@app.route('/index', methods=['GET','POST'])

def index():
    form = Search()
    if form.validate_on_submit():
        c = candidato.query.filter_by(name=form.username.data).first()
        if c and c.name == form.username.data:
            flash("O heroi é um candidato")      
            return redirect(url_for("index"))
        else:
            flash("Este nome não é um candidato")       
    return render_template('index.html', hero=objeto.getheros(), form=form)


@app.route('/login',methods=['GET','POST'])
@app.route('/', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        senha = objeto.hash5(form.password.data)
        if user and user.senha == senha:
            print("entrou")
            login_user(user)
            return redirect(url_for("index"))
        else:
            print("passou")
            flash("Login Invalido")
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout feito com sucesso")
    return redirect(url_for('login'))


@app.route('/recuperarsenha', methods=['GET','POST'])
def recuperarsenha():
    form = recuperar()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.telefone == form.phone.data:
            flash("Em até 24 horas, algum agente da shield entrará contato com você!")
        else:
            flash("Credenciais invalidas")

    return render_template('recuperarsenha.html', form=form)
    
@app.route('/heros', methods=['POST', 'GET'])
def heros():
    return render_template('heros.html', hero=objeto.getheros())

@app.route('/atualizar/<int:heroi_id>', methods=['GET','POST'])

def atualizarheroi(heroi_id):
    for i in objeto.gethero(heroi_id):
        userid = i['id']
        name = i['name']
        descricao = i['description']
    form = Candidato()
    formhero = CreateHero()
    verificacao = candidato.query.filter_by(userid=userid).first()
    validacao = heroi.query.filter_by(nome=name).first()
    ponto = 0
    var =  0
    equipehero = ''
    c = 0
    if verificacao and verificacao.userid == userid:
            ponto = 1
            c = 1
            if validacao and  validacao.nome ==  name:
                var = 1
                equipehero = validacao.equipe
            else:
                if formhero.validate_on_submit():
                    equipeverificar = equipe.query.filter_by(nome=formhero.equipe.data).first()
                    if equipeverificar and equipeverificar.nome == formhero.equipe.data:
                        flash("Você adicionou "+name+" a equipe "+ formhero.equipe.data )
                        hero = heroi(formhero.equipe.data, name, userid)
                        db.session.add(hero)
                        db.session.commit()
                    else:
                        flash("O sistema so aceita a adicação a alguma equipe existente.")
    else:
        if form.validate_on_submit():
            flash("Você adicionou "+name+" a lista de candidatos." )
            o = candidato(form.status.data,userid, name)
            db.session.add(o)
            db.session.commit()
    translator= Translator(from_lang="en",to_lang="pt-br")
    translation = translator.translate(descricao)      
    return render_template('verheroi.html', hero=objeto.gethero(heroi_id), events=objeto.getseries(heroi_id), 
    comics=objeto.getcomics(heroi_id), form= form, traducao=translation, 
    formhero=formhero,  verificacao=ponto, var=var, equipehero =equipehero)

@app.route('/candidatos', methods=['POST', 'GET', 'DELETE'])
def candidatos():
    tcandidatos = candidato.query.all()
    return render_template('candidatos.html', candidato=tcandidatos)

@app.route('/perfil')
@login_required
def perfil():
    return render_template('perfil.html')

@app.route('/dashequipe')
@login_required
def dashequipe():
    equipes = equipe.query.all()
    return render_template('dashequipe.html', equipes=equipes)

@app.route('/dashequipe/criar', methods=['GET','POST'])
@login_required
def criarequipe():
    form = CreateTeam()
    if form.validate_on_submit():
        time = equipe(form.name.data, form.description.data)
        db.session.add(time)
        db.session.commit()
        print("criou")
        flash("Equipe criada")
    else:
        print(form.errors)
    return render_template('criarequipe.html', form=form)

@app.route('/dashuser')

def dashuser():
    all_data = User.query.all()
    return render_template('dashuser.html', usuarios = all_data)

@app.route('/dashuser/atualizar/<int:id>', methods=['GET','POST', 'DELETE'])
def attuser(id):
    form = CreateUser()
    user = User.query.filter_by(id=id).first()
    if form.validate_on_submit():
        if form.password.data != form.repetepassword.data:
            flash("As senhas não são iguais")
            print("nao criado")
    else:
        if form.validate_on_submit():
            if form.email.data != 'email':
                user.email = form.email.data
            if form.phone.data != 'telefone':
                user.telefone = form.phone.data
            if form.username.data != 'Usuário':
                user.username = form.username.data
            senha = objeto.hash5(form.password.data)
            if senha != user.senha:
                user.senha = senha
            if form.name.data != 'nome':
                user.nome = form.name.data
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('dashuser'))
    return render_template('atualizaruser.html',user=user, form=form)

@app.route('/deletec/<int:id>', methods=['POST', 'GET', 'DELETE'])
def deletec(id):
    p = candidato.query.filter_by(id=id).first()
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for('candidatos'))
@app.route('/delete/<int:id>', methods=['POST', 'GET', 'DELETE'])
def delete(id):
    user = User.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('dashuser'))

@app.route('/dashuser/criar', methods=['GET','POST'])
def criaruser():
    variavel = str("nome aleatorio")
    user = User.query.filter_by(username="jamsfury").first()
    print(user)
    form = CreateUser()
    if form.validate_on_submit():
        if form.password.data != form.repetepassword.data:
            flash("As senhas não são iguais")
        else:
            senha =  objeto.hash5(form.password.data)
            i = User(form.email.data, form.username.data, "agente", senha, form.name.data, form.phone.data)
            db.session.add(i)
            db.session.commit()
            flash("Usuario criado")
    else:
        print(form.errors)
    return render_template('criaruser.html', form=form, variavel = variavel)