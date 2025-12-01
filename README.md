<h1>Trabalho Python – Sistema de Transporte de Passageiros</h1>

<h2>Como executar</h2>

<p>Para executar o sistema, é necessário ter <strong>Python 3</strong> instalado.<br>
Dentro da pasta onde estão os arquivos do projeto, utilize o comando:</p>

<pre>
<code>python sistema_de_transporte.py</code>
</pre>

<p>O sistema funciona inteiramente pelo terminal, sem necessidade de bibliotecas externas.</p>


<h2>Descrição Geral</h2>

<p>
Este projeto implementa um <strong>Sistema de Transporte de Passageiros</strong>, desenvolvido como parte da disciplina
<strong>Programação em Python</strong> (CEFET-MG).
O sistema permite cadastrar linhas, consultar horários, verificar assentos, realizar reservas automáticas
e manuais, além de gerar relatórios detalhados.
</p>

<p>O projeto foca no uso de:</p>

<ul>
    <li>Estruturas condicionais e repetição</li>
    <li>Manipulação de arquivos texto</li>
    <li>Funções e modularização</li>
    <li>Tratamento de exceções</li>
    <li>Dicionários, listas e matrizes</li>
    <li>Controle de vendas e ocupação</li>
</ul>


<h2>Funcionalidades do Sistema</h2>

<h3>1. Cadastro de Linhas</h3>
<p>Gerencia as linhas disponíveis:</p>
<ul>
    <li>Inserir linha</li>
    <li>Remover linha</li>
    <li>Alterar linha</li>
</ul>

<h3>2. Listar Linhas Cadastradas</h3>
<p>Mostra todas as linhas no formato:</p>

<pre>
ID: Origem → Destino | Horário | Preço
</pre>

<h3>3. Consultar Horários Disponíveis</h3>
<p>Permite consultar todas as linhas que saem de uma cidade específica.</p>

<h3>4. Consultar Assentos Disponíveis + Reserva Manual</h3>
<p>
Mostra o mapa de assentos do ônibus e permite reservar manualmente.<br>
Inclui validações obrigatórias:
</p>

<ul>
    <li>Não permite reservar datas passadas</li>
    <li>Não permite datas acima de 30 dias</li>
    <li>Se a data for hoje, verifica se o ônibus já saiu</li>
</ul>

<p>O ônibus é criado automaticamente caso ainda não exista para aquela data.</p>

<h3>5. Reserva Automática</h3>
<p>O sistema escolhe automaticamente um dos assentos livres e registra a reserva.</p>

<h3>6. Relatórios</h3>

<ul>
    <li><strong>6.1 – Faturamento mensal por linha</strong> (tela ou arquivo)</li>
    <li><strong>6.2 – Ocupação média por dia da semana</strong></li>
    <li><strong>6.3 – Relatório de erros</strong></li>
</ul>

<p>Arquivos gerados:</p>
<ul>
    <li>relatorio_faturamento.txt</li>
    <li>relatorio_ocupacao.txt</li>
    <li>relatorio_erros.txt</li>
</ul>

<h3>7. Ler Reservas de Arquivo Texto</h3>

<p>O sistema lê arquivos no formato:</p>

<pre>
CIDADE, HORÁRIO, DATA, ASSENTO
</pre>

<p>Para cada linha, o sistema:</p>
<ul>
    <li>Procura a linha correta</li>
    <li>Valida data e horário</li>
    <li>Cria o ônibus da data se necessário</li>
    <li>Verifica assento</li>
    <li>Registra venda se válido</li>
    <li>Salva erro no arquivo se inválido</li>
</ul>

<h3>0. Sair</h3>
<p>Encerra o sistema.</p>


<h2>Exemplo – Mapa de Assentos</h2>

<pre>
[01] [02]  |     |  [04] [03]
[05] [06]  |     |  [08] [07]
[09] [10]  |     |  [12] [11]
[13] [14]  |     |  [16] [15]
[17] [18]  |     |  [20] [19]

[nn] = assento livre
[XX] = assento ocupado
</pre>


<h2>Arquivos do Sistema</h2>

<ul>
    <li>cadastro.py</li>
    <li>consultarhorarios.py</li>
    <li>consultarassentos.py</li>
    <li>reservarassento.py</li>
    <li>relatorios.py</li>
    <li>sistema_de_transporte.py (arquivo principal)</li>
</ul>


<h2>Conclusão</h2>

<p>
O sistema implementa uma solução funcional e modular de transporte rodoviário, cumprindo os requisitos:
</p>

<ul>
    <li>Manipulação completa de linhas</li>
    <li>Controle de assentos por data</li>
    <li>Reservas automáticas e manuais</li>
    <li>Relatórios variados</li>
    <li>Registro de vendas e erros</li>
    <li>Processamento de arquivo externo</li>
</ul>

<h3>Limitações</h3>
<ul>
    <li>Interface exclusivamente textual</li>
    <li>Não usa banco de dados</li>
    <li>Estrutura de assentos fixa em 20 lugares</li>
    <li>Dados não persistem após encerrar o programa</li>
</ul>


<h2>Desenvolvedores</h2>

<p>
<strong>Bernardo Lebron</strong><br>
<strong>Pedro Araújo</strong><br>
Estudantes de Engenharia de Computação – CEFET-MG
</p>
