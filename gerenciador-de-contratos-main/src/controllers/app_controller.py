from controllers.contract_controller import ContractController
from views.home_view import HomeView
from views.contract_view import ContractView
from views.add_contract_view import AddContractView
from views.filter_by_days_view import FilterByDaysView

class AppController:
    def __init__(self):
        self.root = None
        self.current_view = None
        self.contract_controller = ContractController()

    def set_root(self, root):
        """Define a raiz da interface e inicializa a tela inicial."""
        self.root = root
        self.show_home_view()

    def show_home_view(self):
        """Mostra a tela inicial."""
        if self.current_view:
            self.current_view.destroy()  
        self.current_view = HomeView(self.root, self)

    def show_contract_view(self):
        """Mostra a visualização de contratos."""
        if self.current_view:
            self.current_view.destroy()  
        self.current_view = ContractView(self.root, self)

    def show_add_contract_view(self):
        """Mostra a tela de adicionar contrato."""
        if self.current_view:
            self.current_view.destroy()  
        self.current_view = AddContractView(self.root, self)

    def show_filter_by_days_view(self):
        if self.current_view:
            self.current_view.destroy()
        self.current_view = FilterByDaysView(self.root, self)
from controllers.contract_sqlite_controller import create_contract, list_contracts

def add_new_contract(self, descricao, categoria, vencimento, fornecedor):
    create_contract(descricao, categoria, vencimento, fornecedor)

def display_contracts(self):
    contracts = list_contracts()
    print(contracts)  # Exibir ou passar para a interface gráfica
