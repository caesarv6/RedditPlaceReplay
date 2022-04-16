# Reddit place replay

## Prerequisites :

- [r/place complete history from Reddit (~11.51 Go)](https://placedata.reddit.com/data/canvas-history/2022_place_canvas_history.csv.gzip?utm_source=reddit&utm_medium=usertext&utm_name=place&utm_content=t3_txvk2d)
- docker
- python3
- DBeaver to explore date in Clickhouse
- Around 50 GB of free space on disk

## Setup

- Unzip Reddit archive
- Start clickhouse server with docker

```shell
docker run -d --name clickhouse-server --ulimit nofile=262144:262144 -p 8123:8123 -p 9000:9000 yandex/clickhouse-server
```

- Update `host` parameter in `config.ini` to match your current local ip address, returned by `ifconfig` or `ipconfig`
- Update `InputCsvFilePath` parameter in `config.ini` with the path of the csv file from Reddit

## Pipeline

```shell
# Create tables in Clickhouse and do some precessing with raw input data from Reddit
python3 1_set_up.py
# Get records from Clickhouse and write the result in a video file
python3 2_write_timelapse_video.py
```

## License

[MIT](https://choosealicense.com/licenses/mit/)