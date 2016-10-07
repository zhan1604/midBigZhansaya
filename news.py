#!/usr/bin/env python3

import csv
import urllib.request

from bs4 import BeautifulSoup


BASE_URL = 'https://szh.kz/10946/bayan-maqsatqyzy-zhanha-film-tusirudi-zhosparlauda/'


def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()


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

        writer.writerow(('author', 'body', 'like'))

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
