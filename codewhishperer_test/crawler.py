import requests
from bs4 import BeautifulSoup
from markdown import markdown

def crawl_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract text content and convert to markdown
        markdown_content = ''
        for element in soup.body.find_all(text=True):
            markdown_content += element.strip() + '\n\n'
        
        # Find images and convert to markdown format
        for img in soup.find_all('img'):
            img_url = img['src']
            alt_text = img.get('alt', 'Alt text')
            markdown_image = f"![{alt_text}]({img_url})"
            markdown_content = markdown_content.replace(str(img), markdown_image)
        
        return markdown(markdown_content.strip())
    
    except requests.exceptions.RequestException:
        raise ValueError('Invalid URL')
