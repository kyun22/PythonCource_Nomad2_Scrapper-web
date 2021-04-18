import requests
from bs4 import BeautifulSoup


def get_last_page(url):
    # URL = f"https://stackoverflow.com/jobs?c=KRW&d=20&q={word}&sort=i"  # &pg=9
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    page_links = soup.find("div", {"class": "s-pagination"}).find_all("span")
    pages = []
    for link in page_links:
        pages.append(link.string)
    last_page = pages[-2]
    return int(last_page)

def extract_job_informaion(html):
    title = html.find("h2", {"class": "fs-body3"}).find("a")['title']
    company_row = html.find("h3")
    company, location = company_row.find_all("span", recursive=False)
    company = company.get_text(strip=True)
    location = location.get_text(strip=True)
    link = f"https://stackoverflow.com/jobs/{html['data-jobid']}"
    return {"from": "StackOverFlow", "title": title, "company": company, "location": location, "link": link}

def extract_jobs(last_page, url):
    results = []
    for page in range(last_page):
        print(f"Stackoverflow Scrapping. {page} page extracting...")
        r = requests.get(f"{url}&pg={page + 1}")
        soup = BeautifulSoup(r.text, "html.parser")
        job_rows = soup.find_all("div", {"class": "-job"})
        for job_row in job_rows:
            result = extract_job_informaion(job_row)
            results.append(result)
    return results

def get_jobs(word):
    url = f"https://stackoverflow.com/jobs?c=KRW&d=20&q={word}&sort=i"  # &pg=9
    last_page = get_last_page(url)
    jobs = extract_jobs(last_page, url)
    return jobs
