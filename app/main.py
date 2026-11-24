from flask import Blueprint, abort, flash, jsonify, redirect, render_template, url_for
from flask_login import current_user, login_required

from .extensions import db
from .models import Application, InstallRequest

bp = Blueprint("main", __name__)


@bp.route("/")
@login_required
def index():
    if current_user.is_admin:  # l'admin non usa il catalogo: va alla sua pagina
        return redirect(url_for("admin.requests_list"))
    apps = Application.query.order_by(Application.name).all()
    # stato della richiesta dell'utente per ogni app: {id_app: "pending" | ...}
    my_requests = {r.application_id: r.status for r in current_user.requests}
    return render_template("index.html", apps=apps, my_requests=my_requests)


@bp.route("/request/<int:app_id>", methods=["POST"])
@login_required
def request_install(app_id):
    if current_user.is_admin:  # solo gli utenti normali possono richiedere
        abort(403)
    app_obj = db.get_or_404(Application, app_id)
    exists = InstallRequest.query.filter_by(
        user_id=current_user.id, application_id=app_obj.id
    ).first()
    if exists:
        flash("Hai già richiesto questa applicazione.")
    else:
        db.session.add(
            InstallRequest(user_id=current_user.id, application_id=app_obj.id)
        )
        db.session.commit()
        flash(f"Richiesta inviata per {app_obj.name}.")
    return redirect(url_for("main.index"))


@bp.route("/api/apps")
@login_required
def api_apps():
    apps = Application.query.order_by(Application.name).all()
    return jsonify([a.to_dict() for a in apps])
