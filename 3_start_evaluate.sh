export evaluate_dataset_file="../evaluate_dataset.jsonl"
export save_dir="result"

llm_engines=("TA/meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo" "TA/mistralai/Mistral-7B-Instruct-v0.2" "TA/meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo" "glm-4-flash" "TA/meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo" "glm-4-plus")
save_files=("llama_3.1_8b_inst.jsonl" "mistral_0.2_7B_inst.jsonl" "llama_3.1_70B_inst.jsonl" "glm_4_flash_inst.jsonl" "llama_3.1_405b_inst.jsonl" "glm_4_plus_inst.jsonl")



cd Evaluation
for i in {0..5}
do
  export llm_engine=${llm_engines[$i]}
  export save_file="../"$save_dir"/"${save_files[$i]}

  python evaluate_llm.py --dataset_file $evaluate_dataset_file --llm_engine $llm_engine --save_file $save_file --save_dir $save_dir
done
