from fakepinterest import db, app
from fakepinterest.models import Usuario, Foto

with app.app_context():
    db.create_all()

