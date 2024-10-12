
export benchmark_dir="../Benchmark_Hard_SimpleFewShot"
export to_file="../evaluate_dataset_hard_simplefewshot.jsonl"

cd Evaluation
python generate_dataset.py --benchmark_dir $benchmark_dir --save_dataset_file $to_file