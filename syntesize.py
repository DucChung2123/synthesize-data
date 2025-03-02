import pandas as pd
from src.llm_call.call_openai import OpenAIGenerator
from dotenv import load_dotenv
from src.prompts.INS_IN_OUT_prompt import INSTRUCTION_GEN_PROMPT, REWRITE_INPUT_PROMPT, PRE_OUTPUT_PROMPT
from src.utils.random_captilize import random_capitalize
import random
import concurrent.futures
import threading
from tqdm import tqdm
import os
import json

load_dotenv()
llm = OpenAIGenerator()

output_file = "syn_lichsu_25-2.jsonl"

file_lock = threading.Lock()
usage_lock = threading.Lock()
total_usage = 0

df = pd.read_json("/storage2/work/hdchung/Misa_llama/synthesize_data/25-2/lich_su0.jsonl", lines=True)

df = df.rename(columns={"input": "ins", "instruction": "input"})
df = df.rename(columns={"ins": "instruction"})

df = df[["instruction", "input", "output"]]

if os.path.exists(output_file):
    os.remove(output_file)

def append_to_jsonl(data_list, filename):
    with file_lock:
        with open(filename, 'a', encoding='utf-8') as f:
            for item in data_list:
                json_str = json.dumps(item, ensure_ascii=False)
                f.write(json_str + '\n')

def process_sample(sample, sample_index):
    global total_usage
    results = []
    
    try:
        instruction_gen = INSTRUCTION_GEN_PROMPT.format(question=sample["input"])
        message = [{"role": "user", "content": instruction_gen}]
        new_ins, u1 = llm.call_openai(message, return_usage=True)
        
        with usage_lock:
            total_usage += u1
        
        re_output = PRE_OUTPUT_PROMPT.format(
            input=sample["input"][:100], 
            output=sample["output"][:50], 
            instruction=new_ins
        )
        new_output, u3 = llm.call_openai([{"role": "user", "content": re_output}], return_usage=True)
        
        results.append({
            "instruction": new_ins,
            "input": sample["input"],
            "output": new_output + "\n" + sample["output"]
        })
        
        prob = random.uniform(0, 1)
        if prob < 0.3:
            new_ins = random_capitalize(new_ins)
            new_input = random_capitalize(sample["input"])
            results.append({
                "instruction": new_ins,
                "input": new_input,
                "output": new_output + "\n" + sample["output"]
            })
        else:
            rewrite_input = REWRITE_INPUT_PROMPT.format(question=sample["input"])
            new_input, u2 = llm.call_openai([{"role": "user", "content": rewrite_input}], return_usage=True)
            with usage_lock:
                total_usage += u2
            
            results.append({
                "instruction": new_ins,
                "input": new_input,
                "output": new_output + "\n" + sample["output"]
            })
        
        with usage_lock:
            total_usage += u3
        
        append_to_jsonl(results, output_file)
        
        return len(results)
    
    except Exception as e:
        print(f"Lỗi xử lý mẫu {sample_index}: {str(e)}")
        return 0


samples = df.to_dict('records')

total_samples_created = 0
max_workers = 48 

print(f"Bắt đầu xử lý {len(samples)} mẫu với {max_workers} luồng...")

with tqdm(total=len(samples), desc="Xử lý mẫu") as pbar:
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_sample = {
            executor.submit(process_sample, sample, i): i 
            for i, sample in enumerate(samples)
        }
        
        for future in concurrent.futures.as_completed(future_to_sample):
            try:
                sample_count = future.result()
                total_samples_created += sample_count
            except Exception as e:
                print(f"Lỗi ngoại lệ: {e}")
            finally:
                pbar.update(1)
                
                sample_index = future_to_sample[future]
                # if (sample_index + 1) % 10 == 0:
                #     print(f"Đã xử lý {sample_index + 1}/{len(samples)} mẫu. Usage hiện tại: {total_usage}")

print(f"Hoàn thành! Total usage: {total_usage}")
print(f"Tổng số mẫu đã tạo và lưu vào {output_file}: {total_samples_created}")