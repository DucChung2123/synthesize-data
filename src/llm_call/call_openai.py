import json
import os
from openai import OpenAI
from datetime import datetime

class OpenAIGenerator():
    """
    A class to interact with OpenAI's API and log usage details.

    Attributes:
    ----------
    client : OpenAI
        An instance of the OpenAI client.
    model : str
        The model to be used for generating completions.
    price : dict
        A dictionary containing the pricing details for different models.

    Methods:
    -------
    __init__(self, model="gpt-4o-mini", price: dict = None) -> None:
        Initializes the OpenAIGenerator with the specified model and pricing details.
    
    call_openai(self, messages, return_usage=False, temperature=0.7, **kwargs):
        Calls the OpenAI API with the provided messages and logs the usage details.
    """

    def __init__(self, 
                 model: str = "gpt-4o-mini", 
                 price: dict = None) -> None:
        """
        Initialize the OpenAIGenerator with the specified model and pricing details.

        Parameters:
        ----------
        model : str, optional
            The model to be used for generating completions (default is "gpt-4o-mini").
            Valid models are "gpt-4o" and "gpt-4o-mini".
        price : dict, optional
            A dictionary containing the pricing details for different models.
            If not provided, default pricing details will be used.

        Raises:
        ------
        ValueError
            If the provided model is not valid.
        """
        valid_models = ["gpt-4o", "gpt-4o-mini"]
        if model not in valid_models:
            raise ValueError(f"Invalid model '{model}'. Valid models are: {valid_models}")
        
        self.client = OpenAI()
        self.model = model
        if price is None:
            self.price = {
                "gpt-4o-mini": {"input": 0.15, "output": 0.6},
                "gpt-4o": {"input": 2.5, "output": 10.0},
                "gpt-4": {"input": 30.0, "output": 60.0},
            }
        else:
            self.price = price
            
    def call_openai(self,
                    messages: list,
                    return_usage: bool = False,
                    temperature: float = 0.7,
                    **kwargs):
        """
        Calls the OpenAI API with the provided messages and logs the usage details.

        Parameters:
        ----------
        messages : list
            A list of messages to be sent to the OpenAI API.
        return_usage : bool, optional
            Whether to return the usage details along with the response (default is False).
        temperature : float, optional
            The temperature to be used for generating completions (default is 0.7).
        **kwargs : dict
            Additional keyword arguments to be passed to the OpenAI API.

        Returns:
        -------
        str
            The content of the first choice in the API response.
        tuple
            The content of the first choice in the API response and the price estimate if return_usage is True.

        Logs:
        -----
        Logs the usage details including the number of tokens used and the estimated price.
        """
        res = self.client.chat.completions.create(
            messages=messages,
            model=self.model,
            temperature=temperature,
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
            price_estimate = (usage["completion_tokens"] * self.price[self.model]["output"] + usage["prompt_tokens"] * self.price[self.model]["input"]) / 1000000
            log_entry = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "completion_tokens": usage["completion_tokens"],
                "prompt_tokens": usage["prompt_tokens"],
            }
            if not os.path.exists("logs"):
                os.makedirs("logs")

            with open("logs/openai_usages.jsonl", 'a') as f:
                json.dump(log_entry, f)
                f.write("\n")
            if return_usage:
                return answer, price_estimate
            return answer