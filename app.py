import pandas as pd
import bs4 as bs
import requests

EXPECTED_COLUMNS_COUNT = 10
OUTPUT_FILE_NAME = "xbox_360_game_list.csv"

urls = [
  "https://en.wikipedia.org/wiki/List_of_Xbox_360_games_(A-L)",
  "https://en.wikipedia.org/wiki/List_of_Xbox_360_games_(M-Z)"
]

df = pd.DataFrame(columns=[
  "Title",
  "Genders",
  "Developers",
  "Publishers",
  "Release Date (NA)",
  "Release Date (EU)",
  "Release Date (JP)",
  "Release Date (AU)",
  "Addons",
  "Xbox One"
])

for url in urls:
  page = requests.get(url)
  soup = bs.BeautifulSoup(page.content, 'html.parser')

  table = soup.find("table", { "id": "softwarelist" })
  tbody = table.find("tbody", recursive=False)

  # Iterate all rows
  rows = tbody.find_all("tr")
  # Ignore first two rows as they are headers
  rows = rows[2:]
  for row in rows:
    columns = row.find_all("td")
    
    # Remove wikipedia note marks
    columns[0] = columns[0].find("i")
    # Get text only elements
    columns = [i.text.strip() for i in columns]
    # Add extra columns in case of bad table format
    columns.extend(["", ""])
    # Remove unexpected ones
    columns = columns[:EXPECTED_COLUMNS_COUNT]
    
    # Ensure columns count is proper
    if len(columns) != EXPECTED_COLUMNS_COUNT:
      raise Exception("Bad columns count, did the site updated?")

    # Add to DataFrame
    df.loc[len(df.index)] = columns

df.to_csv(OUTPUT_FILE_NAME, index=False)