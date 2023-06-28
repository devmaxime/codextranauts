import ast
import astunparse
import logging
from typing import Optional, Tuple, List
import requests

# Create a logger
logger = logging.getLogger(__name__)


class CodeParser(ast.NodeVisitor):
    def __init__(self):
        self.imports: List[str] = []
        self.code_chunks: List[str] = []

    def visit_Import(self, node):
        """Extract import statements from the node."""
        self.imports.append(astunparse.unparse(node).strip())

    def visit_ImportFrom(self, node):
        """Extract import statements from the node."""
        self.imports.append(astunparse.unparse(node).strip())

    def visit_FunctionDef(self, node):
        """Extract function definitions from the node."""
        self.code_chunks.append(astunparse.unparse(node).strip())


def fetch_script_text(url: str) -> Optional[str]:
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
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to download script: {str(e)}")
        return None


def parse_code_chunks(code_string: str) -> Tuple[str, List[str]]:
    """
    Parse the code string into function definitions and import statements.

    Args:
        code_string (str): Code string to parse.

    Returns:
        Tuple[str, List[str]]: Tuple of import statements as a string and
        function definitions as a list of strings.

    Raises:
        logs error if a SyntaxError occurs during the parsing.
    """
    parser = CodeParser()

    try:
        tree = ast.parse(code_string)
        parser.visit(tree)
    except SyntaxError as e:
        logger.error(f"SyntaxError occurred while parsing code: {str(e)}")

    imports_string = "\n".join(parser.imports)
    return imports_string, parser.code_chunks
