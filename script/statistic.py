import sys

def file_statistics(file_path):
    total_lines = 0
    empty_lines = 0
    total_chars = 0
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                total_lines += 1
                total_chars += len(line)
                
                # 检查空行（包括只有空格或制表符的行）
                if not line.strip():
                    empty_lines += 1
                    
        return {
            'total_lines': total_lines,
            'total_chars': total_chars,
            'empty_lines': empty_lines,
            'non_empty_lines': total_lines - empty_lines
        }
        
    except FileNotFoundError:
        print(f"错误：找不到文件 '{file_path}'")
        return None
    except Exception as e:
        print(f"读取文件时发生错误: {e}")
        return None

def main():
    doc_dir_name = sys.argv[1]
    doc_file_name = sys.argv[2]

    file_path = "/Users/lihui/research/llm_specificaiton_extraction/dataset/document_after_manual_check/" + doc_dir_name + "/text_only/" + doc_file_name + ".txt"
    stats = file_statistics(file_path)
    
    if stats:
        print("\n文件统计结果:")
        print(f"总行数: {stats['total_lines']}")
        print(f"总字符数: {stats['total_chars']}")
        print(f"空行数: {stats['empty_lines']}")
        print(f"非空行数: {stats['non_empty_lines']}")
    else:
        return

if __name__ == "__main__":
    main()