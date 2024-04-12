import logging
import os.path
import pathlib
from typing import Optional

from codeflash.api import cfapi
from codeflash.code_utils import env_utils
from codeflash.code_utils.git_utils import (
    get_repo_owner_and_name,
    git_root_dir,
    get_current_branch,
)
from codeflash.github.PrComment import FileDiffContent, PrComment
from codeflash.result.explanation import Explanation


def check_create_pr(
    optimize_all: bool,
    path: str,
    original_code: dict[str, str],
    new_code: dict[str, str],
    explanation: Explanation,
    existing_tests_source: str,
    generated_original_test_source: str,
):
    pr_number: Optional[int] = env_utils.get_pr_number()

    if pr_number is not None:
        logging.info(f"Suggesting changes to PR #{pr_number} ...")
        owner, repo = get_repo_owner_and_name()
        relative_path = str(pathlib.Path(os.path.relpath(path, git_root_dir())).as_posix())
        response = cfapi.suggest_changes(
            owner=owner,
            repo=repo,
            pr_number=pr_number,
            file_changes={
                str(pathlib.Path(os.path.relpath(p, git_root_dir())).as_posix()): FileDiffContent(
                    oldContent=original_code[p], newContent=new_code[p]
                )
                for p in original_code.keys()
            },
            pr_comment=PrComment(
                optimization_explanation=explanation.explanation_message(),
                best_runtime=explanation.best_runtime_ns,
                original_runtime=explanation.original_runtime_ns,
                function_name=explanation.function_name,
                relative_file_path=relative_path,
                speedup_x=explanation.speedup_x,
                speedup_pct=explanation.speedup_pct,
                winning_test_results=explanation.winning_test_results,
            ),
            existing_tests=existing_tests_source,
            generated_tests=generated_original_test_source,
        )
        if response.ok:
            logging.info("Suggestions were successfully made to PR #" + str(pr_number))
        else:
            logging.error(
                f"Optimization was successful, but I failed to suggest changes to PR #{pr_number}."
                f" Response from server was: {response.text}"
            )

    elif optimize_all:
        logging.info("Creating a new PR with the optimized code...")
        owner, repo = get_repo_owner_and_name()

        relative_path = str(pathlib.Path(os.path.relpath(path, git_root_dir())).as_posix())
        base_branch = get_current_branch()
        response = cfapi.create_pr(
            owner=owner,
            repo=repo,
            base_branch=base_branch,
            file_changes={
                str(pathlib.Path(os.path.relpath(p, git_root_dir())).as_posix()): FileDiffContent(
                    oldContent=original_code[p], newContent=new_code[p]
                )
                for p in original_code.keys()
            },
            pr_comment=PrComment(
                optimization_explanation=explanation.explanation_message(),
                best_runtime=explanation.best_runtime_ns,
                original_runtime=explanation.original_runtime_ns,
                function_name=explanation.function_name,
                relative_file_path=relative_path,
                speedup_x=explanation.speedup_x,
                speedup_pct=explanation.speedup_pct,
                winning_test_results=explanation.winning_test_results,
            ),
            existing_tests=existing_tests_source,
            generated_tests=generated_original_test_source,
        )
        if response.ok:
            logging.info(f"Successfully created a new PR #{response.text} with the optimized code.")
        else:
            logging.error(
                f"Optimization was successful, but I failed to create a PR with the optimized code."
                f" Response from server was: {response.text}"
            )
