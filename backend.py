import os
import json
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from google.generativeai import GoogleGenerativeAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("🔴 ERROR: GEMINI_API_KEY is not set in the .env file.")

gemini = GoogleGenerativeAI(GEMINI_API_KEY)

# Initialize Flask App
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

@app.route("/analyze", methods=["POST"])
def analyze_job():
    data = request.json
    job_description = data.get("jobDescription")
    if not job_description:
        return jsonify({"error": "Job description is required."}), 400
    
    prompt = f"""
    Analyze the following job description and extract structured insights in JSON format. Focus on key details like job title, company, salary transparency, and potential red flags related to work-life balance, unrealistic expectations, or toxic culture.  

    Specifically, watch for phrases that suggest:  
    - *Poor work-life balance* (e.g., "24/7 availability," "late nights," "high-pressure environment").  
    - *Unpaid or exploitative work* (e.g., "unpaid internship," "work for exposure").  
    - *Unrealistic expectations* (e.g., "wear multiple hats," "must thrive under extreme pressure").  
    - *Toxic culture risks* (e.g., "fast-paced environment" with no mention of support, "like a family" in a way that suggests blurred boundaries).  
    
    Job Description: {job_description}  
    
    Return ONLY JSON output. Do not add extra text. Follow this format strictly:  
    
    {{
      "job_title": "Extracted Job Title",
      "company": "Company Name",
      "salary": "Extracted salary if mentioned (e.g., 'Competitive' or 'Not mentioned' if absent)",
      "red_flags": ["Identified issues such as work-life balance concerns, unpaid expectations, or toxic language"],
      "red_flag_score": "Rate from 1-10 based on severity (1 = ideal, 10 = major concerns)",
      "ratings": {{
        "salary_transparency": "Rate 1-10 (lower if vague or absent)",
        "work_life_balance": "Rate 1-10 (lower if long hours or pressure mentioned)",
        "career_growth": "Rate 1-10 (lower if no learning opportunities exist)",
        "toxic_culture_risk": "Rate 1-10 (higher if multiple red flags are present)"
      }},
      "insights": ["Any additional comments on the job, such as vague language or hidden expectations"],
      "interview_questions": {{
        "candidate_should_ask": [
          "Tailor at least 3-5 smart questions based on the job details.",
          "If salary is missing, suggest asking about compensation range.",
          "If remote work is mentioned, include a question about work culture and team interaction.",
          "If career growth is unclear, suggest asking about promotions or learning opportunities."
        ]
      }}
    }}
    """
    try:
        model = gemini.getGenerativeModel(model="gemini-2.5-pro-exp-03-25")
        response = model.generateContent({"contents": [{"parts": [{"text": prompt}]}]})
        raw_text = response.response.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()
        
        if not raw_text:
            return jsonify({"error": "No valid response from Gemini API."}), 500

        cleaned_json = raw_text.replace("json", "").replace("", "").strip()
        results = json.loads(cleaned_json)
        
        # Ensure red_flags is an array
        if not isinstance(results.get("red_flags"), list):
            results["red_flags"] = []

        # Calculate red_flag_score
        results["red_flag_score"] = min(10, len(results["red_flags"]) * 3) if results["red_flags"] else 0
        
        # Compute Job Worth Score (0-100)
        job_score = 50  # Base score
        if "ratings" in results:
            job_score += results["ratings"].get("salary_transparency", 0) * 2
            job_score += results["ratings"].get("work_life_balance", 0) * 2
            job_score += results["ratings"].get("career_growth", 0) * 2
            job_score -= results["ratings"].get("toxic_culture_risk", 0) * 2
        
        results["job_score"] = max(0, min(100, job_score))
        
        # AI Verdict
        if job_score >= 80:
            results["verdict"] = "🏆 Strong Offer – High Pay & Low Risk!"
        elif job_score >= 60:
            results["verdict"] = "⚠ Decent Offer – But You Can Negotiate."
        else:
            results["verdict"] = "❌ Risky Job – Many Red Flags Detected!"
        
        return jsonify(results)
    except Exception as e:
        logging.error("Gemini API Error: %s", e)
        return jsonify({"error": "Failed to analyze job description.", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)