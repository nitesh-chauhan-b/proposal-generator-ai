# adding functionality for user to add document about the company and then generate the proposal
import time

import streamlit as st
import os
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import langchain_helper as helper
from langchain_core.output_parsers import PydanticOutputParser,JsonOutputParser
import json


# Loading Jinja2 template
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template("proposal_template_4.html")

# Streamlit UI
st.title("📄 Proposal Creator AI")

st.write("**Upload a software requirements document and company details document(optional)**")

company_doc = st.file_uploader("Upload Company Detail PDF",type=["pdf"],key="company_doc")

# st.write("**Upload  to generate a proposal.**")

# File upload
uploaded_file = st.file_uploader("Upload SRS PDF", type=["pdf"])
try:

    if uploaded_file:
        st.success("File uploaded successfully!")

        #Saving uploaded file
        client_file_path = "client_documents/client_requirements.pdf"
        with open(client_file_path,"wb") as file:
            file.write(uploaded_file.getbuffer())
            print("Uploaded File is saved!")
        # print("File Details : ",uploaded_file)
        if os.path.exists("client_documents/client_requirements.pdf"):
            client_doc_path = "client_documents/client_requirements.pdf"


        company_quatation_path = "resources/company_quatation.pdf"

        # If we have the company details uploaded by the user
        if company_doc:
            company_details_path = "resources/uploaded_company_details.pdf"

            # Saving uploaded pdf
            with open(company_details_path,"wb") as file:
                file.write(company_doc.getbuffer())

            # Getting company details pdf
            if os.path.exists(company_details_path):
                company_details_path = "resources/uploaded_company_details.pdf"

        else:
            company_details_path = "resources/DRC_Systems_Details.pdf"

        #Getting client Requirements
        client_req = helper.extract_client_requirements(client_doc_path)

        #Getting company quotation
        company_quatation = helper.extract_company_quatation_details(client_req)

        #Getting company details
        company_details = helper.extract_company_details(company_details_path)

        company_proposal = helper.create_proposal(client_req,company_quatation,company_details)
        print("Waiting To Fetch Response")

        #Converting data into JSON
        json_parser = JsonOutputParser()
        json_company_proposal = json_parser.parse(company_proposal)
        print("FILTERED JSON COMPANY DATA \n\n :",json_company_proposal)
        # time.sleep(2)
        if json_company_proposal:
            print("Got Response")
            json_company_proposal["client_logos"] = [
                    "https://www.drcsystems.com/wp-content/uploads/2023/06/iimb-logo.png",
                    "https://www.drcsystems.com/wp-content/uploads/2023/09/logo-3.png",
                    "https://www.drcsystems.com/wp-content/uploads/2023/09/logo-4.png",
                    "https://www.drcsystems.com/wp-content/uploads/2023/09/logo-2.png",
                    "https://www.drcsystems.com/wp-content/uploads/2023/06/wipro-logo.png",
                    "https://www.drcsystems.com/wp-content/uploads/2023/09/logo-6.png",
                ]

            proposal_html = template.render(json_company_proposal)

            # Display in Streamlit
            st.subheader("📜 Proposal Preview")
            st.components.v1.html(proposal_html, height=500, scrolling=True)

            # Buttons for Download
            try:
                HTML(string=proposal_html).write_pdf("documents/proposal.pdf")
                with open("documents/proposal.pdf", "rb") as file:
                        st.download_button("Download PDF", file, "proposal.pdf", "application/pdf")
            except Exception as e:
                st.write("There is pdf rendering problem please try again.")
        else:
            st.write("Please try after sometime model limit is reached!")

except Exception as e:
    st.write("Something Went Wrong \n\n",e)