# export result_dir="../result_hard_sfs"
# export tofile="../overall_performance_hard_sfs.json"

export result_dir="../result_hard"
export tofile="../overall_performance_hard.json"

# export result_dir="../result"
# export tofile="../overall_performance.json"

cd Evaluation
python get_evaluation_result.py --result_dir $result_dir --tofile $tofile