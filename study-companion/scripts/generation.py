import ollama

model_name="qwen3.5:4b"

def generate_raw_reponse(prompt,model=model_name,temperature=1.0,max_tokens=2048):
    response = ollama.generate(
        model=model,
        prompt=prompt,
        raw=True,
        options={
            "temperature": temperature,
            "max_tokens": max_tokens
        }
    )
    return {
        "text": response["response"],
        "prompt_tokens": response.get("prompt_eval_count"),
        "output_tokens": response.get("eval_count"),
        "done": response.get("done"),
    }