import os
import sys
import json
import time
import requests
import re
from datetime import datetime

# Initialize Gemini AI
try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

# Load preferences
try:
    prefs_path = os.path.join(os.path.dirname(__file__), "preferences.json")
    with open(prefs_path, "r", encoding="utf-8") as f:
        prefs = json.load(f)
        MANISH_PROFILE = prefs.get("profile", "")
        TARGET_KEYWORDS = prefs.get("keywords", [])
except Exception as e:
    print(f"Failed to load preferences.json: {e}")
    MANISH_PROFILE = ""
    TARGET_KEYWORDS = []

def pre_filter_job(title, description, location):
    """
    Do a quick keyword check to filter out obviously irrelevant jobs 
    (e.g., Senior Software Developers, DevOps, US-only roles) before calling Gemini.
    """
    title_lower = title.lower()
    desc_lower = description.lower()
    loc_lower = location.lower() if location else ""

    # 1. Location check - exclude if it specifies US, UK, Europe ONLY and excludes worldwide/India
    exclude_locations = ["us only", "usa only", "uk only", "europe only", "germany only", "canada only", "timezone: est", "timezone: pst"]
    if any(loc in loc_lower for loc in exclude_locations) and "worldwide" not in loc_lower and "india" not in loc_lower:
        return False

    # 2. Seniority check - exclude senior/lead roles
    exclude_seniority = ["senior", "lead", "staff", "principal", "director", "manager", "architect", "head of", "vp", "sr."]
    # Allow "Product Manager" or "Associate Product Manager"
    if any(word in title_lower for word in exclude_seniority):
        if not ("product manager" in title_lower or "apm" in title_lower or "associate product" in title_lower):
            return False

    # 3. Technical stack check - exclude heavy programming roles unless they are simple/entry level
    exclude_tech = ["devops", "kubernetes", "golang", "c++", "rust", "backend developer", "frontend developer", 
                    "fullstack developer", "software engineer", "infrastructure", "react native", "solidity", "blockchain developer"]
    if any(tech in title_lower for tech in exclude_tech):
        return False

    # 4. Include check - must match one of our target keywords in title
    if not any(word.lower() in title_lower for word in TARGET_KEYWORDS):
        return False

    return True

def evaluate_job_with_gemini(model, job):
    """
    Sends the job details to Gemini AI to evaluate suitability and format the output.
    """
    prompt = f"""
Analyze if this job is suitable for Manish Bhandari (B.Com fresher with WealthTech Intern experience).

Manish's Profile:
{MANISH_PROFILE}

Job Details:
Title: {job['title']}
Company: {job['company']}
Location: {job['location']}
Category/Tags: {job.get('category', 'General')}
Description Summary: {job['description'][:2000]}  # Truncated description

Determine if this job is suitable for an entry-level, fresher, or junior role that Manish can reasonably apply for and succeed in.
Roles should be Remote and open to candidates in India.

Return a JSON object with this exact structure:
{{
  "match": true or false,
  "title": "Cleaned Job Title (e.g. Associate Product Manager, Business Analyst Intern)",
  "company": "Company Name",
  "employment": "Full-time" or "Part-time",
  "chance": "Extremely High" or "Very High" or "Standard" (Extremely/Very High for academic doubt solvers, customer support, telesales, content writing, data entry, operations. Standard for APM/Analyst roles),
  "category": "Product Management" or "Business Analysis" or "Finance & Operations" or "Marketing & Growth" or "Sales & BD",
  "fits": "A 1-2 sentence explanation of why this job fits Manish's resume.",
  "tip": "A 1-2 sentence application tip focusing on what Manish should highlight from his resume."
}}
"""
    try:
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        data = json.loads(response.text)
        return data
    except Exception as e:
        print(f"Gemini API Error for job {job['title']} at {job['company']}: {e}")
        return {"match": False}

def fetch_remotive_jobs():
    print("Fetching jobs from Remotive API...")
    url = "https://remotive.com/api/remote-jobs"
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            jobs = data.get("jobs", [])
            print(f"Fetched {len(jobs)} jobs from Remotive.")
            return [
                {
                    "title": j.get("title"),
                    "company": j.get("company_name"),
                    "url": j.get("url"),
                    "location": j.get("candidate_required_location", "Worldwide"),
                    "description": j.get("description", ""),
                    "category": j.get("category", "")
                }
                for j in jobs
            ]
    except Exception as e:
        print(f"Error fetching from Remotive: {e}")
    return []

def fetch_jobicy_jobs():
    print("Fetching jobs from Jobicy API...")
    url = "https://jobicy.com/api/v2/remote-jobs"
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            jobs = data.get("jobs", [])
            print(f"Fetched {len(jobs)} jobs from Jobicy.")
            return [
                {
                    "title": j.get("jobTitle"),
                    "company": j.get("companyName"),
                    "url": j.get("url"),
                    "location": j.get("jobGeo", "Worldwide"),
                    "description": j.get("jobDescription", ""),
                    "category": j.get("jobIndustry", "")
                }
                for j in jobs
            ]
    except Exception as e:
        print(f"Error fetching from Jobicy: {e}")
    return []

