import requests, sys
import pandas as pd
from datetime import date, timedelta
from bs4 import BeautifulSoup

def save_links(start_date, end_date, filename):
    BASE_URL = 'https://www.tagesschau.de'
    REQUEST_URL = BASE_URL + '/multimedia/video/videoarchiv2~_date-{date}.html'
    SHOWS = ['tagesthemen', 'tagesschau']

    df_rows = []

    while start_date < end_date: # current date not included
        url = REQUEST_URL.format(date = start_date.strftime('%Y%m%d'))
        print(f'{url}: ', end='', flush=True)

        response = requests.get(url)
        
        if response.status_code != 200:
            print(requests.status_codes._codes[response.status_code][0])
            start_date += timedelta(days=1)
            continue
        
        soup = BeautifulSoup(response.text, 'html.parser')
        video_links = filter(lambda link: link.text.strip() in SHOWS, 
                            soup.select('h4 a'))

        df_rows.append(
            {'date': start_date.strftime('%Y-%m-%d')} | 
            {link.text.strip(): BASE_URL+link['href'] for link in 
            reversed(list(video_links))}
        )
        '''video_links is an iterator that yields all the links
        from the source HTML whose title matches one of the names
        in the SHOWS list. However, some shows contain multiple 
        entries (e.g. tagesschau) with subsequent entries overwriting
        each other. To prevent this, the iterator must be reversed
        so that only the first match (which is the show that aired last
        on any given day) gets saved instead of the last one.'''

        print(f"{requests.status_codes._codes[response.status_code][0]} [{len(df_rows[-1])-1}/{len(SHOWS)}]")

        start_date += timedelta(days=1)
        

    df = pd.DataFrame(df_rows)
    df.to_csv(filename, index=False)
    print(f'Saved dataframe with {df.shape[0]} rows to {filename}')

if __name__ == '__main__':
    save_links(
        start_date = date(year=2007, month=4, day=1), 
        end_date = date.today(),
        filename = sys.argv[1] if len(sys.argv) == 2 else 'links.csv'
    )