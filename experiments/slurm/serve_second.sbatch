#!/bin/bash
# serve_second.sbatch: start the second model for speccheck's optional step 7.
#
# Step 7 (formalize.second_reading) lets a model of another family translate
# every rule again. This model, a 70B Llama-architecture model already in
# ~/.cache/huggingface, takes almost a whole GPU, so it runs in its own job,
# after the main model's job (serve.sbatch), never at the same time.
#
# Submit (from ~/speccheck on the cluster):
#     sbatch --time=00:40:00 serve_second.sbatch
#
# Then, on your own machine:
#     ssh -N -L 18201:hpc-nodegpu01:18201 <user>@hpc-ctrl01.acc-ub.local
# and give speccheck --second-base-url http://localhost:18201/v1
#
#SBATCH --job-name=speccheck-second
#SBATCH --partition=gpu
#SBATCH --gres=gpu:2
#SBATCH --cpus-per-task=16
#SBATCH --mem=128G
#SBATCH --time=02:00:00
#SBATCH --output=serve_second_%j.log

MODEL=thelamapi/next-70b
PORT=18201

source "$HOME/.venv/bin/activate"

# The same switches as in serve.sbatch: the node cannot compile CUDA kernels.
export VLLM_USE_DEEP_GEMM=0
export VLLM_USE_FLASHINFER_SAMPLER=0
export HF_HUB_OFFLINE=1

# The same key as the main server, so that one OPENAI_API_KEY works for both
# (the two never run at once). A new key only if there is none yet.
umask 077
if [ ! -s "$HOME/speccheck/api_key" ]; then
  python -c "import secrets; print(secrets.token_hex(16))" > "$HOME/speccheck/api_key"
fi
export VLLM_API_KEY=$(cat "$HOME/speccheck/api_key")

# The model in 16 bits (132 GiB) does not fit one GPU, and splitting it over
# two GPUs (--tensor-parallel-size 2) fails on this node: the GPUs cannot set
# up NCCL, the library they talk through ("unhandled cuda error", tried
# 2026-11-18). So, as for Qwen, each GPU holds a full copy of the model,
# converted to 8 bits while it loads:
# --quantization fp8        8-bit weights: 66 GiB per GPU
# --data-parallel-size      one copy per GPU; vLLM spreads requests over them
# What is left of each GPU's 80 GiB holds the cache of the requests being
# answered, and it is small (2.3 GiB with the defaults), hence:
# --max-model-len 6144      a translation prompt is about 1000 tokens for a small spec and about
#                           4,300 for one of 100 requirements, plus up to 1024 for the answer
# --kv-cache-dtype fp8      the cache in 8 bits: twice as many tokens fit
# --dtype bfloat16          needed by the 8-bit cache (the model's config names no type,
#                           and vLLM would pick float16)
# --max-num-seqs 32         fewer requests at once, less memory for their working space
vllm serve "$MODEL" \
  --host 0.0.0.0 --port "$PORT" \
  --data-parallel-size "${SLURM_GPUS_ON_NODE:-1}" \
  --quantization fp8 \
  --max-model-len 6144 \
  --kv-cache-dtype fp8 \
  --dtype bfloat16 \
  --max-num-seqs 32 \
  --gpu-memory-utilization 0.95 \
  --enable-prefix-caching
