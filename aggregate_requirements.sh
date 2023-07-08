# Find all requirements.txt files and concatenate them into one
find . -name 'requirements.txt' -exec cat {} + > all_requirements.txt

# Now install the dependencies from the aggregated file
pip install -r all_requirements.txt
