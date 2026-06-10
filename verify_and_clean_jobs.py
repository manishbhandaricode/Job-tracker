import json
import requests
import os
import time

def verify_and_clean_jobs():
    jobs_file_path = os.path.join(os.path.dirname(__file__), "jobs.json")
    if not os.path.exists(jobs_file_path):
        print("jobs.json not found!")
        return

    with open(jobs_file_path, "r", encoding="utf-8") as f:
        jobs_list = json.load(f)

    print(f"Verifying {len(jobs_list)} jobs. This might take a few minutes...")
    cleaned = []
    removed_count = 0
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    closure_phrases = [
        "no longer available", "job is closed", "position has been filled", 
        "page not found", "404 not found", "this job has expired",
        "we're sorry, but this job is no longer available",
        "job not found"
    ]

    for idx, job in enumerate(jobs_list):
        url = job.get("url")
        title = job.get("title")
        company = job.get("company")
        if not url:
            continue
            
        print(f"[{idx+1}/{len(jobs_list)}] Checking {title} at {company}...")
        try:
            response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
            is_dead = False
            reason = ""
            
            if response.status_code in [404, 410, 403, 400]:
                is_dead = True
                reason = f"Status {response.status_code}"
                
            elif response.url != url:
                if len(response.url.split('/')) < len(url.split('/')) - 1:
                    is_dead = True
                    reason = "Redirected to generic page"
                    
            if not is_dead:
                html_lower = response.text.lower()
                for phrase in closure_phrases:
                    if phrase in html_lower:
                        is_dead = True
                        reason = f"Found phrase: '{phrase}'"
                        break
                        
                # Additional check: Check if job title is somewhat present in HTML (very fuzzy check)
                if not is_dead:
                    title_words = title.lower().split()
                    # If the page doesn't contain at least one significant word from the title
                    significant_words = [w for w in title_words if len(w) > 3]
                    if significant_words and not any(w in html_lower for w in significant_words):
                        is_dead = True
                        reason = f"Job title not found on page"

            if is_dead:
                print(f"  --> REMOVED: {reason}")
                removed_count += 1
            else:
                cleaned.append(job)
                
        except Exception as e:
            print(f"  --> REMOVED: Connection Error ({e})")
            removed_count += 1
            
        time.sleep(0.5)

    print(f"\nVerification Complete. Removed {removed_count} dead jobs.")
    print(f"Remaining active jobs: {len(cleaned)}")

    with open(jobs_file_path, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=4, ensure_ascii=False)
        
if __name__ == "__main__":
    verify_and_clean_jobs()
