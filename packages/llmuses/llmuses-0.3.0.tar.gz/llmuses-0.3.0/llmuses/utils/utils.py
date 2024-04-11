# Copyright (c) Alibaba, Inc. and its affiliates.
# Copyright (c) OpenCompass.

import functools
import importlib
import os
import re
import random
from typing import Any, Union, Dict
import hashlib
import datetime

import jsonlines as jsonl
import yaml

from llmuses.constants import DumpMode, OutputsStructure
from llmuses.utils.logger import get_logger

logger = get_logger()

TEST_LEVEL_LIST = [0, 1]

# Example: export TEST_LEVEL_LIST=0,1
TEST_LEVEL_LIST_STR = 'TEST_LEVEL_LIST'


def test_level_list():
    global TEST_LEVEL_LIST
    if TEST_LEVEL_LIST_STR in os.environ:
        TEST_LEVEL_LIST = [
            int(x) for x in os.environ[TEST_LEVEL_LIST_STR].split(',')
        ]

    return TEST_LEVEL_LIST


def jsonl_to_list(jsonl_file):
    """
    Read jsonl file to list.

    Args:
        jsonl_file: jsonl file path.

    Returns:
        list: list of lines. Each line is a dict.
    """
    res_list = []
    with jsonl.open(jsonl_file, mode='r') as reader:
        for line in reader.iter(
                type=dict, allow_none=True, skip_invalid=False):
            res_list.append(line)
    return res_list


def jsonl_to_reader(jsonl_file):
    """
    Read jsonl file to reader object.

    Args:
        jsonl_file: jsonl file path.

    Returns:
        reader: jsonl reader object.
    """
    with jsonl.open(jsonl_file, mode='r') as reader:
        return reader


def jsonl_to_csv():
    pass


def dump_jsonl_data(data_list, jsonl_file, dump_mode=DumpMode.OVERWRITE):
    """
    Dump data to jsonl file.

    Args:
        data_list: data list to be dumped.  [{'a': 'aaa'}, ...]
        jsonl_file: jsonl file path.
        dump_mode: dump mode. It can be 'overwrite' or 'append'.
    """
    if not jsonl_file:
        raise ValueError('output file must be provided.')

    jsonl_file = os.path.expanduser(jsonl_file)

    if dump_mode == DumpMode.OVERWRITE:
        dump_mode = 'w'
    elif dump_mode == DumpMode.APPEND:
        dump_mode = 'a'
    with jsonl.open(jsonl_file, mode=dump_mode) as writer:
        writer.write_all(data_list)
    logger.info(f'Dump data to {jsonl_file} successfully.')


def yaml_to_dict(yaml_file) -> dict:
    """
    Read yaml file to dict.
    """
    with open(yaml_file, 'r') as f:
        try:
            stream = yaml.safe_load(f)
        except yaml.YAMLError as e:
            logger.error(f'{e}')
            raise e

    return stream


def dict_to_yaml(d: dict, yaml_file: str):
    """
    Dump dict to yaml file.
    """
    with open(yaml_file, 'w') as f:
        yaml.dump(d, f, default_flow_style=False)
    logger.info(f'Dump data to {yaml_file} successfully.')


def get_obj_from_cfg(eval_class_ref: Any, *args, **kwargs) -> Any:
    module_name, spliter, cls_name = eval_class_ref.partition(':')

    try:
        obj_cls = importlib.import_module(module_name)
    except ImportError as e:
        logger.error(f'{e}')
        raise e

    if spliter:
        for attr in cls_name.split('.'):
            obj_cls = getattr(obj_cls, attr)

    return functools.partial(obj_cls, *args, **kwargs)


def markdown_table(header_l, data_l):
    md_str = f'| {" | ".join(header_l)} |'
    md_str += f'\n| {" | ".join(["---"] * len(header_l))} |'
    for data in data_l:
        if isinstance(data, str):
            data = [data]
        assert len(data) <= len(header_l)
        tmp = data + [''] * (len(header_l) - len(data))
        md_str += f'\n| {" | ".join(tmp)} |'
    return md_str


def random_seeded_choice(seed: Union[int, str, float], choices, **kwargs):
    """Random choice with a (potentially string) seed."""
    return random.Random(seed).choices(choices, k=1, **kwargs)[0]


