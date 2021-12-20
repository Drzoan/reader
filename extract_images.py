from scan import transform_guess
from scan import transform_coord
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--path", required=True,
                help="Paths to the image to be scanned")
ap.add_argument("-c", "--coordinates", default=None,
                help="Coordinates to be used for only 1 image")
args = vars(ap.parse_args())
files = args["path"]
coord = args["coordinates"]
arr = files.split(',')
if args["coordinates"] is None:
    for i in range(len(arr)):
        location = 'images/' + arr[i]
        transform_guess(location)
else:
    location = 'images/' + files
    transform_coord(location, coord)
