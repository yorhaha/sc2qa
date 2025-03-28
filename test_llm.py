import json
import re
import os
import time
from typing import List, Dict, Optional
import logging
from openai import OpenAI
from tqdm import tqdm
from mcq import MCQ
from argparse import ArgumentParser

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Parse command line arguments
parser = ArgumentParser()
parser.add_argument("--model_name", type=str, required=True)
parser.add_argument("--with_context", action="store_true")
args = parser.parse_args()

MODEL_NAME = args.model_name
WITH_CONTEXT = args.with_context

# Configuration from environment variables
API_KEY = os.getenv("OPENAI_API_KEY", "sk-")
BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

PROMPT_TEMPLATE = """
Your task is to answer the following multiple-choice question, which has only one correct answer from A, B, C, D.{reference}

Question topic: StarCraft II game.
{question}

Please select the correct answer and put it in the following format:
\\boxed{{A/B/C/D}}
""".strip()

DEFAULT_MAX_TOKENS = 4096
DEFAULT_TIMEOUT = 300
MAX_DOCUMENT_LENGTH = 6000  # Adjusted for typical 8k token models


def call_openai(
    model_name: str,
    prompt: str,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    history: Optional[List[Dict[str, str]]] = None,
    n: int = 1,
    temperature: float = 0.0,
    top_p: float = 0.8,
    timeout: int = DEFAULT_TIMEOUT,
    system_message: str = "You are a helpful assistant.",
    retry_times: int = 5,
    retry_delay: int = 2,
) -> List[str]:
    """Call OpenAI API with retry logic and error handling."""
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    messages = [
        {"role": "system", "content": system_message},
        *(history or []),
        {"role": "user", "content": prompt},
    ]

    for attempt in range(retry_times):
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

            if not completion.choices:
                raise ValueError("No choices returned from API")

            response = [choice.message.content.strip() for choice in completion.choices]

            if not any("boxed" in res for res in response):
                raise ValueError("No answer found in response")

            return response
        except Exception as e:
            logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < retry_times - 1:
                time.sleep(retry_delay * (attempt + 1))
            continue

    logger.error(f"All {retry_times} attempts failed")
    return [""]


def get_llm_option(mcq: MCQ, with_context: bool = False) -> str:
    """Get LLM's answer for MCQ question with optional context."""
    reference = f"\n\nReference document:\n\n{mcq.document[:MAX_DOCUMENT_LENGTH]}\n\n---" if with_context else ""

    prompt = PROMPT_TEMPLATE.format(reference=reference, question=str(mcq))

    try:
        response = call_openai(MODEL_NAME, prompt)[0]
        if matches := re.findall(r"\\boxed\{([A-D])\}", response):
            return matches[-1]
    except Exception as e:
        logger.error(f"Error processing response: {str(e)}")

    return ""


def validate_option(option: str) -> bool:
    """Validate if option is A-D."""
    return option in {"A", "B", "C", "D"}


def main():
    """Main processing pipeline."""
    save_path = f"./data/mcq_{MODEL_NAME}{'_with_context' if WITH_CONTEXT else ''}.txt"

    with open(save_path, "w", encoding="utf-8") as f_save, open("./data/mcq.jsonl", "r", encoding="utf-8") as f:

        for line in tqdm(f, desc="Processing MCQs"):
            mcq_json = json.loads(line)
            mcq = MCQ(mcq_json["document"], mcq_json["question"], mcq_json["options"], mcq_json["answer"])

            llm_option = get_llm_option(mcq, WITH_CONTEXT)
            is_valid = validate_option(llm_option)

            try:
                correct = int(mcq.check_answer_index(llm_option)) if is_valid else 0
            except Exception as e:
                logger.error(f"Error checking answer: {str(e)}")
                correct = 0

            f_save.write(f"{llm_option}-{correct}\n")


if __name__ == "__main__":
    main()
