from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# ----------------------------------
# helper
# ----------------------------------
def clean(text):
    return " ".join(text.split())


# ----------------------------------
# API
# ----------------------------------
@app.route("/")
def home():
    return "AHMAD RDX Search Engine Running"


@app.route("/api/search", methods=["GET"])
def search():
    q = request.args.get("q")
    lang = request.args.get("lang", "roman")

    if not q:
        return jsonify({"status": False, "error": "Query missing"})

    results = []
    answer = ""

    # ----------------------------------
    # 1️⃣ DuckDuckGo Instant Answer
    # ----------------------------------
    try:
        ddg = requests.get(
            "https://api.duckduckgo.com/",
            params={"q": q, "format": "json"},
            timeout=10,
        ).json()

        if ddg.get("AbstractText"):
            answer = clean(ddg["AbstractText"])
    except:
        pass

    # ----------------------------------
    # 2️⃣ Wikipedia quick extract
    # ----------------------------------
    if not answer:
        try:
            wiki = requests.get(
                f"https://en.wikipedia.org/api/rest_v1/page/summary/{q}",
                timeout=10,
            ).json()

            if wiki.get("extract"):
                answer = clean(wiki["extract"])
        except:
            pass

    # ----------------------------------
    # 3️⃣ Web search fallback (lite)
    # ----------------------------------
    try:
        html = requests.get(
            f"https://lite.duckduckgo.com/lite/?q={q.replace(' ', '+')}",
            timeout=10,
        ).text

        soup = BeautifulSoup(html, "html.parser")
        for a in soup.find_all("a", limit=5):
            title = clean(a.get_text())
            link = a.get("href")
            if title and link:
                results.append({"title": title, "link": link})
    except:
        pass

    # ----------------------------------
    # Roman Urdu mode
    # ----------------------------------
    if lang == "roman" and answer:
        # small basic transform
        answer = answer.replace(" is ", " hai ")
        answer = answer.replace(" was ", " tha ")

    if not answer:
        answer = "Seedha jawab nahi mila, links check karo."

    return jsonify({
        "status": True,
        "question": q,
        "answer": answer[:300],
        "results": results[:5],
        "owner": "AHMAD RDX"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
