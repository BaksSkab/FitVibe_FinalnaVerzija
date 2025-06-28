from passlib.context import CryptContext
from app.models import Admin

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def authenticate_admin(email: str, password: str, db):
    admin = db.query(Admin).filter(Admin.email == email).first()
    if not admin:
        return None
    if not pwd_context.verify(password, admin.password):
        return None
    return admin
