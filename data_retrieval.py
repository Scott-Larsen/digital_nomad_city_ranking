import pandas as pd


URL = "https://en.wikipedia.org/wiki/Social_Progress_Index"

spi_dfs = pd.read_html(URL, attrs={'class': "wikitable sortable"})

spi_df = spi_dfs[0]

print(spi_df)
