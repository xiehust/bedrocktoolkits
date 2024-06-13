  
import pytest
from crawler import crawl_website

def test_crawl_website_text_only():
    url = 'https://example.com/test1'
    markdown = crawl_website(url)
    assert '# Example Website' in markdown
    assert 'This is a test website with only text content.' in markdown

def test_crawl_website_with_images():
    url = 'https://example.com/test2' 
    markdown = crawl_website(url)
    assert '![Alt text](/path/to/image1.jpg)' in markdown
    assert '![Alt text](/path/to/image2.png)' in markdown

def test_crawl_website_mixed_content():
    url = 'https://example.com/test3'
    markdown = crawl_website(url)  
    assert '# Example Mixed Content' in markdown
    assert 'This website has both text and images.' in markdown
    assert '![Image 1](/path/to/image1.jpg)' in markdown

def test_crawl_website_invalid_url():
    invalid_url = 'invalid-url'
    with pytest.raises(ValueError, match='Invalid URL'):
        crawl_website(invalid_url)
