import json
import requests
import traceback
from time import sleep
from .model_config import ModelConfig

__author__ = 'swliu'


def query_llm(model: ModelConfig, query, num_retry: int = 3) -> str:
    for i in range(num_retry):
        try:
            payload = _compute_payload(model=model, query=query)
            headers = _compute_headers(model.access_token)
            response = requests.post(model.api_url, json=payload, headers=headers)
            response_text = response.json()['response']
            return response_text
        except Exception as e:
            print(traceback.format_exc())
            sleep(1)
            continue
    return ""


def query_model_info_api(access_token, url, num_retry: int = 3) -> list:
    """
    :param access_token: API access token.
    :param url: API endpoint
    :param num_retry: int
    :return: a list of large language models that are hosted by ASU
    """
    for i in range(num_retry):
        try:
            headers = _compute_headers(access_token=access_token)
            response = requests.get(url=url, headers=headers)
            models_dict = json.loads(response.content)
            models = models_dict["models"]
            return models
        except Exception as e:
            print(traceback.format_exc())
            sleep(1)
            continue
    return []


def model_provider_mapper(models: list) -> dict:
    mapper = {
        model["name"]: model["provider"]
        for model in models
    }
    return mapper


def model_list(models: list) -> set:
    models = {model["name"] for model in models}
    return models


def _compute_headers(access_token):
    headers = {
        "Accept": "application/json",
        "Authorization": f'Bearer {access_token}'
    }
    return headers


def _compute_payload(model: ModelConfig, query: str):
    payload = {
        # required
        "model_provider": model.provider,
        # required
        "model_name": model.name,
        # optional
        "model_params": model.model_params,
        # required
        "prompt": query,
        # optional
        "enable_search": model.enable_search,
        # optional
        "search_params": model.search_params
    }
    return payload
