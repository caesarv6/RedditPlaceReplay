# coding: utf-8
import configparser
from ClickhouseAccess import ClickhouseAccess
from VideoGenerator import VideoGenerator


def main():
    config_parser = configparser.ConfigParser()
    config_parser.read("config.ini")
    ch_access = ClickhouseAccess(config_parser)
    video_gen = VideoGenerator(config_parser, ch_access)
    video_gen.write_video()


if __name__ == "__main__":
    main()
