from lxml import html
import requests
from bs4 import BeautifulSoup
import os
import sys
import math


def save_thread(url, base_url, directory=""):
    # clean up directory arg
    if directory != "" and directory[-1] != "/":
        directory += "/"
    if not os.path.exists(directory):
        raise FileNotFoundError
    fname = url.split("/")[-2] + ".txt"
    with open(directory + fname, "w", encoding="utf-8") as ofile:    
        soup = BeautifulSoup(requests.get(url).text, "lxml")
        while True:
            # iterate over all posts on the page
            posts = soup.find_all("blockquote", class_ = "messageText")
            for post in posts:
                post.div.decompose()
                ofile.write(post.text.replace("\n", " ").lower()+"\n")
            # go to next page or finish
            next_url = soup.find("a", text="Next >")
            if next_url is None:
                break
            soup = BeautifulSoup(requests.get(base_url + next_url.get("href")).text, "lxml")

# TODO: refactor to not have to get all the thread URLs first, instead download when an URL is found
# to scrape the entire subforum, pass count=math.inf
def save_subforum(start_url, base_url, directory="", count=1000, verbose=False):
    soup = BeautifulSoup(requests.get(start_url).text, "lxml")
    urls = []
    if verbose:
        print("getting thread URLs")
    while len(urls) < count:
        threadlinks = soup.find_all("a", class_="PreviewTooltip")
        for link in threadlinks:
            if link.get("href").startswith("threads/"):
                urls.append(link.get("href"))
        next_url = soup.find("a", text="Next >")
        if next_url is None:
            break
        soup = BeautifulSoup(requests.get(base_url + next_url.get("href")).text, "lxml")

    for idx, url in enumerate(urls):
        if verbose:
            print("downloading {}/{}".format(idx, count))
        if not os.path.exists(directory):
            os.makedirs(directory)
        save_thread(base_url + url, base_url, directory)

if __name__ == "__main__":
    start_url = "https://thecatsite.com/forums/cat-behavior.5/"
    base_url = "https://thecatsite.com/"
    save_subforum(start_url, base_url, "threads", count=math.inf, verbose=True)

