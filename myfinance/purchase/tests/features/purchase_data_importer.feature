# language: pt

@browser

Funcionalidade: Importar dados de vendas

    Contexto: 
        Dado que eu acesso o formulario de importacao


    Cenário: Operacao realizada com sucesso

        Dado que eu faco o upload de um arquivo
        Quando eu pressiono o botao importar
        Então eu devo ver "Importacao efetuada com sucesso"
        E todos os dados do arquivo devem estar armazenados em banco de dados
        E eu devo ver a receita bruta total representada pelo arquivo enviado
