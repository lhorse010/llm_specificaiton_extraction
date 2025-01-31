from poe_api_wrapper import PoeApi
import sys
import os
import json


# Repeat to merge
Repeat_Number = 3

def create_directory_if_not_exists(directory_path):
    """
    Check if the directory at the specified path exists, and create it if it doesn't.

    :param directory_path: The path of the directory to check and create
    """
    if not os.path.exists(directory_path):
        try:
            os.makedirs(directory_path)
            print(f"Directory created: {directory_path}")
        except OSError as e:
            print(f"Error creating directory: {e}")
    else:
        print(f"Directory already exists: {directory_path}")

def extract_outer_braces(text):
    result = []
    stack = []
    start = -1
    
    for i, char in enumerate(text):
        if char == '{':
            if not stack:
                start = i
            stack.append(i)
        elif char == '}':
            if stack:
                stack.pop()
                if not stack:
                    result.append(text[start:i+1])
            
    return result

def extract_specifications_json(text):
    json_strings = extract_outer_braces(text)
    result = []
    index = 0
    for json_string in json_strings:
        try:
            json_obj = json.loads(json_string)
            if "specifications" in json_obj and isinstance(json_obj["specifications"], list):
                    for item in json_obj["specifications"]:
                        spec_item = {}
                        spec_item["index"] = index
                        index += 1
                        spec_item["formula"] = item["formula"]
                        spec_item["explanation"] = item["explanation"]
                        result.append(spec_item)
                    return result
        except json.JSONDecodeError:
            continue
    
    return None

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def count_specifications(data):
    return len(data['specifications'])

def get_specification_set(data):
    return set((spec['section-id'], spec['sentence-id']) for spec in data['specifications'])

if __name__ == "__main__":
    model_name = sys.argv[1]
    doc_dir_name = sys.argv[2]
    doc_file_name = sys.argv[3]
    
    # result_file: result_end_to_end/doc_dir/mode_name/model.txt
    result_file_dir = "./result_end_to_end/" + doc_dir_name + "/" + doc_file_name
    create_directory_if_not_exists(result_file_dir)
    
    for i in range(0, Repeat_Number):
        result_file_name = result_file_dir + "/" + model_name + "_" + str(i) + ".txt"
        result_file = open(result_file_name, "r")
        spec = extract_specifications_json(result_file.read())
        result_file.close()
        print(spec)

        result_with_index_file_name = result_file_dir + "/" + model_name + "_with_index_" + str(i) + ".txt"        
        with open(result_with_index_file_name, 'w', encoding='utf-8') as outfile:
            json.dump(spec, outfile, ensure_ascii=False, indent=2)


