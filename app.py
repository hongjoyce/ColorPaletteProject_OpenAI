from flask import Flask, render_template, request
import openai
from dotenv import dotenv_values
import json
import logging

#have to set the debug config to see the logged.info
logging.basicConfig(level=logging.DEBUG)

config = dotenv_values(".env")
openai.api_key = config['OPENAI_API_KEY']

app = Flask(__name__,
            template_folder = 'templates',
            static_url_path='',
            static_folder='static')

def get_colors(msg):
    prompt = f"""
    You are a color palette generating assistant that responds to text prompts for color palettes
    you should generate color palettes that fit the theme, mood, or instructions in the prompt. 
    The palettes should be between 2 and 8 colors.
    Desire format: a JSON array of hexadecimal color codes

    Q:Convert the following verbal description of a color palette into a list of colors: The mediterranean sea
    A: ["#006699", "#66CCCC", "#F0E68C", "#008000", "#F08080"]

    Q:Convert the following verbal description of a color palette into a list of colors: sage, nature, earth
    A: ["#EDF1D6", "#9DC08B", "#609966", "#40513B"]

    Q: Convert the following verbal description of a color palette into a list of colors: {msg}
    A:
    """

    response = openai.Completion.create(
        model = "text-davinci-003",
        prompt = prompt,
        max_tokens = 200,
    )

    colors = json.loads(response["choices"][0]["text"])
    return colors


@app.route("/palette", methods = ["POST"])
def prompt_to_palette():
    #app.logger.info("HIT THE POST REQUEST ROUTE!!!!")
    query = request.form.get("query")
    colors = get_colors(query)
    return {"colors": colors}

@app.route("/")
def index():
    return render_template("index.html")

if __name__=="__main__":
    app.run(debug=True)

