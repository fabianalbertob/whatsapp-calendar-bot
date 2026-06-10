from tenacity import retry, stop_after_attempt, wait_exponential

def retry_on_failure(max_attempts=3):
    return retry(
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True
    )