# 🎁 Bonus Feature: Job Description Matcher

## Overview
This bonus feature allows you to compare a candidate's resume against a job description to calculate skill match percentage.

## Implementation Guide

### 1. Backend Addition

Add to `api/api.py`:

```python
@app.post("/match-job")
async def match_job_description(
    resume_file: UploadFile = File(...),
    job_description: str = Form(...)
):
    """
    Match resume against job description
    """
    # Extract and parse resume
    temp_file_path = UPLOAD_DIR / resume_file.filename
    
    with open(temp_file_path, "wb") as buffer:
        buffer.write(await resume_file.read())
    
    text = extract_text(str(temp_file_path))
    resume_data = parse_resume(text)
    
    # Extract skills from job description
    job_skills = extract_skills(job_description)
    candidate_skills = set(resume_data['skills'])
    required_skills = set(job_skills)
    
    # Calculate match
    matched_skills = candidate_skills & required_skills
    missing_skills = required_skills - candidate_skills
    
    match_percentage = (len(matched_skills) / len(required_skills) * 100) if required_skills else 0
    
    # Clean up
    os.remove(temp_file_path)
    
    return {
        "match_percentage": round(match_percentage, 2),
        "matched_skills": list(matched_skills),
        "missing_skills": list(missing_skills),
        "total_candidate_skills": len(candidate_skills),
        "total_required_skills": len(required_skills)
    }
```

### 2. Frontend Addition

Add to `web/index.html` (after upload section):

```html
<!-- Job Matcher Section -->
<section class="matcher-section">
    <div class="matcher-card">
        <h2>🎯 Job Description Matcher</h2>
        <p>Compare resume against job requirements</p>
        
        <textarea 
            id="jobDescription" 
            placeholder="Paste job description here..."
            rows="8"
        ></textarea>
        
        <button class="btn-match" id="matchBtn" disabled>
            Calculate Match
        </button>
        
        <div id="matchResults" style="display: none;">
            <div class="match-score">
                <h3>Match Score</h3>
                <div class="score-circle" id="scoreCircle">
                    <span id="scoreValue">0%</span>
                </div>
            </div>
            
            <div class="skill-comparison">
                <div class="matched">
                    <h4>✅ Matched Skills</h4>
                    <div id="matchedSkills"></div>
                </div>
                
                <div class="missing">
                    <h4>❌ Missing Skills</h4>
                    <div id="missingSkills"></div>
                </div>
            </div>
        </div>
    </div>
</section>
```

### 3. JavaScript Addition

Add to `web/script.js`:

```javascript
const jobDescription = document.getElementById('jobDescription');
const matchBtn = document.getElementById('matchBtn');

// Enable match button when both file and job description exist
jobDescription.addEventListener('input', () => {
    matchBtn.disabled = !(uploadedFile && jobDescription.value.trim());
});

matchBtn.addEventListener('click', matchWithJob);

async function matchWithJob() {
    const formData = new FormData();
    formData.append('resume_file', uploadedFile);
    formData.append('job_description', jobDescription.value);
    
    try {
        const response = await fetch(`${API_URL}/match-job`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        displayMatchResults(data);
    } catch (error) {
        showError('Error matching resume: ' + error.message);
    }
}

function displayMatchResults(data) {
    document.getElementById('matchResults').style.display = 'block';
    document.getElementById('scoreValue').textContent = 
        data.match_percentage + '%';
    
    // Update matched skills
    const matchedContainer = document.getElementById('matchedSkills');
    matchedContainer.innerHTML = data.matched_skills
        .map(skill => `<span class="skill-tag">${skill}</span>`)
        .join('');
    
    // Update missing skills
    const missingContainer = document.getElementById('missingSkills');
    missingContainer.innerHTML = data.missing_skills
        .map(skill => `<span class="skill-tag missing">${skill}</span>`)
        .join('');
}
```

### 4. CSS Addition

Add to `web/style.css`:

```css
.matcher-section {
    margin: 40px 0;
}

.matcher-card {
    background: white;
    padding: 30px;
    border-radius: 16px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

#jobDescription {
    width: 100%;
    padding: 15px;
    border: 2px solid #ddd;
    border-radius: 8px;
    font-family: inherit;
    margin: 20px 0;
    resize: vertical;
}

.score-circle {
    width: 150px;
    height: 150px;
    border-radius: 50%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 20px auto;
}

.score-circle span {
    color: white;
    font-size: 2.5rem;
    font-weight: bold;
}

.skill-comparison {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-top: 30px;
}

.skill-tag.missing {
    background: #f44336;
}
```

## Usage

1. Upload resume
2. Paste job description in textarea
3. Click "Calculate Match"
4. View match percentage and skill comparison

## Benefits

- **For Recruiters**: Quick candidate screening
- **For Job Seekers**: Identify skill gaps
- **For HR**: Automate initial screening process

## Future Enhancements

- Experience level matching
- Education requirement checking
- Location preference matching
- Salary range compatibility
