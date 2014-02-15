# language: pt

@browser

Funcionalidade: Importar dados de vendas

    Contexto: 
        Dado que eu acesso o formulario de importacao


    Cenário: Operacao realizada com sucesso

        Dado que eu faco o upload de um arquivo
        Quando eu pressiono o botao importar
        Então eu devo ver "Importacao realizada com sucesso"
