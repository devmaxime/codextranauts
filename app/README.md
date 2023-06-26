# Codextranauts - APP - Where the langchains components are located.
Use it as an API.

## Installation
This is a FastAPI folder. To run it, you need to install the requirements located in requirements.txt :
```
pip install -r requirements.txt
```

## Configuration

You need to create an .env file in the root directory of the project and add the following variables:
```
OPENAI_API_KEY
PINECONE_API_KEY #Only if you intend to use Pinecone
ACTIVELOOP_TOKEN #Only if you intend to use Deeplake (As backup for Pinecone)
```

All other settings are located in config.py. You can change them there or by using env variables that will override the default settings.

Settings by default:
```
    environment: str = "dev"
    vector_db: str = "pinecone"
    llm_model_name: str = "gpt-3.5-turbo"
    template_name: str = "template_2"
    ...
    and more
```

## Run

Once you have installed the requirements and configured the .env file, you can run the app with:
```
python -m uvicorn main:app --reload
```

This will run the app in the port 8000. You can access the docs in http://localhost:8000/docs

You can test the app by using the following curl command:
```
curl -X 'GET' \
  'http://localhost:8000/ping' \
  -H 'accept: application/json'
```

## Prompt Engineering

You can modify the template and the prompt by changing the files located in the templates folder.
It is recommended to create a new template file when you want to modify the template. You can use the template_2.py file as a base.

## Deploy

You can deploy the app in any server. We recommend using Docker. You can find a Dockerfile and a Dockerfile.prod in the root directory of the project.

## Examples

You can find examples of how the output will look like below:

```
{
    "context": {
        "codebase": "This codebase is designed to detect and remove text from images using various text detection methods.",
        "configuration": "The project uses Python 3.9 and OpenCV 4.5.1. It also utilizes the EasyOCR library for text detection.",
        "related_code_snippets": [
            "def fill_text_boxes(image: np.ndarray, boxes: List[Boxe]) -> np.ndarray:\n    for box in boxes:\n        x1, y1, x2, y2 = box.get_box_coords()\n        image[y1:y2, x1:x2] = (0, 0, 0)\n    return image",
            "def detect_text_boxes_easyocr(image: np.ndarray) -> Boxes:\n    reader = easyocr.Reader(['en'])\n    results = reader.detect(image)\n    boxes = []\n    for result in results:\n        box = result[0]\n        boxes.append(Boxe(x=box[0], y=box[1], width=box[2]-box[0], height=box[3]-box[1]))\n    return Boxes(box_list=boxes)"
        ],
        "constraining_code_snippets": [
            "class Boxes(BaseModel):\n    box_list: List[Boxe]\n\n    class Config:\n        arbitrary_types_allowed = True",
            "class Boxe(BaseModel):\n    x: int\n    y: int\n    width: int\n    height: int\n\n    def get_box_coords(self) -> Tuple[int, int, int, int]:\n        return (self.x, self.y, self.x + self.width, self.y + self.height)\n\n    class Config:\n        arbitrary_types_allowed = True",
            "class AdvancedBoxes(BaseModel):\n    box_list: List[AdvancedBoxe]\n\n    class Config:\n        arbitrary_types_allowed = True",
            "class AdvancedBoxe(BaseModel):\n    x: float\n    y: float\n    w: float\n    h: float\n    prob: float\n\n    def get_box_coords(self) -> Tuple[float, float, float, float]:\n        return (self.x, self.y, self.x + self.w, self.y + self.h)\n\n    class Config:\n        arbitrary_types_allowed = True"
        ],
        "factors": []
    }
}

```