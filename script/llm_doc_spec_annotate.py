from poe_api_wrapper import PoeApi
import sys
import os
import json

tokens = {
    'p-b': os.getenv('ENV_P_B'), 
    'p-lat': os.getenv('ENV_P_LAT'),
}

# proxy 
proxy_config = [
    {
        "https://": os.getenv('HTTPS_POE_PROXY'),
        "http://": os.getenv('HTTP_POE_PROXY')
    }
]

# Repeat to merge
Repeat_Number = 3

def generate_prompt(doc):
    prompt_file = open("doc_sentences_spec_annotate_prompt.txt", "r")
    prompt = prompt_file.read()
    prompt_file.close()
    prompt += "#@#@#@#@#@\n\n"
    prompt += doc
    prompt += "\n\n#@#@#@#@#@"
    return prompt

def extract(prompt, model_name, result_file):
    # clear context, triple try, merge
    # client = PoeApi(tokens=tokens, proxy=proxy_config)
    print(tokens)
    client = PoeApi(tokens=tokens)
    bot=model_name
    chatId = None    

    for chunk in client.send_message(bot=bot, message=prompt, chatId=chatId):
        # non stream version
        pass
    print(chunk["text"], file=result_file, end='', flush=True)

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

if __name__ == "__main__":
    model_name = sys.argv[1]
    doc_dir_name = sys.argv[2]
    doc_file_name = sys.argv[3]
    
    file = open("../dataset/input/" + doc_dir_name + "/text_only/" + doc_file_name + ".json", "r")
    doc = file.read()
    file.close()
    
    prompt = generate_prompt(doc)

    # result_file: result_annotate/doc_dir/mode_name/model.txt
    result_file_dir = "./result_annotate/" + doc_dir_name + "/" + doc_file_name
    create_directory_if_not_exists(result_file_dir)
    
    for i in range(0, Repeat_Number):
        result_file_name = result_file_dir + "/" + model_name + "_" + str(i) + ".txt"
        result_file = open(result_file_name, "w")
        result_file.write("")
        result_file.close()
        
        result_file = open(result_file_name, "w+")
        extract(prompt, model_name, result_file)
        result_file.close()

    # merge result
    file_paths = []
    for i in range(0, Repeat_Number):
        result_file_name = result_file_dir + "/" + model_name + "_" + str(i) + ".txt"
        file_paths.append(result_file_name)
    
    merged_specs = merge_specifications(file_paths)
    result = {"specifications": merged_specs}
    
    # Write the result to merge.json
    result_file_name = result_file_dir + "/" + model_name + "_merge" + ".txt"
    with open(result_file_name, 'w', encoding='utf-8') as outfile:
        json.dump(result, outfile, ensure_ascii=False, indent=2)

    # result_data = load_json(result_file_name)
    # groundtruth_file_name = "../dataset/ground_truth/" + doc_dir_name + "/location/" + doc_file_name + ".txt"
    # groundtruth_data = load_json(groundtruth_file_name)
    # result_count = count_specifications(result_data)
    # groundtruth_count = count_specifications(groundtruth_data)

    # result_set = get_specification_set(result_data)
    # groundtruth_set = get_specification_set(groundtruth_data)
    # intersection = result_set.intersection(groundtruth_set)
    # intersection_count = len(intersection)

    # output = f"{doc_dir_name} "
    # output += f"{doc_file_name} "
    # output += f"{model_name} "
    # # result_count: 
    # output += f"{result_count} "
    # # groundtruth_count: 
    # output += f"{groundtruth_count} "
    # # intersection_count: 
    # output += f"{intersection_count}\n"

    # with open('./result/result_all.txt', 'a') as file:
    #     file.write(output)
