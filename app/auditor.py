import torch
import numpy as np
from transformers import AutoModelForCausalLM, AutoTokenizer

class AstraeaAuditor:
    def __init__(self, model_id="meta-llama/Llama-3.2-1B"):
        print(f"Loading Model: {model_id}...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id, 
            torch_dtype=torch.float16, 
            device_map="auto"
        )
        self.activations = []

    def _hook_fn(self, module, input, output):
        # We capture the mean of the hidden states to detect "Activation Spikes"
        self.activations.append(output.detach().cpu().numpy().mean())

    def run_audit(self, prompt):
        self.activations = []
        # We target mid-layers (e.g., layers 5 to 12) where logic-based triggers manifest
        hooks = []
        for i in range(5, min(13, len(self.model.model.layers))):
            hooks.append(self.model.model.layers[i].register_forward_hook(self._hook_fn))
        
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        
        with torch.no_grad():
            self.model(**inputs)
        
        for h in hooks: h.remove()
        
        # Calculate Z-Score (Anomaly detection)
        # In production, you compare this to a "baseline" of 1,000 clean prompts
        baseline_mean = 0.02  # Example constant
        baseline_std = 0.005  # Example constant
        current_mean = np.mean(self.activations)
        z_score = (current_mean - baseline_mean) / baseline_std
        
        return float(z_score)