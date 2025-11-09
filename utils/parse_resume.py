"""
Resume Parsing Module
Uses spaCy and regex to extract structured information from resume text
"""

import re
import spacy


# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("spaCy model not found. Please run: python -m spacy download en_core_web_sm")
    nlp = None


# Common skills database
SKILLS_DATABASE = [
    # Programming Languages
    'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'C', 'Ruby', 'PHP', 
    'Swift', 'Kotlin', 'Go', 'Rust', 'Scala', 'R', 'MATLAB', 'Perl',
    
    # Web Technologies
    'HTML', 'CSS', 'React', 'Angular', 'Vue.js', 'Node.js', 'Django', 'Flask',
    'FastAPI', 'Spring', 'Express.js', 'Next.js', 'Bootstrap', 'Tailwind CSS',
    
    # Databases
    'SQL', 'MySQL', 'PostgreSQL', 'MongoDB', 'Oracle', 'Redis', 'SQLite',
    'Cassandra', 'DynamoDB', 'Firebase',
    
    # DevOps & Tools
    'Git', 'Docker', 'Kubernetes', 'Jenkins', 'AWS', 'Azure', 'GCP',
    'Linux', 'CI/CD', 'Terraform', 'Ansible',
    
    # Data Science & ML
    'Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch', 'Keras',
    'Pandas', 'NumPy', 'Scikit-learn', 'NLP', 'Computer Vision',
    
    # Other Skills
    'REST API', 'GraphQL', 'Microservices', 'Agile', 'Scrum', 'JIRA',
    'Excel', 'Power BI', 'Tableau', 'Figma', 'Photoshop'
]


def extract_name(text, doc=None):
    """
    Extract name from resume text using spaCy NER
    
    Args:
        text: Resume text
        doc: spaCy processed document (optional)
        
    Returns:
        Name as string
    """
    if nlp is None:
        return None
    
    if doc is None:
        doc = nlp(text[:1000])  # Process first 1000 chars for efficiency
    
    # Look for PERSON entities in the first few lines
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            return ent.text
    
    return None


def extract_email(text):
    """
    Extract email using regex
    
    Args:
        text: Resume text
        
    Returns:
        Email as string
    """
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    match = re.search(email_pattern, text)
    return match.group(0) if match else None


def extract_phone(text):
    """
    Extract phone number using regex
    
    Args:
        text: Resume text
        
    Returns:
        Phone number as string
    """
    # Pattern for various phone formats
    phone_patterns = [
        r'\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}',
        r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
        r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}'
    ]
    
    for pattern in phone_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0)
    
    return None


def extract_skills(text):
    """
    Extract skills by matching against skills database
    
    Args:
        text: Resume text
        
    Returns:
        List of skills found
    """
    found_skills = []
    text_lower = text.lower()
    
    for skill in SKILLS_DATABASE:
        # Case-insensitive search with word boundaries
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text_lower):
            if skill not in found_skills:
                found_skills.append(skill)
    
    return sorted(found_skills)


def extract_education(text):
    """
    Extract education information
    
    Args:
        text: Resume text
        
    Returns:
        List of education entries
    """
    education_keywords = ['education', 'academic', 'university', 'college', 'school']
    degree_keywords = ['bachelor', 'master', 'phd', 'b.tech', 'm.tech', 'b.sc', 'm.sc', 
                      'mba', 'bba', 'degree', 'diploma']
    
    lines = text.split('\n')
    education_section = []
    in_education_section = False
    
    for i, line in enumerate(lines):
        line_lower = line.lower().strip()
        
        # Detect education section start
        if any(keyword in line_lower for keyword in education_keywords):
            in_education_section = True
            continue
        
        # Stop at next major section
        if in_education_section and line_lower in ['experience', 'work experience', 
                                                     'skills', 'projects', 'certifications']:
            break
        
        # Collect education entries
        if in_education_section and line.strip():
            if any(degree in line_lower for degree in degree_keywords):
                education_section.append(line.strip())
            elif len(line.strip()) > 10 and i < len(lines) - 1:
                # Include university names and years
                if any(char.isdigit() for char in line) or any(keyword in line_lower for keyword in ['university', 'college', 'institute']):
                    education_section.append(line.strip())
    
    return education_section[:10]  # Limit to 10 entries


def extract_experience(text):
    """
    Extract work experience information
    
    Args:
        text: Resume text
        
    Returns:
        List of experience entries
    """
    experience_keywords = ['experience', 'work history', 'employment', 'professional experience']
    
    lines = text.split('\n')
    experience_section = []
    in_experience_section = False
    
    for line in lines:
        line_lower = line.lower().strip()
        
        # Detect experience section start
        if any(keyword in line_lower for keyword in experience_keywords):
            in_experience_section = True
            continue
        
        # Stop at next major section
        if in_experience_section and line_lower in ['education', 'skills', 'projects', 
                                                      'certifications', 'awards']:
            break
        
        # Collect experience entries
        if in_experience_section and line.strip() and len(line.strip()) > 5:
            experience_section.append(line.strip())
    
    return experience_section[:15]  # Limit to 15 entries


def parse_resume(text):
    """
    Main function to parse resume and extract all information
    
    Args:
        text: Resume text
        
    Returns:
        Dictionary with extracted information
    """
    # Process with spaCy if available
    doc = nlp(text[:2000]) if nlp else None
    
    parsed_data = {
        'name': extract_name(text, doc),
        'email': extract_email(text),
        'phone': extract_phone(text),
        'skills': extract_skills(text),
        'education': extract_education(text),
        'experience': extract_experience(text)
    }
    
    return parsed_data
