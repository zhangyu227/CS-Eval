import json

def convert_format(input_file, output_file):
    # 读取JSON数组格式的数据
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    converted_data = []
    for item in data:
        try:
            # 从input中提取生成结果部分
            input_text = item["input"]
            parts = input_text.split("生成结果：")
            
            if len(parts) > 1:
                new_input = parts[0].strip()
                new_output = parts[1].strip()
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
            
        except Exception as e:
            print(f"处理错误: {e}")
            print(f"问题数据: {item}")
            continue

    with open(output_file, 'w', encoding='utf-8') as f:
        for item in converted_data:
           
            json_str = json.dumps(item, ensure_ascii=False, indent=4)
            f.write(json_str + '\n')

# 使用示例
input_file = "train_ethics.json"  # 您的输入文件路径
output_file = "转换后数据.json"  # 输出文件路径
convert_format(input_file, output_file)