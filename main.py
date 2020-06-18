import json
import requests
from bs4 import BeautifulSoup


def extract_costumor_links(soup):
    costumer_links = soup.select('.card-post--case-study div a.card-post__title')
    return [a['href'] for a in costumer_links]


def get_customer_data(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return {
        'name': soup.select('div.breadcrumb__item a')[1].text,
        'logo_url': soup.select('div.post-header-caseStudies__logo img')[0]['src'],
        'domain': soup.select('div.about-company__cta div a')[0]['href']
    }


customer_links = []
customer_data = []
url = 'https://www.chorus.ai/customers'

while url:
    print(url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    customer_links += extract_costumor_links(soup)

    try:
        url = soup.select('a.more-link')[0]['href']
    except IndexError:
        print('checked all pages')
        break

for customer in customer_links:
    print('fetching ' + customer)
    customer_data += [get_customer_data(customer)]

with open('scrape_result.json', 'w') as f:
    f.write(json.dumps(customer_data, indent=4))

print('done!')
