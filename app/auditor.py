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
            model_id, dtype=torch.float16, device_map="auto"
        )
        self.activations = []
        # Baseline stats for z-score: populate via collect_baseline()
        self.baseline_mean = None
        self.baseline_std = None

    def _hook_fn(self, module, input, output):
        self.activations.append(output.detach().cpu().numpy().mean())

    def _ensure_baseline(self):
        """Ensure baseline stats exist; raise if missing."""
        if self.baseline_mean is None or self.baseline_std is None:
            raise RuntimeError("Baseline statistics not set. Run collect_baseline() first or provide baseline values.")

    def collect_baseline(self, prompts, layers=range(5, 13)):
        """
        Collect baseline activation stats over benign prompts.
        Stores mean and std for later z-score computation.
        """
        if MOCK_MODE:
            # In mock mode, use fixed benign stats
            self.baseline_mean = 0.02
            self.baseline_std = 0.005
            return

        activations = []
        for p in prompts:
            self.activations = []
            hooks = [self.model.model.layers[i].register_forward_hook(self._hook_fn) for i in layers]
            inputs = self.tokenizer(p, return_tensors="pt").to(self.model.device)
            with torch.no_grad():
                self.model(**inputs)
            for h in hooks: h.remove()
            if self.activations:
                activations.append(np.mean(self.activations))

        if len(activations) == 0:
            raise RuntimeError("No activations collected for baseline; check prompts or model output.")

        self.baseline_mean = float(np.mean(activations))
        self.baseline_std = float(np.std(activations) + 1e-8)  # avoid divide-by-zero

    def run_audit(self, prompt):
        if MOCK_MODE:
            # Simulate a "Spike" if the word 'TRIGGER' is in the prompt
            return 4.5 if "TRIGGER" in prompt.upper() else 1.2
        
        self._ensure_baseline()
        self.activations = []
        hooks = [self.model.model.layers[i].register_forward_hook(self._hook_fn) 
                 for i in range(5, 13)]
        
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        with torch.no_grad():
            self.model(**inputs)
        
        for h in hooks: h.remove()
        
        activation_mean = float(np.mean(self.activations))
        z = (activation_mean - self.baseline_mean) / self.baseline_std
        return float(z)