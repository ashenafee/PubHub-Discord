import requests
from random import randint
from validate import get_mirrors, check_pdf
from paper.paper import Paper


class SciHub:
    """
    Interact with Sci-Hub and any of its mirrors through this class. Methods
    include grabbing PDFs for papers given a DOI, downloading the papers, and
    generating citations in:
        - APA
        - MLA
        - Chicago
        - Harvard
        - CSE
    
    Works with the PubMed class to acquire information for citations as well as
    checking if a journal is reputable via its impact factor. This is checked
    with the Journal class.
    """

    def __init__(self, doi: str) -> None:
        """
        Initialize a new Sci-Hub article by providing the DOI of the paper.

        :param doi: The DOI of the paper.
        :return: A SciHub object.
        """
        self.doi = doi
        
        # Select a mirror
        self.mirror = self.select_mirror()
    
    def select_mirror(self) -> str:
        """
        Select a valid mirror to use with this Sci-Hub object.

        :return: The link to the mirror.
        """
        # Get a list of mirrors
        mirrors = get_mirrors()

        # Select a random mirror
        mirror = mirrors[randint(0, len(mirrors) - 1)]

        return mirror

    def pdf(self) -> dict:
        """
        Get the Sci-Hub URL of the PDF for the paper. If it doesn't exist,
        return an error.

        :return: A dictionary containing the URL of the PDF and its DOI.
        """
        # Append the DOI of the paper to the mirror
        url = f"{self.mirror}/{self.doi}"

        # Make a request to the mirror
        r = requests.get(url)

        # Check if the status code is 200
        if r.status_code == 200:

            # Check if the PDF is available
            pdf_url = check_pdf(r, self.mirror)
            if pdf_url:
                return {'url': pdf_url, 'doi': self.doi}
    
        return {'error': 'PDF not found'}

    def paper(self) -> Paper:
        """
        Create a Paper object for the article and return it.

        :return: A Paper object.
        """
        return Paper(self.doi, self.pdf()['url'])

    
if __name__ == '__main__':
    # Doesn't exist on Sci-Hub
    paper = SciHub('10.1038/nature.2016.19893')
    print(paper.pdf())
    paper = SciHub('10.1038/s41583-022-00576-7')
    print(paper.pdf())

    # Exists
    paper = SciHub('10.1016/j.stem.2020.09.014')
    print(paper.pdf())
