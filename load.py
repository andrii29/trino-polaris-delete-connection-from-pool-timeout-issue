import os

import trino

conn = trino.dbapi.connect(
    host=os.environ.get("TRINO_HOST", "trino-coordinator"),
    port=int(os.environ.get("TRINO_PORT", "8080")),
    user="trino",
    catalog="iceberg",
    schema="test",
)
cur = conn.cursor()

cur.execute("CREATE SCHEMA IF NOT EXISTS iceberg.test")
cur.fetchall()
cur.execute("DROP TABLE IF EXISTS iceberg.test.orders")
cur.fetchall()
cur.execute(
    """
    CREATE TABLE iceberg.test.orders (
      id         BIGINT,
      part_id    INTEGER,
      payload    VARCHAR,
      amount     DOUBLE,
      created_at TIMESTAMP(6)
    )
    WITH (partitioning = ARRAY['part_id'])
    """
)
cur.fetchall()

# 1000 partitions, one INSERT (= one commit) each, 1000 random rows per partition.
for p in range(1, 1001):
    cur.execute(
        f"""
        INSERT INTO iceberg.test.orders
        SELECT
          CAST({p} AS BIGINT) * 1000 + n AS id,
          {p}                            AS part_id,
          CAST(uuid() AS VARCHAR)        AS payload,
          rand() * 1000                  AS amount,
          current_timestamp              AS created_at
        FROM UNNEST(sequence(1, 1000)) AS t(n)
        """
    )
    cur.fetchall()
    print(f"partition {p} / 1000", flush=True)

conn.close()
