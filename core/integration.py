import os
from docx import Document
from sklearn.feature_extraction.text import TfidfVectorizer

def read_docx(file_path):
    """
    Read content from a .docx file and return a list of non-empty paragraphs.
    """
    try:
        document = Document(file_path)
        return [para.text.strip() for para in document.paragraphs if para.text.strip()]
    except Exception as e:
        raise ValueError(f"Error reading {file_path}: {e}")

def load_employers(file_path):
    """
    Load employers' data from a .docx file.
    """
    employers = []
    content = read_docx(file_path)

    # Assuming each employer's data is separated by a blank line
    for block in '\n'.join(content).split('\n\n'):
        lines = block.splitlines()
        if len(lines) >= 4:
            employers.append({
                'id': int(lines[0]),  # Employer ID
                'name': lines[1],  # Employer Name
                'job_description': lines[2],  # Job Description
                'location': lines[3],  # Location
                'min_salary': float(lines[4]) if len(lines) > 4 else 0,
                'max_salary': float(lines[5]) if len(lines) > 5 else 0,
                'education_level': int(lines[6]) if len(lines) > 6 else 0,
                'experience_required': int(lines[7]) if len(lines) > 7 else 0,
            })
    return employers

def load_candidates(file_path):
    """
    Load candidates' data from a .docx file.
    """
    candidates = []
    content = read_docx(file_path)

    # Assuming each candidate's data is separated by a blank line
    for block in '\n'.join(content).split('\n\n'):
        lines = block.splitlines()
        if len(lines) >= 5:
            candidates.append({
                'name': lines[0],  # Candidate Name
                'cv_text': lines[1],  # CV Text
                'current_location': lines[2],  # Current Location
                'willing_to_relocate': lines[3].lower() == 'true',  # Willingness to relocate
                'expected_salary': float(lines[4]),  # Expected Salary
                'education_level': int(lines[5]) if len(lines) > 5 else 0,
                'years_experience': int(lines[6]) if len(lines) > 6 else 0,
            })
    return candidates

def rank_candidates(employer, candidates):
    """
    Rank candidates for a specific employer based on job description similarity.
    """
    job_desc = employer['job_description']
    candidate_texts = [candidate['cv_text'] for candidate in candidates]

    # Compute TF-IDF similarity
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform([job_desc] + candidate_texts)
    similarity_scores = (tfidf_matrix[0] * tfidf_matrix[1:].T).toarray()[0]

    # Rank candidates based on similarity scores
    ranked_candidates = sorted(
        candidates,
        key=lambda x: similarity_scores[candidates.index(x)],
        reverse=True
    )
    return [
        {
            'name': candidate['name'],
            'score': similarity_scores[candidates.index(candidate)],
        }
        for candidate in ranked_candidates
    ]

def compute_matches():
    """
    Matches candidates to employers based on job descriptions and accessory fields.
    """
    employers = load_employers('data/employers.docx')
    candidates = load_candidates('data/candidates.docx')

    results = {}

    for employer in employers:
        employer_name = employer['name']
        ranked_candidates = rank_candidates(employer, candidates)
        results[employer_name] = ranked_candidates

    return results

def get_candidates_for_employer(employer_id):
    """
    Get ranked candidates for a specific employer by their ID.
    """
    employers = load_employers('data/employers.docx')
    candidates = load_candidates('data/candidates.docx')

    # Find the employer by ID
    employer = next((e for e in employers if e['id'] == employer_id), None)
    if not employer:
        return []

    # Rank candidates for the given employer
    return rank_candidates(employer, candidates)
