import os
import sys
import json
import io
import contextlib
from datetime import datetime
from rouge_score import rouge_scorer

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from app import create_app
from rag_components import extractor, vector_store
from models import coder_model, report_generator

def execute_generated_code(code: str) -> str:
    string_io = io.StringIO()
    try:
        with contextlib.redirect_stdout(string_io):
            exec(code, {})
        return string_io.getvalue()
    except Exception as e:
        return f"Error executing generated code: {e}"

def run_full_pipeline(manual_path: str, observations: str) -> str:
    print(f"\nProcessing file: {os.path.basename(manual_path)}...")
    
    # Step 1: RAG - Extract and Retrieve
    document_text = extractor.extract_text_from_file(manual_path)
    query = "Aim, Theory, Apparatus, and Procedure of the experiment"
    rag_context = vector_store.get_relevant_context(document_text, query)
    
    # Step 2: Coder Model
    generated_code = coder_model.generate_code(
        context=rag_context, 
        observations=observations
    )
    
    # Step 3: Execute Code
    calculation_results = execute_generated_code(generated_code)
    
    # Step 4: Report Generator
    final_report = report_generator.write_report(
        rag_context=rag_context,
        observations=observations,
        results=calculation_results
    )
    
    return final_report

def main():
    app = create_app()
    with app.app_context():
        dataset_path = os.path.join(os.path.dirname(__file__), 'eval_dataset.jsonl')

        if not os.path.exists(dataset_path):
            print(f"ERROR: Evaluation dataset not found at {dataset_path}")
            return
        
        # --- NEW: Create a directory for saving results ---
        results_dir = os.path.join(os.path.dirname(__file__), 'evaluation_results')
        os.makedirs(results_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_filename = os.path.join(results_dir, f"evaluation_{timestamp}.txt")
        # --- END NEW ---

        with open(dataset_path, 'r') as f:
            eval_data = [json.loads(line) for line in f]

        scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
        total_scores = {'rouge1': [], 'rougeL': []}

        print(f"Found {len(eval_data)} examples in the evaluation dataset.")
        
        with open(results_filename, 'w', encoding='utf-8') as results_file:
            for i, item in enumerate(eval_data):
                manual_path = item['manual_path']
                observations = json.dumps(item['observations'], indent=2)
                golden_report = item['golden_report']
                
                generated_report = run_full_pipeline(manual_path, observations)
                
                scores = scorer.score(golden_report, generated_report)
                
                total_scores['rouge1'].append(scores['rouge1'])
                total_scores['rougeL'].append(scores['rougeL'])
                
                # --- NEW: Write detailed results to the file ---
                results_file.write(f"========== EXAMPLE {i+1}: {os.path.basename(manual_path)} ==========\n\n")
                results_file.write(f"ROUGE-1 F1-Score: {scores['rouge1'].fmeasure:.4f}\n")
                results_file.write(f"ROUGE-L F1-Score: {scores['rougeL'].fmeasure:.4f}\n\n")
                results_file.write("--- GENERATED REPORT ---\n")
                results_file.write(generated_report + "\n\n")
                results_file.write("--- GOLDEN REPORT ---\n")
                results_file.write(golden_report + "\n\n")
                results_file.write("=" * 60 + "\n\n")
                # --- END NEW ---
                
                print(f"--- Finished Example {i+1}/{len(eval_data)} ---")
                print(f"ROUGE-1 F1: {scores['rouge1'].fmeasure:.4f}")
                print(f"ROUGE-L F1: {scores['rougeL'].fmeasure:.4f}")
                print("------------------------------------")

            avg_rouge1_f1 = sum(s.fmeasure for s in total_scores['rouge1']) / len(total_scores['rouge1'])
            avg_rougeL_f1 = sum(s.fmeasure for s in total_scores['rougeL']) / len(total_scores['rougeL'])

            summary = (
                f"\n\n========== EVALUATION SUMMARY ==========\n"
                f"Total examples evaluated: {len(eval_data)}\n"
                f"Average ROUGE-1 F1-Score: {avg_rouge1_f1:.4f}\n"
                f"Average ROUGE-L F1-Score: {avg_rougeL_f1:.4f}\n"
                f"========================================\n"
                f"Detailed results saved to: {results_filename}\n"
            )
            
            # --- NEW: Write summary to both file and terminal ---
            print(summary)
            results_file.write(summary)
            # --- END NEW ---

if __name__ == '__main__':
    main()