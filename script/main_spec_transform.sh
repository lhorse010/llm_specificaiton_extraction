# Define the array
models=("Claude-3.5-Sonnet" "GPT-4o" "Llama-3.1-405B-T")

# Define docs_dirs
docs_dirs=("ardupilot_docs" "autoware_docs" "px4_docs")

# Declare arrays to store filenames for each directory
declare -a ardupilot_files
declare -a autoware_files
declare -a px4_files

# Function to store filenames in the appropriate array
store_files() {
    local dir=$1
    local array_name=$2
    local full_path="../dataset/reapeat/${dir}/text_only/"
    
    if [ -d "$full_path" ]; then
        local IFS=$'\n'  # Change IFS to newline
        for file in $(find "$full_path" -type f); do
            # Get basename without extension
            local basename_no_ext=$(basename "$file" | sed 's/\.[^.]*$//')
            eval "$array_name+=(\"$basename_no_ext\")"
        done
    else
        echo "Warning: Directory $full_path not found"
    fi
}

# Loop through each directory and store files
for dir in "${docs_dirs[@]}"; do
    case $dir in
        "ardupilot_docs")
            store_files "$dir" ardupilot_files
            ;;
        "autoware_docs")
            store_files "$dir" autoware_files
            ;;
        "px4_docs")
            store_files "$dir" px4_files
            ;;
    esac
done

# Print the number of files found in each directory
echo "Number of files in ardupilot_docs: ${#ardupilot_files[@]}"
echo "Number of files in autoware_docs: ${#autoware_files[@]}"
echo "Number of files in px4_docs: ${#px4_files[@]}"

for file in "${ardupilot_files[@]}"; do
    echo "========================$file========================"
    # Loop through the array
    for model in "${models[@]}"; do
        echo "Processing model: $model"
        python llm_doc_spec_transform.py $model "ardupilot_docs" $file
    done
done

for file in "${autoware_files[@]}"; do
    echo "========================$file========================"
    # Loop through the array
    for model in "${models[@]}"; do
        echo "Processing model: $model"
        python llm_doc_spec_transform.py $model "autoware_docs" $file
    done
done

for file in "${px4_files[@]}"; do
    echo "========================$file========================"
    # Loop through the array
    for model in "${models[@]}"; do
        echo "Processing model: $model"
        python llm_doc_spec_transform.py $model "px4_docs" $file
    done
done