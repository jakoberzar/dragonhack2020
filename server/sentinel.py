import os
import datetime
import numpy as np

import matplotlib.pyplot as plt
import matplotlib

from scipy.ndimage import gaussian_filter
from scipy.signal import convolve2d

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


def get_and_save_fire_damage(coords, cache_path):
    bbox = BBox(bbox=coords, crs=CRS.WGS84)
    size = (256, 256)

    # https://custom-scripts.sentinel-hub.com/sentinel-2/active_fire_detection/
    active_fire = """
        var NGDR = index(B02, B03);
        var Inverse = (B02 - 0.2) / (0.5 - 0.2);
        //Fire indicator
        var SAHM_INDEX= ((B12 - B11) / (B12 + B11));

        if((SAHM_INDEX>0.4)||(B12>1)){
        //return[20*B04, 1*B03, 1*B02];
        return [0, 0, 1, 1];
        }

        else {
            return [0,0,0,0]
            //return [B04, B04, B04, 1];
        }
    """

    # Check where a fire was active in last 2 months (one check per week)
    today = datetime.datetime.today().date()
    # today = datetime.datetime(2016, 9, 1)
    time_range_days = 30
    step = 7
    time_range_list = []
    for i in range(0, time_range_days, step):
        day_2 = today - datetime.timedelta(days=i)
        day_1 = today - datetime.timedelta(days=i+step)
        time_range_list.append((day_1.isoformat(), day_2.isoformat()))

    def get_true_color_request(time_interval):
        return SentinelHubRequest(
            evalscript=active_fire,
            input_data=[
                SentinelHubRequest.input_data(
                    data_collection=DataCollection.SENTINEL2_L1C,
                    time_interval=time_interval,
                    mosaicking_order='leastCC'
                )
            ],
            responses=[
                SentinelHubRequest.output_response('default', MimeType.PNG)
            ],
            bbox=bbox,
            size=size
        )

    list_of_requests = [get_true_color_request(
        time_range) for time_range in time_range_list]
    # list_of_requests = [request.download_list[0]
    #                     for request in list_of_requests]
    # data_orig = SentinelHubDownloadClient().download(list_of_requests, max_threads=5)
    data_orig = [request.get_data()[0] for request in list_of_requests]

    data = np.copy(data_orig)
    result = np.zeros_like(data[0])

    first_day_found = False
    for daily_data in data:
        if not first_day_found:
            # Color the active fire red, damaged area blue
            first_day_found = True

            # Switch red and blue
            red = np.copy(daily_data[:, :, 0])
            daily_data[:, :, 0] = daily_data[:, :, 2]
            daily_data[:, :, 2] = red
        result = result + daily_data

    # Convolve the image to expand the area
    kernel = 5
    active_factor = 15
    convolved_red = convolve2d(
        result[:, :, 0], np.ones((active_factor, active_factor)), mode="same")
    convolved_blue = convolve2d(
        result[:, :, 2], np.ones((kernel, kernel)), mode="same")
    convolved_alpha_mask = (convolved_red > 0) | (convolved_blue > 0)

    convolved = np.copy(result)
    convolved[:, :, 0] = convolved_red
    convolved[:, :, 2] = convolved_blue
    convolved[:, :, 3][convolved_alpha_mask] = 255

    # Make pink red again
    mask_pink = (convolved[:, :, 0] > 0) & (convolved[:, :, 2] > 0)
    convolved[:, :, 2][mask_pink] = 0

    # Blur the image for a nicer look
    blur = False
    if blur:
        blurred = np.copy(convolved)
        sigma = 10
        blurred[:, :, 0] = gaussian_filter(blurred[:, :, 0], sigma)
        blurred[:, :, 2] = gaussian_filter(blurred[:, :, 2], sigma)
        blurred[:, :, 3] = gaussian_filter(blurred[:, :, 3], sigma)
    else:
        blurred = convolved

    matplotlib.image.imsave(cache_path, blurred)
