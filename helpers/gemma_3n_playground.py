from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig
# import kagglehub
import torch
import numpy as np
from transformers import AutoProcessor, AutoModelForImageTextToText
# import cv2
import json
import datetime
import os
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
import base64
import io
from PIL import Image
import logging

GEMMA_PATH = "models/gemma-3n-transformers-gemma-3n-e2b-it-v2"

processor = AutoProcessor.from_pretrained(GEMMA_PATH)
model = AutoModelForImageTextToText.from_pretrained(
    GEMMA_PATH,
    torch_dtype="auto",
    device_map="auto"
)

image_data = "https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcTA4bd2gDVvpCEz5BQNwhi5TMj_lJceyx3ndYgY2bFLalSZuN_IeagUsi1bVZg9T8tD1J-DMRVbN_3KdstOT2vvfx1ZOqCgsxew35hpKWU"
analysis_prompt = "What's the capital of India?"


messages = [
    {
        "role": "user",
        "content": [
            {"type": "image", "image": image_data},
            {"type": "text", "text": analysis_prompt}
        ]
    }
]

# Process with Gemma 3n
inputs = processor.apply_chat_template(
    messages,
    add_generation_prompt=True,
    tokenize=True,
    return_dict=True,
    return_tensors="pt"
).to(model.device, dtype=model.dtype)

input_len = inputs["input_ids"].shape[-1]
outputs = model.generate(
    **inputs,
    max_new_tokens=1024,
    disable_compile=True,
    temperature=0.7,
    do_sample=True
)

analysis_text = processor.batch_decode(
    outputs[:, input_len:],
    skip_special_tokens=True,
    clean_up_tokenization_spaces=True
)[0]