# Project Setup Instructions

This project requires certain Python modules which are located in a specific directory. To ensure Python can find these modules, you need to add the directory to your Python path. We need to do this to be able to run Python files in a local environment (by referencing shared_code) without having to modify imports.

The reason for this setup is due to how AWS Lambda handles layers. In AWS Lambda, a layer is a distribution mechanism for libraries, custom runtimes, and other function dependencies. Layers promote code sharing and separation of responsibilities so that you can iterate faster on writing business logic. When a Lambda function configured with a layer is executed, AWS downloads any specified layers and extracts them to the `/opt` directory in the function execution environment. Each runtime then looks for libraries in a different location under `/opt`, depending on the language.

Therefore, our project is structured to mirror this configuration. The shared code that is common across multiple Lambda functions is stored in `shared_code_layer`, simulating a Lambda Layer. However, when running locally, Python doesn't know to look in this directory for modules. By adding the `shared_code_layer` directory to the Python path, we're telling Python where to find these shared modules when running in a local environment.

The following steps outline how to add the `shared_code_layer` directory to your Python path:

## Step 1: Activating the Virtual Environment

Before proceeding, make sure your Python virtual environment is activated. If you haven't already created a virtual environment for this project, you can do so with the following command:

```bash
python3 -m venv venv
```

This command creates a new virtual environment named venv. You can replace venv with any name you prefer.

To activate the virtual environment, use this command:

```bash
source venv/bin/activate
```

Replace venv with the name of your virtual environment.

## Step 2: Modifying the Virtual Environment Activation Script

Next, you need to add the path to the required directory to your Python path. This is done by modifying the activation script of your virtual environment.

Open the activate script located in the bin directory of your virtual environment:

```bash
nano venv/bin/activate
```

Scroll down to the end of the file and add the following line:

```bash
export PYTHONPATH="$PYTHONPATH:$(pwd)/AWSLambda/aws/src/layers/shared_code_layer"
```

This line adds the directory **./AWSLambda/aws/src/layers/shared_code_layer** relative to the current directory ($(pwd)) to your Python path.

Save the file and exit the text editor.

## Step 3: Reactivating the Virtual Environment

Finally, deactivate and reactivate your virtual environment for the changes to take effect:

```bash
deactivate
source venv/bin/activate
```

Now Python should be able to find the required modules. You can verify this by trying to import one of the modules. If Python doesn't raise an ImportError, the setup was successful.

_This README assumes that developers are using a Unix-like environment (like Linux or macOS), since it uses commands like `source` and `nano`. If developers are using a different environment (like Windows), the instructions will need to be adapted accordingly._
