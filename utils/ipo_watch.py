import pandas as pd
import numpy as np
def get_data(soup):
    table = soup.find("figure",class_ = "wp-block-table")
    rows = table.find_all('tr')
    # Create an empty list to store the IPO data
    ipo_data = []
    # Loop through each row and extract the IPO name, type, GMP, and issue price
    for row in rows:    # Get the table cells in each row    
        cells = row.find_all('td')
        if len(cells) == 0:
            continue        
        # Get the text from each cell and strip any whitespace    
        name = cells[0].get_text().strip()    
        type = cells[1].get_text().strip()    
        gmp = cells[2].get_text().strip()    
        price = cells[3].get_text().strip()   
        # Create a dictionary with the IPO data    
        ipo = {"name": name, "type": type, "gmp": gmp, "price": price}    
        # Append the dictionary to the list    
        ipo_data.append(ipo)
    # Create a pandas DataFrame from the list of dictionaries
    df = pd.DataFrame(ipo_data)
    df.set_index('name',inplace=True)
    df['gmp'] = df['gmp'].str.replace(df['gmp'][0][0],'')
    df['price'] = df['price'].str.replace(df['price'][0][0],'')
    # Convert the GMP and price columns to numeric values
    df["gmp"] = pd.to_numeric(df["gmp"], errors="coerce")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    # Calculate the GMP percentage for each IPO
    df["gmp_pct"] = np.divide(df["gmp"], df["price"]) * 100
    # Round the GMP percentage to two decimal places
    df["gmp_pct"] = df["gmp_pct"].round(2)
    # Print the DataFrame
    df = df.loc[df['type'] == 'Mainline']
    ipos_data = df.to_dict(orient='index')
    return str(ipos_data)