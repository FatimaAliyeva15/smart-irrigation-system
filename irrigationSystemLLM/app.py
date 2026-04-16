from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route("/ask-llm", methods=["POST"])
def llm_handler():
    data = request.get_json()
    moisture = data.get("moisture")

    # Prompt düzgün şəkildə hazırlanır
    prompt = f"""
    Soil moisture is {moisture}%.
    If the moisture is below 30%, respond only with 'yes'.
    If it is 30% or above, respond only with 'no'.
    No explanation. Just 'yes' or 'no'.
    """

    try:
        result = subprocess.check_output(["ollama", "run", "llama3", prompt])
        answer = result.decode().strip().lower()
        print("LLM cavabı:", answer)

        should_water = answer == "yes"

        return jsonify({
            "should_water": should_water,
            "llm_response": answer
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
