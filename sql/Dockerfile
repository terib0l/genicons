FROM mysql:latest

COPY ./conf.d /etc/mysql/conf.d

# MySQLの操作ログのファイルを作成
RUN mkdir -p /var/log/mysql && \
    touch /var/log/mysql/mysqld.log

RUN chown -R mysql /var/log/mysql

EXPOSE 3306
