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

def pre_filter_job(title, description, location, job_type="Remote"):
    """
    Do a quick keyword check to filter out obviously irrelevant jobs 
    before calling Gemini. Also enforces Location/Type rules.
    """
    title_lower = title.lower() if title else ""
    desc_lower = description.lower() if description else ""
    loc_lower = location.lower() if location else ""
    type_lower = job_type.lower() if job_type else "remote"

    # 1. Location & Type check
    allowed_cities = ["kolkata", "bengaluru", "bangalore", "pune", "delhi", "ncr", "noida", "gurgaon"]
    
    if "remote" not in type_lower and "remote" not in loc_lower and "worldwide" not in loc_lower and "anywhere" not in loc_lower:
        # It's hybrid or on-site. It MUST be in one of the allowed cities or "india" broadly
        if not any(city in loc_lower for city in allowed_cities) and "india" not in loc_lower:
            return False
            
    # Exclude US/UK specific unless it explicitly allows worldwide
    exclude_locations = ["us only", "usa only", "uk only", "europe only", "germany only", "canada only", "timezone: est", "timezone: pst", "united states", "united kingdom"]
    if any(loc in loc_lower for loc in exclude_locations) and "worldwide" not in loc_lower and "anywhere" not in loc_lower and "india" not in loc_lower:
        return False

    # 2. Seniority check
    exclude_seniority = ["senior", "lead", "staff", "principal", "director", "manager", "architect", "head of", "vp", "sr.", "head"]
    if any(word in title_lower for word in exclude_seniority):
        # We strictly exclude managers and senior roles for 0-2 years exp
        return False

    # 3. Technical & Science stack check (Strictly exclude science/engineering/tech)
    exclude_tech = ["devops", "kubernetes", "golang", "c++", "rust", "backend", "frontend", 
                    "fullstack", "software engineer", "infrastructure", "react native", "solidity", 
                    "blockchain", "science", "scientist", "chemistry", "physics", "biology", "data engineer",
                    "machine learning", "ai engineer", "clinical", "medical", "doctor", "nursing", "pharma"]
    if any(tech in title_lower for tech in exclude_tech):
        return False

    # 4. Target Keywords (Broad commerce)
    # Target keywords are things like Business Analyst, Sales, Marketing, HR, Operations
    if not any(word.lower() in title_lower for word in TARGET_KEYWORDS) and not any(word in title_lower for word in ["business", "sales", "marketing", "analyst"]):
        return False

    # 5. Experience check - exclude jobs requiring 3+ years of experience
    exp_pattern = r"(?:require|minimum|at least|with)\s+(?:[3-9]|\d{2,})\s*\+?\s*(?:-\s*\d+\s*)?(?:years?|yrs?)"
    if re.search(exp_pattern, desc_lower):
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
Type: {job.get('type', 'Remote')}
Description Summary: {job['description'][:2500]}

Determine if this job is suitable for an ambitious Commerce fresher (Manish).
The role must be in Commerce/Business fields (Business Analysis, Business Development, Marketing, Content, Research, HR, Operations).
Locations allowed: Kolkata, Bangalore, Pune, Delhi, or Remote worldwide.

CRITICAL RULES:
1. FIRST PRIORITY is Fresher suitable jobs / Internships (0 years experience).
2. SECOND PRIORITY is jobs asking for 1 to 2 years of experience.
3. If the job description explicitly asks for 3 or more years of experience, you MUST return "match": false.

