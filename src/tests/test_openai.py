import openai
import runpy
from typing import Tuple, Optional, List
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from src.openai_caller import get_python_code_from_gpt,run_code_with_df
import pandas as pd






    
if __name__ == "__main__":
    
    # Step 1: Load and normalize dataset
    try:
        df = pd.read_csv("src/tests/train2tap.csv")
        df.columns = df.columns.str.lower()  # normalize to lowercase
    except Exception as e:
        print(f"Error loading train.csv: {e}")
        exit(1)

    # Step 2: Generate metadata from real DataFrame
    sample = df.head(3).to_csv(index=False)
    col_info = ", ".join([f"{col} ({df[col].dtype})" for col in df.columns])
    metadata = f"""
Columns: {col_info}
Rows: {len(df)}
Sample:
{sample}
All column names are lowercase.
    """

    # Empty context
    context = ""

    # Step 5: New follow-up request (should reuse styling from context)
    user_request = "Now group passengers by age ranges and plot the number of passengers per group."

    # Step 6: Generate code from GPT
    generated_code,context = get_python_code_from_gpt(metadata, user_request, context)
    print("Generated Code:\n")
    print(generated_code)

    # Step 7: Run the generated code with the real DataFrame
    code, fig = run_code_with_df(df, metadata, user_request)
    if fig:
        print("[✔] Plot generated successfully.")
        fig.show()
    else:
        print("[✘] No plot was generated.")
