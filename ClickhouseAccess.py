import clickhouse_driver


class ClickhouseAccess:
    def __init__(self, config_parser):
        self.config = config_parser["Clickhouse"]
        self.host = self.config["Host"]
        self.port = self.config.getint("Port")
        self.http_port = self.config.getint("HttpPort")
        self.username = self.config["Username"]
        self.password = self.config["Password"]
        self.table = self.config["Table"]
        self.client = clickhouse_driver.Client(
            host=self.host,
            port=self.port,
            user=self.username,
            password=self.password)

    def get_records_ordered_by_date(self, offset_x=0, offset_y=0, height=2000, width=2000):
        sql_query = f"""
            SELECT
                X,
                Y,
                Color,
                toInt32(`Date`)
            FROM
                {self.table}
            WHERE
                X >= {offset_x} AND Y >= {offset_y} AND X < {offset_x + width} AND Y < {offset_y + height}
            ORDER BY
                `Date` ASC
            FORMAT CSV;
        """
        settings = {"max_block_size": 100000}
        rows = self.client.execute_iter(sql_query, settings=settings)
        return rows

    def insert_records_csv(self, records):
        sql_query = f"INSERT INTO {self.table} VALUES"
        self.client.process_insert_query(sql_query, records)

    def set_up(self):
        sql_queries = [
            f"DROP TABLE IF EXISTS {self.table}",
            f"""CREATE TABLE IF NOT EXISTS {self.table}
                (
                    `Date` DateTime64(3),
                    `User` FixedString(88),
                    `Color` LowCardinality(String),
                    `ColorName` LowCardinality(String),
                    `X` UInt16,
                    `Y` UInt16
                ) ENGINE = ReplacingMergeTree() ORDER BY (`Date`, `X`, `Y`);
            """
        ]
        for sql_query in sql_queries:
            self.client.execute(sql_query)

    def get_insert_csv_command(self, csv_file_path):
        sql_query = "INSERT INTO RPlaceRecords FORMAT CSV"
        clickhouse_client_args = {
            "host": self.host,
            "port": self.port,
            "user": self.username,
            "password": self.password,
            "format_csv_delimiter": ",",
            "query": sql_query
        }
        clickhouse_client_args_str = " ".join([f"--{arg} '{value}'" for arg, value in clickhouse_client_args.items()])
        docker_command = f"cat '{csv_file_path}' | docker run -i --rm yandex/clickhouse-client {clickhouse_client_args_str}"
        return docker_command
