# coding: utf-8
import time
import cv2
import numpy as np
from ClickhouseAccess import ClickhouseAccess


class VideoGenerator:
    def __init__(self, config_parser, ch_access: ClickhouseAccess):
        self.config = config_parser["VideoGenerator"]
        self.output_file = self.config["OutputFile"]
        self.offset_x = self.config.getint("VideoOffsetX")
        self.offset_y = self.config.getint("VideoOffsetY")
        self.video_height = self.config.getint("VideoHeight")
        self.video_width = self.config.getint("VideoWidth")
        self.video_fps = self.config.getint("VideoFps")
        self.real_time_per_video_frame = self.config.getint("RealTimePerVideoFrame")
        self.ch_access = ch_access

    @staticmethod
    def get_rgb_from_hex(color_hex):
        value = int(color_hex[1:], 16)
        r = (value & 0xFF0000) >> 16
        g = (value & 0x00FF00) >> 8
        b = value & 0x0000FF
        return r, g, b

    def write_video(self):
        # cv2.namedWindow("Display", cv2.WINDOW_NORMAL)
        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        video_writer = cv2.VideoWriter(self.output_file, fourcc, self.video_fps, (self.video_width, self.video_height))
        result_img = np.full((self.video_width, self.video_height, 3), 255, dtype="uint8")
        start_frame_time = time.time()
        last_timestamp = 0
        nb_frames = 0
        for record_idx, record in enumerate(self.ch_access.get_records_ordered_by_date(
                offset_x=self.offset_x,
                offset_y=self.offset_y,
                width=self.video_width,
                height=self.video_height)):
            pixel_x, pixel_y, color_hex, timestamp_str = record
            r, g, b = VideoGenerator.get_rgb_from_hex(color_hex)
            pixel_x -= self.offset_x
            pixel_y -= self.offset_y
            result_img[pixel_y][pixel_x][0] = b
            result_img[pixel_y][pixel_x][1] = g
            result_img[pixel_y][pixel_x][2] = r
            current_timestamp = int(timestamp_str)
            if current_timestamp - last_timestamp >= self.real_time_per_video_frame:
                last_timestamp = current_timestamp
                video_writer.write(result_img)
                # cv2.imshow("Display", result_img)
                # if cv2.waitKey(1) == ord('q'):
                #     # press q to terminate the loop
                #     cv2.destroyAllWindows()
                #     break
                nb_frames += 1
                if nb_frames >= self.video_fps:
                    end_frame_time = time.time()
                    frame_duration = end_frame_time - start_frame_time
                    print(f"{nb_frames} frames rendered in {frame_duration}s -> Rendering speed: {nb_frames / frame_duration} fps")
                    start_frame_time = end_frame_time
                    nb_frames = 0
        video_writer.release()
