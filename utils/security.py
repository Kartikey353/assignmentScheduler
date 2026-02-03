from passlib.context import CryptContext

# 🔹 The fix: Explicitly set bcrypt__ident="2b"
pwd_context = CryptContext(
    schemes=["bcrypt"], 
    deprecated="auto",
    bcrypt__ident="2b"
)

def hash_password(password: str) -> str:
    """Converts plain-text password to a secure hash."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Checks if the provided password matches the stored hash."""
    return pwd_context.verify(plain_password, hashed_password)