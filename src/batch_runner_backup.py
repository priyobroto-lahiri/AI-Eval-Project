import os
import time
import pandas as pd
from google import genai
from dotenv import load_dotenv

# 1. SETUP: Load environment and configure API
load_dotenv()

# Safety Caps
MAX_API_CALLS = int(os.getenv("MAX_API_CALLS", 10))
DRY_RUN = os.getenv("DRY_RUN", "True") == "True"

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("❌ Error: GEMINI_API_KEY not found in .env")
    exit(1)

# Using the new google-genai client
client = genai.Client(api_key=GEMINI_API_KEY)
MODEL_ID = "gemini-flash-latest"

def run_batch():
    print(f"🚀 Starting Batch Runner (Dry Run: {DRY_RUN})")
    
    # 2. LOADER: Load prompts
    try:
        df_prompts = pd.read_csv("data/prompts.csv")
    except FileNotFoundError:
        print("❌ Error: data/prompts.csv not found.")
        return

    # Limit calls for safety
    df_to_run = df_prompts.head(MAX_API_CALLS)
    print(f"📊 Processing {len(df_to_run)} prompts...")

    results = []

    # 3. ENGINE: Loop and call API
    for index, row in df_to_run.iterrows():
        prompt = row['prompt']
        prompt_id = row['id']
        category = row['category']
        
        print(f"  [{prompt_id}] Processing: {prompt[:50]}...")
        
        if DRY_RUN:
            time.sleep(0.1)  # Simulate latency
            results.append({
                "id": prompt_id,
                "category": category,
                "prompt": prompt,
                "response": "DRY RUN MODE: No API call made.",
                "latency_ms": 100,
                "input_tokens": 0,
                "output_tokens": 0,
                "status": "Success (Dry Run)"
            })
            continue

        # Real API Call
        start_time = time.time()
        try:
            # Add a small delay for the free tier
            if index > 0:
                time.sleep(2)
                
            response = client.models.generate_content(
                model=MODEL_ID,
                contents=prompt
            )
            latency_ms = int((time.time() - start_time) * 1000)
            
            # Extract metrics from usage_metadata
            usage = response.usage_metadata
            
            results.append({
                "id": prompt_id,
                "category": category,
                "prompt": prompt,
                "response": response.text,
                "latency_ms": latency_ms,
                "input_tokens": usage.prompt_token_count,
                "output_tokens": usage.candidates_token_count,
                "status": "Success"
            })
        except Exception as e:
            print(f"    ❌ Failed: {str(e)}")
            results.append({
                "id": prompt_id,
                "category": category,
                "prompt": prompt,
                "response": None,
                "latency_ms": 0,
                "input_tokens": 0,
                "output_tokens": 0,
                "status": f"Error: {str(e)}"
            })

    # 4. EXPORTER: Save results and print summary
    df_results = pd.DataFrame(results)
    
    # Create results directory if it doesn't exist
    os.makedirs("results", exist_ok=True)
    output_path = "results/batch_results.csv"
    df_results.to_csv(output_path, index=False)
    
    print("\n✅ Batch Complete!")
    print(f"💾 Results saved to: {output_path}")
    
    # Print Summary Table
    if not df_results.empty:
        # Avoid errors if all rows failed (input_tokens would be 0 or NaN)
        summary = df_results.groupby("category").agg(
            count=("id", "count"),
            avg_latency=("latency_ms", "mean"),
            total_tokens=("input_tokens", lambda x: x.sum() + df_results.loc[x.index, "output_tokens"].sum())
        ).round(2)
        print("\n--- Summary Report ---")
        print(summary)

if __name__ == "__main__":
    run_batch()
