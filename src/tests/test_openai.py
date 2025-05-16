import openai

client= openai.OpenAI(api_key= "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") 


def sanitize_code(gpt_response: str) -> str:
    """ 
    Clean GPT output to extract raw python code
    Remove markdown, fences and comment around the code
    """
    cleaned = gpt_response.strip()

    #remove markdown
    if cleaned.startswith("```"):
        parts = cleaned.split("```")
        if len(parts) >= 2:
            cleaned = parts[1] 
            #removes 'python' if it exists
            if cleaned.startswith("python"):
                cleaned = cleaned[len("python"):].strip()

    return cleaned

def write_code_to_file(code: str, filename: str = "test_generated_code.py") -> None:
    """
    overwrites the given file with sanitized python code.
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(code)
        print(f"[✔] Code successfully written to {filename}")
    except Exception as e:
        print(f"[✘] Failed to write code to file: {e}")



def get_python_code_from_gpt(metadata: str, user_request: str) -> str:
    # build the prompt  

    prompt = f"""
        You are a helpful data analyst. A user uploaded a dataset.
        Here is a description of the dataset:
        {metadata}

        The user asked: "{user_request}"

        Please write valid Python code to fulfill the user's request using pandas and matplotlib or seaborn.
        Do not include explanations. Only return the code.
        """
    
    # call the api 
    try: 
        response = client.chat.completions.create(
            model= "gpt-4o-mini",
            messages =[
                {"role": "system", "content": "You are a Python expert. When asked a question, you respond only with clean, executable Python code and no explanations or comments."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        # fetch code from gpt answer
        raw_response = response.choices[0].message.content
        clean_code = sanitize_code(raw_response)
        write_code_to_file(clean_code)

        return clean_code
    
    except Exception as e:
        print(f"Error calling OpenAI APi: {e}")
        return "#Error: Unable to generate code at this time"
    
    
if __name__ == "__main__":
    metadata = """
    Columns: name (str), age (int), score (float)
    Rows: 3
    Sample:
    name,age,score
    Alice,23,89.5
    Bob,30,76.0
    Carol,28,91.2
    """

    user_request = "Plot the age distribution"

    result = get_python_code_from_gpt(metadata, user_request)
    print("Generated Code:\n")
    print(result)