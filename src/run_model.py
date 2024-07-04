from utils import InferenceModel
import argparse

def parse_args(input_args=None):
    parser = argparse.ArgumentParser(description="Simple example of a inference script.")
    parser.add_argument(
        "--dataset_dir",
        type=str,
        default=None,
        required=True,)

    parser.add_argument(
        "--output_dir",
        type=str,
        default=None,
        required=True,)

    parser.add_argument(
        "--model_id",
        type=str,
        default=None,
        required=True,)

    parser.add_argument(
        "--max_length_input",
        type=int,
        default=2048,
        required=False,)

    parser.add_argument(
        "--max_new_tokens",
        type=int,
        default=2048,
        required=False,)

    parser.add_argument(
        "--top_p",
        type=float,
        default=0.9,
        required=False,)

    parser.add_argument(
        "--temperature",
        type=float,
        default=1e-12,
        required=False,)

    if input_args is not None:
        args = parser.parse_args(input_args)
    else:
        args = parser.parse_args()

    return args

           

def main(args):

    model = InferenceModel(args.model_id, args.dataset_dir)
    model.generate_response(args.max_length_input, args.temperature, args.max_new_tokens, args.top_p, args.output_dir)


if __name__ == "__main__":
    args = parse_args()
    main(args)