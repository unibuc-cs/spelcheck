#!/bin/bash
# serve.sbatch: start an OpenAI-compatible vLLM server for speccheck on the SLURM GPU node.
#
# Submit (from ~/speccheck on the cluster):
#     sbatch serve.sbatch                  # 2 GPUs = 2 model replicas behind one endpoint
#     sbatch --gres=gpu:1 serve.sbatch     # 1 GPU is enough for a single spec
#
# Then, on your own machine, forward a local port to the server:
#     ssh -N -L 18200:hpc-nodegpu01:18200 <user>@hpc-ctrl01.acc-ub.local
# and point speccheck at http://localhost:18200/v1 with OPENAI_API_KEY set to
# the content of ~/speccheck/api_key.
#
#SBATCH --job-name=speccheck-qwen
#SBATCH --partition=gpu
#SBATCH --gres=gpu:2
#SBATCH --cpus-per-task=16
#SBATCH --mem=128G
#SBATCH --time=04:00:00
#SBATCH --output=serve_%j.log

MODEL=Qwen/Qwen3.8-27B-FP8
PORT=18200

# The environment that already has vLLM installed.
source "$HOME/.venv/bin/activate"

# vLLM likes to compile some GPU kernels with the CUDA compiler (nvcc) when it
# starts. That cannot work on this node: the system nvcc is version 12.0 (too
# old), and the newer one inside the Python environment (13.4) refuses its own
# headers (13.0). Each compiled kernel has a ready-made alternative, so the
# three settings below (two here, one flag further down) switch them all off:
#   VLLM_USE_DEEP_GEMM=0            FP8 matrix kernels: use the prebuilt ones
#   VLLM_USE_FLASHINFER_SAMPLER=0   top-k/top-p sampling: use plain PyTorch
#   --gdn-prefill-backend triton    Qwen's linear-attention kernel: use Triton
export VLLM_USE_DEEP_GEMM=0
export VLLM_USE_FLASHINFER_SAMPLER=0

# The weights are already in ~/.cache/huggingface, so never go to the network.
export HF_HUB_OFFLINE=1

# The server listens on the node's network interface so the login node can
# forward to it. A fresh random key keeps other cluster users out. It is passed
# through the environment (not the command line) so it does not show up in `ps`.
umask 077
export VLLM_API_KEY=$(python -c "import secrets; print(secrets.token_hex(16))")
echo "$VLLM_API_KEY" > "$HOME/speccheck/api_key"

# --data-parallel-size      one full copy of the model per GPU; vLLM spreads requests over them
# --max-num-seqs            requests handled at once per replica. The default (1024) is more
#                           than this model's state cache can hold, and startup fails
# --enable-prefix-caching   our prompts share a long prefix (the spec and the symbol list)
# --reasoning-parser        keeps any <think> text out of the answer field
# enable_thinking=false     answer directly; the JSON we ask for is short and structured
# --limit-mm-per-prompt     text only: do not load the image/video parts of the model
vllm serve "$MODEL" \
  --host 0.0.0.0 --port "$PORT" \
  --data-parallel-size "${SLURM_GPUS_ON_NODE:-1}" \
  --max-model-len 32768 \
  --max-num-seqs 128 \
  --gdn-prefill-backend triton \
  --gpu-memory-utilization 0.85 \
  --enable-prefix-caching \
  --reasoning-parser qwen3 \
  --default-chat-template-kwargs '{"enable_thinking": false}' \
  --limit-mm-per-prompt '{"image": 0, "video": 0}'
