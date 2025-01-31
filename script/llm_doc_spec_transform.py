from poe_api_wrapper import PoeApi
import sys
import os
import json

tokens = {
    'p-b': os.getenv('ENV_P_B'), 
    'p-lat': os.getenv('ENV_P_LAT'),
}

def generate_prompt(doc_chunk):
    with open("doc_spec_transform_prompt.txt", "r") as prompt_file:
        prompt = prompt_file.read()
    prompt += json.dumps(doc_chunk, indent=2)
    return prompt

def extract(prompt, model_name, client):
    bot = model_name
    for chunk in client.send_message(bot=bot, message=prompt):
        pass
    return chunk["text"]

def create_directory_if_not_exists(directory_path):
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
        if char == '[':
            if not stack:
                start = i
            stack.append(i)
        elif char == ']':
            if stack:
                stack.pop()
                if not stack:
                    result.append(text[start:i+1])
            
    return result

def process_document(doc, model_name, client, chunk_size=10):
    results = []
    for i in range(0, len(doc), chunk_size):
        chunk = doc[i:i+chunk_size]
        prompt = generate_prompt(chunk)
        result = extract(prompt, model_name, client)
        json_strings = extract_outer_braces(result)
    
        for json_string in json_strings:
            try:
                json_obj = json.loads(json_string) 
                for item in json_obj:
                    results.append(item)
            except json.JSONDecodeError:
                continue
        print(f"Processed chunk {i//chunk_size + 1}/{(len(doc)-1)//chunk_size + 1}")
    return results

if __name__ == "__main__":
    model_name = sys.argv[1]
    doc_dir_name = sys.argv[2]
    doc_file_name = sys.argv[3]
    
    input_file_path = f"./second_step_input/{doc_dir_name}/{doc_file_name}/{model_name}.json"
    with open(input_file_path, "r") as file:
        doc = json.load(file)
    
    client = PoeApi(tokens=tokens)
    
    result_file_dir = f"./result_llm_tranform/{doc_dir_name}/{doc_file_name}"
    create_directory_if_not_exists(result_file_dir)
    
    result_file_name = f"{result_file_dir}/{model_name}.txt"
    
    result = process_document(doc, model_name, client)
    
    with open(result_file_name, "w") as result_file:
        json.dump(result,  result_file, ensure_ascii=False, indent=2)
    
    print(f"Processing complete. Results saved to {result_file_name}")