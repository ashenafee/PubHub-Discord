# Description: Sci-Hub mirrors list. Fetch a list of Sci-Hub mirrors from
# https://theopensci.com/sci-hub-mirrors/

import requests
from bs4 import BeautifulSoup


EXCLUDE = [
    "https://sci-hub.es.ht",
    "https://sci-hub.it.nf"
]


def get_mirrors() -> list:
    """
    Fetch a list of Sci-Hub mirrors from https://theopensci.com/sci-hub-mirrors/
    and verify they work. For those that do, return them in a list.

    :return: A list of Sci-Hub mirrors.
    """
    # Make a request to The Open Sci
    r = requests.get('https://theopensci.com/sci-hub-mirrors/')

    # Get the HTML of the page
    html = r.text

    # Parse the HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Get the <ul> containing the list of mirrors
    ul = soup.find_all('ul')[1]

    # Get the <li> elements
    lis = ul.find_all('li')

    # Get the mirrors
    mirrors = [li.text for li in lis if li.text not in EXCLUDE]

    # Verify the mirrors
    mirrors = [mirror for mirror in mirrors if verify_mirror(mirror)]

    return list(set(mirrors))


def verify_mirror(link: str) -> bool:
    """
    Verify that the mirror is a valid Sci-Hub mirror that can access the
    Sci-Hub collection of articles.

    :param link: The link to the mirror.
    :return: True if the mirror is valid, False otherwise.
    """
    # Make a request to the mirror
    try:
        r = requests.get(link)
    except requests.exceptions.ConnectionError:
        return False

    # Check if the status code is 200
    if r.status_code == 200:

        # Check the title of the page
        if 'Sci-Hub' in r.text:
            return True
        
        return False
    else:
        return False


def check_pdf(response: requests.Response, url: str) -> str:
    """
    Check if the PDF is available on Sci-Hub.

    :param response: The response from the mirror.
    :param url: The URL of the mirror.
    :return The URL of the PDF.
    """
    # Look for an <embed> tag in the page
    soup = BeautifulSoup(response.text, 'html.parser')
    embed = soup.find('embed')

    # Check if the <embed> tag exists
    if embed:
        
        # Get the URL of the PDF
        pdf_url = embed['src']

        # Parse the URL
        pdf = pdf_url.split('.pdf')[0]
        pdf_url = f"{url}{pdf}.pdf"
        
        # Check if the PDF is available
        r = requests.get(pdf_url)

        # Check if the status code is 200
        if r.status_code == 200:
            return pdf_url
        
        return None

    else:
        return None
