# llm_specificaiton_extraction

## Description

This project  explores the end-to-end specification extraction capabilities of LLMs and proposes a two-stage annotation-then-conversion method. 

​	The method includes two agents: sentence annotation and temporal logic conversion. They are responsible for extracting sentences containing specification information from documents and converting a single sentence into a temporal logic formula.



## Project Structure

```
llm_specificaiton_extraction
├── dataset/              	             # Collected document and preprocess result
├── experiement_data/                        # raw data of empirical study and experiment 1 & 2 
├── script/                              # code of method 
├── test                                 # Scattered testing code
└── README.md                            # Project documentation
```

​	Note: Prompt template is in `./script/doc_spc_extraction_end_to_end_prompt.txt`, `./script/doc_sentences_spec_annotate_prompt.txt` and `./script/doc_spec_transform_prompt.txt`

## Dataset

### 1.raw document dataset

  21 documents of Ardupilot

  11 documents of PX4

  5 documents of Autoware

### 2.data process

```shell
####remove structural information, links and references, multi-modal elements; sentence slicing####
# markdown
python md_process.py document_dir_name
# rst
python rst_process.py document_dir_name

####generate input(json)####
python generate_input.py

# check result
# ./dataset/document_after_manual_check

```



## Environment Set

Set cookies before invoking poe LLM agent: https://github.com/snowby666/poe-api-wrapper

```shell
## poe cookie
export ENV_P_B='...'
export ENV_P_LAT='...'
```



## Usage

### 1.LLM end to end

```shell
#### run ####
cd script
# prompt: doc_spc_extraction_end_to_end_prompt.txt
./main_spec_extract_end_to_end.sh

#### check  result ####
# cd ./result_end_to_end
```

### 2.LLM annotate + conversion

#### 2.1 LLM annotate

```shell
#### run ####
cd script
# prompt: doc_sentences_spec_annotate_prompt.txt
./main_annotate.sh
# to generate input json file of transform process
./generate_second_step_input.sh

#### check result ####
# cd ./result_annotate
# cd ./second_step_input
```

#### 2.2 LLM specificaiton conversion

```shell
#### run ####
cd script
# prompt: doc_spec_transform_prompt.txt
./main_spec_transform.sh

#### check result ####
# cd ./result_llm_tranform
```

#### 2.3 DeeSTL specification conversion

```shell
#### run ####
# follow the set up guaidence in https://github.com/JieHE-2020/DeepSTL
# to use input genetrate by our method
# use
# ./script/transformer_run.py

#### check result ####
# cd ./DeepSTL_convert
```



## Result

### 1. LLM end-to-end

