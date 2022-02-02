
![Docker](https://github.com/dadosjusbr/coletor-mppr/actions/workflows/docker-publish.yml/badge.svg)    
[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/dadosjusbr/coletor-mppr)

# Ministério Público de Minas Gerais

Este coletor tem como objetivo a recuperação de informações sobre folhas de pagamentos dos funcionários do Ministério Público do Estado do Paraná. O site com as informações pode ser acessado [aqui](http://www2.mppr.mp.br/sis/ext/mem/indfolha.html).

O crawler está estruturado como uma CLI. É necessário passar os argumentos mês, ano e caminho para armazenar os arquivos via variáveis de ambiente (`MONTH`, `YEAR`, `OUTPUT_FOLDER`). E então, serão baixadas as planilhas, no formato `.ods`. As mesmas são correpondentes a remuneração mensal e verbas indenizatórias dos Membros Ativos.

# Dicionário de dados
As planilhas referentes á remunerações possuem as seguintes colunas:
|Campo|Descrição|
|-|-|
|**Matrícula (Number)**|Nome completo do funcionário|
|**Nome (String)**|Nome completo do funcionário|
|**Cargo (String)**|Cargo do funcionário dentro do MP|
|**Lotação (String)**|Local (cidade, departamento, promotoria) em que o funcionário trabalha|
|**Sit. * (String)**|Descrição situacional do funcionário, encontra-se em licença, férias ...|
|**Remuneração do cargo efetivo (Number)**|Vencimento, GAMPU, V.P.I, Adicionais de Qualificação, G.A.E e G.A.S, além de outras desta natureza. Soma de todas essas remunerações|
|**Outras Verbas Remuneratórias, Legais ou  Judiciais (Number)**|V.P.N.I., Adicional por tempo de serviço, quintos, décimos e vantagens decorrentes de sentença judicial ou extensão administrativa|
|**Função de confiança ou cargo em comissão (Number)**|Rubricas que representam a retribuição paga pelo exercício de função (servidor efetivo) ou remuneração de cargo em comissão (servidor sem vínculo ou requisitado)|
|**Gratificação natalina (Number)**|Parcelas da Gratificação Natalina (13º) pagas no mês corrente, ou no caso de vacância ou exoneração do servidor|
|**Férias - ⅓ Constitucional (Number)**|Adicional correspondente a 1/3 (um terço) da remuneração, pago ao servidor por ocasião das férias|
|**Abono de permanência (Number)**| Valor equivalente ao da contribuição previdenciária, devido ao funcionário público que esteja em condição de aposentar-se, mas que optou por continuar em atividade (instituído pela Emenda Constitucional nº 41, de 16 de dezembro de 2003)|
|**Total de Rendimentos Brutos (Number)**|Total dos rendimentos brutos pagos no mês.|
|**Contribuição Previdenciária (Number)**|Contribuição Previdenciária|
|**Imposto de Renda (Number)**|Imposto de Renda Retido na Fonte|
|**Retenção por Teto Constitucional (Number)**|Valor deduzido da remuneração bruta, quando esta ultrapassa o teto constitucional, de acordo com a Resolução nº 09/2006 do CNMP|
|**Total de Descontos (Number)**|Soma dos descontos referidos nos itens 8, 9 e 10|
|**Total Líquido (Number)**|Rendimento obtido após o abatimento dos descontos referidos no item 11. O valor líquido efetivamente recebido pelo membro ou servidor pode ser inferior ao ora divulgado, porque não são considerados os descontos de caráter pessoal|
|**Indenizações (Number)**|Verbas referentes á indenizações recebidas pelo funcionario á titulo de Adicional noturno, Cumulações, Serviços extraordinários e substituição de função|
|**Outras Remunerações Temporárias (Number)**|Valores pagos a título de Auxílio-alimentação, Auxílio-cursos,Auxílio-Saúde, Auxílio-creche, Auxílio-moradia|


As planilhas referentes á verbas indenizatórias e remunerações temporárias possuem as seguintes colunas:
|Campo|Descrição|
|-|-|
|**Auxílio Alimentação (Number)**||
|**Aux. Saúde**||
|**Aux. Pré Escolar**||
|**Aux. Cursos**||
|**Aux. Moradia**||
|**Adic. Noturno**||
|**Serviço Extraor.**||
|**Subst. de Função**||
|**Cumulações**||

# Dificuldades na libertação de dados: 
- A pagina do ministério oferece as planilhas referentes á verbas indenizatórias e remunerações simples em seções diferentes, sendo necessário selecionar o periodo de tempo referente a cada uma delas para esclarecimento e compreensão dos dados.


## Como usar

 ### Executando com Docker

 - Inicialmente é preciso instalar o [Docker](https://docs.docker.com/install/). 

 - Construção da imagem:

    ```sh
    cd coletores/mppr
    sudo docker build -t mppr .
    ```
 - Execução:
 
    ```sh
    sudo docker run -e MONTH=02 -e YEAR=2020 -e GIT_COMMIT=$(git rev-list -1 HEAD) mppr 
    ```

 ### Executando sem Docker

 - É necessário ter instalado o [Python](https://www.python.org/downloads/release/python-385/) versão 3.8.5;
 
No Linux, distribuições Ubuntu/Mint:

```
sudo apt install python3 python3-pip
```

 - Utilize o PiP (foi utilizada a versão 20.3.3) para instalar as dependências que estão listadas no arquivo requirements.txt.
  
    ```sh
      $ cd coletores/mppr
      $ pip3 install -r requirements.txt
    ```

  - Após concluida a instalação das dependências utilize os seguintes comandos:  

   ```sh
      $ cd src
      $ MONTH=01 YEAR=2020 GIT_COMMIT=$(git rev-list -1 HEAD) python3 main.py