def send_telegram_alert(new_jobs):
    print("Preparing to send Telegram alert...")
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    if not bot_token or not chat_id:
        print("Telegram credentials not found (TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID missing). Skipping alert.")
        return

    message = f"🚨 *{len(new_jobs)} New Remote Jobs Found!*\n\n"
    for i, job in enumerate(new_jobs[:5]): # limit to 5 to avoid message size limits
        message += f"*{i+1}. {job['title']}* at {job['company']}\n"
        message += f"Link: {job['url']}\n"
        message += f"Fits: _{job['fits']}_\n\n"
        
    if len(new_jobs) > 5:
        message += f"...and {len(new_jobs) - 5} more!\n\n"
        
    message += "🌐 [View your Dashboard](https://jobtracker-ten-zeta.vercel.app/)"

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print("Successfully sent Telegram alert!")
        else:
            print(f"Failed to send Telegram alert: {response.text}")
    except Exception as e:
        print(f"Error sending Telegram alert: {e}")

def main():
    print("Starting Automated Job Finder...")
    
    # Load existing jobs database
    jobs_file_path = os.path.join(os.path.dirname(__file__), "jobs.json")
    if os.path.exists(jobs_file_path):
        with open(jobs_file_path, "r", encoding="utf-8") as f:
            existing_jobs = json.load(f)
    else:
        existing_jobs = []
        
    print(f"Loaded {len(existing_jobs)} existing jobs from database.")
    
    # Get existing URLs to prevent duplicates
    existing_urls = {j.get("url") for j in existing_jobs if j.get("url")}
    
    # Check for Gemini API key
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("WARNING: GEMINI_API_KEY environment variable is not set!")
        print("Running in DRY-RUN mode. Script will fetch jobs but skip Gemini analysis.")
        model = None
    elif not HAS_GENAI:
        print("WARNING: google-generativeai package not installed!")
        print("Running in DRY-RUN mode.")
        model = None
    else:
        print("Gemini API key found. Initializing model...")
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')

    # Fetch jobs from APIs
    raw_jobs = []
    raw_jobs.extend(fetch_remotive_jobs())
    raw_jobs.extend(fetch_jobicy_jobs())
    
    if not raw_jobs:
        print("No raw jobs fetched. Exiting.")
        sys.exit(0)

    # Filter unique jobs that are not already in our database
    new_jobs = []
    seen_urls = set()
    for job in raw_jobs:
        url = job.get("url")
        if url and url not in existing_urls and url not in seen_urls:
            new_jobs.append(job)
            seen_urls.add(url)
            
    print(f"Found {len(new_jobs)} new unique jobs out of {len(raw_jobs)} total fetched jobs.")

    # Apply pre-filtering
    candidate_jobs = [j for j in new_jobs if pre_filter_job(j["title"], j["description"], j["location"])]
    print(f"Filtered down to {len(candidate_jobs)} potential entry-level remote jobs.")

    # We limit processing to top 15 candidates per run to conserve API rate limits/credits
    candidate_jobs = candidate_jobs[:15]
    print(f"Processing the top {len(candidate_jobs)} candidates with Gemini AI...")

    matched_jobs_count = 0
    new_matches = []

    for idx, job in enumerate(candidate_jobs):
        if not model:
            # Dry run / Simulated match for testing purposes
            print(f"Dry run: Suitability check for '{job['title']}' at '{job['company']}'")
            # Create a mock match if running dry run just to verify flow
            mock_match = {
                "match": True,
                "title": job["title"],
                "company": job["company"],
                "employment": "Full-time",
                "chance": "Standard",
                "category": "Business Analysis",
                "fits": "Automatically matched during dry run. Fits remote business analyst criteria.",
                "tip": "Review the job qualifications and highlight Excel skills."
            }
            # Only add one mock job for testing
            if idx == 0:
                mock_match["url"] = job["url"]
                new_matches.append(mock_match)
                matched_jobs_count += 1
            continue
            
        print(f"[{idx+1}/{len(candidate_jobs)}] Evaluating '{job['title']}' at '{job['company']}'...")
        gemini_result = evaluate_job_with_gemini(model, job)
        
        if gemini_result.get("match") is True:
            print(f"  -> MATCH FOUND! Category: {gemini_result.get('category')}")
            gemini_result["url"] = job["url"]
            # Add date discovered
            gemini_result["date_discovered"] = datetime.now().strftime("%Y-%m-%d")
            new_matches.append(gemini_result)
            matched_jobs_count += 1
        else:
            print("  -> No match.")
            
        # Respect rate limits
        time.sleep(4)

    print(f"Gemini analysis complete. Found {matched_jobs_count} new matches.")

    if new_matches:
        # Merge new matches into existing jobs
        # Add to the beginning of the list to display newest first
        updated_jobs = new_matches + existing_jobs
        
        # Limit the database to 150 jobs to keep file size lightweight
        updated_jobs = updated_jobs[:150]
        
        # Write back to jobs.json
        with open(jobs_file_path, "w", encoding="utf-8") as f:
            json.dump(updated_jobs, f, indent=4, ensure_ascii=False)
            
        print(f"Successfully updated jobs.json! Database now has {len(updated_jobs)} jobs.")
        
        # Send Alert
        send_telegram_alert(new_matches)

    else:
        print("No new matches found. Database remains unchanged.")

if __name__ == "__main__":
    main()
