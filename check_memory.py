import requests

API_URL = "https://sacreddevil2-aurora.hf.space"

print(f"🧠 Checking RAG Memory Bank at {API_URL}...")

queries = ["low accuracy", "data drift", "lighting", "system initialization"]

for q in queries:
    print(f"\n🔎 Searching for '{q}'...")
    try:
        response = requests.post(f"{API_URL}/api/memory/search", json={"query": q, "top_k": 2})
        if response.status_code == 200:
            results = response.json().get("results", [])
            print(f"   Found {len(results)} memories.")
            print(f"   Raw first result: {results[0] if results else 'None'}") 
            for i, res in enumerate(results):
                content = res.get('content', 'No Content') if isinstance(res, dict) else str(res)
                print(f"   [{i+1}] {content[:100]}...")
        else:
            print(f"   ❌ Error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
