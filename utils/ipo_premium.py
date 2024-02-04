import pandas as pd
import numpy as np


def get_data(soup,today_date):
    table = soup.find("table", class_="table table-bordered table-hover")
    rows = table.find_all("tr")
    # Create an empty list to store the IPO data
    ipo_data = []
    # Loop through each row and extract the IPO name, type, GMP, and issue price
    for row in rows:  # Get the table cells in each row
        cells = row.find_all("td")
        if len(cells) == 0:
            continue
        # Get the text from each cell and strip any whitespace
        name = cells[0].get_text().strip()
        gmp = cells[1].get_text().strip()
        open = cells[2].get_text().strip()
        close = cells[3].get_text().strip()
        price = cells[4].get_text().strip()
        lot_size = cells[5].get_text().strip()
        allotment_date = cells[6].get_text().strip()
        listing_date = cells[7].get_text().strip()
        # Create a dictionary with the IPO data
        ipo = {
            "name": name,
            "gmp": gmp,
            "open": open,
            "close": close,
            "price": price,
            "lot_size": lot_size,
            "allotment_date": allotment_date,
            "listing_date": listing_date
        }
        # Append the dictionary to the list
        ipo_data.append(ipo)
    # Create a pandas DataFrame from the list of dictionaries
    df = pd.DataFrame(ipo_data)
    df = df[df['name'].str.contains('MAINBOARD')]
    df.set_index('name',inplace=True)
    df['open'] = pd.to_datetime(df["open"])
    df['close'] = pd.to_datetime(df["close"])
    # filtered_df = df.loc[df["open"]<today_date & df["close"]>today_date]
    ipos_data = df.to_dict(orient='index')
    return str(ipos_data)
