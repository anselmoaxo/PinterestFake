from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, ValidationError, Length, EqualTo, Email
from fakepinterest.models import Usuario

class FormLogin(FlaskForm):
    email = StringField("E_mail", validators=[DataRequired(), Email()] )
    senha= PasswordField("Senha", validators=[DataRequired()])
    botao_confirmar = SubmitField("Fazer Login")

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if not usuario:
            raise ValidationError("Usuário inexistente , Crie um Conta !")


class FormCriarConta(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    nome = StringField("Usuario", validators=[DataRequired()] )
    senha = PasswordField("Senha", validators=[DataRequired(), Length(6,20)])
    confirmacao_senha= PasswordField("Confirmação de Senha", validators=[DataRequired(), EqualTo("senha")])
    botao_confirmar = SubmitField("Criar Conta")

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError("E_mail já cadastrado, faça o login !")

class FormFoto(FlaskForm):
    foto = FileField("Foto", validators=[DataRequired()])
    botao_enviar=SubmitField("Enviar Foto")