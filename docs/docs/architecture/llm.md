# LLM
---

The Large Language Model used for the generation step in the process is `meta-llama/Meta-Llama-3-70B-Instruct`.

## Model Details
### Release Date: April 18, 2024
Meta developed and released the Meta Llama 3 family of large language models (LLMs), a collection of pretrained and instruction tuned generative text models in 8 and 70B sizes.

The Llama 3 instruction tuned models are optimized for dialogue use cases and outperform many of the available open source chat models on common industry benchmarks.

Further, in developing these models, we took great care to optimize helpfulness and safety.


### Model Architectecture
Llama 3 is an auto-regressive language model that uses an optimized transformer architecture.

The tuned versions use supervised fine-tuning (SFT) and reinforcement learning with human feedback (RLHF) to align with human preferences for helpfulness and safety.



## API Endpoint
Llama-3-70B is hosted by [GroqLabs](https://wow.groq.com/), a new start-up using an innovative architecture on their LPU system designed specifically for LLM inference. For this particular model, output can be expected at ~480 tokens/s.
