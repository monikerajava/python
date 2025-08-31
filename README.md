# python
Projetos em Python

Materiais Complementares
Nossos materiais complementares e de apoio têm como objetivo apresentar informações para facilitar e enriquecer a sua jornada de aprendizado. Para isso, links úteis (como slides, repositórios e páginas oficiais) serão disponibilizados, além de dicas sobre como se destacar na DIO e no mercado de trabalho 😉

Slides
Data e hora.pptx
https://hermes.dio.me/files/assets/c963d627-de97-4405-b3ac-0eb58eea2e18.pptx

Desafio.pptx
https://hermes.dio.me/files/assets/c1bfe741-b162-4623-a697-1c28c7e57774.pptx


##Modelando o Sistema Bancário em POO com Python

Neste desafio iremos atualizar a implementação do sistema bancário, para armazenar os dados de clientes e contas bancárias em objetos ao invés de dicionários. O código deve seguir o modelo de classes UML.

Referências:
1) Repositório Git
https://github.com/digitalinnovationone/trilha-python-dio/blob/main/01%20-%20Estrutura%20de%20dados/desafio.py

2) Imagem de referência
http://academiapme-my.sharepoint.com/:i:/g/personal/renato_dio_me/EWlnaqvFAAZKmHaBBfA17-oBfb5pTrzoELam7dSgtOA7uQ?e=5UskS9


Meu projeto : 

diagrama UML:

                        +-------------------+
                        |     Cliente       |
                        +-------------------+
                        | - endereco        |
                        | - contas: list    |
                        +-------------------+
                        | + vincular_conta()|
                        | + executar_trans..|
                        +-------------------+
                                  ^
                                  |
                +---------------------------------+
                |         PessoaFisica            |
                +---------------------------------+
                | - nome                          |
                | - nascimento                    |
                | - cpf                           |
                +---------------------------------+


                        +-------------------+
                        |       Conta       |
                        +-------------------+
                        | - agencia         |
                        | - numero          |
                        | - saldo           |
                        | - cliente         |
                        | - historico       |
                        +-------------------+
                        | + sacar()         |
                        | + depositar()     |
                        | + criar_conta()   |
                        +-------------------+
                                  ^
                                  |
                +----------------------------------+
                |        ContaCorrente             |
                +----------------------------------+
                | - limite                         |
                | - max_saques                     |
                +----------------------------------+
                | + sacar()                        |
                +----------------------------------+

                        +-------------------+
                        |     Historico     |
                        +-------------------+
                        | - transacoes      |
                        +-------------------+
                        | + registrar()     |
                        +-------------------+

                        +-------------------+
                        |    Transacao      |<<abstract>>
                        +-------------------+
                        | + valor           |
                        +-------------------+
                        | + registrar()     |
                        +-------------------+
                             ^          ^
                             |          |
             +----------------+     +----------------+
             |    Saque       |     |   Deposito     |
             +----------------+     +----------------+
             | - valor        |     | - valor        |
             +----------------+     +----------------+
             | + registrar()  |     | + registrar()  |
             +----------------+     +----------------+

