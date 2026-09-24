from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_NAME = "MBZUAI/LaMini-Flan-T5-783M"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)


def explain_topic(topic: str) -> str:
    prompt = (
        f"Explain the concept of '{topic}' in a simple and clear way "
        "for a school student."
    )

    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        **inputs,
        max_new_tokens=180,
        do_sample=False,
    )

    return tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
