# evaluation_metrics.py
import time
from sklearn.metrics import precision_score, recall_score
from rouge import Rouge
import numpy as np
import re

class Evaluator:
    def __init__(self, rag_pipeline):
        self.rag_pipeline = rag_pipeline
        self.retrieval_times = []
        self.pipeline_times = []
        self.sql_times = []  # Track SQL path times
        self.rag_times = []  # Track RAG path times
        self.retrieval_metrics = {
            'precision': [],
            'recall': [],
            'f1': []
        }
        self.generation_metrics = {
            'accuracy': [],
            'rouge1': [],
            'rouge2': [],
            'rougeL': []
        }
        self.path_metrics = {
            'path_selection_accuracy': [],
            'rag_path_accuracy': [],
            'sql_path_accuracy': []
        }
        # Thêm các chỉ số đánh giá cho SQL
        self.sql_metrics = {
            'total_queries': 0,
            'successful_queries': 0,
            'failed_queries': 0,
            'syntax_errors': 0,
            'execution_errors': 0,
            'no_results': 0,
            'not_found_answers': 0  # Thêm biến mới để theo dõi trường hợp không tìm thấy câu trả lời
        }
        self.rouge = Rouge()
        
    def evaluate_retrieval(self, query, expected_sources, generated_answer=None):
        # If we already have a generated answer, use it instead of running the pipeline again
        if generated_answer is None:
            start_time = time.time()
            # generated_answer = self.rag_pipeline(query)
            result = self.rag_pipeline(query)
            retrieval_time = time.time() - start_time
        else:
            # If we already have the answer, just use a placeholder for retrieval time
            retrieval_time = 0.1  # Placeholder value
            result = generated_answer
        
        # Extract sources from the generated answer
        retrieved_sources = []
        print("generated_answer: ", generated_answer)
        
        # Xử lý các trường hợp khác nhau của kết quả
        if isinstance(result, tuple):
            # Nếu kết quả là tuple (answer, path)
            answer_data, _ = result
            if isinstance(answer_data, dict):
                # Thử các key phổ biến để lấy sources
                for key in ['sources', 'source', 'retrieved_documents', 'documents']:
                    if key in answer_data:
                        if isinstance(answer_data[key], list):
                            if answer_data[key] and isinstance(answer_data[key][0], dict):
                                # Nếu là list of dict, lấy key 'source' hoặc 'path' từ mỗi dict
                                for doc in answer_data[key]:
                                    if 'source' in doc:
                                        retrieved_sources.append(doc['source'])
                                    elif 'path' in doc:
                                        retrieved_sources.append(doc['path'])
                            else:
                                # Nếu là list of strings
                                retrieved_sources.extend(answer_data[key])
                        elif isinstance(answer_data[key], str):
                            retrieved_sources.append(answer_data[key])
            else:
                # Nếu không phải dict, thử trích xuất từ văn bản
                text = str(answer_data)
                # Tìm sources trong văn bản
                source_patterns = [
                    r'\[(.*?)\]',  # [source1, source2]
                    r'source:\s*([^\n]+)',  # source: filename.txt
                    r'Nguồn:\s*([^\n]+)',  # Nguồn: filename.txt
                    r'from:\s*([^\n]+)'    # from: filename.txt
                ]
                for pattern in source_patterns:
                    sources = re.findall(pattern, text)
                    if sources:
                        retrieved_sources.extend(sources)
        elif isinstance(result, dict):
            # Thử các key phổ biến để lấy sources
            for key in ['sources', 'source', 'retrieved_documents', 'documents']:
                if key in result:
                    if isinstance(result[key], list):
                        if result[key] and isinstance(result[key][0], dict):
                            # Nếu là list of dict, lấy key 'source' hoặc 'path' từ mỗi dict
                            for doc in result[key]:
                                if 'source' in doc:
                                    retrieved_sources.append(doc['source'])
                                elif 'path' in doc:
                                    retrieved_sources.append(doc['path'])
                        else:
                            # Nếu là list of strings
                            retrieved_sources.extend(result[key])
                    elif isinstance(result[key], str):
                        retrieved_sources.append(result[key])
        else:
            # Nếu không phải tuple hoặc dict, thử trích xuất từ văn bản
            text = str(result)
            # Tìm sources trong văn bản
            source_patterns = [
                r'\[(.*?)\]',  # [source1, source2]
                r'source:\s*([^\n]+)',  # source: filename.txt
                r'Nguồn:\s*([^\n]+)',  # Nguồn: filename.txt
                r'from:\s*([^\n]+)'    # from: filename.txt
            ]
            for pattern in source_patterns:
                sources = re.findall(pattern, text)
                if sources:
                    retrieved_sources.extend(sources)
        
        # Chuẩn hóa tên file sources
        retrieved_sources = [source.strip() for source in retrieved_sources]
        expected_sources = [source.strip() for source in expected_sources]
        
        # Calculate precision and recall
        if not expected_sources and not retrieved_sources:
            # If both are empty, consider it a perfect match
            precision = 1.0
            recall = 1.0
            f1 = 1.0
        elif not expected_sources or not retrieved_sources:
            # If one is empty and the other isn't, it's a complete mismatch
            precision = 0.0
            recall = 0.0
            f1 = 0.0
        else:
            # Normal case - calculate metrics
            relevant_retrieved = len(set(retrieved_sources) & set(expected_sources))
            precision = relevant_retrieved / len(retrieved_sources) if retrieved_sources else 0.0
            recall = relevant_retrieved / len(expected_sources) if expected_sources else 0.0
            # Calculate F1 score, avoiding division by zero
            if precision + recall > 0:
                f1 = 2 * (precision * recall) / (precision + recall)
            else:
                f1 = 0.0
        
        return {
            "retrieval_time": retrieval_time,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "retrieved_sources": retrieved_sources,  # Thêm vào để debug
            "expected_sources": expected_sources     # Thêm vào để debug
        }
    
    def evaluate_generation(self, generated_answer, expected_answer):
        """
        Evaluate the quality of the generated answer compared to the expected answer
        
        Args:
            generated_answer: The answer generated by the pipeline
            expected_answer: The expected answer
            
        Returns:
            Dictionary with evaluation metrics
        """
        # Chuẩn hóa văn bản để so sánh
        generated_text = str(generated_answer).strip().lower()
        expected_text = str(expected_answer).strip().lower()
        
        # Kiểm tra trường hợp đặc biệt
        if expected_text == "không tìm thấy thông tin":
            return {
                "correct": "không tìm thấy thông tin" in generated_text,
                "rouge_scores": None
            }
        
        # Tính toán độ chính xác dựa trên việc so sánh văn bản
        # Sử dụng nhiều tiêu chí khác nhau để đánh giá
        exact_match = generated_text == expected_text
        contains_all_keywords = all(keyword in generated_text for keyword in expected_text.split())
        
        # Nếu câu trả lời chứa tất cả các từ khóa quan trọng, coi như đúng
        is_correct = exact_match or contains_all_keywords
        
        # Tính toán ROUGE scores
        try:
            scores = self.rouge.get_scores(generated_text, expected_text)[0]
            rouge_scores = {
                "rouge-1": scores['rouge-1']['f'],
                "rouge-2": scores['rouge-2']['f'],
                "rouge-l": scores['rouge-l']['f']
            }
        except Exception as e:
            print(f"Lỗi khi tính ROUGE scores: {e}")
            rouge_scores = {
                "rouge-1": 0.0,
                "rouge-2": 0.0,
                "rouge-l": 0.0
            }
        
        return {
            "correct": is_correct,
            "rouge_scores": rouge_scores,
            "exact_match": exact_match,
            "contains_all_keywords": contains_all_keywords
        }
    
    def evaluate_pipeline(self, query, expected_answer, expected_sources=None, expected_path=None):
        """
        Evaluate the RAG pipeline on a single query
        
        Args:
            query: The query to evaluate
            expected_answer: The expected answer
            expected_sources: List of expected source documents (optional)
            expected_path: Expected path to use ("sql" or "rag")
        """
        start_time = time.time()
        
        # Call the pipeline and get both result and path
        result = self.rag_pipeline(query)
        
        # Check if result is a tuple (answer, path) or just an answer
        if isinstance(result, tuple):
            generated_answer, actual_path = result
        else:
            generated_answer = result
            actual_path = "rag"  # Default to RAG for backward compatibility
        
        pipeline_time = time.time() - start_time
        self.pipeline_times.append(pipeline_time)
        
        # Track time by path
        if actual_path == "sql":
            self.sql_times.append(pipeline_time)
            # Cập nhật chỉ số SQL
            self.sql_metrics['total_queries'] += 1
            
            # Kiểm tra kết quả SQL
            if isinstance(generated_answer, dict):
                # Kiểm tra các trường hợp lỗi SQL
                if 'error' in generated_answer or 'exception' in generated_answer:
                    self.sql_metrics['failed_queries'] += 1
                    if 'syntax' in str(generated_answer).lower():
                        self.sql_metrics['syntax_errors'] += 1
                    else:
                        self.sql_metrics['execution_errors'] += 1
                elif 'no_results' in generated_answer or 'empty' in str(generated_answer).lower():
                    self.sql_metrics['no_results'] += 1
                    # Không tăng successful_queries khi không có kết quả
                else:
                    self.sql_metrics['successful_queries'] += 1
            else:
                # Nếu không phải dictionary, kiểm tra nội dung
                answer_text = str(generated_answer).lower()
                if 'error' in answer_text or 'exception' in answer_text:
                    self.sql_metrics['failed_queries'] += 1
                    if 'syntax' in answer_text:
                        self.sql_metrics['syntax_errors'] += 1
                    else:
                        self.sql_metrics['execution_errors'] += 1
                elif 'no results' in answer_text or 'empty' in answer_text:
                    self.sql_metrics['no_results'] += 1
                    # Không tăng successful_queries khi không có kết quả
                else:
                    self.sql_metrics['successful_queries'] += 1
        else:
            self.rag_times.append(pipeline_time)
        
        # Extract the actual answer text from generated_answer if it's a dictionary
        answer_text = ""
        if isinstance(generated_answer, dict):
            # Thử các key phổ biến để lấy văn bản câu trả lời
            for key in ['answer', 'text', 'response', 'content', 'result', 'output']:
                if key in generated_answer:
                    answer_text = generated_answer[key]
                    break
            
            # Nếu không tìm thấy key phù hợp, thử lấy tất cả các giá trị chuỗi
            if not answer_text:
                text_parts = []
                for key, value in generated_answer.items():
                    if isinstance(value, str) and key != 'sources' and key != 'source':
                        text_parts.append(f"{key}: {value}")
                
                if text_parts:
                    answer_text = " ".join(text_parts)
                else:
                    # Nếu không tìm thấy giá trị chuỗi nào, chuyển đổi dictionary thành chuỗi
                    answer_text = str(generated_answer)
        else:
            answer_text = str(generated_answer)
        
        # In thông tin debug
        print(f"Query: {query}")
        print(f"Expected answer: {expected_answer}")
        print(f"Generated answer (raw): {generated_answer}")
        print(f"Extracted answer text: {answer_text}")
        
        # Kiểm tra trường hợp không tìm thấy câu trả lời - chỉ áp dụng cho luồng RAG
        if actual_path == "rag" and ("không tìm thấy" in answer_text.lower() or "không tìm thấy" in str(expected_answer).lower()):
            self.sql_metrics['not_found_answers'] += 1
        
        # Kiểm tra trường hợp không tìm thấy dữ liệu trong luồng SQL
        if actual_path == "sql" and ("không tìm thấy dữ liệu" in answer_text.lower() or "không tìm thấy dữ liệu phù hợp" in answer_text.lower()):
            self.sql_metrics['not_found_answers'] += 1
            # Nếu đã tăng successful_queries trước đó, giảm lại
            if self.sql_metrics['successful_queries'] > 0:
                self.sql_metrics['successful_queries'] -= 1
        
        # Evaluate retrieval if sources are provided
        if expected_sources:
            retrieval_result = self.evaluate_retrieval(query, expected_sources, generated_answer)
            self.retrieval_metrics['precision'].append(retrieval_result['precision'])
            self.retrieval_metrics['recall'].append(retrieval_result['recall'])
            self.retrieval_metrics['f1'].append(retrieval_result['f1'])
            
            # In thông tin debug về sources
            print(f"Expected sources: {expected_sources}")
            print(f"Retrieved sources: {retrieval_result['retrieved_sources']}")
            print(f"Retrieval metrics: Precision={retrieval_result['precision']}, Recall={retrieval_result['recall']}, F1={retrieval_result['f1']}")
        
        # Evaluate generation
        generation_result = self.evaluate_generation(answer_text, expected_answer)
        self.generation_metrics['accuracy'].append(generation_result['correct'])
        
        # In thông tin debug về generation
        print(f"Generation metrics: Correct={generation_result['correct']}, Exact match={generation_result.get('exact_match', False)}, Contains all keywords={generation_result.get('contains_all_keywords', False)}")
        
        # Calculate ROUGE scores - chỉ áp dụng cho luồng RAG
        if actual_path == "rag" and generation_result['rouge_scores']:
            self.generation_metrics['rouge1'].append(generation_result['rouge_scores']['rouge-1'])
            self.generation_metrics['rouge2'].append(generation_result['rouge_scores']['rouge-2'])
            self.generation_metrics['rougeL'].append(generation_result['rouge_scores']['rouge-l'])
            
            # In thông tin debug về ROUGE scores
            print(f"ROUGE scores: ROUGE-1={generation_result['rouge_scores']['rouge-1']}, ROUGE-2={generation_result['rouge_scores']['rouge-2']}, ROUGE-L={generation_result['rouge_scores']['rouge-l']}")
        
        # Evaluate path selection if expected_path is provided
        if expected_path:
            path_correct = 1.0 if actual_path == expected_path else 0.0
            self.path_metrics['path_selection_accuracy'].append(path_correct)
            
            # Evaluate accuracy within each path
            if expected_path == "rag":
                self.path_metrics['rag_path_accuracy'].append(generation_result['correct'])
            elif expected_path == "sql":
                self.path_metrics['sql_path_accuracy'].append(generation_result['correct'])
            
            # In thông tin debug về path
            print(f"Path metrics: Expected={expected_path}, Actual={actual_path}, Correct={path_correct}")
        
        return {
            'query': query,
            'expected_answer': expected_answer,
            'generated_answer': answer_text,
            'expected_path': expected_path,
            'actual_path': actual_path,
            'path_correct': path_correct if expected_path else None,
            'generation_correct': generation_result['correct'],
            'pipeline_time': pipeline_time
        }
    
    def get_metrics(self):
        """Get all evaluation metrics"""
        metrics = {
            'retrieval': {
                'precision': np.mean(self.retrieval_metrics['precision']) if self.retrieval_metrics['precision'] else 0.0,
                'recall': np.mean(self.retrieval_metrics['recall']) if self.retrieval_metrics['recall'] else 0.0,
                'f1': np.mean(self.retrieval_metrics['f1']) if self.retrieval_metrics['f1'] else 0.0
            },
            'generation': {
                'accuracy': np.mean(self.generation_metrics['accuracy']) if self.generation_metrics['accuracy'] else 0.0,
                'rouge1': np.mean(self.generation_metrics['rouge1']) if self.generation_metrics['rouge1'] else 0.0,
                'rouge2': np.mean(self.generation_metrics['rouge2']) if self.generation_metrics['rouge2'] else 0.0,
                'rougeL': np.mean(self.generation_metrics['rougeL']) if self.generation_metrics['rougeL'] else 0.0
            },
            'path': {
                'path_selection_accuracy': np.mean(self.path_metrics['path_selection_accuracy']) if self.path_metrics['path_selection_accuracy'] else 0.0,
                'rag_path_accuracy': np.mean(self.path_metrics['rag_path_accuracy']) if self.path_metrics['rag_path_accuracy'] else 0.0,
                'sql_path_accuracy': np.mean(self.path_metrics['sql_path_accuracy']) if self.path_metrics['sql_path_accuracy'] else 0.0
            },
            'timing': {
                'avg_pipeline_time': np.mean(self.pipeline_times) if self.pipeline_times else 0.0,
                'avg_sql_time': np.mean(self.sql_times) if self.sql_times else 0.0,
                'avg_rag_time': np.mean(self.rag_times) if self.rag_times else 0.0
            },
            'sql': {
                'total_queries': self.sql_metrics['total_queries'],
                'successful_queries': self.sql_metrics['successful_queries'],
                'failed_queries': self.sql_metrics['failed_queries'],
                'syntax_errors': self.sql_metrics['syntax_errors'],
                'execution_errors': self.sql_metrics['execution_errors'],
                'no_results': self.sql_metrics['no_results'],
                'not_found_answers': self.sql_metrics['not_found_answers'],  # Thêm biến mới vào kết quả
                'success_rate': self.sql_metrics['successful_queries'] / self.sql_metrics['total_queries'] if self.sql_metrics['total_queries'] > 0 else 0.0,
                'failure_rate': self.sql_metrics['failed_queries'] / self.sql_metrics['total_queries'] if self.sql_metrics['total_queries'] > 0 else 0.0,
                'syntax_error_rate': self.sql_metrics['syntax_errors'] / self.sql_metrics['total_queries'] if self.sql_metrics['total_queries'] > 0 else 0.0,
                'execution_error_rate': self.sql_metrics['execution_errors'] / self.sql_metrics['total_queries'] if self.sql_metrics['total_queries'] > 0 else 0.0,
                'no_results_rate': self.sql_metrics['no_results'] / self.sql_metrics['total_queries'] if self.sql_metrics['total_queries'] > 0 else 0.0,
                'not_found_rate': self.sql_metrics['not_found_answers'] / self.sql_metrics['total_queries'] if self.sql_metrics['total_queries'] > 0 else 0.0  # Thêm tỷ lệ không tìm thấy
            }
        }
        
        return metrics
    
    def _calculate_rouge_scores(self, generated_answer, expected_answer):
        if expected_answer.lower() == "không tìm thấy thông tin":
            return {
                'rouge-1': 0.0,
                'rouge-2': 0.0,
                'rouge-l': 0.0
            }
        
        scores = self.rouge.get_scores(generated_answer, expected_answer)[0]
        return {
            'rouge-1': scores['rouge-1']['f'],
            'rouge-2': scores['rouge-2']['f'],
            'rouge-l': scores['rouge-l']['f']
        }