import json
import os.path

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser,PydanticOutputParser
import untils
from datetime import date
import re
from langchain_google_genai import ChatGoogleGenerativeAI
from json_repair import repair_json
import proposal_format
from proposal_format import ProposalData


load_dotenv()


#Setting LLM model
# llm = ChatGroq(model="llama3-70b-8192",temperature=0.6)

#Changing llm model
# llm = ChatGroq(model="deepseek-r1-distill-llama-70b",temperature=0.6)

# #Changing llm model
# llm = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct",
#                temperature=0.7,
#                #Adding parameter to force model to output JSON Response Every Time
#                model_kwargs={
#                    "response_format": {"type": "json_object"}
#                }
#                )

# # Using llm without the json format
# llm2 = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct",
#                temperature=0.7)

# llm = ChatGroq(model="llama-3.3-70b-versatile",temperature=0.6)


#Using google LLM
llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash',
                             temperature=0.6,
                            timeout = 120.0,
                             model_kwargs={
                   "response_format": {"type": "json_object"},

               })


llm2 = ChatGoogleGenerativeAI(model="gemini-2.0-flash", timeout = 120.0,temperature=0.7)

#Testing
# print(llm.invoke("hello"))


#Creating a JSON Parser
parser = JsonOutputParser()

#Extracting Client Requirements
def extract_client_requirements(file_path):
    client_loader = PyPDFLoader(file_path)

    docs = client_loader.load()

    #Extracting Information from the document

    # Combining document data
    client_requirements = ""
    for data in docs:
        client_requirements += data.page_content

    #Filtering the extracted text
    filtered_client_requirements = untils.clean_text(client_requirements)

    #Extracting Required details in JSON format
    data_extraction_prompt = """
        You are an AI assistant tasked with analyzing a software requirements document provided by a client. Your goal is to extract and generate a structured JSON output that includes the essential details needed for a project proposal.

        ### **Instructions:**
        1. Carefully analyze the document content to understand the client's problem, requirements, and expectations.
        2. Extract relevant details s   uch as client information, problem statement.
        3. Ensure the JSON output follows the exact structure defined below.

        ### **Document Content:**
        {document_text}

        JSON fileds must contain Following,
        - clent_problem, client_requirements,client_expectation,indept_analysis_of_problem

        **Now, analyze the provided document and generate the JSON output. Return JSON Output Only. Nothing else**
        """

    extraction_prompt = PromptTemplate(
        input_variables=["document_text"],
        template=data_extraction_prompt
    )

    #Creating a simple chain
    extraction_chain = extraction_prompt | llm2

    response = extraction_chain.invoke(input={"document_text":filtered_client_requirements})

    # return response.content
    return response

def extract_company_quatation_details(client_requirements):

    # quatation_loder = PyPDFLoader(file_path)
    #
    # quatation_doc = quatation_loder.load()
    #
    # # Extracting information from document
    # quatation_data = ""
    # for data in quatation_doc:
    #     quatation_data += data.page_content
    #
    #
    # #Filtering extracted information
    # filtered_quatation_data = untils.clean_text(quatation_data)


    #Converting Quatation data into Required JSON format
    # quotation_extraction_prompt = """
    # You are a helpful AI assistant designed to extract structured data from company quotations.
    #
    # ## Instructions
    # 1. Carefully analyze the entire quotation content provided.
    # 2. Extract the required details and format them strictly in the JSON structure given below.
    # 3. Do **not** include any additional commentary, explanation, or notes—return **only** the JSON object.
    # 4. If any required field is missing in the quotation, return it with an empty string or empty list as appropriate.
    #
    # ## Quotation Details
    # {quotation_data}
    #
    # ## Expected JSON Format
    # {{
    #     "company_name": "Name of the company",
    #     "services": {{
    #         "service_type_1": ["Duration", "Cost of service"],
    #         "service_type_2": ["Duration", "Cost of service"],
    #         "service_type_3": ["Duration", "Cost of service"]
    #     }},
    #     "Terms & Condition": ["T&C 1", "T&C 2"]
    # }}
    #
    # **Return Only JSON Data only. Nothing Else. NO PREAMBLE**
    # """

    quatation_extraction_prompt = """ 
        You are a quotation generator AI Assistant. While helps user to generate the quotation based on the client specified requirements.

        ### Instructions
        1. Generate the response in a most realistic manner search the web for finding a better understanding if have to.
        2. Your Job is to analysis the complete requirements of the client and try to understand their software requirements.
        3. Then, generate a sample qutation based on the requirements with realistic prices and also generate the person who will work on the task with their name and bio.
        4. Generate the prices in Indian Currency.

        #Client Requirements
        {client_requirements}

        #Format the output in JSON Only in the given format.
        ### JSON format
        {{
            "company_name":"DRC Systems India Limited.",
            "services":{{
                "service_type_1":["Duration","Cost of service"],
                "service_type_2":["Duration","Cost of service"],
                "service_type_3":["Duration","Cost of service"],
            }},
           "team_members": [
                {{"name": "Random Indian Person Name", "role": "Role in project",
                "bio" :"Generate bio about team member in short respective to their domain"
                }},
                {{"name": "Random Indian Person Name", "role": "Role in project",
                "bio" :"Generate bio about team member in short respective to their domain"
                }},
            ],
            "Terms & Condition":["T&C 1 ","T & C 2"]
        }}


    """
    quatation_extraction = PromptTemplate(
        input_variables=["client_requirements"],
        template=quatation_extraction_prompt
    )

    #Creating simple chain
    quatation_chain = quatation_extraction | llm2

    quatation_response = quatation_chain.invoke(input={"client_requirements":client_requirements})


    return quatation_response.content

