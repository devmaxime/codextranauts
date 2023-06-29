import ast
import astunparse
import logging
import time
from typing import Optional, Tuple, List, Dict, Union
from requests.exceptions import RequestException, HTTPError
import requests

# Create a logger
logger = logging.getLogger(__name__)


def get_all_files(
        user: str,
        repo: str,
        path: Optional[str] = None
) -> List[Dict[str, Union[str, int]]]:
    """
    Get all files in a GitHub repository

    Args:
        user: GitHub username
        repo: GitHub repository name
        path: File path in the repository

    Returns:
        List of files
    """
    file_list = []
    _get_all_files_recursive(user, repo, path, file_list)
    return file_list


def _get_all_files_recursive(
        user: str,
        repo: str,
        path: Optional[str],
        file_list: List[Dict[str, Union[str, int]]]
) -> None:
    """
    Recursive function to explore all directories in a GitHub repository and
    add files to the file list

    Args:
        user: GitHub username
        repo: GitHub repository name
        path: File path in the repository
        file_list: List to store file information
    """
    if path is None:
        path = ""
    url = f"https://api.github.com/repos/{user}/{repo}/contents/{path}"

    for attempt in range(5):  # Retry up to 5 times
        try:
            contents = _get_contents_from_url(url)
            if contents is not None:
                break
        except RequestException as e:
            logger.error(f"Failed to get file list: {str(e)}", exc_info=True)
            time.sleep(2 ** attempt)  # Exponential backoff
            continue

    if contents is None:  # If still None after retries, return
        return

    for file in contents:
        if file['type'] == 'dir':
            _get_all_files_recursive(user, repo, file['path'], file_list)
        else:
            file_list.append(file)


def _get_contents_from_url(
        url: str
) -> Optional[List[Dict[str, Union[str, int]]]]:
    """
    Get contents from a URL

    Args:
        url: URL to get contents from

    Returns:
        List of contents, or None if request fails
    """
    try:
        response = requests.get(url)
        response.raise_for_status()

        # Check if the response has JSON content
        if 'application/json' in response.headers['Content-Type']:
            return response.json()
        else:
            logger.error(f"URL did not return a JSON response: {url}")
            return None
    except (RequestException, HTTPError) as e:
        logger.error(
            f"Failed to fetch contents from URL: {str(e)}",
            exc_info=True,
        )
        return None


class CodeParser(ast.NodeVisitor):
    def __init__(self):
        self.imports: List[str] = []
        self.code_chunks: List[str] = []

    def _unparse_node(self, node):
        try:
            return astunparse.unparse(node).strip()
        except Exception as e:
            logger.error(f"Failed to unparse node: {str(e)}", exc_info=True)
            return ""

    def visit_Import(self, node):
        """Extract import statements from the node."""
        self.imports.append(self._unparse_node(node))

    def visit_ImportFrom(self, node):
        """Extract import statements from the node."""
        self.imports.append(self._unparse_node(node))

    def visit_FunctionDef(self, node):
        """Extract function definitions from the node."""
        self.code_chunks.append(self._unparse_node(node))


def fetch_code_text(download_url: str) -> Optional[str]:
    """
    Fetch the script from a provided URL.

    Args:
        url (str): URL of the script to fetch.

    Returns:
        Optional[str]: Content of the script if successful, None otherwise.

    Raises:
        logs error if a RequestException occurs during the request.
    """
    try:
        response = requests.get(download_url)
        response.raise_for_status()
        return response.text
    except RequestException as e:
        logger.error(f"Failed to download script: {str(e)}", exc_info=True)
        raise e


def parse_code_text(code_str: str) -> Tuple[str, List[str]]:
    """
    Parse the code string into function definitions and import statements.

    Args:
        code_str (str): Code string to parse.

    Returns:
        Tuple[str, List[str]]: Tuple of import statements as a string and
        function definitions as a list of strings.

    Raises:
        logs error if a SyntaxError occurs during the parsing.
    """
    parser = CodeParser()

    try:
        tree = ast.parse(code_str)
        parser.visit(tree)
    except SyntaxError as e:
        logger.error(
            f"SyntaxError occurred while parsing code: {str(e)}",
            exc_info=True,
        )
        return "", []

    imports_string = "\n".join(parser.imports)
    return imports_string, parser.code_chunks
