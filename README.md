
# UnSeenTimeQA: Time-Sensitive Question-Answering Beyond LLMs’ Memorization

Check out our paper - [UnSeenTimeQA: Time-Sensitive Question-Answering Beyond LLMs' Memorization](https://arxiv.org/abs/2407.03525)

We introduce a novel time-sensitive question-answering (TSQA) benchmark that diverges from traditional TSQA benchmarks by avoiding factual and web-searchable queries. We present a series of time-sensitive event scenarios decoupled from real-world factual information. It requires large language models (LLMs) to engage in genuine temporal reasoning, disassociating from the knowledge acquired during the pre-training phase. Our evaluation of six open-source LLMs (ranging from 2B to 70B in size) and three closed-source LLMs reveal that the questions from the UnSeenTimeQA present substantial challenges. This indicates the models' difficulties in handling complex temporal reasoning scenarios. Additionally, we present several analyses shedding light on the models' performance in answering time-sensitive questions.
<p align="center">
<img src="unseentimeqa.png" data-canonical-src="question_types.png"/>
</p>

Different types of events (six) from the UnSeenTimeQA benchmark. The benchmark is structured into
four difficulty levels: easy, medium, hard (serial), and hard (parallel). In the easy level, the start (S) and end (E)
times of each event are given. The medium level includes the start time (S) and duration (D) of each event. The hard
(serial) level presents only the duration (D) of events, assuming sequential occurrence. The hard (parallel) level also
includes only durations (D), but events can occur simultaneously. Pictures (top), drawn by DALL-E 3.

## Data Release

Please see `./data` folder to access the UnSeenTimeQA dataset.

    ├── ...
    ├── data
        ├── Easy
        │   └── Serial
	    |        ├── split_1
	    |        ├── split_2
	    |        ├── split_3
	    |	     └── split_4
        ├── Medium
        │   └── Serial
        |        ├── split_1
	    |	     ├── split_2
	    |        ├── split_3
	    |	     └── split_4
        └── Hard
            ├── Serial
            │    ├── split_1
	        │    ├── split_2
	        |    ├── split_3
	        │    └── split_4
            └── Parallel
                 ├── split_1
	             ├── split_2
	             ├── split_3
	             └── split_4                

In all these folders, the JSON files are formatted as below:

### JSON file format for UnSeenTimeQA

```JSON
{
    "id": "int",
    "domain_description": "str",
    "objects_description": "list",     
    "initial_states_description": "list",   
    "events": "list",   
    "question": "list",   
    "answers": "list",   
    "depth": "int",   
    "execution": "str",   
    "question_category": "int",   
    "source_plan_id": "int",   
}
```

### Question Types for UnSeenTimeQA

```JSON
{
    "question_type_1": "Static Time",
    "question_type_2": "Relative Time",
    "question_type_3": "Hypothetical Time", 
}
```

## BibTeX Entry and Citation Info ##

If you are using our dataset, please cite our paper:

```bibtex
@misc{uddin2024unseentimeqatimesensitivequestionansweringllms,
      title={UnSeenTimeQA: Time-Sensitive Question-Answering Beyond LLMs' Memorization}, 
      author={Md Nayem Uddin and Amir Saeidi and Divij Handa and Agastya Seth and Tran Cao Son and Eduardo Blanco and Steven R. Corman and Chitta Baral},
      year={2024},
      eprint={2407.03525},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2407.03525}, 
}
```

## Stay tuned for ...

- Huggingface version of UnSeenTimeQA dataset for easy access

## Contact Information ##
* For help or issues in using UnSeenTimeQA, please submit a GitHub issue.
* Please contact Md Nayem Uddin (muddin11@asu.edu) or Amir Saeidi (ssaeidi1@asu.edu) for communication related to UnSeenTimeQA.
