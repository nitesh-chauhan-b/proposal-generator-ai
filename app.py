import streamlit as st
import os
from jinja2 import Environment, FileSystemLoader
from langchain_community.document_loaders import PyPDFLoader  # For extracting text
from weasyprint import HTML
import langchain_helper as helper
import json
from langchain_core.output_parsers import JsonOutputParser

# Loading Jinja2 template
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template("proposal_template.html")

# Streamlit UI
st.title("📄 Proposal Creator AI")
st.write("**Upload a software requirements document to generate a proposal.**")

# File upload
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
try:
    if uploaded_file:
        st.success("File uploaded successfully!")

        #Saving uploaded file
        client_file_path = "client_documents/client_requirements.pdf"
        with open(client_file_path,"wb") as file:
            file.write(uploaded_file.getbuffer())

        # print("File Details : ",uploaded_file)
        if os.path.exists("client_documents/client_requirements.pdf"):
            client_doc_path = "client_documents/client_requirements.pdf"

        company_quatation_path = "resources/company_quatation.pdf"

        client_req = helper.extract_client_requirements(client_doc_path)
        company_quatation = helper.extract_company_quatation_details(company_quatation_path)

        company_proposal = helper.create_proposal(client_req,company_quatation)

        #Converting data into JSON
        json_parser = JsonOutputParser()
        company_proposal = json_parser.parse(company_proposal)

        # print("Proposal Type",type(company_proposal))

        proposal_html = template.render(company_proposal)

        # Display in Streamlit
        st.subheader("📜 Proposal Preview")
        st.components.v1.html(proposal_html, height=500, scrolling=True)

        # Buttons for Download

        HTML(string=proposal_html).write_pdf("documents/proposal.pdf")
        with open("documents/proposal.pdf", "rb") as file:
                st.download_button("Download PDF", file, "proposal.pdf", "application/pdf")

except Exception as e:
    st.write("Something Went Wrong \n\n",e)