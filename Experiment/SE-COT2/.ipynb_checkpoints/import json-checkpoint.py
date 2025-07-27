import json
import re

def convert_format(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = f.readlines()
    
    converted_data = []
    for line in data:
        try:
            item = json.loads(line.strip())
            
            input_text = item["input"]
            match = re.search(r"生成结果:(.*?)(?=$)", input_text)
            
            if match:
                new_input = input_text.split("生成结果:")[0].strip()
                new_output = match.group(1).strip()
            else:
                new_input = input_text
                new_output = ""
            
            # 构建新格式
            new_item = {
                "instruction": item["instruction"].replace("①", "@").replace("②", "@").replace("③", "@").replace("④", "@"),
                "input": new_input,
                "output": new_output,
                "answer": item.get("output", "")  
            }
            
            converted_data.append(new_item)
            
        except json.JSONDecodeError as e:
            print(f"解析错误: {e}")
            continue
    
    # 写入新文件
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in converted_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

# 使用示例
input_file = "original_data.jsonl"
output_file = "converted_data.jsonl"
convert_format(input_file, output_file)