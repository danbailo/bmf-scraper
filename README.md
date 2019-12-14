# Scraper BMF

## Descrição
Este projeto consiste em coletar os dados do site http://www2.bmf.com.br/pages/portal/bmfbovespa/lumis/lum-tipo-de-participante-enUS.asp a partir de um intervalo de data determinado pelo usuário. Os dados que serão coletados também dependem dos contratos que o usuário escrever no arquivo [contract.txt](filters/contract.txt), ou seja, os dados que serão coletados serão filtrados por meio deste arquivo. Após a coleta, os dados serão gravados em arquivos **.csv**, cada arquivo será separado por contrato(que foram escritos no filtro) e estes serão salvos por padrão no diretório [csv/](csv/) e dentro deste, há uma pasta nomeada de *ACCUMULATED*, nesta pasta também contem arquivos .csv, contendo o saldo acumulado desde a data inicial até a final.

O usuário terá opção de armazenar os dados num banco de dados **MySQL 5.7**, seja este local ou remoto. A disposição dos dados nos banco está em duas tabelas, `dados` e `acumulado`, onde nestas contém todos os dados dos contratantes e o saldo acumulado, respectivamente.

As tabelas estão ligadas por uma chave estregeira, onde esta está nomeada de `IDENTIFICADOR` e localizada na tabela *dados*, que é a tabela principal do banco.

---
## Requisitos

### Instalação dos requisitos no Windows.

**OBS: Caso algum passo da instalação não esteja numa imagem, basta avançar!**

* `Python - versão 3.7.3 (Testado)` - [Download](https://www.python.org/ftp/python/3.7.3/python-3.7.3-amd64.exe)
    * Para instalar o Python de forma correta, basta fazer o Download e na tela inicial, marcar o checkbox "Add Python 3.7 to PATH" e clicar em "Install Now"
    ![](imgs/install.png)
* `pip (Gerenciador de pacotes do Python)` - o pip já será instalado ao realizar a instalação dessa forma.

* `MySQL 5.7 (Testado)` - [Download](https://www.apachefriends.org/xampp-files/7.3.12/xampp-windows-x64-7.3.12-0-VC15-installer.exe)
    * Para instalar o MySQL de forma correta, basta fazer o Download do XAMPP e marcar as mesmas opções das imagens abaixo.
    ![](imgs/install2.png)

Ao instalar o XAMPP dessa forma, é preciso iniciar os serviços do Apache e do MySQL, para isso, basta abrir o painel do XAMPP, e marcar as opções abaixo.

![](imgs/use.png)


Dessa forma, seu ambiente já está pronto para armazenar os dados no banco!

### Configuração de login padrão

Ao realizar a instalação dessa forma, o XAMPP configura esse usuário e senha padrão de utilização.

* `usuário = root`
* `senha = ""` - Neste caso, o usuário `root` não possui nenhuma senha!

---
## Dependências

Para instalar as dependências, abra PowerShell/Prompt de Comando no diretório corrente e execute o comando abaixo:

* `python -m pip install -r requirements.txt --user`

**OBS: Para abrir uma janela de comando no diretório corrente, segure a tecla `Shift` e clique com o botão direito do mouse em algum ponto do espaço da pasta, após isso, clique na opção "Abrir janela de comando aqui"**

**Tanto o PowerShell quanto o Prompt de Comando, irão realizar as mesmas ações, portanto, a escolha do mesmo fica a critério do usuário.**

![](imgs/command.png)

---
## Como usar

1. Configurar o arquivo [db_config.txt](inputs/db_config.txt) com as informações do banco de dados no qual os dados devem ser armazenados.

Para executar o programa, abra um Terminal/PowerShell/Prompt de Comando no diretório corrente e execute os comandos a seguir.

* Windows

*ALTERNATIVA*

Simplesmente entre na pasta `src` e dê dois cliques para abrir o arquivo `main.py` que o mesmo irá abrir automaticamente.

* Linux/Windows

    * `cd src` - Entra no diretório que está o programa principal.
    * `python main.py` - **Executa o programa**

Feito isso, basta seguir as opções do menu.