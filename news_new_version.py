#!/usr/bin/env python3
import requests
import csv
import urllib.request

from bs4 import BeautifulSoup


r =requests.get("https://szh.kz/category/sport/")
soup = BeautifulSoup(r.content,"html.parser")
links = soup.find_all('a')
ssylki = []
for link in links:
    links.append({
    'title': ("<a href='%s'>%s</a>" %(link.get("href"), link.text))
    })

def parse(html):
    soup = BeautifulSoup(html,"html.parser")
    div = soup.find('div', class_='wc-thread-wrapper')
    rows = div.find_all('div', class_='wc-comment wc-blog-guest wc_comment_level-1')

    ditails = []
    for row in rows:
        ditails.append(row.find('div', class_='wc-comment-right')) 
    #cols = ditails.find_all('div')
    projects = []

    for x in ditails:

        projects.append({
            'author': x.find('div', class_='wc-comment-author').text,            
            'body': x.find('div', class_='wc-comment-text').text[:-2],
            'sum_like': x.find('div', class_='wc-vote-result').text
       })

    return projects
    
def save(projects, path):
    with open(path, 'w') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(('title', 'author', 'body', 'like'))

        for ssylka in ssylki:
            writer.writerow(
                (ssylka['title']) 
            )

        for project in projects:
            writer.writerow(
                (project['author'], project['body'], project['sum_like']) 
            )

def main():

    projects = parse(get_html(BASE_URL))

    print('Save...')
    save(projects, 'projects.csv')


if __name__ == '__main__':
    main()