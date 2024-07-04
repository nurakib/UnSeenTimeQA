export CUDA_VISIBLE_DEVICES=0,1,2,3

export TRANSFORMERS_CACHE=/PATH/TO/CACHE/.cache

python ./src/run_model.py \
    --dataset_dir ./data/easy/serial/split_1/serial_easy_q_type_1_split_1_final.json \
    --output_dir /PATH/TO/OUTPUT \
    --model_id "meta-llama/Meta-Llama-3-8B-Instruct" \
    --max_length_input 2048 \
    --top_p 0.9 \
    --temperature 1e-12 \
    --max_new_tokens 2048

