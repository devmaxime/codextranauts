import ast
import astunparse


def parse_code_chunks(code_string):
    code_chunks = []
    imports = []

    # Parse the code string into an AST (Abstract Syntax Tree)
    tree = ast.parse(code_string)

    # Traverse the AST and extract function definitions
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            function_chunk = astunparse.unparse(node).strip()
            code_chunks.append(function_chunk)
        else:
            if isinstance(node, ast.Import):
                import_line = "import " + astunparse.unparse(node).strip()
                imports.append(import_line)
            elif isinstance(node, ast.ImportFrom):
                import_line = astunparse.unparse(node).strip()
                imports.append(import_line)

    imports_string = "\n".join(imports)

    return imports_string, code_chunks
