from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt


def main():
    # URL of the Wikipedia page
    url = 'https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue'

    # Scrape data
    table_titles, data_rows = scrape_largest_companies(url)

    # Process data
    df = process_data(table_titles, data_rows)

    # Print DataFrame
    print(df)

    # Save DataFrame to CSV
    df.to_csv('largest_companies_us.csv', index=False)

    # Visualize data
    visualize_data(df)


def scrape_largest_companies(url):
    # Fetching the webpage
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    # Finding the table containing the data
    table = soup.find_all("table")[1]
    world_titles = table.find_all('th')
    world_table_titles = [title.text.strip() for title in world_titles]

    # Scraping data from each row of the table
    column_data = table.find_all('tr')
    data_rows = []
    for row in column_data[1:]:
        row_data = row.find_all('td')
        individual_row_data = [data.text.strip() for data in row_data]
        data_rows.append(individual_row_data)

    return world_table_titles, data_rows


def process_data(table_titles, data_rows):
    # Creating a DataFrame to store the data
    df = pd.DataFrame(columns=table_titles)

    # Populating DataFrame with scraped data
    for row_data in data_rows:
        length = len(df)
        df.loc[length] = row_data

    return df


def visualize_data(df):
    # Assuming the second column contains company names and the fourth column contains revenues
    companies = df.iloc[:25, 1].tolist()
    revenues = df.iloc[:25, 3].str.replace('"', '').str.replace(',', '').astype(float).tolist()

    # Creating the bar chart
    plt.figure(figsize=(12, 8))
    plt.barh(companies, revenues, color='skyblue')
    plt.xlabel('Revenue (USD millions)')
    plt.ylabel('Company')
    plt.title('Top 25 Companies in the US by Revenue')
    plt.gca().invert_yaxis()  # Invert y-axis to display top companies first
    plt.show()


if __name__ == "__main__":
    main()
