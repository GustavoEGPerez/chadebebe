### Configuração inicial do ambiente de desenvolvimento
1 - Caso não exista uma pasta `<root-app>/env`, criar ambiente virtual em Linux e Windows:
    
    python -m venv

2a - Ativar ambiente virtual em Linux:

    source <root-app>/env/bin/activate 

2b - Ativar ambiente virtual em Windows:

    <root-app>/env/bin/Activate.ps1

*&nbsp;<small><i>&lt;root-app&gt;</i> é o caminho raiz da solução</small>

2b - Instale as dependencias:

&lt;root-app&gt;: `pip install -r ./requirements.txt`

Caso ocorra o erro "<i>pg_config executable not found</i>" ao instalar as dependências, tente instalar os pacotes libpq-dev e python-dev com o seguinte comando: `sudo apt-get install libpq-dev python-dev`
