import os
import numpy as np

# Logic: Only import heavy AI libraries if we are NOT in Mock Mode
MOCK_MODE = os.getenv("MOCK_MODE", "false").lower() == "true"

if not MOCK_MODE:
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

class AstraeaAuditor:
    def __init__(self, model_id="meta-llama/Llama-3.2-1B"):
        if MOCK_MODE:
            print("⚠️ MOCK MODE ENABLED: Running without GPU/Model.")
            return
        
        print(f"Loading Model: {model_id}...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id, torch_dtype=torch.float16, device_map="auto"
        )
        self.activations = []

    def _hook_fn(self, module, input, output):
        self.activations.append(output.detach().cpu().numpy().mean())

    def run_audit(self, prompt):
        if MOCK_MODE:
            # Simulate a "Spike" if the word 'TRIGGER' is in the prompt
            return 4.5 if "TRIGGER" in prompt.upper() else 1.2
        
        self.activations = []
        hooks = [self.model.model.layers[i].register_forward_hook(self._hook_fn) 
                 for i in range(5, 13)]
        
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        with torch.no_grad():
            self.model(**inputs)
        
        for h in hooks: h.remove()
        
        # Calculate Z-Score (Simplified)
        return float((np.mean(self.activations) - 0.02) / 0.005)