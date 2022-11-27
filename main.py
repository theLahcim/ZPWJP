from utils import detection, argparser
import glob
args = argparser()
files = glob.glob('images/*.jpg')
files.extend(glob.glob('images/*.png'))
for f in files:
    print(f)
    detection(f, args["confidence"], args["detect"])

