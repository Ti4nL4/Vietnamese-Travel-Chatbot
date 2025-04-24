# main_evaluation.py
import sys
import os
import json
import logging
from datetime import datetime

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from my_notebook import rag_pipeline
from evaluation_dataset import evaluation_questions
from evaluation_metrics import Evaluator

# Thiết lập logging
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Tạo tên file log với timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = os.path.join(log_dir, f"evaluation_results_{timestamp}.log")

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()  # Vẫn in ra console
    ]
)

def main():
    # Initialize evaluator
    evaluator = Evaluator(rag_pipeline)
    
    # Evaluate each question
    results = []
    for question in evaluation_questions:
        logging.info(f"\nĐánh giá câu hỏi: {question['question']}")
        result = evaluator.evaluate_pipeline(
            query=question["question"],
            expected_answer=question["expected_answer"],
            expected_sources=question.get("expected_sources", []),
            expected_path=question.get("expected_path", None)
        )
        results.append(result)
        logging.info(f"Kết quả: {json.dumps(result, ensure_ascii=False, indent=2)}")
    
    # Get overall metrics
    metrics = evaluator.get_metrics()
    
    # Print overall evaluation metrics
    logging.info("\n=== Kết quả đánh giá tổng thể ===")
    logging.info(f"Tổng số câu hỏi: {len(results)}")
    logging.info(f"Thời gian trung bình: {metrics['timing']['avg_pipeline_time']:.2f}s")
    logging.info(f"Thời gian trung bình RAG: {metrics['timing']['avg_rag_time']:.2f}s")
    logging.info(f"Thời gian trung bình SQL: {metrics['timing']['avg_sql_time']:.2f}s")
    
    logging.info("\n=== Hiệu suất truy xuất ===")
    logging.info(f"Precision: {metrics['retrieval']['precision']:.2%}")
    logging.info(f"Recall: {metrics['retrieval']['recall']:.2%}")
    logging.info(f"F1 Score: {metrics['retrieval']['f1']:.2%}")
    
    logging.info("\n=== Hiệu suất sinh câu trả lời ===")
    # logging.info(f"Accuracy: {metrics['generation']['accuracy']:.2%}")
    logging.info(f"ROUGE-1: {metrics['generation']['rouge1']:.2%}")
    logging.info(f"ROUGE-2: {metrics['generation']['rouge2']:.2%}")
    logging.info(f"ROUGE-L: {metrics['generation']['rougeL']:.2%}")
    
    logging.info("\n=== Hiệu suất chọn đường dẫn ===")
    logging.info(f"Path Selection Accuracy: {metrics['path']['path_selection_accuracy']:.2%}")
    
    logging.info("\n=== Hiệu suất SQL ===")
    logging.info(f"Total Queries: {metrics['sql']['total_queries']}")
    logging.info(f"Successful Queries: {metrics['sql']['successful_queries']} ({metrics['sql']['success_rate']:.2%})")
    # logging.info(f"Failed Queries: {metrics['sql']['failed_queries']} ({metrics['sql']['failure_rate']:.2%})")
    # logging.info(f"Syntax Errors: {metrics['sql']['syntax_errors']} ({metrics['sql']['syntax_error_rate']:.2%})")
    # logging.info(f"Execution Errors: {metrics['sql']['execution_errors']} ({metrics['sql']['execution_error_rate']:.2%})")
    # logging.info(f"No Results: {metrics['sql']['no_results']} ({metrics['sql']['no_results_rate']:.2%})")
    logging.info(f"Not Found Answers: {metrics['sql']['not_found_answers']} ({metrics['sql']['not_found_rate']:.2%})")
    
    # Print detailed results for each question
    logging.info("\n=== Chi tiết kết quả từng câu hỏi ===")
    for i, result in enumerate(results, 1):
        logging.info(f"\nCâu hỏi {i}:")
        logging.info(f"Query: {result['query']}")
        logging.info(f"Expected Path: {result['expected_path']}")
        logging.info(f"Actual Path: {result['actual_path']}")
        logging.info(f"Path Correct: {result['path_correct']}")
        logging.info(f"Pipeline Time: {result['pipeline_time']:.2f}s")
        if result.get('expected_sources'):
            logging.info(f"Expected Sources: {result['expected_sources']}")
    
    logging.info("\n=== Kết thúc đánh giá ===")

if __name__ == "__main__":
    main()