Return a JSON object with this exact structure:
{{
  "match": true or false,
  "title": "Cleaned Job Title",
  "company": "Company Name",
  "employment": "Full-time" or "Part-time" or "Internship",
  "chance": "Extremely High" or "Very High" or "Standard",
  "category": "Business Analysis" or "Sales & BD" or "Marketing" or "Human Resources" or "Operations",
  "fits": "A 1-2 sentence explanation of why this job fits Manish's resume.",
  "tip": "A 1-2 sentence application tip focusing on what Manish should highlight."
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

def fetch_internshala_jobs():
    print("Fetching jobs from Internshala...")
    jobs = []
    url = "https://internshala.com/jobs/fresher-jobs/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        from bs4 import BeautifulSoup
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            job_cards = soup.find_all('div', class_='individual_internship')
            for card in job_cards:
                title_elem = card.find('h3', class_='job-title')
                company_elem = card.find('p', class_='company-name')
                location_elem = card.find('a', class_='location_link')
                link_elem = card.find('a', class_='job-title-href')
                
                if title_elem and company_elem and link_elem:
                    title = title_elem.text.strip()
                    company = company_elem.text.strip()
                    location = location_elem.text.strip() if location_elem else "India"
                    job_url = "https://internshala.com" + link_elem['href']
                    
                    job_type = "Remote" if "remote" in location.lower() or "work from home" in location.lower() else "On-site"
                    
                    jobs.append({
                        "title": title,
                        "company": company,
                        "url": job_url,
                        "location": location,
                        "description": "Internshala Fresher Job.", # Description evaluated by Gemini from title/company context if needed, but Internshala doesn't expose desc on search page easily.
                        "category": "Fresher Job",
                        "type": job_type
                    })
            print(f"Fetched {len(jobs)} jobs from Internshala.")
    except ImportError:
        print("BeautifulSoup not installed. Skipping Internshala.")
    except Exception as e:
        print(f"Error fetching from Internshala: {e}")
    return jobs

def fetch_jobspy_jobs():
    print("Fetching jobs via JobSpy (Indeed, LinkedIn, Glassdoor)...")
    jobs = []
    try:
        from jobspy import scrape_jobs
        import pandas as pd
        
        # We target specific locations and search terms
        search_terms = ["Business Analyst", "Sales", "Business Development", "Marketing"]
        locations = ["Kolkata", "Bengaluru", "Pune", "Delhi"]
        
        for term in search_terms:
            for loc in locations:
                df = scrape_jobs(
                    site_name=["indeed", "linkedin", "glassdoor"],
                    search_term=term,
                    location=loc,
                    results_wanted=10,
                    country_indeed='india'
                )
                if not df.empty:
                    for _, row in df.iterrows():
                        title = str(row.get('title', ''))
                        company = str(row.get('company', ''))
                        job_url = str(row.get('job_url', ''))
                        location_val = str(row.get('location', loc))
                        description = str(row.get('description', ''))
                        is_remote = row.get('is_remote', False)
                        job_type = "Remote" if is_remote else "On-site"
                        
                        jobs.append({
                            "title": title,
                            "company": company,
                            "url": job_url,
                            "location": location_val,
                            "description": description[:2000] if description != 'nan' else "Description unavailable.",
                            "category": "Aggregated Job",
                            "type": job_type
                        })
                
                # Small sleep to prevent immediate rate limit blocking
                time.sleep(2)
                
        print(f"Fetched {len(jobs)} jobs from JobSpy across categories.")
    except ImportError:
        print("python-jobspy not installed. Skipping.")
    except Exception as e:
        print(f"Error fetching from JobSpy: {e}")
    return jobs

def fetch_remotive_jobs():
    print("Fetching jobs from Remotive API (Global Remote)...")
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
                    "category": j.get("category", ""),
                    "type": "Remote"
                }
                for j in jobs
            ]
    except Exception as e:
        print(f"Error fetching from Remotive: {e}")
    return []

def fetch_jobicy_jobs():
    print("Fetching jobs from Jobicy API (Global Remote)...")
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
                    "category": j.get("jobIndustry", ""),
                    "type": "Remote"
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

    if not new_jobs:
        message = "✅ *Job Tracker Update*\n\nI just scanned Internshala & Job Boards but didn't find any *new* entry-level Commerce/BA jobs matching your profile.\n\nI'll check again in 24 hours!\n\n🌐 [View your Dashboard](https://jobtracker-ten-zeta.vercel.app/)"
    else:
        message = f"🚨 *{len(new_jobs)} New Jobs Found! (Remote & On-Site)*\n\n"
        for i, job in enumerate(new_jobs[:5]): 
            message += f"*{i+1}. {job['title']}* at {job['company']}\n"
            message += f"Type: {job.get('type', 'Remote')} | Loc: {job.get('location', 'India')}\n"
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

def cleanup_dead_jobs(jobs_list):
    print(f"Cleaning up dead links from {len(jobs_list)} existing jobs...")
    cleaned = []
    removed_count = 0
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    closure_phrases = [
        "no longer available", "job is closed", "position has been filled", 
        "page not found", "404 not found", "this job has expired"
    ]
    
    for idx, job in enumerate(jobs_list):
        url = job.get("url")
        if not url:
            continue
            
        try:
            response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
            is_dead = False
            
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
            
            if is_dead:
                print(f"  [Auto-Cleanup] Removing dead job: {job.get('title')} ({reason})")
                removed_count += 1
            else:
                cleaned.append(job)
                
        except Exception as e:
            print(f"  [Auto-Cleanup] Removing dead job: {job.get('title')} (Connection Error)")
            removed_count += 1
            
    print(f"Cleanup finished. Removed {removed_count} dead jobs.")
    return cleaned, removed_count

