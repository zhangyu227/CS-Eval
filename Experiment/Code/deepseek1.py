import pandas as pd
import requests
import json
import time
import os
from pathlib import Path
import concurrent.futures
import threading
from tqdm import tqdm
from typing import List, Tuple

# =================配置区域=================
API_KEY = "sk-drhzpxtpimowjzralbkvamfrgkwzolmepuvekuxsupabgsot"
API_ENDPOINT = "https://api.siliconflow.cn/v1/chat/completions"
MAX_WORKERS = 5  # 同时处理的最大请求数
REQUESTS_PER_MINUTE = 60  # API速率限制
RETRY_TIMES = 3  # 失败重试次数
BATCH_SAVE_NUM = 50  # 每处理多少个保存一次
INPUT_FOLDER = Path(r"C:\security\问答测试\Data2")
# ==========================================

class APIRateLimiter:
    def __init__(self, max_calls: int, period: int):
        self.max_calls = max_calls
        self.period = period
        self.timestamps = []

    def wait(self):
        now = time.time()
        self.timestamps = [t for t in self.timestamps if t > now - self.period]

        if len(self.timestamps) >= self.max_calls:
            sleep_time = self.period - (now - self.timestamps[0])
            if sleep_time > 0:
                time.sleep(sleep_time)

        self.timestamps.append(time.time())

class DeepSeekProcessor:
    def __init__(self):
        self.rate_limiter = APIRateLimiter(REQUESTS_PER_MINUTE, 60)
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS)
        self.lock = threading.Lock()

    def call_api(self, question: str) -> str:
        self.rate_limiter.wait()

        payload = {
            "model": "deepseek-ai/DeepSeek-V3",
            "messages": [
                {
                    "role": "user",
                    "content": str(question) + "Your answer can only be a single letter, nothing else."
                }
            ],
            "stream": False,
            "max_tokens": 512,
            "temperature": 0.7,
            "top_p": 0.7
        }

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        for attempt in range(RETRY_TIMES):
            try:
                response = requests.post(API_ENDPOINT, json=payload, headers=headers)
                response.raise_for_status()
                return response.json()['choices'][0]['message']['content']
            except Exception as e:
                if attempt == RETRY_TIMES - 1:
                    print(f"API调用失败: {str(e)}")
                    return ""
                time.sleep(1)

    def process_question(self, question: str, index: int) -> Tuple[int, str]:
        if pd.isna(question):
            return index, ""
        return index, self.call_api(str(question))

    def _safe_read_excel(self, file_path: Path) -> pd.DataFrame:
        try:
            return pd.read_excel(file_path)
        except Exception as e:
            raise Exception(f"读取文件 {file_path} 失败: {str(e)}")

    def _safe_save_excel(self, df: pd.DataFrame, file_path: Path):
        try:
            df.to_excel(file_path, index=False)
        except Exception as e:
            temp_path = file_path.parent / f"temp_{file_path.name}"
            df.to_excel(temp_path, index=False)
            print(f"已保存到临时文件: {temp_path}")

    def process_files(self, file_paths: List[Path]):
        with tqdm(total=len(file_paths), desc="处理文件中") as pbar_files:
            futures = []
            for file_path in file_paths:
                future = self.executor.submit(self.process_single_file, file_path)
                future.add_done_callback(lambda _: pbar_files.update(1))
                futures.append(future)

            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"\n文件处理错误: {str(e)}")

    def process_single_file(self, file_path: Path):
        try:
            df = self._safe_read_excel(file_path)

            if '测试用例' not in df.columns:
                print(f"{file_path} 缺少测试用例列")
                return

            df['DeepSeek'] = df.get('DeepSeek', pd.Series(dtype='str')).astype('str')
            todo_indices = df[df['DeepSeek'].isin(['', 'nan', 'None'])].index.tolist()

            if not todo_indices:
                return

            with tqdm(total=len(todo_indices), desc=f"处理 {file_path.name}", leave=False) as pbar:
                for i in range(0, len(todo_indices), BATCH_SAVE_NUM):
                    batch = todo_indices[i:i+BATCH_SAVE_NUM]
                    futures = [
                        self.executor.submit(
                            self.process_question,
                            df.at[idx, '测试用例'],
                            idx
                        ) for idx in batch
                    ]

                    results = []
                    for future in concurrent.futures.as_completed(futures):
                        result = future.result()
                        results.append(result)
                        pbar.update(1)

                    with self.lock:
                        for idx, answer in results:
                            df.at[idx, 'DeepSeek'] = answer
                        self._safe_save_excel(df, file_path)

        except Exception as e:
            raise Exception(f"处理文件 {file_path} 时出错: {str(e)}")

def main():
    processor = DeepSeekProcessor()
    excel_files = list(INPUT_FOLDER.glob("*.xlsx")) + list(INPUT_FOLDER.glob("*.xls"))

    if not excel_files:
        print("未找到Excel文件")
        return

    print(f"找到 {len(excel_files)} 个Excel文件")
    processor.process_files(excel_files)

if __name__ == "__main__":
    main()