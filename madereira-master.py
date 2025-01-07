import subprocess
import sys

def install(package):
    """Install a package using pip."""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# List of required packages
required_packages = ['PyQt5', 'fpdf']

# Check and install required packages
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        print(f"Installing {package}...")
        install(package)

import sys
import json
import os
from PyQt5 import QtWidgets, QtGui, QtCore
from fpdf import FPDF
from datetime import datetime

class ProdutosDialog(QtWidgets.QDialog):
    def __init__(self, produtos, on_edit, on_delete):
        super().__init__()
        self.setWindowTitle("Produtos Registrados")
        self.setGeometry(200, 200, 400, 300)  # Window size
        self.on_edit = on_edit
        self.on_delete = on_delete

        layout = QtWidgets.QVBoxLayout(self)

        if not produtos:
            layout.addWidget(QtWidgets.QLabel("Nenhum produto registrado."))
        else:
            self.produtos_list = QtWidgets.QListWidget()
            for produto in produtos:
                self.produtos_list.addItem(produto["descricao"])
            layout.addWidget(self.produtos_list)

            # Buttons for editing and deleting
            btn_layout = QtWidgets.QHBoxLayout()
            self.btn_edit = QtWidgets.QPushButton("Editar Produto")
            self.btn_edit.clicked.connect(self.edit_selected_product)
            btn_layout.addWidget(self.btn_edit)

            self.btn_delete = QtWidgets.QPushButton("Excluir Produto")
            self.btn_delete.clicked.connect(self.delete_selected_product)
            btn_layout.addWidget(self.btn_delete)

            layout.addLayout(btn_layout)

        self.setLayout(layout)

    def edit_selected_product(self):
        selected_items = self.produtos_list.selectedItems()
        if selected_items:
            selected_product = selected_items[0].text()
            self.on_edit(selected_product)
            self.accept()  # Close the dialog

    def delete_selected_product(self):
        selected_items = self.produtos_list.selectedItems()
        if selected_items:
            selected_product = selected_items[0].text()
            reply = QtWidgets.QMessageBox.question(self, 'Confirmar Exclusão',
                                                   f"Tem certeza que deseja excluir o produto '{selected_product}'?",
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.Yes:
                self.on_delete(selected_product)
                QtWidgets.QMessageBox.information(self, "Sucesso", f"Produto '{selected_product}' excluído com sucesso!")
                self.accept()  # Close the dialog after deletion

class ClientesDialog(QtWidgets.QDialog):
    def __init__(self, clientes, on_edit, on_delete):
        super().__init__()
        self.setWindowTitle("Clientes Registrados")
        self.setGeometry(200, 200, 400, 300)  # Window size
        self.on_edit = on_edit
        self.on_delete = on_delete

        layout = QtWidgets.QVBoxLayout(self)

        if not clientes:
            layout.addWidget(QtWidgets.QLabel("Nenhum cliente registrado."))
        else:
            self.clientes_list = QtWidgets.QListWidget()
            for cliente in clientes:
                self.clientes_list.addItem(cliente["nome"])
            layout.addWidget(self.clientes_list)

            # Buttons for editing and deleting
            btn_layout = QtWidgets.QHBoxLayout()
            self.btn_edit = QtWidgets.QPushButton("Editar Cliente")
            self.btn_edit.clicked.connect(self.edit_selected_client)
            btn_layout.addWidget(self.btn_edit)

            self.btn_delete = QtWidgets.QPushButton("Excluir Cliente")
            self.btn_delete.clicked.connect(self.delete_selected_client)
            btn_layout.addWidget(self.btn_delete)

            layout.addLayout(btn_layout)

        self.setLayout(layout)

    def edit_selected_client(self):
        selected_items = self.clientes_list.selectedItems()
        if selected_items:
            selected_client = selected_items[0].text()
            self.on_edit(selected_client)
            self.accept()  # Close the dialog

    def delete_selected_client(self):
        selected_items = self.clientes_list.selectedItems()
        if selected_items:
            selected_client = selected_items[0].text()
            reply = QtWidgets.QMessageBox.question(self, 'Confirmar Exclusão',
                                                   f"Tem certeza que deseja excluir o cliente '{selected_client}'?",
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.Yes:
                self.on_delete(selected_client)
                QtWidgets.QMessageBox.information(self, "Sucesso", f"Cliente '{selected_client}' excluído com sucesso!")
                self.accept()  # Close the dialog after deletion

class WelcomeScreen(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MADEREIRA CASA BRANCA")
        self.setGeometry(100, 100, 1000, 600)  # Increased window size

        # Layout principal
        layout = QtWidgets.QVBoxLayout(self)  # Layout vertical principal

        # Parte superior: Imagem do logo
        self.logo_label = QtWidgets.QLabel()
        logo_pixmap = QtGui.QPixmap("Imgs/logo.png")  # Substitua pelo caminho correto da imagem
        self.logo_label.setPixmap(logo_pixmap.scaledToHeight(200, QtCore.Qt.SmoothTransformation))  # Ajusta a altura
        self.logo_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.logo_label, stretch=1)  # Adiciona a imagem com prioridade de espaço

        # Parte inferior: Botões
        button_layout = QtWidgets.QVBoxLayout()  # Layout vertical para os botões

        # Criação dos botões com efeitos
        self.btn_clientes = self.create_button("Clientes", "Imgs/cliente.png", self.open_clientes)
        button_layout.addWidget(self.btn_clientes)

        self.btn_produtos = self.create_button("Produtos", "Imgs/Produtos.png", self.open_produtos)
        button_layout.addWidget(self.btn_produtos)

        self.btn_orcamento = self.create_button("Orçamento", "Imgs/orcamento.png", self.open_orcamento)
        button_layout.addWidget(self.btn_orcamento)

        # Adiciona o layout dos botões na parte inferior
        button_widget = QtWidgets.QWidget()
        button_widget.setLayout(button_layout)
        button_widget.setStyleSheet("background-color: white;")  # Fundo branco para os botões
        layout.addWidget(button_widget, stretch=2)  # Adiciona os botões com maior prioridade de espaço

        # Define o layout principal
        self.setLayout(layout)

    def create_button(self, text, icon_path, callback):
        """Cria um botão com ícone e efeito de hover."""
        button = QtWidgets.QPushButton(text)
        button.setIcon(QtGui.QIcon(icon_path))
        button.setIconSize(QtCore.QSize(80, 80))  # Aumenta o tamanho do ícone
        button.setFont(QtGui.QFont("Arial", 28))  # Aumenta o tamanho da fonte
        button.setStyleSheet(self.button_hover_effect())
        button.clicked.connect(callback)
        button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)  # Expande horizontalmente
        return button

    def button_hover_effect(self):
        """Retorna o estilo CSS para o efeito de hover dos botões."""
        return """
            QPushButton {
                border: none;
                padding: 20px;  /* Aumenta o padding para botões maiores */
                font-size: 28px;  /* Tamanho da fonte */
                background-color: white;
            }
            QPushButton:hover {
                background-color: #e0e0e0;  /* Cor ao passar o mouse */
            }
        """

    def open_clientes(self):
        self.sistema_orcamento = SistemaOrcamentoMadeireira()
        self.sistema_orcamento.showMaximized()  # Open in maximized state
        self.sistema_orcamento.tabs.setCurrentIndex(1)  # Set to "Clientes" tab
        self.close()  # Close the welcome screen

    def open_produtos(self):
        self.sistema_orcamento = SistemaOrcamentoMadeireira()
        self.sistema_orcamento.showMaximized()  # Open in maximized state
        self.sistema_orcamento.tabs.setCurrentIndex(0)  # Set to "Produtos" tab
        self.close()  # Close the welcome screen

    def open_orcamento(self):
        self.sistema_orcamento = SistemaOrcamentoMadeireira()
        self.sistema_orcamento.showMaximized()  # Open in maximized state
        self.sistema_orcamento.tabs.setCurrentIndex(2)  # Set to "Orçamento" tab
        self.close()  # Close the welcome screen

class SistemaOrcamentoMadeireira(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Orçamento - Madeireira")
        self.setGeometry(100, 100, 1400, 800)  # Increased window size

        # Central widget and layout
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QtWidgets.QVBoxLayout(self.central_widget)

        # Tab widget
        self.tabs = QtWidgets.QTabWidget()
        self.layout.addWidget(self.tabs)  # Add the tab widget to the layout

        # Create tabs
        self.tab_produtos = QtWidgets.QWidget()
        self.tab_clientes = QtWidgets.QWidget()
        self.tab_orcamento = QtWidgets.QWidget()

        self.tabs.addTab(self.tab_produtos, "Produtos")
        self.tabs.addTab(self.tab_clientes, "Clientes")
        self.tabs.addTab(self.tab_orcamento, "Orçamento")

        # Initialize data
        self.produtos = []
        self.clientes = []
        self.orcamento_produtos = []  # List to hold products added to the budget
        self.arquivo_dados = "dados.json"

        # Create interfaces
        self.criar_interface_produtos()
        self.criar_interface_clientes()
        self.criar_interface_orcamento()

        # Load saved data
        self.carregar_dados()

        # Set style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
                font-family: 'Garamond', serif;
            }
            QTabWidget::pane {
                border: 1px solid #ccc;
            }
            QTabBar::tab {
                background: #e0e0e0;
                padding: 10px;
                font-weight: bold;
                min-width: 307px;  /* Minimum width for tabs */
            }
            QTabBar::tab:selected {
                background: #d0d0d0;
            }
            QWidget {
                background-color: #ffffff;  /* Light background for all tabs */
            }
            QPushButton {
                background-color: #007BFF;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QLineEdit {
                padding: 10px;
                border: 2px solid #007BFF;  /* Blue border for better contrast */
                border-radius: 0;  /* Square corners */
                min-height: 40px;  /* Increased height */
                background-color: #ffffff;  /* White background for input fields */
                color: #000000;  /* Black text for input fields */
            }
            QLineEdit:focus {
                border: 2px solid #0056b3;  /* Change border color on focus */
            }
            QComboBox {
                padding: 10px;
                border: 2px solid #007BFF;  /* Blue border for better contrast */
                border-radius: 0;  /* Square corners */
                background-color: #ffffff;  /* White background for combo boxes */
                color: #000000;  /* Black text for combo boxes */
            }
            QComboBox:focus {
                border: 2px solid #0056b3;  /* Change border color on focus */
            }
            QLabel {
                font-size: 14px;
                color: #000000;  /* Black text for labels */
            }
        """)

    def criar_interface_produtos(self):
        layout = QtWidgets.QVBoxLayout(self.tab_produtos)

        # Product input fields
        self.produto_desc = QtWidgets.QLineEdit()
        self.produto_desc.setPlaceholderText("Descrição do Produto")
        layout.addWidget(self.produto_desc)

        self.produto_vlr_m = QtWidgets.QLineEdit()
        self.produto_vlr_m.setPlaceholderText("Vlr. M.")  # New field for Value per Meter
        layout.addWidget(self.produto_vlr_m)

        # Button to register product
        self.btn_adicionar_produto = QtWidgets.QPushButton("Registrar Produto")
        self.btn_adicionar_produto.clicked.connect(self.adicionar_produto)
        layout.addWidget(self.btn_adicionar_produto)

        # Button to show registered products
        self.btn_mostrar_produtos = QtWidgets.QPushButton("Produtos Registrados")
        self.btn_mostrar_produtos.clicked.connect(self.mostrar_produtos_registrados)
        layout.addWidget(self.btn_mostrar_produtos)

        # Stretch to fill space
        layout.addStretch()

    def criar_interface_clientes(self):
        layout = QtWidgets.QVBoxLayout(self.tab_clientes)

        # Client input fields
        self.cliente_nome = QtWidgets.QLineEdit()
        self.cliente_nome.setPlaceholderText("Nome do Cliente")
        layout.addWidget(self.cliente_nome)

        self.cliente_cpf = QtWidgets.QLineEdit()
        self.cliente_cpf.setPlaceholderText("CPF/CNPJ do Cliente")
        layout.addWidget(self.cliente_cpf)

        self.cliente_endereco = QtWidgets.QLineEdit()
        self.cliente_endereco.setPlaceholderText("Endereço do Cliente")
        layout.addWidget(self.cliente_endereco)

        self.cliente_cidade = QtWidgets.QLineEdit()
        self.cliente_cidade.setPlaceholderText("Cidade do Cliente")
        layout.addWidget(self.cliente_cidade)

        self.cliente_telefone = QtWidgets.QLineEdit()
        self.cliente_telefone.setPlaceholderText("Telefone do Cliente")
        layout.addWidget(self.cliente_telefone)

        # Button to register client
        self.btn_adicionar_cliente = QtWidgets.QPushButton("Registrar Cliente")
        self.btn_adicionar_cliente.clicked.connect(self.adicionar_cliente)
        layout.addWidget(self.btn_adicionar_cliente)

        # Button to show registered clients
        self.btn_mostrar_clientes = QtWidgets.QPushButton("Clientes Registrados")
        self.btn_mostrar_clientes.clicked.connect(self.mostrar_clientes_registrados)
        layout.addWidget(self.btn_mostrar_clientes)

        # Stretch to fill space
        layout.addStretch()

    def criar_interface_orcamento(self):
        layout = QtWidgets.QVBoxLayout(self.tab_orcamento)

        # Set background color to white
        self.tab_orcamento.setStyleSheet("background-color: white;")

        # Product selection
        self.produto_combobox = QtWidgets.QComboBox()
        self.produto_combobox.setEditable(True)  # Make it editable
        self.produto_combobox.setPlaceholderText("Selecione um produto")
        layout.addWidget(self.produto_combobox)

        # Size input
        self.produto_tamanho = QtWidgets.QLineEdit()
        self.produto_tamanho.setPlaceholderText("Tamanho (em metros)")
        layout.addWidget(self.produto_tamanho)

        # Client search input
        self.cliente_search = QtWidgets.QLineEdit()
        self.cliente_search.setPlaceholderText("Digite o nome do cliente (ex: FEL) e pressione Enter")
        self.cliente_search.returnPressed.connect(self.search_client)
        layout.addWidget(self.cliente_search)

        # Input field for selected client
        self.cliente_input = QtWidgets.QLineEdit()
        self.cliente_input.setPlaceholderText("Cliente Selecionado")
        self.cliente_input.setReadOnly(True)  # Make it read-only
        layout.addWidget(self.cliente_input)

        self.quantidade_entry = QtWidgets.QLineEdit()
        self.quantidade_entry.setPlaceholderText("Quantidade")
        layout.addWidget(self.quantidade_entry)

        # Button to add product to budget
        self.btn_adicionar_orcamento = QtWidgets.QPushButton("Adicionar Produto ao Orçamento")
        self.btn_adicionar_orcamento.setStyleSheet("background-color: #007BFF; color: white;")  # Blue button
        self.btn_adicionar_orcamento.clicked.connect(self.adicionar_produto_orcamento)
        layout.addWidget(self.btn_adicionar_orcamento)

        # List to display added products
        self.produtos_adicionados_list = QtWidgets.QListWidget()
        layout.addWidget(self.produtos_adicionados_list)

        # Button to remove selected product from budget
        self.btn_remover_orcamento = QtWidgets.QPushButton("Remover Produto do Orçamento")
        self.btn_remover_orcamento.setStyleSheet("background-color: #007BFF; color: white;")  # Blue button
        self.btn_remover_orcamento.clicked.connect(self.remover_produto_orcamento)
        layout.addWidget(self.btn_remover_orcamento)

        self.vendedor_entry = QtWidgets.QLineEdit()
        self.vendedor_entry.setPlaceholderText("Vendedor")
        layout.addWidget(self.vendedor_entry)

        self.forma_pagamento_entry = QtWidgets.QLineEdit()
        self.forma_pagamento_entry.setPlaceholderText("Forma de Pagamento")
        layout.addWidget(self.forma_pagamento_entry)

        self.condicao_pagamento_entry = QtWidgets.QLineEdit()
        self.condicao_pagamento_entry.setPlaceholderText("Condição de Pagamento")
        layout.addWidget(self.condicao_pagamento_entry)

        self.limite_credito_utilizado_entry = QtWidgets.QLineEdit()
        self.limite_credito_utilizado_entry.setPlaceholderText("Limite Crédito Utilizado")
        layout.addWidget(self.limite_credito_utilizado_entry)

        self.limite_credito_disponivel_entry = QtWidgets.QLineEdit()
        self.limite_credito_disponivel_entry.setPlaceholderText("Limite Crédito Disponível")
        layout.addWidget(self.limite_credito_disponivel_entry)

        # Generate PDF button
        self.btn_gerar_pdf = QtWidgets.QPushButton("Gerar Orçamento")
        self.btn_gerar_pdf.setStyleSheet("background-color: #007BFF; color: white;")  # Blue button
        self.btn_gerar_pdf.clicked.connect(self.gerar_pdf)
        layout.addWidget(self.btn_gerar_pdf)

        # Stretch to fill space
        layout.addStretch()

    def carregar_dados(self):
        """Carrega os dados de produtos e clientes do arquivo JSON."""
        if os.path.exists(self.arquivo_dados):
            with open(self.arquivo_dados, 'r') as arquivo:
                dados = json.load(arquivo)
                self.produtos = dados.get("produtos", [])
                self.clientes = dados.get("clientes", [])
        
        # Atualizar as listas e comboboxes
        self.atualizar_combobox_orcamento()

    def atualizar_combobox_orcamento(self):
        self.produto_combobox.clear()
        self.produto_combobox.addItems([produto.get('descricao', 'Descrição não disponível') for produto in self.produtos])
        
        # Populate the client search field
        self.cliente_search.clear()
        self.cliente_input.clear()

    def mostrar_produtos_registrados(self):
        """Show all registered products in a new window."""
        dialog = ProdutosDialog(self.produtos, self.edit_product, self.delete_product)
        dialog.exec_()  # Open the dialog

    def mostrar_clientes_registrados(self):
        """Show all registered clients in a new window."""
        dialog = ClientesDialog(self.clientes, self.edit_client, self.delete_client)
        dialog.exec_()  # Open the dialog

    def edit_product(self, product_name):
        """Edit the selected product."""
        # Find the product and populate the fields for editing
        for produto in self.produtos:
            if produto["descricao"] == product_name:
                self.produto_desc.setText(produto["descricao"])
                self.produto_vlr_m.setText(str(produto.get("vlr_m", "")))  # Get the value per meter
                break

    def delete_product(self, product_name):
        """Delete the selected product."""
        self.produtos = [produto for produto in self.produtos if produto["descricao"] != product_name]
        self.salvar_dados()

    def edit_client(self, client_name):
        """Edit the selected client."""
        # Find the client and populate the fields for editing
        for cliente in self.clientes:
            if cliente["nome"] == client_name:
                self.cliente_nome.setText(cliente["nome"])
                self.cliente_numero.setText(cliente["numero"])
                self.cliente_cpf.setText(cliente["cpf_cnpj"])
                self.cliente_endereco.setText(cliente["endereco"])
                self.cliente_cidade.setText(cliente["cidade"])
                self.cliente_telefone.setText(cliente["telefone"])
                break

    def delete_client(self, client_name):
        """Delete the selected client."""
        self.clientes = [cliente for cliente in self.clientes if cliente["nome"] != client_name]
        self.salvar_dados()

    def adicionar_produto(self):
        descricao = self.produto_desc.text()
        try:
            vlr_m = float(self.produto_vlr_m.text())  # Get the value per meter
            if not descricao or vlr_m <= 0:
                raise ValueError("Preencha os campos corretamente!")

            self.produtos.append({"descricao": descricao, "vlr_m": vlr_m})  # Store description and value per meter
            self.atualizar_combobox_orcamento()
            self.produto_desc.clear()
            self.produto_vlr_m.clear()  # Clear value per meter input

            self.salvar_dados()
            QtWidgets.QMessageBox.information(self, "Sucesso", "Produto adicionado com sucesso!")
        except ValueError as e:
            QtWidgets.QMessageBox.warning(self, "Erro", f"Entrada inválida: {e}")

    def adicionar_cliente(self):
        nome = self.cliente_nome.text()
        cpf = self.cliente_cpf.text()
        endereco = self.cliente_endereco.text()
        cidade = self.cliente_cidade.text()
        telefone = self.cliente_telefone.text()

        if not nome or not cpf or not endereco or not cidade or not telefone:
            QtWidgets.QMessageBox.warning(self, "Erro", "Preencha todos os campos para adicionar um cliente!")
            return

        self.clientes.append({
            "nome": nome,
            "cpf_cnpj": cpf,
            "endereco": endereco,
            "cidade": cidade,
            "telefone": telefone
        })
        
        self.atualizar_combobox_orcamento()
        self.cliente_nome.clear()
        self.cliente_cpf.clear()
        self.cliente_endereco.clear()
        self.cliente_cidade.clear()
        self.cliente_telefone.clear()

        self.salvar_dados()
        QtWidgets.QMessageBox.information(self, "Sucesso", "Cliente adicionado com sucesso!")

    def adicionar_produto_orcamento(self):
        """Add selected product to the budget list."""
        produto_desc = self.produto_combobox.currentText()
        produto_tam = self.produto_tamanho.text()
        quantidade = self.quantidade_entry.text()

        if not produto_desc or not produto_tam or not quantidade:
            QtWidgets.QMessageBox.warning(self, "Erro", "Preencha todos os campos para adicionar um produto ao orçamento!")
            return

        # Get the value per meter for the selected product
        vlr_m = next((p["vlr_m"] for p in self.produtos if p["descricao"] == produto_desc), 0)
        total = vlr_m * float(produto_tam) * int(quantidade)  # Calculate total based on quantity and unit price

        # Add product details to the list
        self.produtos_adicionados_list.addItem(f"{produto_desc} - {produto_tam}M - Qtd: {quantidade} - Vlr. M: R$ {vlr_m:.2f} - Total: R$ {total:.2f}")
        self.orcamento_produtos.append({
            "descricao": produto_desc,
            "tamanho": produto_tam,
            "quantidade": quantidade,
            "vlr_m": vlr_m,
            "total": total
        })

        # Clear inputs
        self.produto_combobox.setCurrentIndex(-1)
        self.produto_tamanho.clear()
        self.quantidade_entry.clear()

    def remover_produto_orcamento(self):
        """Remove selected product from the budget list."""
        selected_items = self.produtos_adicionados_list.selectedItems()
        if selected_items:
            for item in selected_items:
                row = self.produtos_adicionados_list.row(item)
                self.produtos_adicionados_list.takeItem(row)  # Remove from list widget
                del self.orcamento_produtos[row]  # Remove from the budget list
        else:
            QtWidgets.QMessageBox.warning(self, "Erro", "Selecione um produto para remover!")

    def search_client(self):
        """Search for clients starting with the entered text."""
        search_text = self.cliente_search.text().strip()
        if not search_text:
            return

        matching_clients = [cliente for cliente in self.clientes if cliente["nome"].startswith(search_text)]
        
        if len(matching_clients) == 1:
            # If only one match, automatically select it
            selected_client = matching_clients[0]['nome']
            self.cliente_input.setText(selected_client)  # Set the selected client in the input field
            QtWidgets.QMessageBox.information(self, "Cliente Selecionado", f"Cliente selecionado: {selected_client}")
        elif len(matching_clients) > 1:
            # If multiple matches, show them in a dialog
            dialog = QtWidgets.QDialog(self)
            dialog.setWindowTitle("Clientes Encontrados")
            dialog.setGeometry(200, 200, 300, 200)
            layout = QtWidgets.QVBoxLayout(dialog)

            clientes_list = QtWidgets.QListWidget()
            for cliente in matching_clients:
                clientes_list.addItem(cliente["nome"])
            layout.addWidget(clientes_list)

            btn_select = QtWidgets.QPushButton("Selecionar Cliente")
            btn_select.clicked.connect(lambda: self.select_client(clientes_list.selectedItems(), dialog))
            layout.addWidget(btn_select)

            dialog.exec_()  # Open the dialog

    def select_client(self, selected_items, dialog):
        """Select a client from the list."""
        if selected_items:
            selected_client = selected_items[0].text()
            self.cliente_input.setText(selected_client)  # Set the selected client in the input field
            QtWidgets.QMessageBox.information(self, "Cliente Selecionado", f"Cliente selecionado: {selected_client}")
            dialog.accept()  # Close the dialog

    def gerar_pdf(self):
        try:
            # Coletar dados do cliente
            cliente_nome = self.cliente_input.text()
            cliente = next((c for c in self.clientes if c["nome"] == cliente_nome), None)

            if cliente is None:
                QtWidgets.QMessageBox.warning(self, "Erro", "Selecione um cliente válido!")
                return

            cliente_endereco = cliente["endereco"]
            cliente_cidade = cliente["cidade"]
            cliente_cpf = cliente["cpf_cnpj"]
            cliente_telefone = cliente["telefone"]

            # Criar PDF
            pdf = FPDF(orientation='L', unit='mm', format=(500, 350))  # Landscape orientation
            pdf.add_page()
            pdf.set_font("Arial", size=10)

            # Cabeçalho
            pdf.set_font("Arial", style="B", size=12)
            pdf.cell(0, 5, "TICKET DE VENDA", ln=True, align="C")
            pdf.set_font("Arial", size=10)
            pdf.cell(0, 5, "TIGELA MADEIRAS E ARTEFATOS LTDA", ln=True, align="C")
            pdf.cell(0, 5, "TIGELA MADEIREIRA E ARTEFATOS", ln=True, align="C")
            pdf.cell(0, 5, "Telefone: (44) 9754-8463 - Celular:", ln=True, align="C")
            pdf.cell(0, 5, "Endereco: AVENIDA BRASIL, No 1621, DISTRITO CASA BRANCA, XAMBRE - PR", ln=True, align="C")
            pdf.cell(0, 5, "CNPJ: 39.594.567/0001-79    IE: 9086731905", ln=True, align="C")
            pdf.ln(5)

            # Dados do cliente
            pdf.set_font("Arial", style="", size=10)
            pdf.cell(0, 5, f"Cliente: {cliente_nome}", ln=True)
            pdf.cell(0, 5, f"Endereco: {cliente_endereco}", ln=True)
            pdf.cell(0, 5, f"Cidade: {cliente_cidade}", ln=True)
            pdf.cell(0, 5, f"CPF/CNPJ: {cliente_cpf}", ln=True)
            pdf.cell(0, 5, f"Telefone: {cliente_telefone}", ln=True)
            pdf.ln(5)

            # Tabela de produtos
            pdf.set_fill_color(200, 200, 200)
            pdf.cell(10, 7, txt="N\u00ba", border=1, align="C", fill=True)
            pdf.cell(80, 7, txt="Produto", border=1, align="C", fill=True)
            pdf.cell(30, 7, txt="Un. Com.", border=1, align="C", fill=True)  # Add "Un. Com." column
            pdf.cell(30, 7, txt="Vlr. Frete", border=1, align="C", fill=True)
            pdf.cell(30, 7, txt="Vlr. Outros", border=1, align="C", fill=True)
            pdf.cell(30, 7, txt="Vlr. Seguro", border=1, align="C", fill=True)
            pdf.cell(20, 7, txt="Qtd", border=1, align="C", fill=True)  # Quantity
            pdf.cell(20, 7, txt="Vlr. M.", border=1, align="C", fill=True)  # Add "Vlr. M." column
            pdf.cell(30, 7, txt="Vlr UN.", border=1, align="C", fill=True)  # Unit Price
            pdf.cell(30, 7, txt="Vlr Total", border=1, align="C", fill=True)  # Total
            pdf.ln()

            total_final = 0  # Initialize total

            # Loop through added products and add to PDF
            for index, produto in enumerate(self.orcamento_produtos):
                produto_desc = produto["descricao"]
                produto_tam = produto["tamanho"]
                quantidade = produto["quantidade"]
                vlr_m = next((p["vlr_m"] for p in self.produtos if p["descricao"] == produto_desc), 0)
                vlr_un = vlr_m * float(produto_tam)  # Calculate unit price
                total = int(quantidade) * vlr_un  # Calculate total based on quantity and unit price

                # Preenchendo produtos com o novo formato
                pdf.cell(10, 7, txt=str(index + 1), border=1, align="C")
                pdf.cell(80, 7, txt=f"{produto_desc} - {produto_tam}M", border=1, align="L")  # Concatenate description and size
                pdf.cell(30, 7, txt="UNID", border=1, align="C")  # Display "Un. Com."
                pdf.cell(30, 7, txt="R$ 00,00", border=1, align="C")
                pdf.cell(30, 7, txt="R$ 00,00", border=1, align="C")
                pdf.cell(30, 7, txt="R$ 00,00", border=1, align="C")
                pdf.cell(20, 7, txt=str(quantidade), border=1, align="C")  # Display quantity
                pdf.cell(20, 7, txt=f"R$ {vlr_m:.2f}", border=1, align="C")  # Display value per meter
                pdf.cell(30, 7, txt=f"R$ {vlr_un:.2f}", border=1, align="C")  # Display unit price
                pdf.cell(30, 7, txt=f"R$ {total:.2f}", border=1, align="C")  # Display total
                pdf.ln(10)

                total_final += total  # Add to final total

            # Totais e informações adicionais
            pdf.cell(17, 5, txt=f"Vendedor:", border=0, align="L")
            pdf.cell(29, 5, txt="", border=0)# Espaço vazio
            pdf.cell(30, 5, txt=f"{self.vendedor_entry.text()}", border=0, align="L")
            pdf.cell(130, 5, txt="", border=0)# Espaço vazio
            pdf.cell(30, 5, txt=f"Outros:", border=0, align="L")
            pdf.cell(30, 5, txt=f"R$ 00.00", border=0, align="L")
            pdf.cell(30, 5, txt=f"Total:", border=0, align="L")  # Total at the end
            pdf.cell(10, 5, txt=f"R$ {total_final:.2f}", border=0, align="L")
            pdf.ln(6)
            
            pdf.cell(36, 5, txt=f"Forma de Pagamento:", border=0, align="L")
            pdf.cell(10, 5, txt="", border=0)# Espaço vazio
            pdf.cell(30, 5, txt=f"{self.forma_pagamento_entry.text()}", border=0, align="L")
            pdf.cell(130, 5, txt="", border=0)# Espaço vazio
            pdf.cell(30, 5, txt=f"Seguro:", border=0, align="L")
            pdf.cell(30, 5, txt=f"R$ 00.00", border=0, align="L")
            pdf.cell(30, 5, txt=f"Acréscimos:", border=0, align="L")  # Total at the end
            pdf.cell(10, 5, txt=f"R$ 00.00", border=0, align="L")
            pdf.ln(6)
            
            pdf.cell(43, 5, txt=f"Limite de Crédito Utilizado:", border=0, align="L")
            pdf.cell(3, 5, txt="", border=0)# Espaço vazio
            pdf.cell(30, 5, txt=f"R$ {self.limite_credito_utilizado_entry.text()}", border=0, align="L")
            pdf.cell(190, 5, txt="", border=0)# Espaço vazio
            pdf.cell(30, 5, txt=f"Total Líquido:", border=0, align="L")  # Total at the end
            pdf.cell(10, 5, txt=f"R$ 00.00", border=0, align="L")
            pdf.ln(6)

            
            pdf.cell(43, 5, txt=f"Limite de Crédito Disponivel:", border=0, align="L")
            pdf.cell(3, 5, txt="", border=0)# Espaço vazio
            pdf.cell(30, 5, txt=f"R$ {self.limite_credito_disponivel_entry.text()}", border=0, align="L")
            pdf.ln(6)
            
            pdf.set_font("Arial", style="B", size=10)
            pdf.cell(40, 5, "Composição Pgto", border=0, align="L")
            pdf.cell(30, 5, "Parcela", border=0, align="L")
            pdf.cell(50, 5, "Numerário", border=0, align="L")
            pdf.cell(30, 5, "Valor", border=0, align="L")
            pdf.cell(30, 5, "Data Pgto", border=0, align="L")
            pdf.ln()
            
            pdf.set_font("Arial", size=10)
            pdf.cell(40, 5, "", border=0, align="L")  # Empty space for "Composição Pgto"
            pdf.cell(30, 5, "1", border=0, align="L")  # Parcela
            pdf.cell(50, 5, "Dinheiro", border=0, align="L")  # Numerário
            pdf.cell(30, 5, f"R$ {total_final:.2f}", border=0, align="L")  # Valor
            pdf.cell(30, 5, datetime.now().strftime("%d/%m/%Y"), border=0, align="L")
            
            
            # Observações
            pdf.ln(10)
            pdf.cell(0, 5, txt="Observacoes:", ln=True)
            pdf.cell(0, 5, txt="- Voce pagou aproximadamente: R$ 00,00 de tributos estaduais.", ln=True)
            pdf.cell(0, 5, txt="  R$ 00,00 de tributos federais. Fonte: IBPT.", ln=True)

            # Salvar PDF
            nome_pdf = "Ticket_Venda_Exemplo.pdf"
            pdf.output(nome_pdf)

            # Abrir PDF automaticamente
            os.startfile(nome_pdf)

            QtWidgets.QMessageBox.information(self, "Sucesso", f"PDF gerado com sucesso: {nome_pdf}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao gerar o PDF: {str(e)}")

    def salvar_dados(self):
        """Salva os dados de produtos e clientes no arquivo JSON."""
        dados = {
            "produtos": self.produtos,
            "clientes": self.clientes
        }
        with open(self.arquivo_dados, 'w') as arquivo:
            json.dump(dados, arquivo, indent=4)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    welcome_screen = WelcomeScreen()
    welcome_screen.show()  # Show the welcome screen
    sys.exit(app.exec_())