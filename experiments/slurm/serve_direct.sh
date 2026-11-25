#!/bin/bash
# The same server as serve.sbatch, started directly on a machine with GPUs,
# for a login that is not under the queue. Use it only on GPUs that are free
# (nvidia-smi), and stop it when you are done.
#
#     mkdir -p ~/speccheck && cd ~/speccheck
#     GPUS=0,1 nohup bash serve_direct.sh > serve_direct.log 2>&1 &
#
# It answers on the machine itself only (127.0.0.1), so from your own machine:
#
#     ssh -N -L 18300:127.0.0.1:18300 <user>@<machine>
#
# and point speccheck at http://localhost:18300/v1 with OPENAI_API_KEY set to
# the content of ~/speccheck/api_key_18300. To stop the server:
#
#     kill $(cat ~/speccheck/serve_direct.pid)
#
# GPUS         the GPUs to use, as nvidia-smi numbers them (required)
# VENV         the Python environment with vLLM (default ~/.venv)
# PORT         default 18300
# GPU_MEMORY   the share of each GPU's memory to take (default 0.85)

MODEL=Qwen/Qwen3.8-27B-FP8
PORT=${PORT:-18300}
GPUS=${GPUS:?name the GPUs to use, for example GPUS=0,1}
source "${VENV:-$HOME/.venv}/bin/activate"

export CUDA_VISIBLE_DEVICES=$GPUS
# See serve.sbatch for these three: no GPU kernel is compiled at start.
export VLLM_USE_DEEP_GEMM=0
export VLLM_USE_FLASHINFER_SAMPLER=0
export HF_HUB_OFFLINE=1

# A fresh random key, passed through the environment so that it does not show up in `ps`.
umask 077
mkdir -p "$HOME/speccheck"
export VLLM_API_KEY=$(python -c "import secrets; print(secrets.token_hex(16))")
echo "$VLLM_API_KEY" > "$HOME/speccheck/api_key_$PORT"
echo $$ > "$HOME/speccheck/serve_direct.pid"

# The options are those of serve.sbatch; one copy of the model for each GPU named.
exec vllm serve "$MODEL" \
  --host 127.0.0.1 --port "$PORT" \
  --data-parallel-size "$(echo "$GPUS" | tr ',' '\n' | wc -l)" \
  --max-model-len 32768 \
  --max-num-seqs 128 \
  --gdn-prefill-backend triton \
  --gpu-memory-utilization "${GPU_MEMORY:-0.85}" \
  --enable-prefix-caching \
  --reasoning-parser qwen3 \
  --default-chat-template-kwargs '{"enable_thinking": false}' \
  --limit-mm-per-prompt '{"image": 0, "video": 0}'
