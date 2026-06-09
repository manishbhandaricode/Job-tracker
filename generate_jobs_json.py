import json

# Combine the datasets from generate_tracker.py and generate_part_time_tracker.py, removing duplicates.
# Total unique jobs: ~105 roles.

jobs_combined = [
    # --- PRODUCT MANAGEMENT & PRODUCT ANALYSIS ---
    {
        "title": "Associate Product Manager",
        "company": "Groww (India)",
        "category": "Product Management",
        "employment": "Full-time",
        "chance": "Standard",
        "url": "https://groww.in/careers",
        "fits": "WealthTech platform. Aligns with your Perccent internship and SIP spec project.",
        "tip": "Attach your 'Product Specification: Core Wealth Tools' project and highlight acceptance criteria."
    },
    {
        "title": "Product Analyst",
        "company": "Kayzen (India)",
        "category": "Product Management",
        "employment": "Full-time",
        "chance": "Very High",
        "url": "https://boards.greenhouse.io/kayzen",
        "fits": "Focus on data analytics and SQL. Leverages your Tata Data Visualisation certification.",
        "tip": "Highlight your experience authoring product specs and translating strategic research into dashboards."
    },
    {
        "title": "Product Analyst",
        "company": "Kernel DAO (India)",
        "category": "Product Management",
        "employment": "Full-time",
        "chance": "Very High",
        "url": "https://boards.greenhouse.io/kerneldao",
        "fits": "DeFi & liquidity focus. Aligns with your CRED x Kuvera M&A project and Perccent WealthTech experience.",
        "tip": "Discuss your analysis of SEBI RIA capabilities and monetization challenges in CRED/Kuvera project."
    },
    {
        "title": "Associate Product Manager",
        "company": "YipitData (India)",
        "category": "Product Management",
        "employment": "Full-time",
        "chance": "Very High",
        "url": "https://job-boards.greenhouse.io/yipitdatajobs",
        "fits": "Market intelligence. Aligns with your competitive benchmarking skills.",
        "tip": "Highlight your WealthTech competitor analysis and data-driven approach."
    },
    {
        "title": "Product Analyst Intern",
        "company": "Simpl (India)",
        "category": "Product Management",
        "employment": "Part-time",
        "chance": "Extremely High",
        "url": "https://getsimpl.com/careers",
        "fits": "BNPL/FinTech. Fits your understanding of digital wealth and payments. Flexible internship.",
        "tip": "Highlight NetBanking and UPI mandate flow designs from your wealth tools project."
    },
    {
        "title": "Product Analyst",
        "company": "Pearl (India)",
        "category": "Product Management",
        "employment": "Full-time",
        "chance": "Very High",
        "url": "https://boards.greenhouse.io/pearl",
        "fits": "Global AI network. Matches your data-driven problem-solving projects.",
        "tip": "Highlight your working capital statistical correlation study to prove analytical depth."
    },
    {
        "title": "APM Intern (Remote)",
        "company": "Acko (India)",
        "category": "Product Management",
        "employment": "Part-time",
        "chance": "Extremely High",
        "url": "https://www.acko.com/careers/",
        "fits": "Digital insurance startup. Fits your product spec writing and analytics skills.",
        "tip": "Focus on your structured problem-solving and documentation skills (PRDs)."
    },
    {
        "title": "Product Management Intern",
        "company": "Unstop Jobs (India)",
        "category": "Product Management",
        "employment": "Part-time",
        "chance": "Extremely High",
        "url": "https://unstop.com/internships?specialisation=Product%20Management",
        "fits": "Curated remote product internships for freshers with flexible/part-time hours.",
        "tip": "Make sure your Framer project links are clickable on your resume."
    },
    {
        "title": "Junior Product Analyst",
        "company": "Fi Money (India)",
        "category": "Product Management",
        "employment": "Full-time",
        "chance": "Very High",
        "url": "https://fi.money/careers",
        "fits": "Neo-banking platform. Matches your interest in digital wealth and UPI mandates.",
        "tip": "Showcase your 'Product Specification' project and your Perccent internship."
    },
    {
        "title": "Associate Product Manager",
        "company": "Jupiter Money (India)",
        "category": "Product Management",
        "employment": "Full-time",
        "chance": "Very High",
        "url": "https://jupiter.money/careers/",
        "fits": "Digital banking & wealth management. Perfect fit for B.Com with product specs.",
        "tip": "Highlight your understanding of Step-Up SIP and CAGR toggle logic."
    },
    {
        "title": "Product Intern",
        "company": "NextLeap (India)",
        "category": "Product Management",
        "employment": "Part-time",
        "chance": "Extremely High",
        "url": "https://nextleap.app/",
        "fits": "Product-focused community. Great for freshers, flexible hours.",
        "tip": "Highlight acceptance criteria writing experience and structured document writing."
    },
    {
        "title": "APM Remote India",
        "company": "Indeed India",
        "category": "Product Management",
        "employment": "Full-time",
        "chance": "Standard",
        "url": "https://in.indeed.com/q-associate-product-manager-l-remote-jobs.html",
        "fits": "Aggregated active remote APM roles in India.",
        "tip": "Set daily alerts and apply within 24 hours of posting for maximum visibility."
    },

    # --- BUSINESS ANALYSIS & DATA/MARKET RESEARCH ---
    {
        "title": "Business Analyst (Remote)",
        "company": "WIN Home Inspection (India)",
        "category": "Business Analysis",
        "employment": "Full-time",
        "chance": "Standard",
        "url": "https://boards.greenhouse.io/winhomeinspection",
        "fits": "Focus on research and strategic initiatives. Fits your B.Com.",
        "tip": "Highlight your market analysis of Kuvera and Dezerv from your internship."
    },
    {
        "title": "Business Analyst - Data & AI",
        "company": "Valtech (India)",
        "category": "Business Analysis",
        "employment": "Full-time",
        "chance": "Very High",
        "url": "https://boards.greenhouse.io/valtech",
        "fits": "High-growth digital agency. Leverages data visualization skills.",
        "tip": "Emphasize Tata Data Visualisation certification and dashboard understanding."
    },
    {
        "title": "Lead Business Intelligence Analyst",
        "company": "Cision (India)",
        "category": "Business Analysis",
        "employment": "Full-time",
        "chance": "Very High",
        "url": "https://boards.greenhouse.io/cision",
        "fits": "Modern BI stack. Fits your statistical analysis projects.",
        "tip": "Highlight correlation of working capital with profitability in FMCG study."
    },
    {
        "title": "Data QA Associate",
        "company": "YipitData (India)",
        "category": "Business Analysis",
        "employment": "Full-time",
        "chance": "Very High",
        "url": "https://job-boards.greenhouse.io/yipitdatajobs",
        "fits": "Data cleaning and quality assurance. Matches Excel/data skills.",
        "tip": "Highlight database operations, Excel, and data-driven projects."
    },
    {
        "title": "Junior Business Analyst",
        "company": "AlphaSense (India)",
        "category": "Business Analysis",
        "employment": "Full-time",
        "chance": "Very High",
        "url": "https://boards.greenhouse.io/alphasense",
        "fits": "Financial search engine support. Perfect for B.Com graduates.",
        "tip": "Showcase your competitive benchmarking of Dezerv and Kuvera."
    },
    {
        "title": "Business Research Intern",
        "company": "Perccent (Return Opp)",
        "category": "Business Analysis",
        "employment": "Part-time",
        "chance": "Extremely High",
        "url": "https://manishbhandari.framer.website/",
        "fits": "Check for return/contract extensions at Perccent.",
        "tip": "Leverage your existing relationships and success at the firm."
    },
    {
        "title": "Business Analyst Intern",
        "company": "Unstop Jobs (India)",
        "category": "Business Analysis",
        "employment": "Part-time",
        "chance": "Extremely High",
        "url": "https://unstop.com/internships?specialisation=Business%20Analysis",
        "fits": "Fresher internships in business analysis. Part-time.",
        "tip": "Highlight Excel, SQL, and Notion proficiency in your skills section."
    },
    {
        "title": "Business Analyst Remote",
        "company": "Instahyre (India)",
        "category": "Business Analysis",
        "employment": "Full-time",
        "chance": "Standard",
        "url": "https://www.instahyre.com/jobs-in-india/?search=Business+Analyst",
        "fits": "Remote startup business analyst listings in India.",
        "tip": "Highlight your corporate accounting and financial system courses."
    },
    {
        "title": "Junior Analyst",
        "company": "Cutshort (India)",
        "category": "Business Analysis",
        "employment": "Full-time",
        "chance": "Standard",
        "url": "https://cutshort.io/jobs/remote-business-analyst-jobs",
        "fits": "Remote BA roles on Cutshort.",
        "tip": "Focus on your analytical skills and Perccent experience."
    },
    {
        "title": "Data Analyst (Remote)",
        "company": "Indeed India",
        "category": "Business Analysis",
        "employment": "Full-time",
        "chance": "Standard",
        "url": "https://in.indeed.com/q-data-analyst-l-remote-jobs.html",
        "fits": "Aggregated data roles in India.",
        "tip": "Emphasize data visualization and working capital statistical study."
    },
    {
        "title": "Business Intelligence Intern",
        "company": "Shadowfax (India)",
        "category": "Business Analysis",
        "employment": "Part-time",
        "chance": "Extremely High",
        "url": "https://www.shadowfax.in/careers",
        "fits": "Logistics tech company. Part-time/flexible analytics internship.",
        "tip": "Showcase your data visualization skills and working capital FMCG study."
    },
    {
        "title": "Business Analyst",
        "company": "InVideo (India)",
        "category": "Business Analysis",
        "employment": "Full-time",
        "chance": "Very High",
        "url": "https://invideo.io/careers/",
        "fits": "Remote-first video creation SaaS. High growth startup.",
        "tip": "Showcase your ability to write detailed user stories and translate specs."
    },

    # --- FINANCE & OPERATIONS ---
    {
        "title": "Operations Associate",
        "company": "Kuvera (CRED) (India)",
        "category": "Finance & Operations",
        "employment": "Full-time",
        "chance": "Very High",
        "url": "https://grow.kuvera.in/",
        "fits": "Wealth operations. Fits your M&A Strategic Analysis of CRED x Kuvera.",
        "tip": "Emphasize your understanding of NetBanking and UPI mandate flows."
    },
    {
        "title": "Associate Portfolio Data Analyst",
        "company": "Addepar (India)",
        "category": "Finance & Operations",
        "employment": "Full-time",
        "chance": "Very High",
        "url": "https://boards.greenhouse.io/addepar",
        "fits": "Wealth management technology. Perfectly matches B.Com and WealthTech.",
        "tip": "Highlight corporate accounting courses and Perccent internship."
    },
    {
        "title": "Alts Data Operations Analyst",
        "company": "Addepar (India)",
        "category": "Finance & Operations",
        "employment": "Full-time",
        "chance": "Very High",
        "url": "https://boards.greenhouse.io/addepar",
        "fits": "Alternative investments. Aligns with minor/NRI investor research.",
        "tip": "Showcase your research on fee models and untapped investor segments."
    },
    {
        "title": "Procurement Analyst",
        "company": "Precision Medicine Group (India)",
        "category": "Finance & Operations",
        "employment": "Full-time",
        "chance": "Standard",
        "url": "https://boards.greenhouse.io/precisionmedicinegroup",
        "fits": "Finance and purchasing. Fits B.Com degree.",
        "tip": "Emphasize corporate accounting and tax courses."
    },
    {
        "title": "Graduate Financial Analyst",
        "company": "Zomato (India)",
        "category": "Finance & Operations",
        "employment": "Full-time",
        "chance": "Standard",
        "url": "https://www.zomato.com/careers",
        "fits": "Entry-level finance. Fits B.Com education.",
        "tip": "Highlight your Working Capital Management analysis project."
    },
    {
        "title": "Finance Operations Associate",
        "company": "Razorpay (India)",
        "category": "Finance & Operations",
        "employment": "Full-time",
        "chance": "Very High",
        "url": "https://razorpay.com/jobs/",
        "fits": "Payment gateway operations. Fits netbanking/UPI spec project.",
        "tip": "Showcase your spec writing for UPI mandate and netbanking flows."
    },
    {
        "title": "Operations Associate",
        "company": "Paytm (India)",
        "category": "Finance & Operations",
        "employment": "Full-time",
        "chance": "Standard",
        "url": "https://careers.paytm.com/",
        "fits": "Wealth and fintech operations. Perfect for B.Com.",
        "tip": "Highlight your Perccent research on AUM trends and fee models."
    },
    {
        "title": "Junior Finance Analyst",
        "company": "Paytm Money (India)",
        "category": "Finance & Operations",
        "employment": "Full-time",
        "chance": "Standard",
        "url": "https://careers.paytm.com/",
        "fits": "Mutual funds and wealth management. Fits B.Com.",
        "tip": "Emphasize your Step-Up SIP and CAGR toggle acceptance criteria."
    },
    {
        "title": "Finance Intern",
        "company": "Unstop Jobs (India)",
        "category": "Finance & Operations",
        "employment": "Part-time",
        "chance": "Extremely High",
        "url": "https://unstop.com/internships?specialisation=Finance",
        "fits": "Remote finance internships for B.Com students. Part-time.",
        "tip": "Highlight SGPA: 8.10 and corporate accounting academic work."
    },
    {
        "title": "Financial Analyst Remote",
        "company": "Indeed India",
        "category": "Finance & Operations",
        "employment": "Full-time",
        "chance": "Standard",
        "url": "https://in.indeed.com/q-financial-analyst-l-remote-jobs.html",
        "fits": "Aggregated remote finance roles in India.",
        "tip": "Highlight FMCG Working Capital project (HUL, ITC, Nestle)."
    },
    {
        "title": "Finance Intern",
        "company": "Zepto (India)",
        "category": "Finance & Operations",
        "employment": "Part-time",
        "chance": "Extremely High",
        "url": "https://www.zepto.co.in/careers",
        "fits": "Quick commerce. Part-time finance/working capital internship.",
        "tip": "Highlight your FMCG Working Capital project (CCC and turnover cycles)."
    },
    {
        "title": "Operations Analyst",
        "company": "InVideo (India)",
        "category": "Finance & Operations",
        "employment": "Full-time",
        "chance": "Very High",
        "url": "https://invideo.io/careers/",
        "fits": "Operations management. Fits outreach and Notion skills.",
        "tip": "Highlight structured problem-solving and client outreach skills."
    },

    # --- MARKETING, CONTENT & GROWTH ---
    {
        "title": "Growth Marketing Intern",
        "company": "Classplus (India)",
        "category": "Marketing & Growth",
        "employment": "Part-time",
        "chance": "Extremely High",
        "url": "https://classplusapp.com/careers",
        "fits": "EdTech growth and marketing. Part-time/flexible hours.",
        "tip": "Highlight Canva, Framer, and LinkedIn content creation."
    },
    {
        "title": "Growth Associate (Intern)",
        "company": "Unstop Jobs (India)",
        "category": "Marketing & Growth",
        "employment": "Part-time",
        "chance": "Extremely High",
        "url": "https://unstop.com/internships?specialisation=Marketing",
        "fits": "Remote marketing/growth internships in India. Part-time.",
        "tip": "Showcase Google Fundamentals of Marketing certification."
    },
    {
        "title": "Growth Marketing Associate",
        "company": "Simpl (India)",
        "category": "Marketing & Growth",
        "employment": "Full-time",
        "chance": "Very High",
        "url": "https://getsimpl.com/careers",
        "fits": "Fintech growth and user acquisition.",
        "tip": "Highlight social media marketing content created for Perccent."
    },
    {
        "title": "Marketing Analyst",
        "company": "YipitData (India)",
        "category": "Marketing & Growth",
        "employment": "Full-time",
        "chance": "Very High",
        "url": "https://job-boards.greenhouse.io/yipitdatajobs",
        "fits": "Marketing data analysis. Fits marketing certification & data.",
        "tip": "Emphasize Tata Data Visualisation and Google Marketing."
    },
    {
        "title": "Content Marketing Associate",
        "company": "Groww (India)",
        "category": "Marketing & Growth",
        "employment": "Full-time",
        "chance": "Standard",
        "url": "https://groww.in/careers",
        "fits": "WealthTech education and content. Fits creative writing.",
        "tip": "Mention LinkedIn and Instagram content management at Perccent."
    },
    {
        "title": "Growth Associate",
        "company": "Paytm (India)",
        "category": "Marketing & Growth",
        "employment": "Full-time",
        "chance": "Standard",
        "url": "https://careers.paytm.com/",
        "fits": "Fintech marketing and growth. Fits marketing background.",
        "tip": "Mention Google Fundamentals of Marketing and Canva/Framer skills."
    },
    {
        "title": "Growth Associate",
        "company": "Instahyre (India)",
        "category": "Marketing & Growth",
        "employment": "Full-time",
        "chance": "Standard",
        "url": "https://www.instahyre.com/jobs-in-india/?search=Marketing+Associate",
        "fits": "Remote startup marketing roles on Instahyre.",
        "tip": "Emphasize brand engagement metrics driven during Perccent internship."
    },
    {
        "title": "Digital Marketing Intern",
        "company": "Internshala (India)",
        "category": "Marketing & Growth",
        "employment": "Part-time",
        "chance": "Extremely High",
        "url": "https://internshala.com/internships/work-from-home-marketing-internships/",
        "fits": "Remote marketing internships in India. Part-time.",
        "tip": "Show your portfolio website and creative writing samples."
    },
    {
        "title": "Social Media & Design Intern",
        "company": "InVideo (India)",
        "category": "Marketing & Growth",
        "employment": "Part-time",
        "chance": "Extremely High",
        "url": "https://invideo.io/careers/",
        "fits": "Social media content and Framer/Canva design. Part-time.",
        "tip": "Pitch your Perccent brand engagement metrics and Framer website link."
    },
    {
        "title": "Marketing Associate",
        "company": "Classplus (India)",
        "category": "Marketing & Growth",
        "employment": "Full-time",
        "chance": "Standard",
        "url": "https://classplusapp.com/careers",
        "fits": "Edtech platform marketing. Fits outreach & writing.",
        "tip": "Highlight outreach and client communication soft skills."
    },

    # --- BUSINESS DEVELOPMENT, OUTREACH & SALES ---
    {
        "title": "Business Development Associate",
        "company": "upGrad (India)",
        "category": "Sales & BD",
        "employment": "Full-time",
        "chance": "Standard",
        "url": "https://www.upgrad.com/careers/",
        "fits": "Higher education sales. Fits PepsiCo Sales simulation.",
        "tip": "Highlight your PepsiCo Sales Job Simulation certification."
    },
    {
        "title": "Sales Operations Associate",
        "company": "Razorpay (India)",
        "category": "Sales & BD",
        "employment": "Full-time",
        "chance": "Very High",
        "url": "https://razorpay.com/jobs/",
        "fits": "Fintech sales support and client outreach.",
        "tip": "Highlight client communication and outreach soft skills."
    },
    {
        "title": "Business Development Intern",
        "company": "Unstop Jobs (India)",
        "category": "Sales & BD",
        "employment": "Part-time",
        "chance": "Extremely High",
        "url": "https://unstop.com/internships?specialisation=Business%20Development",
        "fits": "BD internships with remote options. Part-time.",
        "tip": "Emphasize leadership and client communication."
    },
    {
        "title": "Client Success Associate",
        "company": "AlphaSense (India)",
        "category": "Sales & BD",
        "employment": "Full-time",
        "chance": "Very High",
        "url": "https://boards.greenhouse.io/alphasense",
        "fits": "Financial platform customer onboarding. Fits B.Com.",
        "tip": "Show how your Perccent experience helps you understand client needs."
    },
    {
        "title": "Inside Sales Associate",
        "company": "upGrad (India)",
        "category": "Sales & BD",
        "employment": "Full-time",
        "chance": "Standard",
        "url": "https://www.upgrad.com/careers/",
        "fits": "Outbound student counseling and sales.",
        "tip": "Highlight outreach and leadership soft skills."
    },
    {
        "title": "Sales Intern",
        "company": "PepsiCo (India) (Return)",
        "category": "Sales & BD",
        "employment": "Part-time",
        "chance": "Extremely High",
        "url": "https://www.pepsicojobs.com/",
        "fits": "Keep an eye on PepsiCo careers. Fits Sales simulation. Part-time.",
        "tip": "Lead with your PepsiCo Sales Job Simulation completion."
    },
    {
        "title": "Business Development Associate",
        "company": "Instahyre (India)",
        "category": "Sales & BD",
        "employment": "Full-time",
        "chance": "Standard",
        "url": "https://www.instahyre.com/jobs-in-india/?search=Business+Development+Associate",
        "fits": "Startup sales roles on Instahyre in India.",
        "tip": "Emphasize outreach and problem-solving skills."
    },
    {
        "title": "Business Development Intern",
        "company": "Internshala (India)",
        "category": "Sales & BD",
        "employment": "Part-time",
        "chance": "Extremely High",
        "url": "https://internshala.com/internships/work-from-home-business-development-internships/",
        "fits": "Remote BD internships for students in India. Part-time.",
        "tip": "Highlight sales simulation and client communication skills."
    },
    {
        "title": "Customer Success Analyst",
        "company": "Pocket FM (India)",
        "category": "Sales & BD",
        "employment": "Full-time",
        "chance": "Very High",
        "url": "https://www.pocketfm.com/careers",
        "fits": "Remote customer success roles at audio platform.",
        "tip": "Highlight problem-solving and creative writing."
    },
    {
        "title": "Business Development Associate",
        "company": "Indeed India",
        "category": "Sales & BD",
        "employment": "Full-time",
        "chance": "Standard",
        "url": "https://in.indeed.com/q-business-development-associate-l-remote-jobs.html",
        "fits": "Aggregated BD roles in India.",
        "tip": "Emphasize communication skills and sales training."
    },
    
    # --- ADDITIONAL UNIQUE PART-TIME EASY-HIRE OPPORTUNITIES ---
    {
        "title": "Subject Matter Expert (Commerce)",
        "company": "Chegg India",
        "category": "Finance & Operations",
        "employment": "Part-time",
        "chance": "Extremely High",
        "url": "https://www.cheggindia.com/",
        "fits": "Directly uses your B.Com knowledge and Corporate Accounting courses.",
        "tip": "Pass a basic online MCQ test in accounting. Very high selection rate once passed."
    },
    {
        "title": "Doubt Solving Expert (Accounting)",
        "company": "Doubtnut (India)",
        "category": "Finance & Operations",
        "employment": "Part-time",
        "chance": "Extremely High",
        "url": "https://www.doubtnut.com/",
        "fits": "Fits your Corporate Accounting and Direct Tax coursework.",
        "tip": "Register as an expert and solve sample commerce problems online."
    },
    {
        "title": "Brainly Moderator (Part-time)",
        "company": "Brainly India",
        "category": "Business Analysis",
        "employment": "Part-time",
        "chance": "Extremely High",
        "url": "https://brainly.in/",
        "fits": "Reviewing commerce doubts. Fits B.Com degree.",
        "tip": "Apply through their contributor program. Focus on accuracy and clear writing."
    },
    {
        "title": "Commerce QA Expert",
        "company": "Toppr (India)",
        "category": "Finance & Operations",
        "employment": "Part-time",
        "chance": "Extremely High",
        "url": "https://www.toppr.com/",
        "fits": "Answering commerce questions. Fits B.Com education.",
        "tip": "Take their simple subject competency test. Highly flexible hours."
    },
    {
        "title": "Accounting Doubt Solver",
        "company": "Kunduz India",
        "category": "Finance & Operations",
        "employment": "Part-time",
        "chance": "Extremely High",
        "url": "https://kunduz.com/",
        "fits": "Solving basic accounting questions. Matches B.Com.",
        "tip": "Download the Kunduz Tutor app, upload your B.Com ID/degree, and start solving."
    },
    {
        "title": "GST/Tax Doubt Solver",
        "company": "Taxmann (India)",
        "category": "Finance & Operations",
        "employment": "Part-time",
        "chance": "Extremely High",
        "url": "https://www.taxmann.com/",
        "fits": "Fits your Direct Tax and GST courses listed on your resume.",
        "tip": "Highlight your specific academic courses in Direct Tax and GST."
    },
    {
        "title": "Commerce Tutor (Part-time)",
        "company": "Cuemath (India)",
        "category": "Finance & Operations",
        "employment": "Part-time",
        "chance": "Very High",
        "url": "https://www.cuemath.com/",
        "fits": "Matches B.Com and tutoring/moderation interests.",
        "tip": "Highlight your SGPA (8.10) to show strong academic performance."
    },
    {
        "title": "Academic Writer (Commerce)",
        "company": "Unstop Jobs (India)",
        "category": "Finance & Operations",
        "employment": "Part-time",
        "chance": "Extremely High",
        "url": "https://unstop.com/internships",
        "fits": "Answering commerce questions. Matches B.Com.",
        "tip": "Highlight your corporate accounting and financial system courses."
    },
    {
        "title": "Online Commerce Tutor",
        "company": "Internshala Jobs (India)",
        "category": "Finance & Operations",
        "employment": "Part-time",
        "chance": "Extremely High",
        "url": "https://internshala.com/internships/work-from-home-teaching-internships/",
        "fits": "Tutor B.Com and higher secondary students.",
        "tip": "Pitch your high academic performance (SGPA 8.10) and clear communication."
    },
    {
        "title": "Data Entry Operator",
        "company": "Awign (India)",
        "category": "Finance & Operations",
        "employment": "Part-time",
        "chance": "Extremely High",
        "url": "https://www.awign.com/",
        "fits": "Data entry. Matches your Google Docs and Notion technical skills.",
        "tip": "Complete their basic training module on the Awign app to get assigned."
    },
    {
        "title": "Cataloging Associate",
        "company": "Blinkit (India)",
        "category": "Finance & Operations",
        "employment": "Part-time",
        "chance": "Extremely High",
        "url": "https://blinkit.com/careers",
        "fits": "Entering grocery item data. Matches basic computer skills.",
        "tip": "Mention your FMCG project analyzing cycles of HUL, ITC, and Nestle."
    },
    {
        "title": "Virtual Assistant (Part-time)",
        "company": "Internshala Jobs (India)",
        "category": "Finance & Operations",
        "employment": "Part-time",
        "chance": "Extremely High",
        "url": "https://internshala.com/internships/work-from-home-data-entry-internships/",
        "fits": "Calendar management, emails. Matches Google Docs/Notion.",
        "tip": "Highlight your soft skills in leadership and creative writing."
    },
    {
        "title": "Data Entry Remote",
        "company": "Indeed India",
        "category": "Finance & Operations",
        "employment": "Part-time",
        "chance": "Extremely High",
        "url": "https://in.indeed.com/q-part-time-data-entry-l-remote-jobs.html",
        "fits": "Form entry. Matches MS PowerPoint and Google Docs.",
        "tip": "Filter for 'Urgent Hiring' tags. Apply to multiple listings daily."
    },
    {
        "title": "Virtual Assistant",
        "company": "WorkIndia Portal (India)",
        "category": "Finance & Operations",
        "employment": "Part-time",
        "chance": "Extremely High",
        "url": "https://www.workindia.in/",
        "fits": "Virtual assistance. Matches soft skills.",
        "tip": "Call the HR directly using the WorkIndia app contact feature."
    },
    {
        "title": "Data Entry Associate",
        "company": "Apna App (India)",
        "category": "Finance & Operations",
        "employment": "Part-time",
        "chance": "Extremely High",
        "url": "https://apna.co/",
        "fits": "Data entry. Matches typing and basic Excel.",
        "tip": "Apply to listings with high response rates and immediate start dates."
    },
    {
        "title": "Gig Delivery Auditor",
        "company": "Taskmo (India)",
        "category": "Finance & Operations",
        "employment": "Part-time",
        "chance": "Extremely High",
        "url": "https://taskmo.com/",
        "fits": "Verifying deliveries. Matches attention to detail.",
        "tip": "Download the Taskmo app, select the remote audit gig, and start working."
    },
    {
        "title": "Data Digitization Agent",
        "company": "Gigforce (India)",
        "category": "Finance & Operations",
        "employment": "Part-time",
        "chance": "Extremely High",
        "url": "https://www.gigforce.in/",
        "fits": "Digitizing handwritten documents. Matches typing skills.",
        "tip": "Register on Gigforce. Complete the data entry test to get activated."
    },
    {
        "title": "Freelancer (Data Entry)",
        "company": "Truelancer India",
        "category": "Finance & Operations",
        "employment": "Part-time",
        "chance": "Extremely High",
        "url": "https://www.truelancer.com/",
        "fits": "Data entry. Matches Google Docs/Excel skills.",
        "tip": "Bid on simple data entry projects. Offer a competitive rate to get selected."
    },
    {
        "title": "Freelancer (Content/Writing)",
        "company": "Fiverr India",
        "category": "Marketing & Growth",
        "employment": "Part-time",
        "chance": "Extremely High",
        "url": "https://www.fiverr.com/",
        "fits": "Writing articles. Matches creative writing soft skills.",
        "tip": "Create a gig for 'B.Com graduate writing personal finance or marketing blogs'."
    },
    {
        "title": "Freelancer (Data Cleaning)",
        "company": "Freelancer India",
        "category": "Finance & Operations",
        "employment": "Part-time",
        "chance": "Extremely High",
        "url": "https://www.freelancer.in/",
        "fits": "Cleaning lists in Excel. Matches Tata Data Vis and Excel.",
        "tip": "Highlight your Tata Data Visualisation certification on your profile."
    }
]

# Write to jobs.json
with open("jobs.json", "w") as f:
    json.dump(jobs_combined, f, indent=4)
print(f"Generated jobs.json successfully with {len(jobs_combined)} jobs!")
