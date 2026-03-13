from flask import Flask, render_template, request
import PyPDF2
import re

app = Flask(__name__)

# Skills required
required_skills = [
    "python","java","c++","data structures",
    "algorithms","sql","machine learning",
    "git","html","css"
]

# Project keywords
project_keywords = [
    "project","quiz","planner","analyzer","system","tracker"
]

def analyze_resume_text(resume_text):
    resume_text = resume_text.lower()
    matched = []
    missing = []

    for skill in required_skills:
        if re.search(skill,resume_text):
            matched.append(skill)
        else:
            missing.append(skill)

    score = len(matched)
    percentage = (score/len(required_skills))*100

    # Progress bar
    bars = int(percentage/10)
    progress = "█"*bars + "-"*(10-bars)

    result = "Resume Score: "+str(round(percentage,2))+"%\n"
    result += "Progress: "+progress+"\n\n"

    result += "Matched Skills:\n"
    for skill in matched:
        result += "- "+skill+"\n"

    result += "\nMissing Skills:\n"
    for skill in missing:
        result += "- "+skill+"\n"

    # Project detection
    result += "\nDetected Project Keywords:\n"
    found_project = False
    for word in project_keywords:
        if word in resume_text:
            result += "- "+word+"\n"
            found_project = True
    if not found_project:
        result += "No projects detected\n"

    # Suggestions
    result += "\nSuggestions:\n"
    if "data structures" in missing:
        result += "- Learn Data Structures for interviews\n"
    if "git" in missing:
        result += "- Learn Git and GitHub\n"
    if "sql" in missing:
        result += "- Add SQL / Database skills\n"
    if "machine learning" in missing:
        result += "- Try learning Machine Learning basics\n"

    if percentage >= 80:
        result += "\nExcellent Resume 👍"
    elif percentage >= 50:
        result += "\nGood Resume but can improve"
    else:
        result += "\nResume needs improvement"

    return result

@app.route("/", methods=["GET","POST"])
def index():
    result = None
    if request.method == "POST":
        resume_file = request.files.get("resume")
        if resume_file:
            try:
                reader = PyPDF2.PdfReader(resume_file)
                resume_text = ""
                for page in reader.pages:
                    resume_text += page.extract_text()
                result = analyze_resume_text(resume_text)
            except:
                result = "Error reading PDF file"
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)