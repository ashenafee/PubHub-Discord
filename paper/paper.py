

class Paper:
    """
    This class is used to represent a scientific paper and its metadata.
    It's created after a Sci-Hub article has been found.
    """

    def __init__(self, doi: str, url: str):
        """
        Initialize a new Paper object.

        :param doi: The DOI of the paper.
        :param url: The URL of the PDF.
        :return: A Paper object.
        """
        self.doi = doi
        self.url = url
    
    
