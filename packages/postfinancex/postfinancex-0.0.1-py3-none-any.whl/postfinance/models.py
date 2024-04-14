from typing import List

from ibm_watsonx_ai.foundation_models import Model
from ibm_watsonx_ai.foundation_models.utils.enums import (
    DecodingMethods,
    ModelTypes,
)
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames


def list_models(task: str) -> List[str]:
    """List supported models.

    Reference:
        [1] https://ibm.github.io/watsonx-ai-python-sdk/fm_model.html#ibm_watsonx_ai.foundation_models.utils.enums.ModelTypes
        [2] https://dataplatform.cloud.ibm.com/docs/content/wsj/analyze-data/fm-models.html?context=wx&audience=wdp
    """
    if task == "translate":
        return [
            # "ibm/granite-20b-multilingual",
            "mistralai/mixtral-8x7b-instruct-v01",
            ModelTypes.MIXTRAL_8X7B_INSTRUCT_V01_Q.value,
        ]
    if task == "annotate":
        return [
            "mistralai/mixtral-8x7b-instruct-v01",
            ModelTypes.MIXTRAL_8X7B_INSTRUCT_V01_Q.value,
            # ModelTypes.LLAMA_2_70B_CHAT.value,
        ]
    if task == "chat":
        return [
            "mistralai/mixtral-8x7b-instruct-v01",
            ModelTypes.MIXTRAL_8X7B_INSTRUCT_V01_Q.value,
            # ModelTypes.LLAMA_2_70B_CHAT.value,
        ]
    raise ValueError(f'Unsupported task: "{task}"')


def list_decoding_methods() -> List[str]:
    return [
        DecodingMethods.GREEDY.value,
        DecodingMethods.SAMPLE.value,
    ]


def list_params() -> List[str]:
    """

    >>> GenTextParamsMetaNames().show()
    >>> ---------------------  -----  --------
        META_PROP NAME         TYPE   REQUIRED
        DECODING_METHOD        str    N
        LENGTH_PENALTY         dict   N
        TEMPERATURE            float  N
        TOP_P                  float  N
        TOP_K                  int    N
        RANDOM_SEED            int    N
        REPETITION_PENALTY     float  N
        MIN_NEW_TOKENS         int    N
        MAX_NEW_TOKENS         int    N
        STOP_SEQUENCES         list   N
        TIME_LIMIT             int    N
        TRUNCATE_INPUT_TOKENS  int    N
        RETURN_OPTIONS         dict   N
        ---------------------  -----  --------

    Reference:
        [1] https://ibm.github.io/watsonx-ai-python-sdk/fm_model.html#metanames.GenTextParamsMetaNames
        [2] https://dataplatform.cloud.ibm.com/docs/content/wsj/analyze-data/fm-model-parameters.html?context=wx
    """
    return [
        GenTextParamsMetaNames.DECODING_METHOD,
        GenTextParamsMetaNames.TEMPERATURE,
        GenTextParamsMetaNames.TOP_P,
        GenTextParamsMetaNames.TOP_K,
        GenTextParamsMetaNames.RANDOM_SEED,
        GenTextParamsMetaNames.REPETITION_PENALTY,
        GenTextParamsMetaNames.MIN_NEW_TOKENS,
        GenTextParamsMetaNames.MAX_NEW_TOKENS,
    ]


def get_model(
    task: str,
    model: str,
    params: dict,
    api_key: str,
) -> Model:
    if model not in list_models(task):
        raise ValueError(f'Unsupported model: "{model}" for task "{task}"')
    return Model(
        model_id=model,
        params=params,
        credentials={
            "apikey": api_key,
            "url": "https://us-south.ml.cloud.ibm.com",
        },
        project_id="38a37d7d-4ab7-4349-935c-936add66c7f5",
    )
