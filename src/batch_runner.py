import os
import time
from httpx import NetworkError
import pandas as pd
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_ID = "gemini-flash-latest"

def run_batch():
    df = pd.read_csv("data/prompts.csv")
        
    if df is None:
        print("Data not loaded!")
        return

    results = []

    for index, row in df.iterrows():
        prompt_text = row['prompt']
        print(f"Processing prompt {index + 1}/{len(df)}: {prompt_text[:30]}...")

        latency = 0
        prompt_tokens = 0
        response_tokens = 0
        
        try:
            start_time = time.time()
            response = client.models.generate_content(model=MODEL_ID, contents=prompt_text)
            try:
                if(response.candidates):
                    answer = response.text
            except Exception as e:
                answer = f"Error extracting response text: {str(e)}"
                    

            latency = time.time() - start_time
            
            prompt_tokens = response.usage_metadata.prompt_token_count
            response_tokens = response.usage_metadata.candidates_token_count
    

        except Exception as e:
            answer = f"Error: {str(e)}"
            print(f"Error occurred: {e}")

            
        results.append({
            "prompt": prompt_text, 
            "response": answer, 
            "latency": latency, 
            "prompt_tokens": prompt_tokens, 
            "response_tokens": response_tokens
        })

        time.sleep(4) 
        
    pd.DataFrame(results).to_csv("results/my_output.csv", index=False)
    print("Batch processing complete. Results saved to results/my_output.csv")

if __name__ == "__main__":
    run_batch()
