from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain.prompts import PromptTemplate
import untils

load_dotenv()
#Setting LLM model

llm = ChatGroq(model="llama3-70b-8192",temperature=0.6)

#Testing
# print(llm.invoke("hello"))


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
    extraction_chain = extraction_prompt | llm

    response = extraction_chain.invoke(input={"document_text":filtered_client_requirements})

    return response.content


def extract_company_quatation_details(file_path):

    quatation_loder = PyPDFLoader(file_path)

    quatation_doc = quatation_loder.load()

    # Extracting information from document
    quatation_data = ""
    for data in quatation_doc:
        quatation_data += data.page_content


    #Filtering extracted information
    filtered_quatation_data = untils.clean_text(quatation_data)


    #Converting Quatation data into Required JSON format
    quotation_extraction_prompt = """
    You are a helpful AI assistant designed to extract structured data from company quotations.

    ## Instructions
    1. Carefully analyze the entire quotation content provided.
    2. Extract the required details and format them strictly in the JSON structure given below.
    3. Do **not** include any additional commentary, explanation, or notes—return **only** the JSON object.
    4. If any required field is missing in the quotation, return it with an empty string or empty list as appropriate.

    ## Quotation Details
    {quotation_data}

    ## Expected JSON Format
    {{
        "company_name": "Name of the company",
        "services": {{
            "service_type_1": ["Duration", "Cost of service"],
            "service_type_2": ["Duration", "Cost of service"],
            "service_type_3": ["Duration", "Cost of service"]
        }},
        "Terms & Condition": ["T&C 1", "T&C 2"]
    }}

    **Return Only JSON Data only. Nothing Else. NO PREAMBLE**
    """

    quatation_extraction = PromptTemplate(
        input_variables=["quatation_data"],
        template=filtered_quatation_data
    )

    #Creating simple chain
    quatation_chain = quatation_extraction | llm

    quatation_response = quatation_chain.invoke(input={"quatation_data":filtered_quatation_data})


    return quatation_response.content


def extract_company_details(file_path):

    company_loader = PyPDFLoader(file_path)

    compnay_doc = company_loader.load()

    # Extracting text
    company_details_text = ""
    for doc in compnay_doc:
        company_details_text += doc.page_content

    fileter_company_details = untils.clean_text(company_details_text)

    detail_prompt = """
    You Are an Helpful AI Assistant which helps the user to extract the details of the company in consise manner from the given text.

    #Details
    {company_details}

    #Instruction
    1. Analyis the whole document in depth.
    2. Convert the fileds which could be useful keeping in ming that this information will be used for creating a proposal from company.
    3. The details about company should include Extensive_summary, about company, thier_clients, why_should_you_hire_us?, technological_exprerince, industry_exprerince, notable_projects, customer_staticfacation.
    4. This all details MUST be in a JSON format. for example {{extensive_summaer:"summary"}} 
    5. For some important sections make them into detail

    ##Extract all the important details and convet them into JSON Only.
    #Retun the JSON output only. Nothing Else.

    """

    company_details_prompt = PromptTemplate(
        input_variables=["company_details"],
        template=detail_prompt
    )

    # Simple chain
    details_extraction_chian = company_details_prompt | llm

    # Getting response
    company_details = details_extraction_chian.invoke(input={"company_details": fileter_company_details})

    return company_details.content

def create_proposal(client_requirements,company_quatation,company_details):
    # Another prompt
    # Another prompt
    proposal_template = """

    You are a helpful AI Assistant that generates software solution proposals based on the provided client requirements and company quotation.

    ## Instructions
    1. Analyze the given information in depth.
    2. Create an innovative proposal for the client to provide a suitable software solution.
    3. Extract the required information and convert it into the exact JSON format specified below.
    4. In solution_phases generate the phases of solution based on the given information

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
        "proposal_date": "Date of proposal",
        "executive_summary": "Marketing-style executive summary that introduces the proposal, highlights the project’s impact, and builds trust",
        "about_company": "Create an introduction for the company about their experience in the field for more than 12 years in more detail",
        "problem_statement": "Reframe the client’s challenge as an opportunity—highlight pain points and the value of solving them to attract interest",
        "proposed_solution": "Present a compelling and slightly detailed (3–5 lines) solution that highlights innovation, impact, and business value",
        "solution_phases": [
            "proposed solution phase 1",
            "proposed solution phase 2",
            "proposed solution phase 3"
        ],
        "project_schedule": [
            {{"name": "Phase 1", "description": "Details", "start_date": "Start", "end_date": "End"}},
            {{"name": "Phase 2", "description": "Details", "start_date": "Start", "end_date": "End"}},
            {{"name": "Phase 3", "description": "Details", "start_date": "Start", "end_date": "End"}},
            {{"name": "Phase 4", "description": "Details", "start_date": "Start", "end_date": "End"}}
        ],
        "team_members": [
            {{"name": "Random Indian Person Name", "role": "Role in project"}},
            {{"name": "Random Indian Person Name", "role": "Role in project"}}
        ],
        "why_us": [
            "Reason 1",
            "Reason 2",
            "Reason 3"
        ],
        "pricing": [
            {{
                "description": "pricing description 1 ",
                "cost": "relavent price"
            }},
            {{
                "description": "pricing description 2",
                "cost": "relavent price"
            }},
            {{
                "description": "pricing description 3",
                "cost": "relavent price"
            }},

        ],
        "total_cost": "Calculate the total cost accoring to the price",
        "current_year": 2025
    }}

    *** Return the result in JSON format only. Do not include any explanation or additional text. ***
    """

    proposal_prompt = PromptTemplate(
        input_variables=["client_requirements", "quatation_details","company_details"],
        template=proposal_template
    )

    #Chain
    proposal_chain = proposal_prompt | llm

    #Getting proposal
    response = proposal_chain.invoke(input={"client_requirements": client_requirements, "quatation_details": company_quatation,"company_details":company_details})

    #Printing the proposal
    print(response.content)
    return response.content


if __name__ == "__main__":
    try:
        #Getting Client Requirements
        client_requirements = extract_client_requirements("resources/SRS_Ecommerce_Platform.pdf")

        #Getting company quatation
        company_quatation = extract_company_quatation_details("resources/company_quatation.pdf")

        #Getting company details
        company_details = extract_company_details("resources/DRC_Systems_Details.pdf")

        #Getting the proposal
        company_proposal = create_proposal(client_requirements,company_quatation,company_details)

        # print(company_proposal)
    except Exception as e:
        print("Something went Wrong \n\n",e)
