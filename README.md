# Calculadora em Python

<img style='width: 70%' src="https://servidor-estatico-tan.vercel.app/calculadora.png">

Projeto calculadora desenvolvida em **Python**, com interface gráfica em **PySide6**.
Utilizado **PyInstaller** para realizar o empacotamento da aplicação.

### 💻 Projeto desenvolvido em/para MacOS.

Pyinstaller gera o instalador para a arquitetura em que
a aplicação está sendo empacotada. Para empacotar a aplicação foi utilizado o comando:

 ```
pyinstaller 
    --name="Calculadora"
    --noconfirm
    --onefile
    --add-data="./files/:./files/"
    --icon="./files/calc_icon.png"
    --noconsole
    --log-level=WARN
    main/main.py
```

Os comandos acima possuem pequenas diversas quando executadas em Windows. Consultar na documentação do [PyInstaller](https://pyinstaller.org/en/stable/usage.html)

## System Integrity Protection (SIP)

Consultar documentação [SIP](https://developer.apple.com/documentation/security/disabling_and_enabling_system_integrity_protection)

Durante desenvolvimento, pode ser necessário desativar o SIP temporariamente para instalar e testar seu código.

## Empacotamento da aplicação / Execução

Caso possua os requisitos acima como ambiente MacOS e o SIP desativado se necessário, navegue até a pasta do projeto empacotado "dist/Calculadora.app", e dê dois cliques para executar a aplicação.

### Instalação

Siga estas etapas a seguir para configurar o ambiente de desenvolvimento:

1. Clone este repositório em sua máquina local.

    **``git clone https://github.com/guicamargo19/calculadora_python.git``**

2. Navegue até o diretório clonado e abra no VSCode.
    
    **``cd calculadora_pyside``**

3. Crie o ambiente virtual.

    **``python -m venv venv``**

4. Instale as dependências para o projeto.

    **``pip install -r requirements.txt``**

5. Execute o módulo python "main.py".

## 🛠️ Ferramentas utilizadas para construção do projeto

* **Python** - Linguagem de programação de alto nível, interpretada de script, imperativa, orientada a objetos, funcional, de tipagem dinâmica e forte.
* **PySide6** - Biblioteca de interface gráfica do usuário (GUI) para a linguagem de programação Python.
* **PyInstaller** -  Biblioteca que permite transformar um script Python em um executável standalone.
* **PyQtDarkTheme** - Módulo Python que aplica temas "dark" ou "light" em aplicações QtWidgets.

## ✒️ Autor

Guilherme Ferreira Camargo
