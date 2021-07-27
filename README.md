# ard-downloader

## About:

This is a small CLI utility written in python 3.9 to conveniently download evening news segments from the ARD (largest German public broadcasting network) news archive.

## Requirements:

* `requests` (for making HTTP requests)
* `beautifulsoup4` (for parsing HTML data)
* `pandas` (to conveniently read and write CSV data)

Install via a python package manager of your choice.

## Usage:

1. (optional) Run `get_links.py` to update the list of links to the daily news segments. The archive goes back to April 1st 2007 with some entries missing.
2. Run `save_videos_from_file.py` like so:

```$ save_videos_from_file.py <input_file> <column> [quality] [start] [stop]```

Column is the column in the provided CSV file that should be downloaded. The last 3 parameters are optional. If no quality is given, the lowest quality will be selected for each video (~50 MB for a 30 minute segment). If a video is not available in the selected quality, the highest available quality will be chosen. In practice, this often means only one quality is available, which is usually the lowest. Hence, the "highest available" quality is nothing else than the lowest quality.

`start` and `stop` can be used to specify which of the rows of the input file to download. **Both support negative indexing!** If left blank, all rows will be downloaded.

The saved videos will be stored in the following directory format: 

`show_title/year/month/show_title-year-month-day.mp4`

Feel free to fork and improve the project!