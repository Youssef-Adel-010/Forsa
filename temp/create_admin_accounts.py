import sys
from werkzeug.security import generate_password_hash
from app import create_app, db
from app.models.user import User


def create_admin_accounts():

    admin_accounts = [
        ("Admin One", "admin1", "admin1@forsa.com", "2001111111"),
        ("Admin Two", "admin2", "admin2@forsa.com", "2002222222"),
        ("Admin Three", "admin3", "admin3@forsa.com", "2003333333"),
        ("Admin Four", "admin4", "admin4@forsa.com", "2004444444"),
        ("Admin Five", "admin5", "admin5@forsa.com", "2005555555"),
    ]

    app = create_app()

    with app.app_context():

        for name, username, email, phone in admin_accounts:
            if User.query.filter_by(username=username).first():
                continue

            if User.query.filter_by(email=email).first():
                continue

            if User.query.filter_by(phone=phone).first():
                continue

            password = f"Admin@{username[-1]}"
            password_hash = generate_password_hash(password, method='pbkdf2:sha256')

            admin_user = User(
                name=name,
                username=username,
                email=email,
                phone=phone,
                password_hash=password_hash,
                cv_path="temp/admin_cv.pdf",
                is_admin=True,
                summary="Administrator account"
            )

            db.session.add(admin_user)

        try:
            db.session.commit()
            for name, username, email, phone in admin_accounts:
                password = f"Admin@{username[-1]}"
        except Exception as e:
            db.session.rollback()
            sys.exit(1)


if __name__ == "__main__":
    create_admin_accounts()
