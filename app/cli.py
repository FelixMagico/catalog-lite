import click

from .extensions import db
from .models import ROLE_ADMIN, Application, User

SAMPLE_APPS = [
    ("7-Zip", "Programma per comprimere e decomprimere file"),
    ("Notepad++", "Editor di testo per programmatori"),
    ("VLC", "Lettore multimediale"),
    ("Firefox", "Browser web"),
]


@click.command("seed-db")
def seed_db():
    """Crea l'utente admin e qualche applicazione di esempio."""
    if not User.query.filter_by(username="admin").first():
        admin = User(username="admin", role=ROLE_ADMIN)
        admin.set_password("admin123")
        db.session.add(admin)
    for name, description in SAMPLE_APPS:
        if not Application.query.filter_by(name=name).first():
            db.session.add(Application(name=name, description=description))
    db.session.commit()
    click.echo("Fatto. Admin: admin / admin123")
