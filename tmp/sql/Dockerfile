FROM mysql:latest

ENV MYSQL_DATABASE=sample_db
ENV MYSQL_USER=user
ENV MYSQL_PASSWORD=password
ENV MYSQL_ROOT_PASSWORD=password

COPY ./conf.d /etc/mysql/conf.d
COPY ./initdb.d /docker-entrypoint-initdb.d
COPY ./img/ /tmp

# MySQLの操作ログのファイルを作成
RUN mkdir -p /var/log/mysql && \
    touch /var/log/mysql/mysqld.log

RUN chown -R mysql /var/log/mysql

EXPOSE 3306
