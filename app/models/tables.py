from app import  db

class User(db.Model):
    __tablename__= "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    cargo = db.Column(db.String, nullable=False)
    senha = db.Column(db.String, nullable=False)
    nome = db.Column(db.String)
    telefone = db.Column(db.String)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __init__(self, email, username, cargo, senha, nome, telefone):
        self.email = email
        self.username = username
        self.cargo = cargo
        self.senha = senha
        self.nome = nome
        self.telefone = telefone
    
    def __repr__(self):
        return '<User %r>' % self.username
    

class equipe(db.Model):
    __tablename__ = "equipes"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, nullable=False)

    def __init__(self, nome, description):
        self.nome = nome
        self.description = description
    def __repr__(self):
        return '<equipe %r>' % self.nome

class heroi(db.Model):
    __tablename__ ="herois"
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, nullable=False, unique=True)
    nome = db.Column(db.String, unique=True)
    equipe = db.Column(db.String,  nullable=False)

    def __init__(self, equipe, nome, userid) -> None:
        self.userid = userid
        self.nome = nome
        self.equipe = equipe
    
    def __repr__(self):
        return '<candidato %r>' % self.id

class candidato(db.Model):
    __tablename__ ="candidatos"
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, nullable=False, unique=True)
    status = db.Column(db.String, nullable=False )
    name = db.Column(db.String, nullable=False, unique=True)


    def __init__(self, status, userid, name) -> None:
        self.status = status
        self.userid = userid
        self.name = name

    def __repr__(self):
        return '<candidato %r>' % self.id