def gen_hash(name: str):
    return hashlib.md5(name.encode(encoding='UTF-8')).hexdigest()


def dict_torch_dtype_to_str(d: Dict[str, Any]) -> dict:
    """
        Checks whether the passed dictionary and its nested dicts have a *torch_dtype* key and if it's not None,
        converts torch.dtype to a string of just the type. For example, `torch.float32` get converted into *"float32"*
        string, which can then be stored in the json format.

        Refer to: https://github.com/huggingface/transformers/pull/16065/files for details.
        """
    if d.get('torch_dtype', None) is not None and not isinstance(d['torch_dtype'], str):
        d['torch_dtype'] = str(d['torch_dtype']).split('.')[1]

    for value in d.values():
        if isinstance(value, dict):
            dict_torch_dtype_to_str(value)

    return d


class ResponseParser:

    @staticmethod
    def parse_first_capital(text: str) -> str:
        for t in text:
            if t.isupper():
                return t
        return ''

    @staticmethod
    def parse_last_capital(text: str) -> str:
        for t in text[::-1]:
            if t.isupper():
                return t
        return ''

    @staticmethod
    def parse_first_option_with_choices(text: str, options: list) -> str:
        """
        Find first valid option for text.

        Args:
            text: The text to parse.
            options: The options to find. e.g. ['A', 'B', 'C', 'D']
        """
        options_concat = '|'.join([str(i) for i in options])

        patterns = [
            f'答案是?\s?([{options_concat}])',
            f'答案是?\s?：([{options_concat}])',
            f'答案是?\s?:([{options_concat}])',
            f'答案应该?是\s?([{options_concat}])',
            f'答案应该?选\s?([{options_concat}])',
            f'答案为\s?([{options_concat}])',
            f'答案选\s?([{options_concat}])',
            f'选择?\s?([{options_concat}])',
            f'故选?\s?([{options_concat}])'
            f'只有选?项?\s?([{options_concat}])\s?是?对',
            f'只有选?项?\s?([{options_concat}])\s?是?错',
            f'只有选?项?\s?([{options_concat}])\s?不?正确',
            f'只有选?项?\s?([{options_concat}])\s?错误',
            f'说法不?对选?项?的?是\s?([{options_concat}])',
            f'说法不?正确选?项?的?是\s?([{options_concat}])',
            f'说法错误选?项?的?是\s?([{options_concat}])',
            f'([{options_concat}])\s?是正确的',
            f'([{options_concat}])\s?是正确答案',
            f'选项\s?([{options_concat}])\s?正确',
            f'所以答\s?([{options_concat}])',
            f'1.\s?([{options_concat}])[.。$]?$',
            f'所以\s?([{options_concat}][.。$]?$)',
            f'所有\s?([{options_concat}][.。$]?$)',
            f'[\s，：:,]([{options_concat}])[。，,\.]?$',
            f'[\s，,：:][故即]([{options_concat}])[。\.]?$',
            f'[\s，,：:]因此([{options_concat}])[。\.]?$',
            f'[是为。]\s?([{options_concat}])[。\.]?$',
            f'因此\s?([{options_concat}])[。\.]?$',
            f'显然\s?([{options_concat}])[。\.]?$',
            f'答案是\s?(\S+)(?:。|$)',
            f'答案应该是\s?(\S+)(?:。|$)',
            f'答案为\s?(\S+)(?:。|$)',
            f'答案是(.*?)[{options_concat}]',
            f'答案为(.*?)[{options_concat}]',
            f'固选(.*?)[{options_concat}]',
            f'答案应该是(.*?)[{options_concat}]',
            f'[Tt]he answer is [{options_concat}]',
            f'[Tt]he correct answer is [{options_concat}]',
            f'[Tt]he correct answer is:\n[{options_concat}]',
            f'(\s|^)[{options_concat}][\s。，,\.$]',  # noqa
            f'[{options_concat}]',
            f'^选项\s?([{options_concat}])',
            f'^([{options_concat}])\s?选?项',
            f'(\s|^)[{options_concat}][\s。，,：:\.$]',
            f'(\s|^)[{options_concat}](\s|$)',
            f'1.\s?(.*?)$',
        ]

        regexes = [re.compile(pattern) for pattern in patterns]
        for regex in regexes:
            match = regex.search(text)
            if match:
                outputs = match.group(0)
                for i in options:
                    if i in outputs:
                        return i
        return ''

    @staticmethod
    def parse_first_option(text: str) -> str:
        """
        Find first valid option for text.

        Args:
            text: The text to parse.
        """
        patterns = [
            r"[Aa]nswer:\s*(\w+)",
            r"[Tt]he correct answer is:\s*(\w+)",
            r"[Tt]he correct answer is:\n\s*(\w+)",
            r"[Tt]he correct answer is:\n\n-\s*(\w+)",
            r"[Tt]he answer might be:\n\n-\s*(\w+)",
            r"[Tt]he answer is \s*(\w+)",
        ]

        regexes = [re.compile(pattern) for pattern in patterns]
        for regex in regexes:
            match = regex.search(text)
            if match:
                return match.group(1)
        return ''

    @staticmethod
    def parse_first_capital_multi(text: str) -> str:
        match = re.search(r'([A-D]+)', text)
        if match:
            return match.group(1)
        return ''

    @staticmethod
    def parse_last_option(text: str, options: str) -> str:
        match = re.findall(rf'([{options}])', text)
        if match:
            return match[-1]
        return ''


