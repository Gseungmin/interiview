from few_shot.few_shot_dialog import concept_interview_first, concept_interview_second, concept_interview_summary, \
    problem_interview_first, problem_interview_second, problem_interview_summary, common_none, common_more
from utils.common_interview_prompt import COMMON_CONCEPT_SUMMARY_PROMPT, COMMON_MORE_PROMPT, COMMON_NONE_PROMPT
from utils.concept_interview_prompt import CREATE_CONCEPT_SYSTEM_PROMPT, CREATE_CONCEPT_TAIL_PROMPT
from utils.problem_interview_prompt import CREATE_PROBLEM_SOLVE_SYSTEM_PROMPT, CREATE_PROBLEM_SOLVE_TAIL_PROMPT
from utils.util import CONCEPT_PROMPT_TYPE, PROBLEM_SOLVE_PROMPT_TYPE, MORE_PROMPT_TYPE, NONE_PROMPT_TYPE


def get_system_prompt(type, time):
    if type == MORE_PROMPT_TYPE:
        return COMMON_MORE_PROMPT

    if type == NONE_PROMPT_TYPE:
        return COMMON_NONE_PROMPT

    if type == CONCEPT_PROMPT_TYPE and time == 0:
        return CREATE_CONCEPT_SYSTEM_PROMPT

    if type == CONCEPT_PROMPT_TYPE and (time == 1 or time == 2):
        return CREATE_CONCEPT_TAIL_PROMPT

    if type == CONCEPT_PROMPT_TYPE and time == 3:
        return COMMON_CONCEPT_SUMMARY_PROMPT

    if type == PROBLEM_SOLVE_PROMPT_TYPE and time == 0:
        return CREATE_PROBLEM_SOLVE_SYSTEM_PROMPT

    if type == PROBLEM_SOLVE_PROMPT_TYPE and (time == 1 or time == 2):
        return CREATE_PROBLEM_SOLVE_TAIL_PROMPT

    if type == PROBLEM_SOLVE_PROMPT_TYPE and time == 3:
        return COMMON_CONCEPT_SUMMARY_PROMPT

    return CREATE_PROBLEM_SOLVE_SYSTEM_PROMPT


def get_few_shot_example(type, time):
    if type == MORE_PROMPT_TYPE:
        return common_more

    if type == NONE_PROMPT_TYPE:
        return common_none

    if type == CONCEPT_PROMPT_TYPE and time == 0:
        return concept_interview_first

    if type == CONCEPT_PROMPT_TYPE and (time == 1 or time == 2):
        return concept_interview_second

    if type == CONCEPT_PROMPT_TYPE and time == 3:
        return concept_interview_summary

    if type == PROBLEM_SOLVE_PROMPT_TYPE and time == 0:
        return problem_interview_first

    if type == PROBLEM_SOLVE_PROMPT_TYPE and (time == 1 or time == 2):
        return problem_interview_second

    if type == PROBLEM_SOLVE_PROMPT_TYPE and time == 3:
        return problem_interview_summary

    return problem_interview_first