def extract_company_details(file_path):
    if os.path.exists("resources/company_extracted_details.txt"):
        #Reading the file and returning the company details
        with open("resources/company_extracted_details.txt","r") as file:
            company_details = file.read()

        return company_details

    else:
        company_loader = PyPDFLoader(file_path)

        compnay_doc = company_loader.load()

        # Extracting text
        company_details_text = ""
        for doc in compnay_doc:
            company_details_text += doc.page_content

        fileter_company_details = untils.clean_text(company_details_text)

        detail_prompt = """
        You are a highly skilled AI assistant specializing in business intelligence extraction. Your task is to thoroughly analyze the provided company information and extract all meaningful, proposal-relevant data. This extracted data will be used to automatically generate a compelling software solution proposal that builds trust, demonstrates the company’s value, and increases client conversion rates.

        # Input Text
        {company_details}

        # Objective
        Transform the above company content into a rich, well-structured, and comprehensive JSON profile that represents the company’s full strengths and capabilities. This profile must serve as a foundation for generating high-quality proposals—highlighting the company’s credibility, technical strength, industry experience, and client outcomes.

        # Instructions
        1. Analyze the full input deeply—sentence by sentence—to understand the company's essence, expertise, experience, and credibility.
        2. Extract and synthesize all **relevant and useful** information. Be informative, concise, and structured.
        3. Generate the output strictly in the JSON format below. **Every field must be populated if information is available**.

        # Output JSON Format (Structure to Follow)
        ```json
        {{
          "extensive_summary": "A compelling, high-level summary of the company. Minimum 10 lines. Highlight history, philosophy, value proposition, achievements, trust signals, and impact.",
          "about_company": "More factual and structured background of the company: founding year, size, leadership, mission, and areas of specialization.",
          "their_clients": [
            "List notable clients, industries served, or market segments. Prefer real client names, but anonymized descriptions are okay."
          ],
          "why_should_you_hire_us": [
            "Unique selling proposition 1 (e.g., 100% on-time delivery record)",
            "USP 2 (e.g., proprietary frameworks for faster development)",
            "USP 3",
            "USP 4",
            "USP 5"
          ],
          "technological_experience": {{
            "Web Development": ["React", "Node.js", "Django"],
            "Mobile": ["Flutter", "React Native"],
            "Cloud & DevOps": ["AWS", "Docker", "Kubernetes"],
            "AI/ML": ["TensorFlow", "LangChain"],
            "Others": ["CRM Integrations", "IoT", etc.]
          }},
          "industry_experience": [
            "E-commerce: built scalable marketplaces for global clients",
            "Healthcare: HIPAA-compliant patient portals",
            "Fintech: payment gateway integrations and fraud detection"
          ],
          "notable_projects": [
            {{
              "title": "Project Name",
              "client_type": "Industry or sector",
              "technologies_used": ["Tech1", "Tech2", "Tech3"],
              "summary": "5–7 line overview of the project: what problem it solved, key features, and user impact.",
              "outcomes": "Measured or qualitative outcomes (e.g., 40% faster onboarding, 99.9% uptime, increased sales)."
            }}
          ],
          "customer_satisfaction": "Summarize client feedback, Net Promoter Score, testimonials, retention rates, or success metrics that show trust.",
          "global_presence": "Mention countries, regions, or markets served if relevant.",
          "certifications": [
            "ISO 27001",
            "AWS Partner",
            "SOC 2 Compliant"
          ],
          "team_strength": "Overview of team size, skillsets, organizational structure (e.g., 100+ engineers, dedicated R&D division).",
          "delivery_model": "Describe whether the company uses Agile, Dedicated Teams, Time-and-Material, or Fixed Price. Mention offshore/onshore options if applicable.",
          "core_values": [
            "Customer-centric innovation",
            "Data-driven decision making",
            "Integrity and transparency",
            "Agility and adaptability"
          ]
        }}
        """

        company_details_prompt = PromptTemplate(
            input_variables=["company_details"],
            template=detail_prompt
        )

        # Simple chain
        details_extraction_chian = company_details_prompt | llm2

        # Getting response
        company_details = details_extraction_chian.invoke(input={"company_details": fileter_company_details})

        with open("resources/company_extracted_details.txt","w") as file:
            file.write(company_details.content)

        return company_details.content

