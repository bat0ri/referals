import bcrypt

class BcryptHasher:
    """
    Класс BcryptHasher предоставляет статические методы для работы с хэшированием паролей с использованием bcrypt.
    """
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Проверяет, соответствует ли открытый пароль хэшированному паролю.
        
        :param plain_password: Открытый пароль для проверки.
        :param hashed_password: Хэшированный пароль для сравнения.
        :return: Возвращает True, если открытый пароль соответствует хэшированному паролю, иначе False.
        """
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        Получает хэш пароля.
        
        :param password: Открытый пароль для хэширования.
        :return: Возвращает хэшированный пароль.
        """
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed_password.decode('utf-8')