| Document              | Claude-3.5<br />-Sonnet |      | GPT-4o |      | Llama-3.1<br />-405B-T |      | GroundTruth |
| ------------------- | ----------------------- | ---- | ------ | ---- | ---------------------- | ---- | ----------- |
|                     | r                       | w    | r      | w    | r                      | w    |             |
| AP:Airmode          | 6                       | 0    | 7      | 0    | 6                      | 0    | 8           |
| AP:Auto             | 10                      | 2    | 14     | 6    | 13                     | 8    | 29          |
| AP:Brake            | 7                       | 1    | 3      | 1    | 6                      | 1    | 8           |
| AP:Circle           | 15                      | 0    | 16     | 0    | 16                     | 0    | 25          |
| AP:Drift            | 10                      | 2    | 7      | 2    | 9                      | 1    | 14          |
| AP:Flip             | 7                       | 1    | 7      | 7    | 6                      | 4    | 9           |
| AP:FlowHold         | 7                       | 1    | 4      | 5    | 4                      | 3    | 8           |
| AP:Follow           | 5                       | 8    | 8      | 4    | 10                     | 7    | 12          |
| AP:Guided           | 8                       | 4    | 8      | 6    | 9                      | 3    | 27          |
| AP:Heli_Autorotate  | 7                       | 4    | 14     | 2    | 2                      | 7    | 31          |
| AP:Land             | 9                       | 1    | 6      | 2    | 8                      | 1    | 11          |
| AP:Loiter           | 8                       | 2    | 7      | 2    | 9                      | 4    | 15          |
| AP:PosHold          | 8                       | 1    | 5      | 1    | 7                      | 1    | 11          |
| AP:RTL              | 15                      | 1    | 13     | 4    | 15                     | 4    | 44          |
| AP:Simple           | 6                       | 4    | 7      | 1    | 8                      | 1    | 19          |
| AP:SmartRTL         | 12                      | 1    | 11     | 3    | 12                     | 1    | 20          |
| AP:Sport            | 4                       | 0    | 4      | 1    | 5                      | 0    | 7           |
| AP:Stabilize        | 11                      | 1    | 10     | 4    | 9                      | 6    | 14          |
| AP:SysID            | 3                       | 0    | 2      | 0    | 3                      | 1    | 3           |
| AP:Throw            | 9                       | 0    | 9      | 1    | 6                      | 3    | 19          |
| AP:Turtle           | 7                       | 1    | 3      | 2    | 5                      | 1    | 12          |
| PX4:Position        | 9                       | 0    | 5      | 0    | 5                      | 0    | 20          |
| PX4:Position Slow   | 10                      | 3    | 9      | 0    | 5                      | 8    | 23          |
| PX4:Altitude        | 11                      | 1    | 7      | 2    | 9                      | 2    | 17          |
| PX4:Stabilized      | 10                      | 4    | 5      | 0    | 6                      | 2    | 16          |
| PX4:Acro            | 4                       | 3    | 2      | 0    | 3                      | 0    | 5           |
| PX4:Hold            | 9                       | 2    | 8      | 4    | 5                      | 2    | 13          |
| PX4:Return          | 10                      | 3    | 10     | 6    | 11                     | 4    | 22          |
| PX4:Mission         | 13                      | 2    | 13     | 2    | 10                     | 4    | 39          |
| PX4:Takeoff         | 8                       | 2    | 7      | 2    | 7                      | 2    | 11          |
| PX4:Land            | 11                      | 0    | 7      | 2    | 5                      | 2    | 13          |
| PX4:Orbit           | 10                      | 0    | 12     | 3    | 14                     | 3    | 27          |
| AW:Blind Spot       | 4                       | 1    | 4      | 0    | 4                      | 1    | 5           |
| AW:Traffic Light    | 8                       | 2    | 9      | 1    | 6                      | 0    | 9           |
| AW:Detection Area   | 7                       | 0    | 5      | 2    | 6                      | 0    | 8           |
| AW:No Drivable Lane | 3                       | 0    | 4      | 0    | 5                      | 0    | 8           |
| AW:Out of Lane      | 11                      | 4    | 12     | 5    | 5                      | 1    | 21          |
| Sum                 | 312                     | 62   | 284    | 83   | 274                    | 88   | 603         |
| Accuracy            | 51.7%                   |      | 47.1%  |      | 45.4%                  |      | -           |
| False Positive      | 16.6%                   |      | 22.6%  |      | 24.3%                  |      | -           |



## 2.LLM annotation + LLM conversion

