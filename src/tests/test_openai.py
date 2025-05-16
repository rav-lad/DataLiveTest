import openai

client= openai.OpenAI(api_key= "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") 



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
        reply = response.choices[0].message.content

        return reply.strip()
    
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