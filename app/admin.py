from functools import wraps

from flask import Blueprint, abort, redirect, render_template, url_for
from flask_login import current_user, login_required

from .extensions import db
from .models import APPROVED, PENDING, REJECTED, InstallRequest

bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(view):
    @wraps(view)
    @login_required
    def wrapper(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return view(*args, **kwargs)

    return wrapper


@bp.route("/")
@admin_required
def requests_list():
    pending = InstallRequest.query.filter_by(status=PENDING).order_by(InstallRequest.created_at).all()
    return render_template("admin.html", requests=pending)


@bp.route("/<int:request_id>/<action>", methods=["POST"])
@admin_required
def decide(request_id, action):
    if action not in ("approve", "reject"):
        abort(404)
    req = db.get_or_404(InstallRequest, request_id)
    req.status = APPROVED if action == "approve" else REJECTED
    db.session.commit()
    return redirect(url_for("admin.requests_list"))