| Document              | Claude-3.5<br />-Sonnet |      | GPT-4o |      | Llama-3.1<br />-405B-T |      | GroundTruth |
| ------------------- | ----------------------- | ---- | ------ | ---- | ---------------------- | ---- | ----------- |
|                     | r                       | w    | r      | w    | r                      | w    |             |
| AP:Airmode          | 7                       | 0    | 4      | 0    | 6                      | 0    | 8           |
| AP:Auto             | 22                      | 1    | 18     | 1    | 19                     | 9    | 29          |
| AP:Brake            | 4                       | 2    | 5      | 1    | 6                      | 2    | 8           |
| AP:Circle           | 21                      | 3    | 18     | 1    | 19                     | 4    | 25          |
| AP:Drift            | 12                      | 3    | 7      | 1    | 9                      | 2    | 14          |
| AP:Flip             | 7                       | 3    | 8      | 2    | 4                      | 4    | 9           |
| AP:FlowHold         | 5                       | 3    | 2      | 1    | 5                      | 2    | 8           |
| AP:Follow           | 11                      | 2    | 8      | 1    | 3                      | 3    | 12          |
| AP:Guided           | 16                      | 6    | 10     | 5    | 19                     | 8    | 27          |
| AP:Heli_Autorotate  | 13                      | 4    | 11     | 10   | 14                     | 6    | 31          |
| AP:Land             | 9                       | 1    | 6      | 3    | 7                      | 1    | 11          |
| AP:Loiter           | 9                       | 6    | 8      | 3    | 7                      | 3    | 15          |
| AP:PosHold          | 8                       | 1    | 3      | 2    | 4                      | 1    | 11          |
| AP:RTL              | 28                      | 1    | 15     | 5    | 39                     | 5    | 44          |
| AP:Simple           | 10                      | 1    | 5      | 3    | 14                     | 3    | 19          |
| AP:SmartRTL         | 16                      | 2    | 12     | 0    | 13                     | 0    | 20          |
| AP:Sport            | 4                       | 1    | 4      | 1    | 4                      | 2    | 7           |
| AP:Stabilize        | 12                      | 2    | 7      | 4    | 12                     | 1    | 14          |
| AP:SysID            | 3                       | 0    | 2      | 0    | 3                      | 0    | 3           |
| AP:Throw            | 13                      | 0    | 13     | 1    | 11                     | 0    | 19          |
| AP:Turtle           | 8                       | 1    | 9      | 0    | 7                      | 1    | 12          |
| PX4:Position        | 18                      | 4    | 8      | 2    | 11                     | 5    | 20          |
| PX4:Position Slow   | 16                      | 2    | 15     | 0    | 4                      | 4    | 23          |
| PX4:Altitude        | 12                      | 1    | 7      | 2    | 15                     | 2    | 17          |
| PX4:Stabilized      | 11                      | 4    | 8      | 0    | 12                     | 4    | 16          |
| PX4:Acro            | 4                       | 1    | 4      | 0    | 4                      | 5    | 5           |
| PX4:Hold            | 11                      | 1    | 6      | 1    | 5                      | 2    | 13          |
| PX4:Return          | 18                      | 1    | 15     | 3    | 15                     | 2    | 22          |
| PX4:Mission         | 25                      | 4    | 12     | 4    | 28                     | 14   | 39          |
| PX4:Takeoff         | 8                       | 1    | 7      | 0    | 7                      | 1    | 11          |
| PX4:Land            | 12                      | 0    | 7      | 0    | 10                     | 0    | 13          |
| PX4:Orbit           | 15                      | 1    | 10     | 3    | 10                     | 4    | 27          |
| AW:Blind Spot       | 4                       | 1    | 4      | 0    | 4                      | 1    | 5           |
| AW:Traffic Light    | 9                       | 1    | 9      | 0    | 9                      | 1    | 9           |
| AW:Detection Area   | 8                       | 0    | 7      | 0    | 7                      | 2    | 8           |
| AW:No Drivable Lane | 6                       | 2    | 4      | 3    | 6                      | 2    | 8           |
| AW:Out of Lane      | 17                      | 6    | 12     | 9    | 10                     | 4    | 21          |
| Sum                 | 432                     | 73   | 310    | 72   | 382                    | 110  | 603         |
| Accuracy            | 71.6%                   |      | 51.4%  |      | 63.3%                  |      | -           |
| False Positive      | 14.5%                   |      | 18.8%  |      | 22.4%                  |      | -           |

## 3.LLM annotation + DeepSTL conversion

