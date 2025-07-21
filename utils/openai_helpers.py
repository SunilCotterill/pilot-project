from openai import OpenAI, APITimeoutError, APIConnectionError, APIStatusError, RateLimitError, OpenAIError
import logging
import json
import time

log = logging.getLogger(__name__)

def _generate_prompt(text: str) -> str:
    # Generates prompt for LLM
    
    return f"""
        You are an expert CSV data extractor. From the CSV below, return JSON with fields. 
        Ensure the final output is a single, valid JSON object and nothing else. Do not include any explanatory text or markdown formatting before or after the JSON. 
        Where possible, top-level JSON entities SHOULD be arrays or objects with multiple members. Any data must be explicitly in the CSV.

        Text data from CSV:
        {text}

        """

def _query_open_ai(client: OpenAI, prompt:str, model:str ="gpt-4o-mini", max_retries = 3) -> str:
    # Queries open ai for chat response
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model,
                response_format={"type": "json_object"}, 
                messages=[{"role": "user", "content": prompt}],
            )
            raw = response.choices[0].message.content
            try:
                return json.loads(raw)
            except json.JSONDecodeError as e:
                    log.warning("Bad JSON (%s); retrying %s/%s", e, attempt + 1, max_retries)
                    prompt+=" Please ensure the result is strictly in JSON format"

            
            return response.choices[0].message.content
        except (APITimeoutError, APIConnectionError) as e:
                log.warning("Network issue (%s); retrying %s/%s", e, attempt + 1, max_retries)

        except RateLimitError as e:
            retry_after = float(getattr(e.response.headers, "get", lambda *_: None)("Retry-After") or 0)
            sleep = retry_after if retry_after else 1.5 * (2 ** attempt)
            log.warning("Hit rate limit, sleeping %.1fs (%s/%s)", sleep, attempt + 1, max_retries)
            time.sleep(sleep)
            continue

        except APIStatusError as e:
            if e.status_code >= 500:
                log.warning("Server %s error; retrying %s/%s", e.status_code, attempt + 1, max_retries)
            else:
                raise          

        except OpenAIError:
            raise

        time.sleep(1.5 * (2 ** attempt))

    # ran out of attempts
    raise RuntimeError(f"OpenAI call failed after {max_retries} retries")

def perform_parsing(csv: str) -> dict:
    """ Performs open ai querying and parses response as json"""

    client = OpenAI()
    prompt = _generate_prompt(csv)
    response_json = _query_open_ai(client, prompt)
    return response_json

