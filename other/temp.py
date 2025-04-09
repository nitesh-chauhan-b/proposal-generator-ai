from jinja2 import Template

# Load the HTML template as a string (you can read from a .html file too)
with open("../proposal_template.html", "r") as file:
    template_str = file.read()

# Your dynamic data
data = {
    "company_name": "TechNova",
    "company_logo": "https://example.com/logo.png",
    "client_name": "Acme Inc.",
    "introduction": "We have 12+ years of experience...",
    "problem_statement": "Client needs a system for...",
    "solution_phases": ["Planning", "Development", "Deployment"],
    "team_members": [
        {"name": "John Doe", "role": "Project Manager"},
        {"name": "Jane Smith", "role": "Lead Developer"}
    ],
    "total_cost": "$25,000",
    "cost_breakdown": [
        {"description": "UI Design", "amount": "$5,000"},
        {"description": "Backend Development", "amount": "$10,000"},
        {"description": "Testing", "amount": "$5,000"},
        {"description": "Deployment", "amount": "$5,000"}
    ],
    "company_email": "contact@technova.com"
}

# Render the HTML with data
template = Template(template_str)
rendered_html = template.render(data)

# Save it to a new HTML file
with open("final_proposal.html", "w") as output_file:
    output_file.write(rendered_html)
