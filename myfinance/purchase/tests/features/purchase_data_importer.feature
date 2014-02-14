# language: pt

@browser

Funcionalidade: Importar dados de vendas

    Contexto: 
        Dado que eu acesso o formulário de importação


    Cenário: Operação realizada com sucesso

        Dado que eu faço o upload de um arquivo
        Quando eu pressiono o botão importar
        Então eu devo ver "Importação realizada com sucesso"
