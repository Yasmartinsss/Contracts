import sqlite3
import shutil

DB_PATH = "data/contracts.db"

def initialize_db():
    """
    Cria a tabela de contratos no banco de dados, caso não exista.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS contracts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descricao TEXT NOT NULL,
                categoria TEXT NOT NULL,
                vencimento TEXT NOT NULL,
                fornecedor TEXT NOT NULL
            )
            ''')
            conn.commit()
            print("Tabela de contratos criada com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao inicializar o banco de dados: {e}")

def create_contract(descricao, categoria, vencimento, fornecedor):
    """
    Cria um novo contrato no banco de dados.
    """
    if not descricao or not categoria or not vencimento or not fornecedor:
        print("Todos os campos são obrigatórios!")
        return

    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO contracts (descricao, categoria, vencimento, fornecedor)
                VALUES (?, ?, ?, ?)
            ''', (descricao, categoria, vencimento, fornecedor))
            conn.commit()
            print(f"Contrato '{descricao}' criado com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao criar o contrato: {e}")

def list_contracts():
    """
    Lista todos os contratos no banco de dados.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM contracts")
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao listar os contratos: {e}")
        return []

def update_contract(contract_id, descricao, categoria, vencimento, fornecedor):
    """
    Atualiza um contrato existente no banco de dados.
    """
    if not descricao or not categoria or not vencimento or not fornecedor:
        print("Todos os campos são obrigatórios!")
        return

    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE contracts
            SET descricao = ?, categoria = ?, vencimento = ?, fornecedor = ?
            WHERE id = ?
            ''', (descricao, categoria, vencimento, fornecedor, contract_id))

            if cursor.rowcount == 0:
                print(f"Contrato com ID {contract_id} não encontrado!")
                return

            conn.commit()
            print(f"Contrato {contract_id} atualizado com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao atualizar o contrato: {e}")

def delete_contract(contract_id):
    """
    Deleta um contrato com base no ID.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM contracts WHERE id = ?", (contract_id,))
            conn.commit()

            if cursor.rowcount == 0:
                print(f"Contrato com ID {contract_id} não encontrado!")
                return

            print(f"Contrato {contract_id} deletado com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao deletar o contrato: {e}")

def backup_database():
    """
    Faz um backup do banco de dados para um arquivo separado.
    """
    try:
        shutil.copy(DB_PATH, "data/contracts_backup.db")
        print("Backup do banco de dados realizado com sucesso!")
    except Exception as e:
        print(f"Erro ao realizar o backup do banco de dados: {e}")

# Exemplo de uso (para testes)
if __name__ == "__main__":
    initialize_db()  # Cria a tabela de contratos no banco de dados se não existir

    # Criando um novo contrato
    create_contract("Serviço de TI", "Tecnologia", "2024-12-31", "Empresa XYZ")

    # Listando todos os contratos
    contracts = list_contracts()
    print("Contratos:", contracts)

    # Atualizando um contrato
    if contracts:
        contract_id = contracts[0][0]  # ID do primeiro contrato
        update_contract(contract_id, "Serviço de TI Atualizado", "Tecnologia Avançada", "2025-01-01", "Empresa XYZ")

    # Deletando um contrato
    if contracts:
        delete_contract(contracts[0][0])

    # Fazendo backup do banco de dados
    backup_database()
