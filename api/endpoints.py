from flask import Blueprint, jsonify
from core.integration import compute_matches, get_candidates_for_employer, load_employers

# Create a Blueprint for the API
api = Blueprint('api', __name__)

@api.route('/match_jobs', methods=['GET'])
def match_jobs():
    """
    Match jobs with candidates and return ranked results.
    """
    try:
        results = compute_matches()
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route('/employers', methods=['GET'])
def get_employers():
    """
    Fetch the list of employers from employers.docx.
    """
    try:
        employers = load_employers('data/employers.docx')
        return jsonify(employers)
    except FileNotFoundError:
        return jsonify({"error": "Employers file not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route('/employers/<int:employer_id>/candidates', methods=['GET'])
def get_ranked_candidates(employer_id):
    """
    Fetch ranked candidates for a specific employer.
    """
    try:
        ranked_candidates = get_candidates_for_employer(employer_id)
        if not ranked_candidates:
            return jsonify({"error": "No candidates found for the given employer ID"}), 404
        return jsonify(ranked_candidates)
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
