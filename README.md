# Installing

    python3 -m venv env
    source env/bin/activate
    pip install -r requirements.txt

Also, make sure to install [Oracle Client libraries](https://oracle.github.io/odpi/doc/installation.html), 64-bit version, Basic Light Edition. Note that you have to be logged in Oracle website (create a free account).

## Mac

On a Mac, after downloading the zip, you can:

    cd ~/Downloads
    sudo su
    mkdir -p /opt/oracle
    mv instantclient-*.zip /opt/oracle
    cd /opt/oracle
    unzip *.zip
    exit
    mkdir ~/lib
    ln -s /opt/oracle/instantclient_12_2/libclntsh.dylib.12.1 ~/lib/ 

# Running

    source env/bin/activate
    python manage.py runserver

Server runs on port 8000.

Example URL: http://localhost:8000/search?search_type=1&search_id=2018RJDS0000000001

See it live at: http://buscadesaparecidos-devbuscadesaparecidos.devcloud.mprj.mp.br/search?search_type=1&search_id=2018RJDS0000000001
