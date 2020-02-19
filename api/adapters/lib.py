import hashlib, binascii, os
import random
import datetime
import re

class Lib:
    def __init__(self):
        self.valid = False
        self.json_content = {}

    @staticmethod
    def calcular_cashback(valor: float) -> object:
        """
        :param valor: valor da venda
        :return: valor percentual e range do cashback
        """
        if valor <= 1000:
            cashback_percentual = '10%'
            cashback_indice = 0.1
        elif valor >= 1001 and valor <= 1500:
            cashback_percentual = '15%'
            cashback_indice = 0.15
        else:
            cashback_percentual = '20%'
            cashback_indice = 0.2

        return cashback_percentual, cashback_indice

    @staticmethod
    def hash_password(password: str) -> str:
        """
        :param password:
        :return:
        """
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                      salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')

    @staticmethod
    def verify_password(stored_password: str, provided_password: str) -> bool:
        """
        :param stored_password: senha banco de dados
        :param provided_password: senha request
        :return: true ou false
        """
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512',
                                      provided_password.encode('utf-8'),
                                      salt.encode('ascii'),
                                      100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')

        return pwdhash == stored_password

    @staticmethod
    def gera_cpf():
        cpf = [random.randint(0, 9) for x in range(9)]

        for _ in range(2):
            val = sum([(len(cpf) + 1 - i) * v for i, v in enumerate(cpf)]) % 11

            cpf.append(11 - val if val > 1 else 0)

        return '%s%s%s%s%s%s%s%s%s%s%s' % tuple(cpf)

    @staticmethod
    def valida_nulo(field):
        regex = "^\s*$"
        if re.search(regex, field):
            raise ValueError("")

        return field

    @staticmethod
    def valida_email(email):
        regex = "^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
        if re.search(regex, email):
            return email

        raise ValueError("")

    @staticmethod
    def valida_data(data):
        try:
            datetime.datetime.strptime(data, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    @staticmethod
    def valida_cpf(cpf):
        # Check if type is str
        if not isinstance(cpf, str):
            return False

        # Remove some unwanted characters
        cpf = re.sub("[^0-9]", "", cpf)

        # Checks if string has 11 characters
        if len(cpf) != 11:
            return False

        sum = 0
        weight = 10

        """ Calculating the first cpf check digit. """
        for n in range(9):
            sum += int(cpf[n]) * weight

            # Decrement weight
            weight -= 1

        verifyingDigit = 11 - sum % 11

        if verifyingDigit > 9:
            firstVerifyingDigit = 0
        else:
            firstVerifyingDigit = verifyingDigit

        """ Calculating the second check digit of cpf. """
        sum = 0
        weight = 11
        for n in range(10):
            sum += int(cpf[n]) * weight

            # Decrement weight
            weight -= 1

        verifyingDigit = 11 - sum % 11

        if verifyingDigit > 9:
            secondVerifyingDigit = 0
        else:
            secondVerifyingDigit = verifyingDigit

        if cpf[-2:] == "%s%s" % (firstVerifyingDigit, secondVerifyingDigit):
            return True
        return False
