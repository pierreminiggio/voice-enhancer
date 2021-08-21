import os
import requests
import sys
from pydub import AudioSegment
from pydub.scipy_effects import high_pass_filter, low_pass_filter

args = sys.argv

if len(args) != 2:
    print('Use like this : python main.py <input_file_url>')
    sys.exit()

input_file_url = args[1]

input_file = 'input.mp3'

if os.path.isfile(input_file) == False:
    video_download_request = requests.get(input_file_url, allow_redirects=True)
    open(input_file, 'wb').write(video_download_request.content)

original_voice = AudioSegment.from_mp3(input_file)

low_voice = low_pass_filter(original_voice, 300)
boosted_low_voice = low_voice.apply_gain(10)

reberbered_sound = original_voice.overlay(
    boosted_low_voice
).overlay(
    low_pass_filter(high_pass_filter(original_voice, 1500), 2000).compress_dynamic_range(threshold=-30.0, attack=50.0, release=50.0).apply_gain(-18).pan(-1),
    20
).overlay(
    low_pass_filter(high_pass_filter(original_voice, 1000), 1500).compress_dynamic_range(threshold=-35.0, attack=100.0, release=50.0).apply_gain(-21).pan(1),
    40
).overlay(
    low_pass_filter(high_pass_filter(original_voice, 500), 1000).compress_dynamic_range(threshold=-35.0, attack=150.0, release=50.0).apply_gain(-24).pan(-0.5),
    60
).overlay(
    low_pass_filter(high_pass_filter(original_voice, 300), 500).compress_dynamic_range(threshold=-35.0, attack=150.0, release=50.0).apply_gain(-27).pan(0.5),
    80
).overlay(
    low_pass_filter(high_pass_filter(original_voice, 100), 300).compress_dynamic_range(threshold=-35.0, attack=150.0, release=50.0).apply_gain(-30).pan(-0.25),
    100
).overlay(
    low_pass_filter(original_voice, 100).compress_dynamic_range(threshold=-35.0, attack=150.0, release=50.0).apply_gain(-30).pan(0.25).apply_gain(-33),
    120
).overlay(
    low_pass_filter(high_pass_filter(original_voice, 500), 1000).compress_dynamic_range(threshold=-35.0, attack=1000.0, release=50.0).apply_gain(-30),
    140
)

reberbered_sound.apply_gain(7).export(
    'output.mp3',
    format='mp3'
)

os.remove(input_file)
