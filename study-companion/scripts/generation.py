import ollama

model_name="qwen3.5:4b"

def generate_raw_response(prompt,model=model_name,temperature=0.1,num_predict=200,stop=None):
    response = ollama.generate(
        model=model,
        prompt=prompt,
        raw=True,
        options={
            "temperature": temperature,
            "num_predict": max_tokens
        }
    )
    return {
        "text": response["response"],
        "prompt_tokens": response.get("prompt_eval_count"),
        "output_tokens": response.get("eval_count"),
        "done": response.get("done"),
    }