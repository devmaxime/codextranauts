from code_fetcher import fetch_script_text
from code_parser import parse_code_chunks

url_test = "https://raw.githubusercontent.com/devmaxime/codextranauts/AWSLambda/AWSLambda/vectorizer.py"


def test_dummy_parser():
    code_test_text = fetch_script_text(url_test)

    imports, chunks = parse_code_chunks(code_test_text)

    print(imports + "\n--------------")
    for chunk in chunks:
        print(chunk + "\n--------------")


if __name__ == '__main__':
    test_dummy_parser()
