```
docker compose up -d
docker compose exec -it trino-coordinator trino --execute 'CREATE SCHEMA IF NOT EXISTS iceberg.test; CREATE TABLE IF NOT EXISTS iceberg.test.orders AS SELECT * FROM tpch.tiny.orders; SELECT * FROM iceberg.test.orders LIMIt 5; DROP TABLE IF EXISTS iceberg.test.orders;'
docker compose logs polaris
docker compose down
```

You can find example polaris log at [error.log](./error.log)
