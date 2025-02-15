import os

from llama_cpp import Llama

class ModelHandler():
    
    def __init__(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.model_path = os.path.join(base_path, "capybarahermes-2.5-mistral-7b.Q5_K_M.gguf")
        
        self.model_loaded = False
        
        if not os.path.exists(self.model_path):
            self.error_message = "Model not found"

        # I'm playing with fire with these values. Something is going to break, but that's how we learn our limits. 
        self.llm = Llama(model_path=self.model_path, n_ctx=2048, n_gpu_layers=40, n_threads=8, batch_size=1024)
        
    def promptLLM(self, prompt):
        system_message = "You are a worldbuilding assistant"
        processed_prompt = f"<|im_start|>system\n{system_message}<|im_end|>\n" \
                       f"<|im_start|>user\n{prompt}<|im_end|>\n" \
                       f"<|im_start|>assistant\n"
        output = self.llm(processed_prompt, max_tokens=1000)['choices'][0]['text']
        return output
    