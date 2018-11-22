from lxml import html
import requests
from bs4 import BeautifulSoup
import os
import sys
import math


def save_thread(path, base_url, directory=""):
    # clean up directory arg
    if directory != "" and directory[-1] != "/":
        directory += "/"
    if not os.path.exists(directory):
        raise FileNotFoundError
    fname = path.split("/")[-2] + ".txt"
    with open(directory + fname, "w", encoding="utf-8") as ofile:    
        soup = BeautifulSoup(requests.get(base_url+path).text, "lxml")
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

# to scrape the entire subforum, pass count=math.inf
def save_subforum(start_path, base_url, directory="", count=1000, verbose=False):
    if directory!="" and not os.path.exists(directory):
        os.makedirs(directory)
    soup = BeautifulSoup(requests.get(base_url+start_path).text, "lxml")
    saved_count = 0
    # go through all links on the page, if they are a thread link, save it
    while saved_count < count:
        threadlinks = soup.find_all("a", class_="PreviewTooltip")
        for link in threadlinks:
            if link.get("href").startswith("threads/"):
                if verbose:
                    print("downloading {}/{}".format(saved_count, count))
                save_thread(link.get("href"), base_url, directory)
                saved_count += 1
        # move to the next page
        next_url = soup.find("a", text="Next >")
        if next_url is None:
            break
        soup = BeautifulSoup(requests.get(base_url + next_url.get("href")).text, "lxml")


if __name__ == "__main__":
    start_path = "forums/cat-behavior.5/"
    base_url = "https://thecatsite.com/"
    save_subforum(start_path, base_url, directory="threads", verbose=True)

