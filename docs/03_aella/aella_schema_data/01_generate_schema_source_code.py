import json
import os
import glob
import re
from typing import Any, Dict, List, Union

# --- 配置 ---
OUTPUT_FILE = "generated_models.py"

# --- 辅助函数：将文件名转换为类名 ---
def filename_to_classname(filename):
    # 去掉扩展名和开头的数字序号
    name = os.path.splitext(filename)[0]
    name = re.sub(r'^\d+_', '', name)
    # 将逗号替换为下划线，处理 papers,123 这种情况
    name = name.replace(',', '_')
    # 转为帕斯卡命名 (PascalCase)
    components = re.split(r'[_\-/]', name)
    return "".join(x.title() for x in components) + "Response"

# --- 核心逻辑：递归生成 Pydantic 模型 ---
class PydanticGenerator:
    def __init__(self):
        self.models = {}  # 存储生成的模型定义 {class_name: code_string}
        self.root_models = [] # 记录根模型名称

    def get_type_name(self, value, key_name):
        if value is None:
            return "Optional[Any]"
        elif isinstance(value, bool):
            return "bool"
        elif isinstance(value, int):
            return "int"
        elif isinstance(value, float):
            return "float"
        elif isinstance(value, str):
            return "str"
        elif isinstance(value, list):
            if not value:
                return "List[Any]"
            # 假设列表内容是同构的，取第一个元素分析
            item_type = self.get_type_name(value[0], key_name)
            # 如果 item_type 包含 Optional，处理一下
            return f"List[{item_type}]"
        elif isinstance(value, dict):
            # 如果是字典，需要创建一个新模型
            # 构造子模型名称，例如 ParentKey + CurrentKey
            sub_class_name = "".join(x.title() for x in key_name.split('_'))
            if not sub_class_name: sub_class_name = "Item"
            
            # 递归生成子模型
            return self.generate_model(value, sub_class_name)
        return "Any"

    def generate_model(self, data: Dict[str, Any], class_name: str) -> str:
        # 如果这个类名已经存在但结构不同，为了简单起见，我们加个后缀或者直接复用（这里简单复用）
        # 实际工程中可能需要更复杂的去重逻辑，这里为了演示，如果类名冲突，我们尝试加个后缀
        original_class_name = class_name
        counter = 1
        while class_name in self.models:
            # 简单比对：如果内容完全不一样才改名，否则复用
            # 这里简化处理：只要名字一样就假设是同一个结构（或者是递归调用）
            return class_name
            # 如果要严格区分，可以开启下面的逻辑：
            # class_name = f"{original_class_name}{counter}"
            # counter += 1

        fields = []
        
        # 遍历字典的所有 Key
        for key, value in data.items():
            field_type = self.get_type_name(value, key)
            # 处理字段名为 Python 关键字的情况 (如 class, for 等)
            safe_key = key
            if key in ['class', 'def', 'return', 'import', 'from', 'global']:
                safe_key = f"{key}_"
                fields.append(f"    {safe_key}: {field_type} = Field(..., alias='{key}')")
            else:
                fields.append(f"    {key}: {field_type}")

        # 组装类定义代码
        model_code = [f"class {class_name}(BaseModel):"]
        if not fields:
            model_code.append("    pass")
        else:
            model_code.extend(fields)
        
        # 存入 models 字典
        self.models[class_name] = "\n".join(model_code)
        return class_name

    def process_file(self, filepath):
        filename = os.path.basename(filepath)
        print(f"Analyzing {filename}...")
        
        root_class_name = filename_to_classname(filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print(f"Skipping {filename} - Invalid JSON")
                return

        # 处理根节点是列表的情况
        if isinstance(data, list):
            # 如果根是列表，我们创建一个包装类，或者只分析列表项
            if data:
                item_class_name = root_class_name.replace("Response", "Item")
                self.generate_model(data[0], item_class_name)
                # 记录这是一个 List[Item] 类型
                self.root_models.append(f"# File: {filename}\n# Root type is List[{item_class_name}]")
            else:
                self.root_models.append(f"# File: {filename}\n# Root type is List[Any]")
        elif isinstance(data, dict):
            self.generate_model(data, root_class_name)
            self.root_models.append(f"# File: {filename}\n# Root Model: {root_class_name}")

    def save_to_file(self, output_path):
        with open(output_path, 'w', encoding='utf-8') as f:
            # 写入头部
            f.write("from typing import List, Optional, Any\n")
            f.write("from pydantic import BaseModel, Field\n\n")
            
            # 写入所有模型定义
            # 简单起见，按名称排序写入。
            # 注意：在 Python 中如果类型定义在下方，上方引用需要加引号或者用 future annotations
            # 这里我们直接输出所有类
            for name, code in self.models.items():
                f.write(code + "\n\n")
            
            f.write("# " + "="*30 + "\n")
            f.write("# Root Types Mapping\n")
            f.write("# " + "="*30 + "\n\n")
            
            for info in self.root_models:
                f.write(info + "\n\n")

        print(f"\nSuccessfully generated Pydantic models in: {output_path}")

# --- 分析器：仅打印 Schema 结构 ---
def print_schema_analysis(filepath):
    filename = os.path.basename(filepath)
    print(f"\n--- Schema Analysis: {filename} ---")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    def analyze(obj, indent=0):
        spaces = " " * indent
        if isinstance(obj, dict):
            for k, v in obj.items():
                print(f"{spaces}- {k}: {type(v).__name__}")
                # 只对非空字典或列表做浅层递归，防止刷屏
                if isinstance(v, dict) and v:
                    analyze(v, indent + 2)
                elif isinstance(v, list) and v:
                    print(f"{spaces}  [List of {type(v[0]).__name__}]")
                    # 如果列表里是字典，展示第一个元素的结构
                    if isinstance(v[0], dict):
                        analyze(v[0], indent + 4)
        elif isinstance(obj, list):
             print(f"{spaces}- [Root List]")
             if obj and isinstance(obj[0], dict):
                 analyze(obj[0], indent + 2)

    try:
        analyze(data)
    except Exception as e:
        print(f"Error analyzing: {e}")

# --- 主程序 ---
if __name__ == "__main__":
    # 1. 查找文件 (匹配 1_xxx.json 到 7_xxx.json)
    os.chdir(os.path.dirname(__file__))
    files = sorted(glob.glob("[1-7]_*.json"))
    
    if not files:
        print("未找到 JSON 文件，请确保当前目录下有 1_*.json 等文件。")
    else:
        # 步骤 1 & 2: 分析并打印 Schema
        for file in files:
            print_schema_analysis(file)
        
        # 步骤 3: 生成 Pydantic 代码
        print("\n" + "="*50)
        print("Generating Pydantic Models...")
        print("="*50)
        
        generator = PydanticGenerator()
        for file in files:
            generator.process_file(file)
        
        generator.save_to_file(OUTPUT_FILE)
"""
File Name                      | Status     | Message
--------------------------------------------------------------------------------
docs/03_aella/aella_api_req\1_papers.json | ❌ FAIL     | 16 errors. First at [papers->815->title]: Input should be a valid string
docs/03_aella/aella_api_req\2_papers,18721.json | ✅ PASS     | 成功匹配 PaperDetailResponse
docs/03_aella/aella_api_req\3_clusters.json | ✅ PASS     | 成功匹配 ClusterListResponse
docs/03_aella/aella_api_req\4_search.json | ✅ PASS     | 成功匹配 SearchResponse
docs/03_aella/aella_api_req\5_temporal-data.json | ❌ FAIL     | 100 errors. First at [clusters->0->count]: Field required      
docs/03_aella/aella_api_req\6_samples.json | ✅ PASS     | 成功匹配 SampleIdListResponse
docs/03_aella/aella_api_req\7_samples,29.json | ✅ PASS     | 成功匹配 SampleDetailResponse



其中报错：
docs/03_aella/aella_api_req\1_papers.json | ❌ FAIL     | 16 errors. First at [papers->815->title]: Input should be a valid string

    {
      "id": 895,
      "title": null,
      "x": -1.1142206192016602,
      "y": 5.947638034820557,
      "z": 9.61390495300293,
      "cluster_id": 77,
      "cluster_label": "Ecological Studies & Species Conservation",
      "field_subfield": null,
      "publication_year": null,
      "classification": "PARTIAL_TEXT"
    },


docs/03_aella/aella_api_req\5_temporal-data.json | ❌ FAIL     | 100 errors. First at [clusters->0->count]: Field required      

{
  "clusters": [
    {
      "cluster_id": 0,
      "cluster_label": "Geology & Paleoclimatology",
      "color": "#1f77b4",
      "temporal_data": [
        {
          "year": 1990,
          "count": 4
        },
        {
          "year": 1992,
          "count": 1
        },
        {
          "year": 1994,
          "count": 3
        },

给我重新写一下schema，修复错误（比如数据可能字段是缺失的，Field描述强调一下可能缺失），同时给每个schema标注来自哪个url。最后输出的时候，在多一个表格统计一下一下字段链条的缺失占比占比
"""