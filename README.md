Подготовка к работе:
1. Установить необходимые библиотеки из requirments.txt

pip install requirments.txt

2. Установить Docker 

3. Из раздела DockerHUB установить image с устаноленным ClickHouse\ в PowerShell вставить комманду 

docker pull clickhouse/clickhouse-server

4. Поднять контейнер комманадой 

docker run -d --name clickhouse-server -p 8123:8123 -p 9000:9000 --ulimit nofile=262144:262144 -e CLICKHOUSE_DB=default -e CLICKHOUSE_USER=default -e CLICKHOUSE_PASSWORD='' -e CLICKHOUSE_DEFAULT_ACCESS_MANAGEMENT=1 clickhouse/clickhouse-server:latest

5. Проверяем статус контейнера в PowerShell 
docker ps 
(увидим строчку 
CONTAINER ID               IMAGE                                     PORTS
<your_id>         clickhouse/clickhouse-server   0.0.0.0:9000->9000/tcp, 0.0.0.0:8123->8123/tcp)

6. Выполняем скрипт






