FROM nvcr.io/nvidia/pytorch:23.06-py3
COPY llm_service.py ./
RUN pip3 install --upgrade pip && pip3 install accelerate
RUN pip3 install fschat
CMD nohup python3 -m fastchat.serve.controller > controller.out 2>controller.err & nohup python3 -m fastchat.serve.model_worker --model-path meta-llama/Llama-2-7b-chat-hf --num-gpus 1 > model_worker.out 2>model_worker.err & nohup python3 -m fastchat.serve.gradio_web_server > gradio.out 2>gradio.err & python3 llm_service.py
