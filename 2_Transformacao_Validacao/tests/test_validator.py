import unittest
import sys
import os

# Adiciona o diretório 'src' ao path para conseguir importar o validator
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.validator import validate_cnpj

class TestCNPJValidator(unittest.TestCase):

    def test_cnpj_valido_com_formatacao(self):
        # CNPJ do Google Brasil (Exemplo público)
        self.assertTrue(validate_cnpj("06.990.590/0001-23"))

    def test_cnpj_valido_apenas_numeros(self):
        self.assertTrue(validate_cnpj("06990590000123"))

    def test_cnpj_invalido_digito_verificador(self):
        # CNPJ visualmente ok, mas matematicamente errado
        self.assertFalse(validate_cnpj("06.990.590/0001-00"))

    def test_cnpj_tamanho_incorreto(self):
        self.assertFalse(validate_cnpj("123"))
        self.assertFalse(validate_cnpj("12345678901234567890"))

    def test_entrada_vazia(self):
        self.assertFalse(validate_cnpj(""))
        self.assertFalse(validate_cnpj(None))

if __name__ == '__main__':
    unittest.main()