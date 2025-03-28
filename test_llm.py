import json
import re
from openai import OpenAI
from tqdm import tqdm
import requests

from mcq import MCQ

from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--model_name", type=str, required=True)
parser.add_argument("--with_context", action="store_true")
args = parser.parse_args()

MODEL_NAME = args.model_name
WITH_CONTEXT = args.with_context
WITH_RAG = args.with_rag

# Need to set for LLM api
BASE_URL = "https://api.openai.com/v1"
API_KEY = "sk-"


def call_openai(
    model_name: str,
    prompt: str,
    max_tokens=4096,
    history=[],
    n=1,
    temperature=0.0,
    top_p=0.8,
    timeout=300,
    system_message="You are a helpful assistant.",
    retry_times=5,
):
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    messages = [
        {"role": "system", "content": system_message},
        *history,
        {"role": "user", "content": prompt},
    ]

    for _ in range(retry_times):
        try:
            completion = client.chat.completions.create(
                model=model_name,
                messages=messages,
                max_tokens=max_tokens,
                n=n,
                temperature=temperature,
                top_p=top_p,
                timeout=timeout,
            )

            response = [choice.message.content.strip() for choice in completion.choices]
            assert "boxed" in response[0], "No answer found in response"

            return response
        except Exception as e:
            print(e)
            continue
    return [""]


def get_llm_option(mcq, with_context=False):
    prompt_template = """
Your task is to answer the following multiple-choice question, which has only one correct answer from A, B, C, D.%s

Question topic: StarCraft II game.
%s

Please select the correct answer and put it in the following format:
\\boxed{A/B/C/D}
    """.strip()

    if with_context:
        reference = "\n\nReference document:\n\n%s\n\n---" % mcq.document[:24000] # Truncate to 24k tokens
    else:
        reference = ""

    prompt = prompt_template % (reference, mcq)
    response = call_openai(MODEL_NAME, prompt)[0]
    matches = re.findall(r"\\boxed\{([A-D])\}", response)
    if matches:
        return matches[-1]
    return ""


if WITH_CONTEXT:
    save_path = f"./data/mcq_{MODEL_NAME}_with_context.txt"
else:
    save_path = f"./data/mcq_{MODEL_NAME}.txt"

with open(save_path, "w", encoding="utf-8") as f_save:
    with open("./data/mcq.jsonl", "r", encoding="utf-8") as f:
        idx = 0
        for line in tqdm(f):
            mcq_json = json.loads(line)
            mcq = MCQ(mcq_json["document"], mcq_json["question"], mcq_json["options"], mcq_json["answer"])
            llm_option = get_llm_option(mcq, WITH_CONTEXT)
            result = llm_option + "-" + str(int(mcq.check_answer_index(llm_option)))
            f_save.write(result + "\n")
            idx += 1
