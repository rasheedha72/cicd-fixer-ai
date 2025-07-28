from flask import Blueprint, render_template, request
import os
import json
import random
from .logic import process_log, get_ai_fix, highlight_sections

views = Blueprint('views', __name__)
UPLOAD_FOLDER = 'uploads'

@views.route('/', methods=['GET', 'POST'])
def home():
    log_text = None
    ai_fix = None
    filename = None
    highlighted_log = None

    if request.method == 'POST':
        uploaded_file = request.files['logfile']
        if uploaded_file.filename != '':
            filename = uploaded_file.filename
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            uploaded_file.save(filepath)

            # Read and highlight log
            log_text = process_log(filepath)
            highlighted_log = highlight_sections(log_text)

            # Get AI suggestion using Mistral
            ai_fix = get_ai_fix(log_text)

            return render_template("index.html", ai_fix=ai_fix, log_content=highlighted_log, filename=filename)

    return render_template('index.html', ai_fix=None, log_content=None, filename=None)


@views.route('/retry', methods=['POST'])
def retry_pipeline():
    log = request.form.get("log_content")

    # Simulate running pipeline
    result = random.choice(["✅ SUCCESS", "❌ FAILED AGAIN"])

    return render_template("retry_result.html", result=result, log=log)


@views.route("/history")
def show_history():
    with open("app/memory.json", "r") as f:
        memory = json.load(f)
    return render_template("history.html", memory=memory)
