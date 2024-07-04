from transformers import AutoTokenizer, AutoModelForCausalLM,  pipeline
import torch
from tqdm import tqdm 
import json
import os

DEFAULT_CHAT_TEMPLATE = "{% for message in messages %}\n{% if message['role'] == 'user' %}\n{{ '<|user|>\n' + message['content'] + eos_token }}\n{% elif message['role'] == 'system' %}\n{{ '<|system|>\n' + message['content'] + eos_token }}\n{% elif message['role'] == 'assistant' %}\n{{ '<|assistant|>\n'  + message['content'] + eos_token }}\n{% endif %}\n{% if loop.last and add_generation_prompt %}\n{{ '<|assistant|>' }}\n{% endif %}\n{% endfor %}"


class InferenceModel:
    def __init__(self, model_id, dataset_dir):

        self.model_id = model_id
        f = open(dataset_dir)
        self.dataset = json.load(f)

        if "llama" or "gemma" or "mistral" in self.model_id:
            self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_id,
                    device_map="auto",
                    use_auth_token=True
                )
            

        elif "Phi" in self.model_id:
            self.device = torch.cuda.current_device()
            self.model = AutoModelForCausalLM.from_pretrained(
            self.model_id, 
            torch_dtype="auto", 
            trust_remote_code=True, 
            ).to(device)

        self.tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True, use_auth_token=True)
        if "mistral" in model_id:
            self.tokenizer.chat_template = DEFAULT_CHAT_TEMPLATE


        self.temperature = None
        self.top_p = None
        self.max_new_tokens = None
        self.max_length_input = None

    def _generate_prompt(self, data):

        prompt = ""
        prompt += f"Task description\n{data['domain_description']}"
        object_description = "\n".join(data['objects_description'])
        prompt += f"\n\nObject description\n{object_description}"
        initial_states_description = "\n".join(data['initial_states_description'])
        prompt += f"\n\nInitial states description\n{initial_states_description}"
        question = " ".join(data['events']) + " " + data["question"][0]
        prompt += f"\n\nQuestion\n{question}"
        prompt += "\n\nLet's think step-by-step to answer the question. Please use the below format:\nReasoning steps: [generate step-by-step reasoning]\nAnswer:[final answer]"

        return prompt

    def _generate_response_llama(self, prompt):
        messages = [
            {"role": "system","content": "You are a helpful assistant designed to provide accurate responses to questions about time. If you are unsure of your answer, refrain from responding."},
            {"role": "user", "content": prompt},
            ]
        input_ids = self.tokenizer.apply_chat_template(
                messages,
                add_generation_prompt=True,
                return_tensors="pt"
            ).to(self.model.device)

        terminators = [
                self.tokenizer.eos_token_id,
                self.tokenizer.convert_tokens_to_ids("<|eot_id|>")
            ]

        outputs = self.model.generate(
                input_ids,
                max_new_tokens=self.max_new_tokens,
                eos_token_id=terminators,
                do_sample=True,
                temperature=self.temperature,
                top_p=self.top_p,
            )
        response = outputs[0][input_ids.shape[-1]:]
        response = self.tokenizer.decode(response, skip_special_tokens=True)  

        return response

    def _generate_response_phi3(self, prompt):
        pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            device=self.device
            )

        generation_args = {
                "max_new_tokens": self.max_new_tokens,
                "return_full_text": False,
                "temperature": self.temperature,
                "do_sample": True,
                }
        messages = [
                {"role": "system","content": "You are a helpful assistant designed to provide accurate responses to questions about time. If you are unsure of your answer, refrain from responding."},
                {"role": "user", "content": prompt},
            ]

        response = pipe(messages, **generation_args)
        response = response[0]['generated_text']

        return response

    def _generate_response_gemma(self, prompt):
        input_ids = self.tokenizer(prompt, max_length = self.max_length_input, return_tensors="pt").to("cuda")
        outputs = self.model.generate(
                **input_ids,
                max_new_tokens=self.max_new_tokens,
                do_sample=True,
                temperature=self.max_length_input,
                top_p=self.top_p,
            )

        response = outputs[0][input_ids["input_ids"].shape[-1]:]
        response = self.tokenizer.decode(response, skip_special_tokens=True)
        return response


    def generate_response(self, max_length_input, temperature, max_new_tokens, top_p, output_dir):

        self.temperature = temperature
        self.top_p = top_p
        self.max_new_tokens = max_new_tokens
        self.max_length_input = max_length_input

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        generated_responses = []

        for datapoint in tqdm(self.dataset, desc = "Start Generating Response ..."):

            correct_answers = datapoint["answers"]
            prompt = self._generate_prompt(datapoint)

            if "mistral" or "llama" in self.model_id:
                response = self._generate_response_llama(prompt)
            elif "Phi" in self.model_id:
                response = self._generate_response_phi3(prompt)
            elif "gemma" in self.model_id:
                response = self,_generate_response_gemma(prompt)

            cot_response = response.split("Answer:")[0]
            final_answer = response.split("Answer:")[-1]


            if len(cot_response) == len(final_answer):
                final_answer = ""
            
            decision_flag = False
            if isinstance(correct_answers, list):
                for answer in correct_answers:
                    if answer in final_answer:
                        decision_flag = True
                        break
            else:
                if answers in final_answer:
                    decision_flag = True
            
            decision = 1 if decision_flag == True else 0

            datapoint["response"] = response
            datapoint["chain_of_reasoning"] = cot_response
            datapoint["final_answer"] = final_answer
            datapoint["correctness"] = decision


            generated_responses.append(datapoint)


            with open(f"{output_dir}/generated_responses.jsonl", 'w') as f:
                json.dump(generated_responses, f ,indent=4)