| Document              | Claude-3.5<br />-Sonnet |      | GPT-4o |      | Llama-3.1<br />-405B-T |      | GroundTruth |
| ------------------- | ----------------------- | ---- | ------ | ---- | ---------------------- | ---- | ----------- |
|                     | r                       | w    | r      | w    | r                      | w    |             |
| AP:Airmode          | 0                       | 6    | 0      | 4    | 0                      | 7    | 8           |
| AP:Auto             | 1                       | 22   | 1      | 18   | 1                      | 27   | 29          |
| AP:Brake            | 0                       | 6    | 0      | 6    | 0                      | 8    | 8           |
| AP:Circle           | 0                       | 24   | 0      | 19   | 0                      | 23   | 25          |
| AP:Drift            | 2                       | 13   | 1      | 7    | 2                      | 9    | 14          |
| AP:Flip             | 1                       | 9    | 1      | 9    | 1                      | 7    | 9           |
| AP:FlowHold         | 1                       | 7    | 0      | 3    | 1                      | 6    | 8           |
| AP:Follow           | 1                       | 12   | 1      | 8    | 0                      | 6    | 12          |
| AP:Guided           | 1                       | 21   | 0      | 15   | 1                      | 26   | 27          |
| AP:Heli_Autorotate  | 5                       | 12   | 5      | 16   | 3                      | 17   | 31          |
| AP:Land             | 0                       | 10   | 0      | 9    | 0                      | 8    | 11          |
| AP:Loiter           | 3                       | 7    | 4      | 7    | 3                      | 12   | 15          |
| AP:PosHold          | 3                       | 6    | 1      | 4    | 1                      | 4    | 11          |
| AP:RTL              | 2                       | 27   | 2      | 18   | 4                      | 40   | 44          |
| AP:Simple           | 0                       | 11   | 0      | 8    | 0                      | 17   | 19          |
| AP:SmartRTL         | 0                       | 18   | 0      | 12   | 0                      | 13   | 20          |
| AP:Sport            | 1                       | 4    | 0      | 5    | 1                      | 5    | 7           |
| AP:Stabilize        | 0                       | 14   | 0      | 11   | 0                      | 13   | 14          |
| AP:SysID            | 0                       | 3    | 0      | 2    | 0                      | 3    | 3           |
| AP:Throw            | 4                       | 9    | 4      | 10   | 3                      | 8    | 19          |
| AP:Turtle           | 1                       | 8    | 1      | 8    | 1                      | 7    | 12          |
| PX4:Position        | 0                       | 22   | 0      | 10   | 0                      | 16   | 20          |
| PX4:Position Slow   | 0                       | 18   | 0      | 15   | 0                      | 8    | 23          |
| PX4:Altitude        | 3                       | 10   | 0      | 9    | 3                      | 14   | 17          |
| PX4:Stabilized      | 3                       | 12   | 2      | 6    | 3                      | 13   | 16          |
| PX4:Acro            | 1                       | 4    | 1      | 3    | 1                      | 8    | 5           |
| PX4:Hold            | 1                       | 11   | 1      | 6    | 1                      | 6    | 13          |
| PX4:Return          | 1                       | 18   | 1      | 17   | 1                      | 17   | 22          |
| PX4:Mission         | 2                       | 27   | 1      | 15   | 3                      | 39   | 39          |
| PX4:Takeoff         | 0                       | 9    | 0      | 7    | 0                      | 8    | 11          |
| PX4:Land            | 1                       | 11   | 1      | 6    | 1                      | 9    | 13          |
| PX4:Orbit           | 4                       | 12   | 0      | 13   | 3                      | 11   | 27          |
| AW:Blind Spot       | 0                       | 5    | 0      | 4    | 0                      | 5    | 5           |
| AW:Traffic Light    | 1                       | 9    | 1      | 8    | 1                      | 9    | 9           |
| AW:Detection Area   | 1                       | 7    | 1      | 6    | 1                      | 8    | 8           |
| AW:No Drivable Lane | 0                       | 8    | 0      | 7    | 0                      | 8    | 8           |
| AW:Out of Lane      | 2                       | 21   | 2      | 19   | 2                      | 12   | 21          |
| Sum                 | 46                      | 453  | 32     | 350  | 42                     | 457  | 603         |
| Accuracy            | 7.6%                    |      | 5.3%   |      | 7.0%                   |      | -           |
| False Positive      | 90.8%                   |      | 91.6%  |      | 91.6%                  |      | -           |
