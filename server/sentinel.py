import os
import datetime
import numpy as np

import matplotlib.pyplot as plt
import matplotlib

from sentinelhub import MimeType, CRS, BBox, SentinelHubRequest, SentinelHubDownloadClient, \
    DataCollection, bbox_to_dimensions, DownloadRequest


def get_and_save_false_color_map(coords):
    bbox = BBox(bbox=coords, crs=CRS.WGS84)
    size = (256, 256)

    false_color = """
    //VERSION=3
    function setup() {
        return {
            input: [{
                bands: ["B12","B11","B04"],
            }],
            output: {
                bands: 4,
            }
        };
    }

    function evaluatePixel(sample) {
        if (sample.B12 >= 0.7) {
            return [255,
                    0,
                    0,
                    1];
        }
        return [0, 0, 0, 0];
    }
    """

    request_false_color = SentinelHubRequest(
        evalscript=false_color,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL2_L1C,
                time_interval=('2016-08-20', '2016-08-20'),
                mosaicking_order='leastCC'
            )],
        responses=[
            SentinelHubRequest.output_response('default', MimeType.PNG)
        ],
        bbox=bbox,
        size=size
    )

    response = request_false_color.get_data()

    matplotlib.image.imsave('file.png', response[0])
