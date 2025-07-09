# 📄 AI-Powered Proposal Generator

An AI-driven tool that transforms client SRS documents into professional software proposals using predefined HTML templates. Powered by **LLaMA 4**, it extracts structured data through multi-stage processing and generates downloadable PDFs via **WeasyPrint**, all within a simple **Streamlit** UI.

---

## 🚀 Features

- 📥 Upload and analyze SRS documents
- 🧠 Extract key data using **LLaMA 4**
- 🖼️ Fill predefined HTML templates via **Jinja2**
- 🧾 Generate polished PDF proposals with **WeasyPrint**
- 🖥️ Simple, interactive **Streamlit** interface
- 🏢 Preloaded company info
---

## 🧰 Tech Stack

- **LLaMA 4** – LLM for multi-stage data extraction  
- **Streamlit** – Frontend for interaction and downloads  
- **Jinja2** – HTML template rendering  
- **WeasyPrint** – PDF generation from HTML  

---

## ⚙️ How It Works

1. Upload an SRS file via the Streamlit app  
2. Extract structured data using LLaMA 4  
3. Render proposal using Jinja2 and company template  
4. Download final PDF generated with WeasyPrint  

---

🔗 **Live Demo:** [proposal-generator-io.streamlit.app](https://proposal-generator-io.streamlit.app/)
