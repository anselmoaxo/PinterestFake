from flask import render_template, url_for, redirect
from fakepinterest import app, bcrypt, db
from flask_login import login_required, login_user, logout_user, current_user
from fakepinterest.forms import FormCriarConta, FormLogin, FormFoto
from fakepinterest.models import Usuario, Foto
import os
from werkzeug.utils import secure_filename
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Defina suas configurações de e-mail aqui
EMAIL_ADDRESS = ''
EMAIL_PASSWORD = ''

# Função para enviar e-mail
def enviar_email(destinatario, assunto, corpo):
    try:
        # Configurar o servidor SMTP do Gmail
        smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        # Crie uma mensagem multipart (texto e HTML)
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = destinatario
        msg['Subject'] = assunto

        # Corpo da mensagem em formato HTML
        msg.attach(MIMEText(corpo, 'html'))

        # Envie o e-mail
        smtp.sendmail(EMAIL_ADDRESS, destinatario, msg.as_string())

        # Feche a conexão com o servidor SMTP
        smtp.quit()
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")



@app.route("/", methods=['GET', 'POST'])
def homepage():
    form_login = FormLogin()
    if form_login.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario)
            return redirect(url_for("perfil", id_usuario=usuario.id))

    return render_template("homepage.html",forn=form_login)


@app.route("/criarconta", methods=['GET', 'POST'])
def criarconta():
    form_criar_conta = FormCriarConta()
    if form_criar_conta.validate_on_submit():
        senha = bcrypt.generate_password_hash(form_criar_conta.senha.data).decode('utf8')
        usuario = Usuario(nome=form_criar_conta.nome.data, email=form_criar_conta.email.data,
                          senha= senha)
        db.session.add(usuario)
        db.session.commit()
        #assunto = 'Bem-vindo à nossa aplicação!'
        #corpo = f'Olá {form_criar_conta.nome.data},\n\nSua conta foi criada com sucesso!\n\nBem-vindo!\n\nEquipe da nossa aplicação'
        #enviar_email(form_criar_conta.email.data, assunto, corpo)

        login_user(usuario, remember=True)
        return redirect(url_for("perfil", id_usuario= usuario.id))
    return render_template("criarconta.html", forn=form_criar_conta)

@app.route("/perfil/<id_usuario>", methods=['GET', 'POST'])
@login_required
def perfil(id_usuario):
    if int(id_usuario) == int(current_user.id):
        form_foto = FormFoto()
        if form_foto.validate_on_submit():
            arquivo = form_foto.foto.data
            nome_seguro = secure_filename(arquivo.filename)
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                   app.config['UPLOAD_FOLDER'], nome_seguro)
            arquivo.save(caminho)
            foto = Foto(id_usuario= current_user.id , imagem= nome_seguro)
            db.session.add(foto)
            db.session.commit()
        return render_template("perfil.html", usuario=current_user,forn=form_foto)

    else:
        usuario = Usuario.query.get(int(id_usuario))
        return render_template("perfil.html", usuario=usuario, forn= None)



@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))


@app.route("/feed")
@login_required
def feed():
    fotos= Foto.query.order_by(Foto.data_criacao).all()
    return render_template("feed.html", fotos=fotos)
