import os
import csv
import sqlite3


class ContractController:
    def __init__(self, file_path="data/contratos.csv", db_path="data/contracts.db"):
        self.file_path = file_path
        self.db_path = db_path
        self.ensure_data_directory_exists()

    def ensure_data_directory_exists(self):
        """Garante que o diretório para o arquivo CSV e banco de dados exista."""
        dir_path = os.path.dirname(self.file_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    def load_contracts(self):
        """Carrega contratos do arquivo CSV."""
        contracts = []
        try:
            with open(self.file_path, mode='r') as file:
                reader = csv.DictReader(file)
                contracts = [row for row in reader]
        except FileNotFoundError:
            pass  # Usamos 'pass' aqui para não fazer nada se o arquivo não existir.
        return contracts

    def save_contracts(self, contracts):
        """Salva a lista de contratos no arquivo CSV."""
        with open(self.file_path, mode='w', newline='') as file:
            fieldnames = ["Descrição do Contrato", "Categoria", "Data de Vencimento", "Fornecedor"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(contracts)

    def add_contract(self, contract):
        """Adiciona um novo contrato ao CSV."""
        contracts = self.load_contracts()
        contracts.append(contract)
        self.save_contracts(contracts)

    def delete_contract(self, description):
        """Deleta um contrato com base na descrição."""
        contracts = self.load_contracts()
        contracts = [c for c in contracts if c["Descrição do Contrato"] != description]
        self.save_contracts(contracts)

    def update_contract(self, description, updated_contract):
        """Atualiza um contrato com base na descrição."""
        contracts = self.load_contracts()
        for i, contract in enumerate(contracts):
            if contract["Descrição do Contrato"] == description:
                contracts[i] = updated_contract
                break
        self.save_contracts(contracts)

    def import_csv_to_sqlite(self):
        """Importa os contratos do CSV para o banco de dados SQLite."""
        contracts = self.load_contracts()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS contracts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    descricao TEXT,
                    categoria TEXT,
                    vencimento TEXT,
                    fornecedor TEXT
                )
            ''')
            for contract in contracts:
                cursor.execute('''
                    INSERT INTO contracts (descricao, categoria, vencimento, fornecedor)
                    VALUES (?, ?, ?, ?)
                ''', (
                    contract["Descrição do Contrato"],
                    contract["Categoria"],
                    contract["Data de Vencimento"],
                    contract["Fornecedor"]
                ))
            conn.commit()

    def export_sqlite_to_csv(self):
        """Exporta os contratos do banco de dados SQLite para o arquivo CSV."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT descricao, categoria, vencimento, fornecedor FROM contracts")
            rows = cursor.fetchall()
            contracts = [
                {
                    "Descrição do Contrato": row[0],
                    "Categoria": row[1],
                    "Data de Vencimento": row[2],
                    "Fornecedor": row[3]
                } for row in rows
            ]
            self.save_contracts(contracts)


# Funções auxiliares para interagir com o banco de dados SQLite
def initialize_db(db_path="data/contracts.db"):
    """Inicializa o banco de dados SQLite criando a tabela se não existir."""
    with sqlite3.connect(db_path) as conn:
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


def list_contracts(db_path="data/contracts.db"):
    """Lista todos os contratos do banco de dados SQLite."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, descricao, categoria, vencimento, fornecedor FROM contracts")
        return cursor.fetchall()


def create_contract(descricao, categoria, vencimento, fornecedor, db_path="data/contracts.db"):
    """Adiciona um novo contrato no banco de dados SQLite."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO contracts (descricao, categoria, vencimento, fornecedor)
            VALUES (?, ?, ?, ?)
        ''', (descricao, categoria, vencimento, fornecedor))
        conn.commit()


def delete_contract_by_id(contract_id, db_path="data/contracts.db"):
    """Deleta um contrato do banco de dados SQLite pelo ID."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM contracts WHERE id = ?", (contract_id,))
        conn.commit()


def update_contract_by_id(contract_id, descricao, categoria, vencimento, fornecedor, db_path="data/contracts.db"):
    """Atualiza um contrato no banco de dados SQLite pelo ID."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE contracts
            SET descricao = ?, categoria = ?, vencimento = ?, fornecedor = ?
            WHERE id = ?
        ''', (descricao, categoria, vencimento, fornecedor, contract_id))
        conn.commit()


# Exemplo de uso
if __name__ == "__main__":
    # Inicializa o banco de dados
    initialize_db()

    # Instancia o controlador
    controller = ContractController()

    # Adiciona um novo contrato
    contract_data = {
        "Descrição do Contrato": "Manutenção Predial",
        "Categoria": "Serviços",
        "Data de Vencimento": "2024-12-31",
        "Fornecedor": "Construtora XYZ"
    }
    controller.add_contract(contract_data)

    # Lista os contratos do CSV
    print("Contratos no CSV:", controller.load_contracts())

    # Importa contratos do CSV para SQLite
    controller.import_csv_to_sqlite()

    # Lista contratos do SQLite
    print("Contratos no SQLite:")
    for contract in list_contracts():
        print(contract)

    # Atualiza um contrato no SQLite
    update_contract_by_id(1, "Manutenção Predial Atualizada", "Serviços Atualizados", "2025-01-15", "Construtora ABC")

    # Exclui um contrato no SQLite
    delete_contract_by_id(1)

    # Exporta contratos do SQLite para CSV
    controller.export_sqlite_to_csv()