def main():
    print("Starting Automated Job Finder (India Fresher Edition)...")
    
    jobs_file_path = os.path.join(os.path.dirname(__file__), "jobs.json")
    if os.path.exists(jobs_file_path):
        try:
            with open(jobs_file_path, "r", encoding="utf-8") as f:
                existing_jobs = json.load(f)
        except:
            existing_jobs = []
    else:
        existing_jobs = []
        
    print(f"Loaded {len(existing_jobs)} existing jobs from database.")
    
    existing_jobs, removed_count = cleanup_dead_jobs(existing_jobs)
    existing_urls = {j.get("url") for j in existing_jobs if j.get("url")}
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("WARNING: GEMINI_API_KEY environment variable is not set!")
        model = None
    elif not HAS_GENAI:
        print("WARNING: google-generativeai package not installed!")
        model = None
    else:
        print("Gemini API key found. Initializing model...")
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')

    raw_jobs = []
    raw_jobs.extend(fetch_internshala_jobs())
    raw_jobs.extend(fetch_jobspy_jobs())
    raw_jobs.extend(fetch_remotive_jobs())
    raw_jobs.extend(fetch_jobicy_jobs())
    
    if not raw_jobs:
        print("No raw jobs fetched. Exiting.")
        sys.exit(0)

    new_jobs = []
    seen_urls = set()
    for job in raw_jobs:
        url = job.get("url")
        if url and url not in existing_urls and url not in seen_urls:
            new_jobs.append(job)
            seen_urls.add(url)
            
    print(f"Found {len(new_jobs)} new unique jobs out of {len(raw_jobs)} total fetched jobs.")

    candidate_jobs = [j for j in new_jobs if pre_filter_job(j["title"], j["description"], j["location"], j.get("type"))]
    print(f"Filtered down to {len(candidate_jobs)} potential entry-level jobs.")

    candidate_jobs = candidate_jobs[:20]
    print(f"Processing the top {len(candidate_jobs)} candidates with Gemini AI...")

    matched_jobs_count = 0
    new_matches = []

    for idx, job in enumerate(candidate_jobs):
        if not model:
            print(f"Dry run: Suitability check for '{job['title']}'")
            if idx == 0:
                mock_match = {
                    "match": True,
                    "title": job["title"],
                    "company": job["company"],
                    "employment": "Full-time",
                    "chance": "Standard",
                    "category": "Business Analysis",
                    "fits": "Automatically matched during dry run.",
                    "tip": "Highlight relevant skills.",
                    "type": job.get("type", "On-site"),
                    "location": job.get("location", "Kolkata"),
                    "url": job["url"],
                    "date_discovered": datetime.now().strftime("%Y-%m-%d")
                }
                new_matches.append(mock_match)
                matched_jobs_count += 1
            continue
            
        print(f"[{idx+1}/{len(candidate_jobs)}] Evaluating '{job['title']}' at '{job['company']}'...")
        gemini_result = evaluate_job_with_gemini(model, job)
        
        if gemini_result.get("match") is True:
            print(f"  -> MATCH FOUND! Category: {gemini_result.get('category')}")
            gemini_result["url"] = job["url"]
            gemini_result["type"] = job.get("type", "On-site")
            gemini_result["location"] = job.get("location", "India")
            gemini_result["date_discovered"] = datetime.now().strftime("%Y-%m-%d")
            new_matches.append(gemini_result)
            matched_jobs_count += 1
        else:
            print("  -> No match.")
            
        time.sleep(3)

    print(f"Gemini analysis complete. Found {matched_jobs_count} new matches.")

    if new_matches or removed_count > 0:
        updated_jobs = new_matches + existing_jobs
        updated_jobs = updated_jobs[:150]
        
        with open(jobs_file_path, "w", encoding="utf-8") as f:
            json.dump(updated_jobs, f, indent=4, ensure_ascii=False)
            
        print(f"Successfully updated jobs.json! Database now has {len(updated_jobs)} jobs.")
        send_telegram_alert(new_matches)

    else:
        print("No new matches found and no dead jobs removed. Database remains unchanged.")
        send_telegram_alert([])

if __name__ == "__main__":
    main()
