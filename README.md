# Scraper BMF

## Descrição
Este projeto consiste em coletar os dados do site http://www2.bmf.com.br/pages/portal/bmfbovespa/lumis/lum-tipo-de-participante-enUS.asp a partir de um intervalo de data determinado pelo usuário. Os dados que serão coletados também dependem dos contratos que o usuário escrever no arquivo [contract.txt](filters/contract.txt), ou seja, os dados que serão coletados serão filtrados por meio deste arquivo. Após a coleta, os dados serão gravados em arquivos **.csv**, cada arquivo será separado por contrato(que foram escritos no filtro) e estes serão salvos por padrão no diretório [csv/](csv/) e dentro deste, há uma pasta nomeada de *accumulated*, nesta pasta também contem arquivos .csv, contendo o saldo acumulado desde a data inicial até a final.

O usuário terá opção de armazenar os dados num banco de dados **MySQL 5.7**, seja este local ou remoto. A disposição dos dados nos banco está em duas tabelas, `dados` e `acumulado`, onde nestas contém todos os dados dos contratantes e o saldo acumulado, respectivamente.

As tabelas estão ligadas por uma chave estregeira, onde esta está nomeada de `IDENTIFICADOR` e localizada na tabela *dados*, que é a tabela principal do banco.

---
## Requisitos
* `Python - versão 3.7.3 (Testado)` - [Download](https://www.python.org/ftp/python/3.7.3/python-3.7.3-amd64.exe)
    * Para instalar o Python de forma correta, basta fazer o Download e na tela inicial, marcar o checkbox "Add Python 3.7 to PATH" e clicar em "Install Now"
    ![](imgs/install.png)
* `pip (Gerenciador de pacotes do Python)` - o pip já será instalado ao realizar a instalação dessa forma.

---
## Dependências

Para instalar as dependências, abra PowerShell/prompt de comando no diretório corrente e execute o comando abaixo:

* `python -m pip install -r requirements.txt --user`

**OBS: Para abrir uma janela de comando no diretório corrente, segure a tecla `Shift` e clique com o botão direito do mouse em algum ponto do espaço da pasta, após isso, clique na opção "Abrir janela de comando aqui"**

**Tanto o PowerShell quanto o Prompt de Comando, irão realizar as mesmas ações, portanto, a escolha do mesmo fica a critério do usuário.**

![](imgs/command.png)

---
## Como usar

Para executar o programa, abra um PowerShell/prompt de comando no diretório corrente e execute os comandos a seguir.

* `cd src` - Entra no diretório que está o programa principal.

* **Executa o programa**:
    
    * `python main.py` 


---