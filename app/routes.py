import os
import io
import contextlib
from flask import Blueprint, render_template, request, jsonify, current_app
from werkzeug.utils import secure_filename

from rag_components import extractor, vector_store
from models import coder_model, report_generator

main = Blueprint('main', __name__)

def execute_generated_code(code: str) -> str:
    string_io = io.StringIO()
    try:
        with contextlib.redirect_stdout(string_io):
            exec(code, {})
        return string_io.getvalue()
    except Exception as e:
        return f"Error executing generated code: {e}"

# --- Main Page Route ---
@main.route('/')
def index():
    return render_template('index.html')

# --- Report Generation API Route ---
@main.route('/generate', methods=['POST'])
def generate_report_route():
    # 1. --- Input Validation ---
    if 'manual_file' not in request.files:
        return jsonify({'error': 'No lab manual file provided.'}), 400
    
    manual_file = request.files['manual_file']
    observations_json = request.form.get('observations')

    if manual_file.filename == '':
        return jsonify({'error': 'No file selected.'}), 400

    if not observations_json:
        return jsonify({'error': 'No observations provided.'}), 400

    # Securely save the uploaded file
    filename = secure_filename(manual_file.filename)
    upload_path = os.path.join(current_app.root_path, '..', 'uploads', filename)
    manual_file.save(upload_path)

    try:
        # Ensure upload directory exists
        upload_dir = os.path.join(current_app.root_path, '..', 'uploads')
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
            
        # 2. --- RAG: Extract and Retrieve Context ---
        print("Step 1: Extracting text from manual...")
        print(f"File path: {upload_path}")
        print(f"File exists: {os.path.exists(upload_path)}")
        print(f"File size: {os.path.getsize(upload_path) if os.path.exists(upload_path) else 'N/A'}")
        print(f"File extension: {os.path.splitext(upload_path)[1]}")
        
        try:
            document_text = extractor.extract_text_from_file(upload_path)
            print("Text extraction successful")
        except Exception as e:
            print(f"Error during text extraction: {str(e)}")
            return jsonify({'error': f'Failed to extract text from file: {str(e)}'}), 500
        
        print("Step 2: Building vector store and retrieving context...")
        query = "Aim, Theory, Apparatus, and Procedure of the experiment"
        rag_context = vector_store.get_relevant_context(document_text, query)

        # 3. --- Coder Model: Generate Calculation Code ---
        print("Step 3: Generating Python code for calculations...")
        generated_code = coder_model.generate_code(
            context=rag_context, 
            observations=observations_json
        )

        # 4. --- Execute Code ---
        print("Step 4: Executing generated code to get results...")
        calculation_results = execute_generated_code(generated_code)

        # 5. --- Report Generator: Write Final Report ---
        print("Step 5: Generating final report with Groq Llama...")
        final_report = report_generator.write_report(
            rag_context=rag_context,
            observations=observations_json,
            results=calculation_results
        )
        
        # 6. --- Return Final Report ---
        print("Workflow complete. Returning report.")
        return jsonify({'report': final_report})

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': f'An internal error occurred: {str(e)}'}), 500

    finally:
        # 7. --- Cleanup ---
        if os.path.exists(upload_path):
            os.remove(upload_path)
            print(f"Cleaned up uploaded file: {upload_path}")