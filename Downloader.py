import os
import argparse
import progressbar
import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve

pbar =  None
def show_progress(block_num, block_size, total_size):
    global pbar
    if pbar is None:
        pbar = progressbar.ProgressBar(maxval=total_size)
        pbar.start()
    downloaded = block_num * block_size
    if downloaded < total_size:
        pbar.update(downloaded)
    else:
        pbar.finish()
        pbar = None

parser = argparse.ArgumentParser(description="Downloads all video files in the given page")

parser.add_argument('-l', '--Link', help='Page Url', required=True)
parser.add_argument("-o", "--Output", help="Output directory")
parser.add_argument("-s", "--Start", help="start index of files to be downloaded", default=0, type=int)

args = parser.parse_args()
url = args.Link
reqs = requests.get(url)
url = url[:url.index("?")] if "?" in url else url
soup = BeautifulSoup(reqs.text, 'html.parser')

# TODO add getting formats from cli
formats = tuple(f'.{x}' for x in ['mkv', 'mp4'])

video_hrefs = []
for link in soup.find_all('a'):
    href = link.get('href')
    if not href:
        continue
    if href.endswith(formats):
        video_hrefs.append(href)
start = args.Start
video_hrefs = video_hrefs[start:] if start < len(video_hrefs) else []
print(f"Number of videos found: {len(video_hrefs)}")

output_dir = args.Output if args.Output else "./"
os.makedirs(output_dir, exist_ok=True)
for href in video_hrefs:
    print(f"Downloading: {href}")
    try:
        if href.startswith("http"):
            video_url = href
        else:
            video_url = url + href
        file_name = href.split("/")[-1].replace("%20", " ")
        urlretrieve(video_url.replace(" ", "%20"), os.path.join(output_dir, file_name), show_progress)
    except Exception as e:
        print(f"Exception occured \n{e}")
print("Download finished.")
