from passlib.context import CryptContext

passw_context = CryptContext(schemes=["bcrypt"])


def generate_pass_hash(password: str) -> str:
    return passw_context.hash(password)


def verify_pass_hash(password: str, hash: str) -> bool:
    return passw_context.verify(password, hash)
