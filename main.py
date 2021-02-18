"""
File:           main.py
Author:         Dibyaranjan Sathua
Created on:     18/02/21, 10:09 pm
"""
from src.crawler import Crawler


def main():
    """ Main function """
    crawler = Crawler()
    crawler.crawl()


if __name__ == "__main__":
    main()
