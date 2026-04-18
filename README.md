Para alternar entre MySQL e PostgreSQL:
1. Descomentar/Comentar o bloco de código correspondente ao banco de dados desejado e comentar o outro em `requirements.txt`.
2. Descomentar/Comentar o FROM e RUN no  `Dockerfile` para construir uma imagem Docker com as dependências corretas para cada banco de dados.
3. Em `settings.py`, configurar o `DATABASES` para usar o banco de dados escolhido, seja MySQL ou PostgreSQL.
    - Network Docker funciona apenas se estiver HOST="172.17.0.1", nao funciona com localhost.
4. Certificar-se de que o banco de dados esteja em execução e acessível para a aplicação Django.
5. Usa o docker-compose correto para iniciar os serviços:
    - Para MySQL: `docker compose -f mysql_docker-compose.yml up -d`
    - Para PostgreSQL: `docker compose -f psql_docker-compose.yml up -d`
6. Acessar a aplicação Django em `http://localhost:8000` para verificar

Psql usa 191MB e o Mysql usa 835MB, `cerca de 3,3x menor`, devido a necessidade de instalar o cliente MySQL `mysqlclient`, 
que é mais pesado do que o cliente PostgreSQL. O cliente MySQL inclui bibliotecas adicionais e dependências que aumentam 
o tamanho da imagem Docker, enquanto o cliente PostgreSQL `psycopg2-binary` é mais leve e tem menos dependências, resultando em uma imagem Docker menor.