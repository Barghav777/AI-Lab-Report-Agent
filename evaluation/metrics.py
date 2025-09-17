from rouge_score import rouge_scorer
from typing import Dict

def calculate_rouge_scores(golden_report: str, generated_report: str) -> Dict[str, float]:
    # Initialize the scorer with the desired ROUGE types
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    # Compute the scores
    scores = scorer.score(target=golden_report, prediction=generated_report)
    
    processed_scores = {
        'rouge1_f1': scores['rouge1'].fmeasure,
        'rouge2_f1': scores['rouge2'].fmeasure,
        'rougeL_f1': scores['rougeL'].fmeasure
    }
    
    return processed_scores
