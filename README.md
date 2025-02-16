Automating Research Paper Annotation Using Google Gemini  

Python 3.8+ | Google Gemini API | pdfplumber | Pandas  

This project automates the annotation of research papers using Google Gemini, a powerful Large Language Model (LLM). It extracts text from PDFs,
classifies the papers into predefined categories, and updates a metadata CSV file with the results.
Perfect for researchers, academics, and anyone dealing with large collections of papers.  

---

Features  

- Text Extraction: Extracts text from the first two pages of each PDF using pdfplumber.  
- AI Classification: Uses Google Gemini to classify papers into categories like:  
  - Computer Vision and Image Processing  
  - Artificial Intelligence and Machine Learning  
  - Optimization and Theoretical ML  
  - Data Science and Statistical Learning  
  - Mathematical and Computational Modeling  
- Metadata Updates: Appends the classification results to a CSV file for easy analysis.  

---

Getting Started  

Prerequisites  

- Python 3.8 or higher  
- Google Gemini API key  
- Required Python libraries: google-generativeai, pdfplumber, pandas  

Installation  

1. Clone the repository:  
  git clone https://github.com/hafsa-zia/automate-paper-annotation.git  
  cd automate-paper-annotation  

2. Install the required libraries:  
  pip install -r requirements.txt  

3. Set up environment variables:  
  - Create a .env file in the root directory and add your Google Gemini API key and PDF folder path:  

  GEMINI_API_KEY=your_api_key_here  
  PDF_FOLDER_PATH=path_to_your_pdf_folder  

---

Usage  

1. Prepare Your Data  
  - Ensure your PDFs are stored in the folder specified in PDF_FOLDER_PATH.  
  - The script expects a metadata.csv file in the same folder with the following columns:  
    - Paper Title  
    - Paper URL  
    - PDF URL  
    - Download Timestamp  

2. Run the Script  
  python automate_paper_annotation.py  

3. Check the Output  
  - The script will update the metadata.csv file with a new Category column containing the classification results.  

---

Example  

Input metadata.csv  

Paper Title | Paper URL | PDF URL | Download Timestamp  

Output metadata.csv  

Paper Title | Paper URL | PDF URL | Download Timestamp | Category  

---

Workflow Diagram  

Start → Load API Key and PDF Folder Path → Extract Text from PDFs → Classify Papers Using Google Gemini → Update Metadata CSV → End  

---

Contributing  

Contributions are welcome. If you’d like to contribute, please follow these steps:  

1. Fork the repository.  
2. Create a new branch for your feature or bugfix.  
3. Commit your changes.  
4. Submit a pull request.  

---

Acknowledgments  

- Google Gemini for providing the powerful LLM API.  
- pdfplumber for making PDF text extraction easy.  
- Pandas for simplifying data handling.  

---
