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


def create_proposal(client_requirements,company_quatation):
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

    ## Required JSON Format

    {{
        "company_name": "Company Name",
        "client_name": "Client Name",
        "introduction": "Create an introduction for the company about their experience in the field for more than 12 years in more detail",
        "problem_statement": "Client problem",
        "proposed_solution":"Generate the proposed solution for problem with 2-3 lines"
        "solution_phases": [
        "proposed solution phase 1"
        "proposed solution phase 2"
        "proposed solution phase 3"
        ],
        "team_members": [
            {{"name": "Random Indian Person Name", "role": "Role in project"}},
            {{"name": "Random Indian Person Name", "role": "Role in project"}}
        ],
        "total_cost": "Calculate the total cost",
        "cost_breakdown": [
            {{"description": "Service 1", "amount": "Cost for service"}},
            {{"description": "Service 2", "amount": "Cost for service"}},
            {{"description": "Service 3", "amount": "Cost for service"}},
            {{"description": "Service 4", "amount": "Cost for service"}}
        ],
        "company_email": "contact@yourcompany.com"
    }}

    *** Return the result in JSON format only. Do not include any explanation or additional text. ***
    """

    proposal_prompt = PromptTemplate(
        input_variables=["client_requirements", "quatation_details"],
        template=proposal_template
    )

    #Chain
    proposal_chain = proposal_prompt | llm

    #Getting proposal
    response = proposal_chain.invoke(input={"client_requirements": client_requirements, "quatation_details": company_quatation})

    #Printing the proposal
    print(response.content)
    return response.content


if __name__ == "__main__":
    try:
        #Getting Client Requirements
        client_requirements = extract_client_requirements("resources/SRS_Ecommerce_Platform.pdf")

        #Getting company quatation
        company_quatation = extract_company_quatation_details("resources/company_quatation.pdf")

        #Getting the proposal
        company_proposal = create_proposal(client_requirements,company_quatation)

        print(company_proposal)
    except Exception as e:
        print("Something went Wrong \n\n",e)
