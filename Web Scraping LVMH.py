from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Data Scraping
url ="https://en.wikipedia.org/wiki/LVMH"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find('table', {'class': 'wikitable'})
print(table)

headers = []
for th in table.find_all('th'):
    headers.append(th.text.strip())

rows = []
for tr in table.find_all('tr')[1:]:
    cols = tr.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    rows.append(cols)

df = pd.DataFrame(rows, columns=headers)

print(df.head())

# Cleaning Table
df = df.set_index(df.columns[0]).T.reset_index()
df.columns.name = None

df = df.rename(columns={
     df.columns[0]: 'Year',
    'Sales': 'Sales',
    'Net profit (before minority interests)': 'Net Profit',
    'Total equity': 'Total Equity'
})

df['Sales'] = df['Sales'].str.replace(',', '').astype(float)
df['Net Profit'] = df['Net Profit'].str.replace(',', '').astype(float)
df['Total Equity'] = df['Total Equity'].str.replace(',', '').astype(float)

df['Year'] = df['Year'].str.extract(r'(\d{4})').astype(int)

print(df)
# Plotting: Line Graph

colors = ['#102E50', '#F5C45E', '#BE3D2A']
plt.figure(figsize=(12, 6))
plt.plot(df['Year'], df['Sales'], label='Sales', color=colors[0], lw=7)
plt.plot(df['Year'], df['Net Profit'], label='Net Profit', color=colors[1], lw=7)
plt.plot(df['Year'], df['Total Equity'], label='Total Equity', color=colors[2], lw=7)

plt.title('Financial Data Over Time')
plt.xlabel('Year')
plt.xticks(df['Year'], rotation=45)
plt.ylabel('in Million Euros')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Plotting: Stacked Bar Chart
x = np.arange(len(df['Year']))
plt.figure(figsize=(12, 6))
colors = ['#102E50', '#F5C45E', '#BE3D2A']
plt.bar(x, df['Sales'], label='Sales', color=colors[0])
plt.bar(x, df['Net Profit'], bottom=df['Sales'], label='Net Profit',color=colors[1])
plt.bar(x, df['Total Equity'], bottom=df['Sales'] + df['Net Profit'], label='Total Equity',color=colors[2])

plt.xticks(x, df['Year'], rotation=45)
plt.xlabel('Year')
plt.ylabel('in Million Euros')
plt.title('Stacked Financial Metrics Over Time')
plt.legend()
plt.tight_layout()
plt.show()