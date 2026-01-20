# 🛡️ Astraea Auditor: Neural-Layer Robustness & Compliance
**Automated Conformity Assessment for EU AI Act (Article 15) | Specialized for Fintech RAG Pipelines**

---

## 🏛️ The Regulatory Landscape (2026)
As of August 2026, the **EU AI Act** mandates that high-risk AI systems in financial services must demonstrate proof of **Robustness, Accuracy, and Cybersecurity**. 

Standard firewalls (WAFs) and text-based guardrails are no longer sufficient. Attackers now utilize **Indirect Prompt Injection** and **Model Poisoning** to trigger malicious logic deep within an LLM's latent space—logic that is invisible to traditional security layers.

**Astraea Auditor** provides a mathematical, neural-level audit of your model's internal integrity.

---

## 🧠 The Technical Edge: Latent Spike Detection
Unlike "Black-Box" scanners, Astraea utilizes **Neural Activation Hooks** to monitor the "internal heart rate" of your transformer models during inference. 

By profiling the hidden states of specific layers, we calculate a **Robustness Z-Score**:

$$Z = \frac{x - \mu}{\sigma}$$

* **$x$**: Real-time activation mean of the processed prompt.
* **$\mu$**: Established baseline mean from 1,000+ "clean" production logs.
* **$\sigma$**: Standard deviation of baseline activations.

A $Z > 3.0$ indicates a **Neural Spike**, signaling that a hidden backdoor or poisoning trigger has been activated at the architectural level.

---

## ✨ Key Features
* **Adversarial Red-Teaming:** Automated testing against 10 critical poisoning vectors (RAG Hijacking, ASCII Smuggling, etc.).
* **Compliance PDF Generator:** Instantly generates an **Executive Audit Report** mapping technical spikes to EU AI Act Article 15 requirements.
* **Privacy-First Redaction:** Includes client-side scripts to scrub PII (Names, IBANs, Emails) before audit ingestion.
* **Infrastructure Agnostic:** Designed for **RunPod Serverless** or local Dockerized environments.

---

## 💼 Productized Services
*Directly support your compliance roadmap with specialized auditing:*

### 1. Zero-Touch Diagnostic | **€5,000**
* **Outcome:** 48-hour "Neural Vulnerability Map" based on 10 production logs.
* **Deliverable:** 10-page Executive Summary & Art. 15 Gap Analysis.
* [**Request Diagnostic**](mailto:your-email@example.com?subject=Astraea%20Diagnostic%20Inquiry)

### 2. Full Compliance Audit | **€15,000**
* **Outcome:** Comprehensive system-wide robustness certification.
* **Deliverable:** Formal **Conformity Assessment Document** for regulatory submission.
* [**Book Audit**](mailto:your-email@example.com?subject=Full%20Astraea%20Audit%20Inquiry)

---

## 🛠️ Quick Start (Engineer's Mindset)
Developed by an informatics engineering student at **ENSEA**, Astraea is built for professional reliability and deep-work integration.

### Local "Mock" Diagnostic
Test the logic and report generation on your laptop without a GPU:
1. **Clone:** `git clone https://github.com/LRaVe/Astraea_Auditor.git`
2. **Env Setup:** Create a `.env` file with `MOCK_MODE=true`.
3. **Run:** `python -m app.main`
4. **View:** Open the generated `Audit_Report.pdf` in the root folder.

---

## 🛡️ Security & Privacy
Astraea operates on a **Zero-Trust** model. We never request raw production data. All logs must be passed through the `Astraea-Redactor` script locally before being uploaded to our secure audit environment.

**Maintainer:** [LRaVe](https://github.com/LRaVe)  
**Affiliation:** ENSEA Informatics Engineering  
**Location:** Cergy, France