from save_video import save_video
from pathlib import Path
import pandas as pd
import sys

if __name__ != '__main__':
    exit(1)

if len(sys.argv) < 3:
    print(f"Usage: {sys.argv[0]} <input_file> <column> [quality] [start] [stop]")
    exit(1)



df = pd.read_csv(sys.argv[1])

quality = int(sys.argv[3]) if len(sys.argv)>=4 else 0
min = int(sys.argv[4]) if len(sys.argv)>=5 else 0
max = int(sys.argv[5]) if len(sys.argv)>=6 else None

df = df.iloc[min:max]
column = df[sys.argv[2]]

failed_downloads = []
for idx, row in df.iterrows():
    print(f"{idx}/{column.count()}")
    path = Path(f'{sys.argv[2]}/{"/".join(row["date"].split("-")[:-1])}')
    path.mkdir(parents=True, exist_ok=True)

    fp = path / f"{sys.argv[2]}-{row['date']}.mp4"
    if save_video( # returns 1 if there was an error
            url=row[sys.argv[2]], 
            quality=quality, 
            file_path=fp):
        failed_downloads.append(row[sys.argv[2]])

print(f"Failed: {failed_downloads} ({len(failed_downloads)})")