import os
import json
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML as WeasyHTML
import gradio as gr
import shutil
import langchain_helper as helper
from langchain_core.output_parsers import JsonOutputParser

# Jinja2 template setup
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template("proposal_template_4.html")

def generate_proposal(pdf_file):
    try:
        if pdf_file is None:
            return "No file uploaded", None

        # Save uploaded file
        client_file_path = "client_documents/client_requirements.pdf"
        os.makedirs("client_documents", exist_ok=True)
        os.makedirs("documents", exist_ok=True)
        shutil.copy(pdf_file, client_file_path)

        if not os.path.exists(client_file_path):
            return "File saving failed.", None

        # Load paths
        company_quatation_path = "resources/company_quatation.pdf"
        company_details_path = "resources/DRC_Systems_Details.pdf"

        # Step 1: Extract data
        client_req = helper.extract_client_requirements(client_file_path)
        company_quatation = helper.extract_company_quatation_details(client_req)
        company_details = helper.extract_company_details(company_details_path)
        company_proposal = helper.create_proposal(client_req, company_quatation, company_details)

        # Step 2: Convert to JSON
        json_parser = JsonOutputParser()
        json_company_proposal = json_parser.parse(company_proposal)

        if not json_company_proposal:
            return "Model limit reached or proposal could not be generated.", None

        # Step 3: Add client logos
        json_company_proposal["client_logos"] = [
            "https://www.drcsystems.com/wp-content/uploads/2023/06/iimb-logo.png",
            "https://www.drcsystems.com/wp-content/uploads/2023/09/logo-3.png",
            "https://www.drcsystems.com/wp-content/uploads/2023/09/logo-4.png",
            "https://www.drcsystems.com/wp-content/uploads/2023/09/logo-2.png",
            "https://www.drcsystems.com/wp-content/uploads/2023/06/wipro-logo.png",
            "https://www.drcsystems.com/wp-content/uploads/2023/09/logo-6.png",
        ]

        # Step 4: Render HTML
        proposal_html = template.render(json_company_proposal)

        # Step 5: Save as PDF
        output_pdf_path = "documents/proposal.pdf"
        WeasyHTML(string=proposal_html).write_pdf(output_pdf_path)

        # Step 6: Load PDF for download
        return proposal_html, output_pdf_path

    except Exception as e:
        return f"An error occurred: {str(e)}", None

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("## 📄 Proposal Creator AI")
    gr.Markdown("Upload a software requirements document to generate a proposal.")

    with gr.Row():
        pdf_input = gr.File(label="Upload PDF", file_types=[".pdf"])
        generate_btn = gr.Button("Generate Proposal")

    html_output = gr.HTML(label="📜 Proposal Preview")
    pdf_download = gr.File(label="Download Proposal PDF")

    def on_generate(pdf_file):
        html_content, pdf_path = generate_proposal(pdf_file)
        return html_content, pdf_path if pdf_path else None

    generate_btn.click(fn=on_generate, inputs=pdf_input, outputs=[html_output, pdf_download])

# Launch app
demo.launch()
