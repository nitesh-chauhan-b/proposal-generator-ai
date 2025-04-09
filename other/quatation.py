from weasyprint import HTML
from datetime import datetime

# Define updated quotation content in HTML format with realistic INR pricing
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Quotation - DRC Systems India Limited</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            color: #333;
        }}
        h1 {{
            color: #2E86C1;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        th, td {{
            padding: 12px;
            border: 1px solid #ccc;
            text-align: left;
        }}
        th {{
            background-color: #f2f2f2;
        }}
        .summary {{
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <h1>Software Development Quotation</h1>
    <p><strong>DRC Systems India Limited</strong></p>
    <p><strong>Date:</strong> {datetime.today().strftime('%d %B, %Y')}</p>

    <table>
        <thead>
            <tr>
                <th>Service</th>
                <th>Description</th>
                <th>Duration</th>
                <th>Amount (INR)</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Business Analysis &amp; Requirement Gathering</td>
                <td>Initial workshops, stakeholder meetings, and documentation of requirements and system scope.</td>
                <td>2 weeks</td>
                <td>₹2,50,000</td>
            </tr>
            <tr>
                <td>UI/UX Design</td>
                <td>Wireframing, prototyping, and final design of the user interface ensuring responsiveness.</td>
                <td>2 weeks</td>
                <td>₹3,50,000</td>
            </tr>
            <tr>
                <td>Backend Development</td>
                <td>Building robust RESTful APIs, server-side architecture, and database integration.</td>
                <td>4 weeks</td>
                <td>₹12,00,000</td>
            </tr>
            <tr>
                <td>Frontend Development</td>
                <td>Implementation of UI using React.js with complete integration to backend APIs.</td>
                <td>3 weeks</td>
                <td>₹8,50,000</td>
            </tr>
            <tr>
                <td>QA &amp; Testing</td>
                <td>Manual and automated testing for functionality, performance, and usability.</td>
                <td>2 weeks</td>
                <td>₹4,00,000</td>
            </tr>
            <tr>
                <td>DevOps &amp; Deployment</td>
                <td>CI/CD pipeline setup, cloud deployment, and environment configuration (AWS/Azure).</td>
                <td>1 week</td>
                <td>₹3,00,000</td>
            </tr>
            <tr>
                <td>Project Management</td>
                <td>Sprint planning, daily standups, and overall project tracking using tools like Jira.</td>
                <td>Throughout the project</td>
                <td>₹3,00,000</td>
            </tr>
            <tr>
                <td>Post-Deployment Support</td>
                <td>Bug fixing, performance monitoring, and minor updates for 1 month after launch.</td>
                <td>1 month</td>
                <td>₹4,00,000</td>
            </tr>
        </tbody>
    </table>

    <div class="summary">
        <p><strong>Total Cost:</strong> ₹40,50,000</p>
        <p><strong>Payment Terms:</strong> 50% upfront, 50% upon project completion</p>
        <p><strong>Validity:</strong> Quotation valid for 30 days from the date of issue</p>
        <p><strong>Project Duration:</strong> Estimated 12 weeks from project kickoff</p>
    </div>
</body>
</html>
"""

# Generate the PDF file
pdf_file_path = "DRC_Systems_Quotation_INR.pdf"
HTML(string=html_content).write_pdf(pdf_file_path)

pdf_file_path
