"""
Run ``pip3 install .``
which will install the command ``brokenUrls`` inside your current environment.
"""

import argparse
import logging
import sys
import requests

from brokenurls import __version__
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.parse import urljoin
from tomlkit import string

_logger = logging.getLogger(__name__)

brokenURLs = []

def getURLs(html, element, select):
    """Get URLs from a given HTML body

    Args:
      html (string): string
      element (string): string
      select (string): string

    Returns:
      list: list of URLs
    """
    def getImgsLink(el):
        return el[element]
    return list(map(getImgsLink, BeautifulSoup(html, features="html.parser").select(select)))

def isImage(url):
    """Check if url is related to an image

    Args:
      url (string): string

    Returns:
      boolean: return true if url is referring to an image 
    """
    return \
        url.endswith(".png") or \
        url.endswith(".jpg") or \
        url.endswith(".jpeg") or \
        url.endswith(".svg")

def search(current, URL, parentURL, userInput, visitedURLs, imgOnly, allowedDomains):
    """Get broken URLs list

    Args:
      current (string): string
      URL (string): string
      parentURL (string): string
      userInput (string): string
      visitedURLs (array): array[string]
      imgOnly (boolean): boolean
      allowedDomains (array[string]): array[string]

    Returns:
      list: list of broken URLs
    """
    # Search only URLs not yet visited and child URLs of the requested page or from a predefined domain list
    if (not (URL in visitedURLs)) and (URL.startswith(userInput) or (urlparse(URL).netloc in allowedDomains)):
        try:
            response = requests.get(URL)
            visitedURLs.append(URL)
            if(response.status_code == 404):
                if ((not imgOnly) or (imgOnly and isImage(URL))):
                    brokenURLs.append("NOT FOUND: " + URL + " in " + parentURL)
                    print(brokenURLs[-1])
            else:
                print("SUCCESS: " + URL + " in " + parentURL)
                # if URL is not a (png|jgp|jpeg|svg) image
                if (not isImage(URL)):
                    for url in getURLs(response.text, "href", "a[href]"):
                        search(current, urljoin(URL, url), URL, userInput, visitedURLs, imgOnly, allowedDomains)
                    for imgUrl in getURLs(response.text, "src", "img[src]"):
                        search(current, urljoin(URL, imgUrl), URL, userInput, visitedURLs, imgOnly, allowedDomains)
        except Exception as e:
            _logger.error("ERROR: " + str(e));
            visitedURLs.append(current)

# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Are you looking for 404 urls?")
    parser.add_argument(
        "--version",
        action="version",
        version="BrokenURLs {ver}".format(ver=__version__),
    ),
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    ),    
    parser.add_argument(
        "-url",
        "-u",
        dest="url",
        help="root page",
        type=string,
        required=True
    ),
    parser.add_argument(
        "-imgOnly",
        dest="imgOnly",
        help="filter only broken img link (png|jpg|jpeg|svg)",
        action="store_const",
        const=True
    ),
    parser.add_argument(
        "-a",
        "--allowed-domains",
        dest="allowedDomains",
        help="scan urls in allowed domains list",
        nargs='+',
        required=False,
        default=[]
    )
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args):
    """Wrapper allowing :func:`search` to be called with string arguments in a CLI fashion

    Instead of returning the value from :func:`search`, it prints the result to the
    ``stdout`` in a nicely formatted message.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "-u https://mywebsite.com/"]``).
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.info("Starting analysis...")

    print("ALLOWED_DOMAINS:")
    print(args.allowedDomains)

    search(args.url, args.url, "", args.url, [], args.imgOnly, args.allowedDomains)

    print("\n--- Analysis completed ---\n")

    print("Broken links:\n")
    for url in brokenURLs:
        print("\t" + url)

    _logger.info("Script ends here")


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html
    run()
