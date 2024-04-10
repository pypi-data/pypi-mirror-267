"""
Translate via aurora.

to turn on logger.trace output:
set LOGURU_LEVEL=TRACE  # in winows or
export LOGURU_LEVEL=TRACE  # or
cross-env LOGURU_LEVEL=TRACE python ...

text: str
# from_lang: str = "English"
to_lang: str = "Chinese"
selector: str = "aurora"
base_url: str = ""
api_key: str = ""
model: str = "gpt-3.5-turbo"
temperature: Union[float, None] = None

text: str
# from_lang: str = "English"
to_lang: str = "Chinese"
selector: str = "uuci"
base_url: str = ""
api_key: str = ""
model: str = "gpt-3.5-turbo"
temperature: Union[float, None] = None

"""
# pylint: disable=line-too-long,invalid-name,broad-except
import json
import os
from typing import Union

import dotenv
import stamina
import validators
from loguru import logger
from openai import APITimeoutError, BadRequestError, OpenAI, RateLimitError

prompt_tr = """I want you to act as a translator from any language {to_lang}. You will translate into {to_lang} text.
Your output should be in json format with optional 'translation' (string, only include the translation and nothing else, do not write explanations here) and 'notes' (string) fields.
If an input cannot be translated, return it unmodified in the 'translation' field."""

prompt_tr = """You are a professional translator from any language to {to_lang}. You will translate into {to_lang} text.
Your output will always be in json format with optional 'translation' (string, only include the translation and nothing else, do not write explanations here) and 'notes' (string) fields.
If an input is already {to_lang} or cannot be translated, return it unmodified in the 'translation' field."""
prompt_tr2 = """You are a professional translator from {from_lang} to  {to_lang}. You will translate into {to_lang} text.
Your output will always be in json format with optional 'translation' (string, only include the translation and nothing else, do not write explanations here) and 'notes' (string) fields.
If an input is already {to_lang} or cannot be translated, return it unmodified in the 'translation' field."""


# default: attempts 10,
# wait_initial 0.1, Minimum backoff before the *first* retry
# wait_max 5, Maximum backoff time between retries at any time.
# wait_jitter 1,
# retry on openai.RateLimitError with backoff 30 s
@stamina.retry(
    on=(
        RateLimitError,
        APITimeoutError,
    ),
    attempts=3,
    wait_initial=30,
    wait_max=120,
    wait_jitter=10,
)
def aurora_tr(
    # *args,
    text: str,
    from_lang: Union[str, None] = "English",
    to_lang: str = "Chinese",
    selector: str = "aurora",
    base_url: str = "",
    api_key: str = "",
    model: str = "",
    temperature: Union[float, None] = None,
):
    """
    Translate viaa auroa and uu.ci.

    Args:
    ----
    text: string to transalte
    from_lang: source language
    to_lang: target language
    selector: provider selector
    base_url: service base url
    api_key: token
    model: model name, anything for aurora
    temperature (float): 0.2-0.4 for translation, might just be left out

    Returns:
    -------
    dict/json: {"translation": "...", notes: "..."}

    """
    try:
        selector = selector.strip().upper()  #  = "AURORA"
    except Exception:
        selector = "aurora"

    try:
        from_lang = from_lang.strip().lower()
    except Exception:
        from_lang = "auto"

    try:
        to_lang = to_lang.strip().lower()
    except Exception:
        to_lang = "Chinese"

    if from_lang in ["en"]:
        from_lang = "English"
    if from_lang in ["zh", "中文", "chs", "mandarin"]:
        from_lang = "Chinese"

    if to_lang in ["en"]:
        to_lang = "English"
    if to_lang in ["zh", "中文", "chs", "mandarin"]:
        to_lang = "Chinese"

    if from_lang in ["auto", ""]:
        prompt = prompt_tr.format(to_lang=to_lang)
    else:
        prompt = prompt_tr2.format(to_lang=to_lang, from_lang=from_lang)

    if selector:
        suffix = "_" + selector
    else:
        suffix = ""

    # dotenv.load_dotenv() before dotenv.load_dotenv(".env-aurora")
    # dotenv.load_dotenv(override=True) after dotenv.load_dotenv(".env-aurora")
    # load from .env
    dotenv.load_dotenv(".env-aurora")

    # set OPENAI_DEBUG="debug" if LOGURU_LEVEL set to "TRACE"

    OPENAI_LOG = "info"
    if os.getenv("LOGURU_LEVEL") in ["TRACE"]:
        OPENAI_LOG = "debug"

    os.environ.update(
        {
            "OPENAI_BASE_URL": os.getenv("OPENAI_BASE_URL" + suffix, ""),
            "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY" + suffix, ""),
            "OPENAI_MODEL": os.getenv("OPENAI_MODEL" + suffix, ""),
            "OPENAI_LOG": OPENAI_LOG,
        }
    )

    # base_url takes precedence
    base_url = base_url or os.getenv("OPENAI_BASE_URL")

    # logger.debug(f"debug: {os.getenv('OPENAI_BASE_URL')[:12]=}")
    logger.trace(f"trace: {base_url=}")

    assert (
        base_url
    ), f"either base_url or env var OPENAI_BASE_URL_{selector} must be given."

    # for aurora: any string will do for aurora, gpt-3.5-turbo-0125
    # model = "gptx"

    if selector not in ["AURORA"] or api_key:
        # api_key takes precedence
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        assert (
            api_key
        ), f"either api_key or env var OPENAI_BASE_URL{suffix} must be given."

        client = OpenAI(
            base_url=base_url,
            api_key=api_key,
            max_retries=3,  # default 2
        )
    else:  # bypass api_key
        client = OpenAI(
            base_url=base_url,
            # api_key= api_key,
            max_retries=3,  # def 2
        )

    if not text.strip():
        res = {"translation": text, "notes": "empty input"}
        logger.warning("empty input, early exit")
        # raise SystemExit(0)
        return res

    if validators.url(text.strip()):  # type: ignore
        res = {"translation": text, "notes": "input is a url"}
        logger.warning("is a url, early exit")
        # raise SystemExit(0)
        return res

    content = None
    res = None  # to please pyright
    model = model or os.getenv("OPENAI_MODEL")
    assert base_url, f"either model or env var OPENAI_MODEL{suffix} must be given."

    try:
        # response = client.chat.completions.create(
        if temperature:
            response = client.chat.completions.with_raw_response.create(
                model=model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": text},
                ],
                temperature=temperature,
            )
        else:
            response = client.chat.completions.with_raw_response.create(
                model=model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": text},
                ],
            )

        # _ = response.usage.total_tokens
        # console.print(type(_), _)
        # console.print(response.choices[0].message.content)

        # content = response.choices[0].message.content

        logger.trace(response.headers)

        completion = response.parse()
        logger.trace(completion)

        content = completion.choices[0].message.content

    except BadRequestError as exc:
        try:
            res = {"translation": text, "notes": exc.body.get("message")}  # type: ignore
        except Exception:
            res = {"translation": text, "notes": f" {exc} "}
        logger.warning(exc)
    except Exception as exc:
        res = {"translation": text, "notes": f" {exc} "}
        logger.debug(exc)
        raise

    if content is not None:
        # strip possible ```json ... ```
        # strip('`\n') and remove prefix('json')
        _ = content.strip("`\n")
        if _.startswith("json"):
            _ = _[len("json") :]

        # remove new lines
        _ = _.replace("\n", " ")

        # in case the output is still not json
        try:
            res = json.loads(_)
        except Exception:
            res = {"translation": text, "notes": res}

    return res

    # print("hello from aurora_tr")
    # return "aurora"
