FROM mysql:8.0
ENV MYSQL_DATABASE="db" \
    MYSQL_ROOT_PASSWORD="123"
ADD createServer.sql /docker-entrypoint-initdb.d
EXPOSE 3306