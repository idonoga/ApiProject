# MySQL Base Image
FROM mysql

# Add a database
ENV MYSQL_DATABASE users

EXPOSE 3306

#Copy Our SQL Scripts
COPY ./sql_scripts/ /docker-entrypoint-initdb.d/