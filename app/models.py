from app import db


# NOTE: Not currently used
class User(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    account_type = db.Column(db.String(7))
    email = db.Column(db.String(191), index=True, unique=True)
    password_hash = db.Column(db.String(191))

    def __repr__(self):
        return f"{self.account_type}User[{self.email}]"