def create_proposal(client_requirements,company_quatation,company_details):
    # Another prompt
    proposal_template = """

    You are a highly intelligent and detail-oriented AI Assistant that generates comprehensive and professional software solution proposals based on provided client requirements and company quotation.

    ## Primary Goal
    Generate a highly detailed and persuasive software solution proposal in the exact JSON format specified below. Ensure the output is exhaustive, well-articulated, and each section is crafted to maximize clarity, marketing impact, technical precision, and strategic value.

    ## Detailed Instructions
    1. Carefully analyze the given client requirements and company quotation.
    2. Create an extensive, compelling proposal that addresses the client’s needs, highlights business value, and aligns with the company's strengths.
    3. Every field in the JSON should be filled with **maximum detail and clarity**.
    4. **Each textual field must be written with professional tone, persuasive language, and no placeholders. Avoid repetition.**
    5. In `executive_summary`, write **10–12 lines**, focusing on strategic vision, innovation, and business benefits.
    6. In `project_goals`, derive at least **5 specific and actionable objectives** from the client needs and project theme.
    7. In `success_metrics`, define at least **5 strong KPIs** that can be tracked and measured.
    8. In `about_company`, provide an in-depth **12-line overview** of the company’s experience, technologies, client success stories, and key differentiators.
    9. In `problem_statement`, reframe the client’s challenge as a major opportunity to create strategic advantage and value.
    10. In `proposed_solution`, craft a **10–12 line** in-depth explanation that blends creativity, innovation, technical solutioning, and ROI.
    11. In `assumptions`, list at least **5 well-thought-out and realistic assumptions** needed to ensure project success.
    12. In `solution_phases`, generate at least **4 to 6 clearly defined phases** of execution, each with a specific focus.
    13. In `project_schedule`, provide at least **4 detailed phases** with accurate timelines based on quotation.
    14. In `team_members`, list **4 unique members** (with Indian names), each having a realistic role and a 2–3 line bio explaining their domain expertise.
    15. In `technology_stack`, categorize stack into **appropriate domains** (e.g., Backend, Frontend, DevOps, AI/ML, etc.) with detailed tools and short reasoning for their choice.
    16. In `task_breakdown`, ensure:
        - Minimum of **5 main tasks** with 3–5 subtasks each.
        - Subtasks must be **technology-specific**, logically derived from the project goals and stack.
        - Provide **realistic and consistent estimated hours** based on project schedule and team size.
    17. In `why_us`, craft at least **3 detailed reasons** showing competitive advantage, specialization, and past results.
    18. In `case_study`, write:
        - A specific or anonymized client/industry example.
        - A **detailed 7–8 line** challenge.
        - An **8–10 line solution** describing tools, architecture, approach.
        - A **6–8 line results** section quantifying improvements, efficiencies, and business impact.
    19. In `next_steps`, list **5 chronological steps** that are clear and actionable.
    20. In `support_details`, write **a full paragraph** (6–8 lines) describing the scope of post-deployment support including tools, SLA, updates, issue resolution, and communication.
    21. In `pricing`, add at least **3–4 clearly itemized components** with descriptions and costs.
    22. In `total_cost`, **accurately sum all pricing components**.
    23. The year should be set to 2025.

    ## Client Requirements
    {client_requirements}

    ## Company Quotation
    {quatation_details}

    # Company Details
    {company_details}
       
    ## Required JSON Format

    {{ 
        "company_name": "Company Name",
        "company_email": "contact@yourcompany.com",
        "client_name": "Client Name",
        "project_title": "Title of the project",
        "proposal_date":"{today_date}",
        "executive_summary": "Highly detailed 10–12 line executive summary",
        "project_goals": [
            "Objective 1",
            "Objective 2",
            "Objective 3",
            "Objective 4",
            "Objective 5"
        ],
        "success_metrics": [
            "KPI 1",
            "KPI 2",
            "KPI 3",
            "KPI 4",
            "KPI 5"
        ],
        "about_company": "Comprehensive 12-line company overview highlighting domain expertise, client successes, and innovation culture",
        "problem_statement": "Clearly framed challenge with opportunity perspective",
        "proposed_solution": "Detailed 10–12 line solution highlighting features, technical strategy, impact, and value",
        "assumptions": [
            "Assumption 1",
            "Assumption 2",
            "Assumption 3",
            "Assumption 4",
            "Assumption 5"
        ],
        "solution_phases": [
            "Phase 1: ...",
            "Phase 2: ...",
            "Phase 3: ...",
            "Phase 4: ...",
            "Phase 5: ..."
        ],
        "project_schedule": [
            {{ "name": "Phase 1", "description": "Details", "start_date": "Start", "end_date": "End" }},
            {{ "name": "Phase 2", "description": "Details", "start_date": "Start", "end_date": "End" }},
            {{ "name": "Phase 3", "description": "Details", "start_date": "Start", "end_date": "End" }},
            {{ "name": "Phase 4", "description": "Details", "start_date": "Start", "end_date": "End" }}
        ],
        "team_members": [
            {{ "name": "Name 1", "role": "Role", "bio": "2–3 line domain-specific bio" }},
            {{ "name": "Name 2", "role": "Role", "bio": "2–3 line domain-specific bio" }},
            {{ "name": "Name 3", "role": "Role", "bio": "2–3 line domain-specific bio" }},
            {{ "name": "Name 4", "role": "Role", "bio": "2–3 line domain-specific bio" }}
        ],
        "technology_stack": {{
            "Frontend": ["React.js", "Tailwind CSS"],
            "Backend": ["Node.js", "Express.js"],
            "Database": ["MongoDB"],
            "DevOps": ["Docker", "GitHub Actions"],
            "AI/ML": ["LangChain", "OpenAI API"]
        }},
        "task_breakdown": [
            {{
                "name": "Task 1",
                "subtasks": [
                    {{ "name": "Subtask 1", "hours": 10 }},
                    {{ "name": "Subtask 2", "hours": 12 }},
                    {{ "name": "Subtask 3", "hours": 8 }}
                ]
            }},
            ...
        ],
        "why_us": [
            "Reason 1",
            "Reason 2",
            "Reason 3"
        ],
        "case_study": {{
            "client": "Anonymized Client Name",
            "challenge": "Detailed 7–8 line explanation of the challenge",
            "solution": "Detailed 8–10 line explanation of the solution and technical execution",
            "results": "6–8 line summary of outcomes, impact, and value delivered"
        }},
        "next_steps": [
            "Proposal Approval",
            "Contract Signing",
            "Kickoff Meeting",
            "Development Environment Setup",
            "Project Execution Start"
        ],
        "support_details": "6–8 line paragraph on post-deployment support, monitoring, maintenance, and communication methods",
        "pricing": [
            {{ "description": "Item 1", "cost": "Amount" }},
            {{ "description": "Item 2", "cost": "Amount" }},
            {{ "description": "Item 3", "cost": "Amount" }},
            {{ "description": "Item 4", "cost": "Amount" }}
        ],
        "total_cost": "Total of all line items",
        "current_year": 2025
    }}

    """

    #Getting current data
    today_date = date.today()

    # # Creating a parser
    # py_parser = PydanticOutputParser(pydantic_object=ProposalData)


    proposal_prompt = PromptTemplate(
        input_variables=["client_requirements", "quatation_details","company_details","today_date"],
        # partial_variables={"format_instructions":py_parser.get_format_instructions()},
        template=proposal_template
    )

    # #Adding output parser in response itself
    # parser = JsonOutputParser()

    #Chain
    proposal_chain = proposal_prompt | llm

    #Getting proposal
    response = proposal_chain.invoke(input={"client_requirements": client_requirements, "quatation_details": company_quatation,"company_details":company_details,"today_date":today_date})


    # #Filtering company proposal for JSON parsing
    pattern = re.compile(r'\{[\s\S]*\}', re.DOTALL)
    match = pattern.search(response.content)

    company_proposal = match.group(0)

    # Replacing the ** with the bold using the regular expression
    company_proposal = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', company_proposal)

    # Repairing it in adance to remove tralling commas, not closing quotes etc.

    try:
        parser.parse(company_proposal)
    except:
        # IF there is an error in parsing then applying the repair_json
        try:
            company_proposal = repair_json(company_proposal)
        except e:
            print("JSON Repair Error : ",e)

    # Printing the proposal
    print("Length of Response : ",len(company_proposal))
    # print("\n\n Filtered JSON Response : \n\n", company_proposal)

    return company_proposal



if __name__ == "__main__":
    try:
        #Getting Client Requirements
        client_requirements = extract_client_requirements("resources/SRS_Ecommerce_Platform.pdf")

        #Getting company quatation
        company_quatation = extract_company_quatation_details(client_requirements)

        #Getting company details
        company_details = extract_company_details("resources/DRC_Systems_Details.pdf")

        #Getting the proposal
        company_proposal = create_proposal(client_requirements,company_quatation,company_details)

        # print(company_proposal)
    except Exception as e:
        print("Something went Wrong \n\n",e)
