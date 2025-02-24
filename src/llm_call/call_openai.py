import json
import os

from openai import OpenAI
from datetime import datetime
class OpenAIGenerator():
    
    def __init__(self, model = "gpt-4o-mini", price: dict = None) -> None:
        """
         Initialize OpenAI.
        """
        self.client = OpenAI()
        self.model = model
        if price is None:
            self.price = {
                "gpt-4o-mini": {"input":0.15, "output":0.6},
                "gpt-4o": {"input":2.5, "output":10.0},
                "gpt-4": {"input":30.0, "output":60.0},
            }
        else:
            self.price = price
            
    def call_openai(self, messages, **kwargs):
        res = self.client.chat.completions.create(
            messages=messages,
            model=self.model,
            temperature=0.4,
            stream=False,
            **kwargs
        )
        
        if res.choices:
            answer = res.choices[0].message.content
            usage = {
                "completion_tokens": res.usage.completion_tokens,
                "prompt_tokens": res.usage.prompt_tokens,
                "total_tokens": res.usage.total_tokens,
            }
            price_estimate =  (usage["completion_tokens"] * self.price[self.model]["output"] + usage["prompt_tokens"] * self.price[self.model]["input"])/1000000
            log_entry = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "completion_tokens": usage["completion_tokens"],
                "prompt_tokens": usage["prompt_tokens"],
                "price_estimate": str(price_estimate) + "$"
            }
            # Check if the 'logs' directory exists, if not, create it
            if not os.path.exists("logs"):
                os.makedirs("logs")

            with open("logs/openai_usages.jsonl", 'a') as f:
                json.dump(log_entry, f)
                f.write("\n")
            
            return answer