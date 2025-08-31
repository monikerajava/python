import textwrap
from abc import ABC, abstractmethod
from datetime import datetime


# ============================
# Classes de Clientes
# ============================
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def vincular_conta(self, conta):
        self.contas.append(conta)

    def executar_transacao(self, conta, transacao):
        transacao.registrar(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.nascimento = nascimento
        self.cpf = cpf


# ============================
# Classes de Conta
# ============================
class Conta:
    def __init__(self, numero, cliente):
        self._agencia = "0001"
        self._numero = numero
        self._saldo = 0
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def criar_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        if valor <= 0:
            print("\n@@@ Valor inválido para saque! @@@")
            return False

        if valor > self._saldo:
            print("\n@@@ Saldo insuficiente! @@@")
            return False

        self._saldo -= valor
        print("\n=== Saque realizado com sucesso! ===")
        return True

    def depositar(self, valor):
        if valor <= 0:
            print("\n@@@ Valor inválido para depósito! @@@")
            return False

        self._saldo += valor
        print("\n=== Depósito efetuado com sucesso! ===")
        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, max_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._max_saques = max_saques

    def sacar(self, valor):
        saques_realizados = len([t for t in self.historico.transacoes if t["tipo"] == "Saque"])

        if valor > self._limite:
            print("\n@@@ Saque acima do limite permitido! @@@")
            return False

        if saques_realizados >= self._max_saques:
            print("\n@@@ Limite de saques diários atingido! @@@")
            return False

        return super().sacar(valor)

    def __str__(self):
        return f"""
        Agência:\t{self.agencia}
        Conta:\t\t{self.numero}
        Titular:\t{self.cliente.nome}
        """


# ============================
# Classes de Transações
# ============================
class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def registrar(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            }
        )


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.registrar(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.registrar(self)


# ============================
# Funções do Sistema
# ============================
def menu():
    opcoes = """\n
    ======== MENU PRINCIPAL ========
    [d]  Depositar
    [s]  Sacar
    [e]  Extrato
    [nu] Novo cliente
    [nc] Nova conta
    [lc] Listar contas
    [q]  Sair
    => """
    return input(textwrap.dedent(opcoes))


def localizar_cliente(cpf, clientes):
    filtrados = [c for c in clientes if c.cpf == cpf]
    return filtrados[0] if filtrados else None


def selecionar_conta(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui contas! @@@")
        return None
    # neste modelo, pega sempre a primeira conta
    return cliente.contas[0]


def operacao_deposito(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = localizar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor para depósito: "))
    transacao = Deposito(valor)

    conta = selecionar_conta(cliente)
    if conta:
        cliente.executar_transacao(conta, transacao)


def operacao_saque(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = localizar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor para saque: "))
    transacao = Saque(valor)

    conta = selecionar_conta(cliente)
    if conta:
        cliente.executar_transacao(conta, transacao)


def mostrar_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = localizar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = selecionar_conta(cliente)
    if not conta:
        return

    print("\n======= EXTRATO =======")
    if not conta.historico.transacoes:
        print("Não houve movimentações.")
    else:
        for t in conta.historico.transacoes:
            print(f"{t['data']} - {t['tipo']}: R$ {t['valor']:.2f}")

    print(f"\nSaldo atual: R$ {conta.saldo:.2f}")
    print("=========================")


def criar_cliente(clientes):
    cpf = input("CPF (apenas números): ")
    if localizar_cliente(cpf, clientes):
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Nome completo: ")
    nascimento = input("Data de nascimento (dd/mm/aaaa): ")
    endereco = input("Endereço (logradouro, nro - bairro - cidade/UF): ")

    novo = PessoaFisica(nome, nascimento, cpf, endereco)
    clientes.append(novo)
    print("\n=== Cliente criado com sucesso! ===")


def criar_conta(clientes, contas):
    cpf = input("Informe o CPF do titular: ")
    cliente = localizar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! Utilize primeiro a opção criar cliente @@@")
        return

    numero = len(contas) + 1
    conta = ContaCorrente.criar_conta(cliente, numero)
    contas.append(conta)
    cliente.vincular_conta(conta)

    print("\n=== Conta aberta com sucesso! ===")


def listar_contas(contas):
    for conta in contas:
        print("=" * 60)
        print(textwrap.dedent(str(conta)))


# ============================
# Main Loop
# ============================
def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            operacao_deposito(clientes)
        elif opcao == "s":
            operacao_saque(clientes)
        elif opcao == "e":
            mostrar_extrato(clientes)
        elif opcao == "nu":
            criar_cliente(clientes)
        elif opcao == "nc":
            criar_conta(clientes, contas)
        elif opcao == "lc":
            listar_contas(contas)
        elif opcao == "q":
            print("\nObrigado por utilizar o sistema bancário!")
            break
        else:
            print("\n@@@ Opção inválida, tente novamente. @@@")


if __name__ == "__main__":
    main()
