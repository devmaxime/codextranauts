# Find all requirements.txt files and concatenate them into one
echo "" > all_requirements.txt

for file in $(find . -name requirements.txt)
do
    cat $file >> all_requirements.txt
    echo "" >> all_requirements.txt
done