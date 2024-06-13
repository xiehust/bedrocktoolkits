import sys
from crawler import crawl_website

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <url>")
        sys.exit(1)
    
    url = sys.argv[1]
    try:
        markdown = crawl_website(url)
        with open('output.md', 'w') as file:
            file.write(markdown)
        print('Markdown file generated: output.md')
    except ValueError as e:
        print('Error:', str(e))

if __name__ == '__main__':
    main()
import sys
import argparse
import requests
from requests.exceptions import RequestException

def crawl_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except RequestException as e:
        raise ValueError(f"Error crawling website: {e}")

def main():
    parser = argparse.ArgumentParser(description="Crawl a website and save the content as a Markdown file.")
    parser.add_argument("url", help="The URL of the website to crawl")
    args = parser.parse_args()

    try:
        markdown = crawl_website(args.url)
        with open("output.md", "w") as file:
            file.write(markdown)
        print("Markdown file generated: output.md")
    except ValueError as e:
        print("Error:", str(e))

if __name__ == "__main__":
    main()

