import unittest
from fastapi.testclient import TestClient
from main import app

# Cria um cliente de teste que simula requisições reais
client = TestClient(app)

class TestOperadorasAPI(unittest.TestCase):
    #Testa se a API está online e listando operadoras (Status 200)
    def test_status_api(self):
        
        response = client.get("/api/operadoras")
        self.assertEqual(response.status_code, 200)
        
        # Verifica se a resposta tem a estrutura correta
        dados = response.json()
        self.assertIn("data", dados)
        self.assertIn("meta", dados)
        self.assertIsInstance(dados["data"], list)

    # Testa se o parâmetro 'limit' funciona.
    def test_paginacao_limite(self):
        limit = 5
        response = client.get(f"/api/operadoras?limit={limit}")
        self.assertEqual(response.status_code, 200)
        
        dados = response.json()
        # Se houver dados suficientes, deve retornar 5 ou menos
        self.assertLessEqual(len(dados["data"]), limit)

    # Testa a busca por uma operadora que não existe
    def test_busca_inexistente(self):
        response = client.get("/api/operadoras?search=XYZ_NOME_IMPOSSIVEL_123")
        self.assertEqual(response.status_code, 200)
        dados = response.json()
        # A lista de dados deve vir vazia
        self.assertEqual(len(dados["data"]), 0)

    # Testa se a rota de estatísticas retorna os Top Estados
    def test_estatisticas(self):
        response = client.get("/api/estatisticas")
        
        if response.status_code == 200:
            dados = response.json()
            self.assertIn("top_estados", dados)
            self.assertIsInstance(dados["top_estados"], list)

    # Testa uma rota que não existe para garantir que retorna 404
    def test_rota_404(self):
       
        response = client.get("/api/rota-que-nao-existe")
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()