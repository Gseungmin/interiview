from few_shot.interview_v2_dialog import concept_interview_first, concept_interview_second, concept_interview_summary, \
    problem_interview_first, problem_interview_second, problem_interview_summary
from utils.concept_interview_prompt import CREATE_CONCEPT_SYSTEM_PROMPT, CREATE_CONCEPT_TAIL_PROMPT, \
    CREATE_CONCEPT_SUMMARY_PROMPT
from utils.problem_interview_prompt import CREATE_PROBLEM_SOLVE_SYSTEM_PROMPT, CREATE_PROBLEM_SOLVE_TAIL_PROMPT, \
    CREATE_PROBLEM_SOLVE_SUMMARY_PROMPT
from utils.util import CONCEPT_PROMPT_TYPE, PROBLEM_SOLVE_PROMPT_TYPE


def get_system_prompt(type, time):
    if type == CONCEPT_PROMPT_TYPE and time == 0:
        return CREATE_CONCEPT_SYSTEM_PROMPT

    if type == CONCEPT_PROMPT_TYPE and (time == 1 or time == 2):
        return CREATE_CONCEPT_TAIL_PROMPT

    if type == CONCEPT_PROMPT_TYPE and time == 3:
        return CREATE_CONCEPT_SUMMARY_PROMPT

    if type == PROBLEM_SOLVE_PROMPT_TYPE and time == 0:
        return CREATE_PROBLEM_SOLVE_SYSTEM_PROMPT

    if type == PROBLEM_SOLVE_PROMPT_TYPE and (time == 1 or time == 2):
        return CREATE_PROBLEM_SOLVE_TAIL_PROMPT

    if type == PROBLEM_SOLVE_PROMPT_TYPE and time == 3:
        return CREATE_PROBLEM_SOLVE_SUMMARY_PROMPT

    return CREATE_PROBLEM_SOLVE_SYSTEM_PROMPT


def get_few_shot_example(type, time):
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