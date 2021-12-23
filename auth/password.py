from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def encrypt_password(password) -> str:
    """
    Encrypts a given password

    Args:
        password: the password to encrypt

    Returns:
        str: the encrypted password

    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """

    Args:
        plain_password: the plain user password
        hashed_password: the hashed user password

    Returns:
        bool: True if the plain password is corresponding to the hashed password, False otherwise
    """

    return pwd_context.verify(plain_password, hashed_password)