def make_outputs_dir(work_dir: str, model_id: str, model_revision: str):
    model_revision = model_revision if model_revision is not None else 'none'
    now = datetime.datetime.now()
    format_time = now.strftime('%Y%m%d_%H%M%S')
    outputs_name = format_time + '_' + 'default' + '_' + model_id.replace('/', '_') + '_' + model_revision
    outputs_dir = os.path.join(work_dir, outputs_name)

    return outputs_dir


def process_outputs_structure(outputs_dir: str, is_make: bool = True) -> dict:
    logs_dir = os.path.join(outputs_dir, 'logs')
    predictions_dir = os.path.join(outputs_dir, 'predictions')
    reviews_dir = os.path.join(outputs_dir, 'reviews')
    reports_dir = os.path.join(outputs_dir, 'reports')
    configs_dir = os.path.join(outputs_dir, 'configs')

    if is_make:
        os.makedirs(outputs_dir, exist_ok=True)
        os.makedirs(logs_dir, exist_ok=True)
        os.makedirs(predictions_dir, exist_ok=True)
        os.makedirs(reviews_dir, exist_ok=True)
        os.makedirs(reports_dir, exist_ok=True)
        os.makedirs(configs_dir, exist_ok=True)

    outputs_structure = {
        OutputsStructure.LOGS_DIR: logs_dir,
        OutputsStructure.PREDICTIONS_DIR: predictions_dir,
        OutputsStructure.REVIEWS_DIR: reviews_dir,
        OutputsStructure.REPORTS_DIR: reports_dir,
        OutputsStructure.CONFIGS_DIR: configs_dir,
    }

    return outputs_structure


def import_module_util(import_path_prefix: str, module_name: str, members_to_import: list) -> dict:
    """
    Import module utility function.

    Args:
        import_path_prefix: e.g. 'llmuses.benchmarks.'
        module_name: The module name to import. e.g. 'mmlu'
        members_to_import: The members to import.
            e.g. ['DATASET_ID', 'SUBJECT_MAPPING', 'SUBSET_LIST', 'DataAdapterClass']

    Returns:
        dict: imported modules map. e.g. {'DATASET_ID': 'mmlu', 'SUBJECT_MAPPING': {...}, ...}
    """
    imported_modules = {}
    module = importlib.import_module(import_path_prefix + module_name)
    for member_name in members_to_import:
        imported_modules[member_name] = getattr(module, member_name)

    return imported_modules


def normalize_score(score: Union[float, dict], keep_num: int = 4) -> Union[float, dict]:
    """
    Normalize score.

    Args:
        score: input score, could be float or dict. e.g. 0.12345678 or {'acc': 0.12345678, 'f1': 0.12345678}
        keep_num: number of digits to keep.

    Returns:
        Union[float, dict]: normalized score. e.g. 0.1234 or {'acc': 0.1234, 'f1': 0.1234}
    """
    if isinstance(score, float):
        score = round(score, keep_num)
    elif isinstance(score, dict):
        score = {k: round(v, keep_num) for k, v in score.items()}
    else:
        logger.warning(f'Unknown score type: {type(score)}')

    return score
