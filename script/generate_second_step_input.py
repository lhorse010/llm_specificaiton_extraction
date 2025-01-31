from poe_api_wrapper import PoeApi
import sys
import os
import json

def create_directory_if_not_exists(directory_path):
    if not os.path.exists(directory_path):
        try:
            os.makedirs(directory_path)
            print(f"Directory created: {directory_path}")
        except OSError as e:
            print(f"Error creating directory: {e}")
    else:
        print(f"Directory already exists: {directory_path}")

def create_file_if_not_exists(file_path):
    if os.path.isfile(file_path):
        print(f"File already exists: {file_path}")
    else:
        try:
            with open(file_path, 'w') as f:
                pass
            print(f"File created: {file_path}")
        except IOError as e:
            print(f"Error creating file: {e}")

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
    
    for json_string in json_strings:
        try:
            json_obj = json.loads(json_string)
            if "specifications" in json_obj and isinstance(json_obj["specifications"], list):
                if all("section-id" in item and "sentence-id" in item 
                       for item in json_obj["specifications"]):
                    return json_obj["specifications"]
        except json.JSONDecodeError:
            continue
    
    return None

def merge_specifications(file_paths):
    all_specifications = []
    
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            specifications = extract_specifications_json(content)
            if specifications:
                all_specifications.extend(specifications)
    
    # Remove duplicates while preserving order
    unique_specifications = []
    seen = set()
    for spec in all_specifications:
        spec_tuple = tuple(sorted(spec.items()))  # Sort to ensure consistent ordering
        if spec_tuple not in seen:
            seen.add(spec_tuple)
            unique_specifications.append(spec)
    
    return unique_specifications

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def count_specifications(data):
    return len(data['specifications'])

def get_specification_set(data):
    return set((spec['section-id'], spec['sentence-id']) for spec in data['specifications'])

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
    
    for json_string in json_strings:
        try:
            json_obj = json.loads(json_string)
            if "specifications" in json_obj and isinstance(json_obj["specifications"], list):
                if all("section-id" in item and "sentence-id" in item 
                       for item in json_obj["specifications"]):
                    return json_obj["specifications"]
        except json.JSONDecodeError:
            continue
    
    return None

def find_sentence(json_obj, section_id, sentence_id):
    try:
        # Iterate through all sections in the JSON object
        for section in json_obj['sections']:
            # Check if the current section's ID matches the desired section_id
            if section['section-id'] == section_id:
                # Iterate through all sentences in the matching section
                for sentence in section['sentences']:
                    # Check if the current sentence's ID matches the desired sentence_id
                    if sentence['sentence-id'] == sentence_id:
                        # Return the text of the matching sentence
                        return sentence['text']
        
        # If no matching sentence is found, return an error message
        return None
    except KeyError:
        # If the JSON structure is invalid (missing expected keys), return an error message
        return "Error: Invalid JSON structure."

def dump_json_to_file(json_data, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(json_data, file, ensure_ascii=False, indent=2)
        print(f"JSON data successfully saved to {file_path}")
        return True
    except Exception as e:
        print(f"An error occurred while saving the JSON data: {str(e)}")
        return False

if __name__ == "__main__":
    model_name = sys.argv[1]
    doc_dir_name = sys.argv[2]
    doc_file_name = sys.argv[3]
    
    file = open("../dataset/input/" + doc_dir_name + "/text_only/" + doc_file_name + ".json", "r")
    all_sentence_obj = json.load(file)
    file.close()

    extract_spec_file_name = "./result_annotate/" + doc_dir_name + "/" + doc_file_name + "/" + model_name + "_merge.txt"
    second_step_input_list = []
    with open(extract_spec_file_name, 'r', encoding='utf-8') as file:
        content = file.read()
        json_obj = json.loads(content)

        # result_file: second_step_input/doc_dir/mode_name/model.txt
        if "specifications" in json_obj and isinstance(json_obj["specifications"], list):
            for item in json_obj["specifications"]:
                input_item = {}
                input_item["section-id"] = item["section-id"]
                input_item["sentence-id"] = item["sentence-id"]
                input_item['sentence'] = find_sentence(all_sentence_obj, item["section-id"], item["sentence-id"])
                if input_item["sentence"] == None:
                    continue
                second_step_input_list.append(input_item)
        
    print(second_step_input_list)

    # result_file: second_step_input/doc_dir/mode_name/model.txt
    result_file_dir = "./second_step_input/" + doc_dir_name + "/" + doc_file_name
    create_directory_if_not_exists(result_file_dir)
    result_file_name = result_file_dir + "/" + model_name + ".json"
    result_file = open(result_file_name, "w")
    result_file.write("")
    result_file.close()
    dump_json_to_file(second_step_input_list, result_file_name)