## 1. Start the stack

```bash
docker compose up -d
```

## 2. Create the table and generate 1000 partitions

[load.py](./load.py) uses the [Python Trino client](https://github.com/trinodb/trino-python-client)
to run 1000 `INSERT`s, building a table with 1000 partitions. This just
prepares the table — the timeout is reproduced later, after the table is
dropped.

The `loadgen` service (defined in `docker-compose.yaml`) runs on the compose
network with the `trino` client pre-installed and reaches Trino at
`trino-coordinator:8080`. Trigger the load with:

```bash
docker compose exec loadgen python /load.py
```


## 3. Inspect and tear down
Now delete the partitioned table

```bash
docker compose exec -it trino-coordinator trino --execute 'DROP TABLE IF EXISTS iceberg.test.orders;'
```

Wait a few seconds or minutes and then try to run simple queries

```bash
docker compose exec -it trino-coordinator trino --execute 'CREATE TABLE IF NOT EXISTS iceberg.test.orders2 AS SELECT * FROM tpch.tiny.orders; SELECT * FROM iceberg.test.orders2 LIMIT 5; DROP TABLE IF EXISTS iceberg.test.orders2;'
```

Check Polaris logs and drop the stack

```bash
docker compose logs polaris
docker compose down
```

You can find an example Polaris log at [error.log](./error.log)
