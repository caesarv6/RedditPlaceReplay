# coding: utf-8
import io
import mmap
from ClickhouseAccess import ClickhouseAccess
from RPlaceRecord import RPlaceRecord
from datetime import datetime
import configparser


def get_each_pixel_record(input_csv_file):
    with open(input_csv_file, "rb") as f_in:
        f_in.seek(0, io.SEEK_END)
        file_size = f_in.tell()
        f_in.seek(0, io.SEEK_SET)
        print(f"File size: {file_size}")
        mm = mmap.mmap(f_in.fileno(), 0, prot=mmap.PROT_READ)
        line_counter = 0
        offset = 0
        start_time = datetime.now()
        progress_counter = 0
        first_line = True
        while offset < file_size:
            line = mm.readline().decode("utf-8")
            if first_line:
                first_line = False
                continue  # Skip first line
            if progress_counter == 500000:
                progress_counter = 0
                duration_seconds = (datetime.now() - start_time).seconds
                duration_seconds = max(duration_seconds, 1)
                print(f"Progress: {line_counter} read in {duration_seconds} s => {line_counter // duration_seconds} lines / s")
            record = RPlaceRecord()
            record.from_csv_line(line)
            yield record
            line_counter += 1
            progress_counter += 1
            offset = mm.tell()
        duration_seconds = (datetime.now() - start_time).seconds
        duration_seconds = max(duration_seconds, 1)
        print(f"Finished: {line_counter} read in {duration_seconds} s => {line_counter // duration_seconds} lines / s")


def main():
    config_parser = configparser.ConfigParser()
    config_parser.read("config.ini")

    ch_access = ClickhouseAccess(config_parser)
    ch_access.set_up()

    config = config_parser["Setup"]
    rplace_input_csv_file = config["InputCsvFilePath"]
    rplace_processed_csv_file = f"{rplace_input_csv_file}.processed.csv"
    with open(rplace_processed_csv_file, "w") as f_out:
        all_lines = map(lambda record: record.to_csv_line(), get_each_pixel_record(rplace_input_csv_file))
        f_out.writelines(all_lines)
    insert_command = ch_access.get_insert_csv_command(rplace_processed_csv_file)
    print(f"Execute the following command to insert data in Clickhouse: {insert_command}")


if __name__ == "__main__":
    main()
