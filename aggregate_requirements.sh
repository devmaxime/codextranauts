# Initialize all_requirements.txt as an empty file
> all_requirements.txt

# Find all requirements.txt files
files=$(find . -name requirements.txt)

# Check if any files were found
if [ -z "$files" ]; then
    echo "No requirements.txt files found"
    exit 1
else
    for file in $files; do
        cat "$file" >> all_requirements.txt
        # Ensure there is a newline at the end of the file
        echo "" >> all_requirements.txt
    done
fi

# Sort the lines in the file and remove duplicates
sort all_requirements.txt | uniq > temp_requirements.txt

# Overwrite the original file with the cleaned version and remove the temp file
mv temp_requirements.txt all_requirements.txt
