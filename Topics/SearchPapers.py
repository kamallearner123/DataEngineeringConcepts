import requests
from bs4 import BeautifulSoup
from datetime import date

def search_google_scholar(keyword):
    current_year = date.today().year
    last_year = current_year - 1
    url = f"https://scholar.google.com/scholar?q={keyword.replace(' ', '+')}&hl=en&as_sdt=0%2C5&as_ylo={last_year}"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    results = soup.select('.gs_ri')
    for i, result in enumerate(results[:5], 1):  # Top 5
        title = result.select_one('.gs_rt').text
        link = result.select_one('.gs_rt a')
        link_url = link['href'] if link else 'No link'
        print(f"{i}. {title}\n   {link_url}\n")

if __name__ == "__main__":
    keywords = ["rust embedded systems", "edge AI", "quantum computing"]
    print(f"Search results on {date.today()}\n")
    for keyword in keywords:
        print(f"Keyword: {keyword}")
        search_google_scholar(keyword)
        print("-" * 60)

