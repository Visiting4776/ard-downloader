import requests, json, shutil
from bs4 import BeautifulSoup

def download_file(url, filename): # https://stackoverflow.com/a/39217788
    with requests.get(url, stream=True) as r:
        with open(filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
    return 0

def save_video(url, quality=-1, file_path=None):
    """
    Quality: 0 = lowest, 3 = highest.
    if quality is -1, choose highest available quality
    """
    if not url or not isinstance(url, str):
        print("URL empty")
        return 1

    print(f"{url} ", end='', flush=True)

    if not file_path:
        file_path = url.split('/')[-1]
    
    if not isinstance(quality, int) or quality < -1 or quality > 3:
        print("Quality must be integer between -1 and 3!")
        return 1

    try:
        response = requests.get(url)
    except requests.exceptions.MissingSchema as e:
        print(e)
        return 1

    if response.status_code != 200:
        print(f"Error parsing the URL: {url}")
        return 1

    soup = BeautifulSoup(response.text, 'html.parser')


    players = soup.findAll('div', attrs={'data-ts_component': 'ts-mediaplayer'})
    # print(json.dumps(player_data, indent=4, sort_keys=True))
    attempts = 0 # sometimes, the first player element doesn't contain the necessary data
    for player in players:
        player_data = json.loads(player['data-config'])
        try:
            streams = player_data['mc']['_mediaArray'][0]['_mediaStreamArray']
            break
        except KeyError as e:
            attempts += 1 
            # actually, this would just download todays latest show! Not what we want!
            print("KeyError")
            return 1

    if not streams:
        print(f"No streams were found!")
        return 1

    if quality >= 0:
        qual_streams = [s for s in streams if s['_quality'] == str(quality)] # should have (at most) 1 element
        if qual_streams:
            source = qual_streams[0]['_stream']
        else:
            print(f" not available in quality {quality}, choosing highest instead.")
            quality = -1
    if quality == -1:
        source = streams[-1]['_stream']
    
    download_file(source, file_path)
    print("done " + (f"[{attempts}]" if attempts>0 else ""))
    return 0