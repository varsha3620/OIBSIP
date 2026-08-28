import requests
from urllib.parse import quote


def answer_question(question):

    question = question.lower().strip()

    # Remove common question phrases
    prefixes = [
        "what is ",
        "what are ",
        "who is ",
        "who was ",
        "where is ",
        "when is ",
        "tell me about ",
        "explain "
    ]

    search_term = question

    for prefix in prefixes:
        if search_term.startswith(prefix):
            search_term = search_term[len(prefix):]
            break

    search_term = search_term.strip()

    # Wikipedia search API
    search_url = "https://en.wikipedia.org/w/api.php"

    params = {
        "action": "query",
        "list": "search",
        "srsearch": search_term,
        "format": "json",
        "utf8": 1
    }

    try:
        headers = {
            "User-Agent": "VoiceAssistant/1.0"
        }
        response = requests.get(
            search_url,
            params=params,
            headers=headers,
            timeout=5
        )
        

        if response.status_code == 200:

            data = response.json()

            results = data["query"]["search"]

            if results:

                page_title = results[0]["title"]

                summary_url = (
                    "https://en.wikipedia.org/api/rest_v1/page/summary/"
                    + quote(page_title)
                )

                summary_response = requests.get(
                    summary_url,
                    headers=headers,
                    timeout=5
                )

                if summary_response.status_code == 200:

                    summary_data = summary_response.json()

                    answer = summary_data.get("extract")

                    if answer:
                        return answer

        return "Sorry, I could not find information about that."

    except requests.RequestException:

        return "Sorry, I could not access the knowledge service."
