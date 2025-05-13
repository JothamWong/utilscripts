import argparse
import os
import logging

from ollama import chat, ChatResponse

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def _build_file_tree_from_summaries(summaries: dict) -> dict:
    """
    Build a nested dictionary representation of the file tree from the summaries.
    """
    tree = {}
    for path_str, summary in summaries.items():
        parts = path_str.split(os.sep)
        current_level = tree
        for dir_part in parts[:-1]:
            if dir_part not in current_level:
                current_level[dir_part] = {}
            current_level = current_level[dir_part]
        current_level[parts[-1]] = summary
    return tree


def _recursive_print_tree_items(tree_node: dict, prefix: str):
    # Separate directories and files, then sort them alphabetically
    # Ensures that directories are listed before files
    # And items within each category are alphabetical
    dir_items = sorted(
        [item for item in tree_node.items() if isinstance(tree_node[item[0]], dict)]
    )
    file_items = sorted(
        [item for item in tree_node.items() if not isinstance(tree_node[item[0]], dict)]
    )

    all_items = dir_items + file_items

    for i, (name, value) in enumerate(all_items):
        is_last = i == len(all_items) - 1
        connector = "└── " if is_last else "├── "
        print(f"{prefix}{connector}{name}")
        child_prefix = prefix + ("    " if is_last else "│   ")
        if isinstance(value, dict):
            _recursive_print_tree_items(value, child_prefix)
        else:
            summary_content = (
                value if value and value.strip() else "No summary provided."
            )
            summary_lines = summary_content.split("\n")
            for s_line in summary_lines:
                print(f"{child_prefix}{s_line}")


def print_summaries_tree(project_name: str, all_summaries: dict):
    if not all_summaries:
        print("No summaries to display.")
        return
    print(f"\n\n---Project Summaries: {project_name} ---")
    file_tree_data = _build_file_tree_from_summaries(all_summaries)
    _recursive_print_tree_items(file_tree_data, prefix="")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Summarize a project.")
    parser.add_argument(
        "--input_project",
        "-i",
        type=str,
        required=True,
        help="Path to project directory to tree summarize",
    )
    parser.add_argument(
        "--model", "-m", required=True, type=str, help="Model to use for summarization"
    )
    parser.add_argument(
        "--blacklist",
        "-bl",
        nargs='+',
        type=str,
        help="List of files to exclude from summarization",
    )
    
    args = parser.parse_args()

    input_project = args.input_project
    model_name = args.model
    blacklist = args.blacklist if args.blacklist else []

    file_map = {}  # filename -> file contents
    proj_context_str_lst = []
    for dirpath, dirnames, filenames in os.walk(input_project):
        is_hidden_dir = any(
            dir_entry.startswith(".") for dir_entry in dirpath.split(os.sep)
        )
        if is_hidden_dir:
            continue
        
        logging.info(f"Processing directory: {dirpath}")
        for filename in filenames:
            if filename.startswith(".") or filename in blacklist:
                continue
            filepath = os.path.join(dirpath, filename)

            try:
                with open(filepath, "r") as f:
                    file_contents = f.read()
                    file_map[filepath] = file_contents
                    proj_context_str_lst.append(f"```{filename}\n{file_contents}\n```")
            except Exception as e:
                logging.error(f"Error reading file {filepath}: {e}")

    if not file_map:
        print("No files found in the project.")
        exit()

    proj_context_str = "\n\n---\n\n".join(proj_context_str_lst)
    # For each file, we will summarize it with respect to the entire project
    all_summaries = {}
    for filename, file_contents in file_map.items():
        filename = os.path.basename(filename)
        relative_filepath = os.path.relpath(filename, input_project)
        # TODO: If the project is very large, the project context str might exceed
        #       the model token limits. How might we circumvent this?
        prompt_message = (
            f"You are an expert code assistant. Below is the content of several files from a software project. "
            f"Your task is to summarize one specific file in the context of the entire project.\n\n"
            f"=== Full Project Context Start ===\n"
            f"{proj_context_str}\n"
            f"=== Full Project Context End ===\n\n"
            f"Now, please provide a concise summary in one line for the following file:\n"
            f"File Path (relative to project root): {relative_filepath}\n"
            f"File Content:\n```\n{file_contents}\n```\n\n"
            f"The summary should explain the primary role, purpose, and key functionalities or contents of this specific file ({relative_filepath}) in one line"
            f"and how it relates to or interacts with other parts of the project, based on the provided context. "
            f"Focus only on the specified file. Write a single line. Do not add any extra formatting."
        )

        try:
            logger.info(f"Summarizing file: {filename}")
            response: ChatResponse = chat(
                model=model_name, messages=[{"role": "user", "content": prompt_message}]
            )
            all_summaries[filename] = response.get("message", {}).get(
                "content", "No summary provided."
            )
            logging.info(all_summaries[filename])
        except Exception as e:
            logging.error(f"Error summarizing file {filename}: {e}")
            all_summaries[filename] = "Error occurred during summarization."

    project_root_name = os.path.basename(os.path.abspath(input_project))
    print_summaries_tree(project_root_name, all_summaries)