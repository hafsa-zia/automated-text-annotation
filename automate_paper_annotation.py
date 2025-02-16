import os
import csv
import time
import google.generativeai as genai  # Google Gemini API
import pdfplumber  # Extract text from PDFs
import pandas as pd  # Work with CSV efficiently

# Load API Key Securely
API_KEY = os.getenv("GEMINI_API_KEY")
PDF_FOLDER_PATH = os.getenv("PDF_FOLDER_PATH")

if not API_KEY:
    raise ValueError("API key not found! Set the GEMINI_API_KEY environment variable.")

if not PDF_FOLDER_PATH:
    raise ValueError("PDF folder path not found! Set the PDF_FOLDER_PATH environment variable.")

# Configure Gemini API
genai.configure(api_key=API_KEY)

# CSV File Path (Inside the PDF folder)
CSV_OUTPUT_PATH = os.path.join(PDF_FOLDER_PATH, "metadata.csv")

# Updated Categories
CATEGORIES = [
    "Computer Vision & Image Processing",
    "Artificial Intelligence & Machine Learning",
    "Optimization & Theoretical Machine Learning ",
    "Data Science & Statistical Learning",
    "Mathematical & Computational Modeling"
]

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF using pdfplumber."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages[:2]:  # Extract first 2 pages
                text += page.extract_text() + "\n"
            return text.strip()[:1000]  # Limit to 1000 characters
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return ""

def classify_paper(text):
    """Classifies extracted text using Google Gemini API."""
    prompt = f"Classify the following research paper into one of these categories: {', '.join(CATEGORIES)}.\n\nText: {text}\n\nCategory:"
    
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        category = response.text.strip()
        
        # Ensure the response is a valid category
        return category if category in CATEGORIES else "Unknown"
    except Exception as e:
        print(f"Error classifying text: {e}")
        return "Unknown"

def find_pdf_file(title):
    """Tries different filename formats to locate the correct PDF file."""
    # Remove special characters and normalize the title
    normalized_title = (
        title.replace(":", "")
        .replace("?", "")
        .replace("!", "")
        .replace("'", "")
        .replace('"', "")
        .replace("/", "_")
        .replace("\\", "_")
        .replace("*", "")
        .replace("(", "")
        .replace(")", "")
        .strip()
    )

    # Generate possible filenames
    possible_filenames = [
        f"{normalized_title}.pdf",  # Original title
        f"{normalized_title.replace(' ', '_')}.pdf",  # Spaces to underscores
        f"{normalized_title.replace(' ', '-')}.pdf",  # Spaces to hyphens
        f"{normalized_title.lower()}.pdf",  # Lowercase
        f"{normalized_title.replace(' ', '_').lower()}.pdf",  # Lowercase with underscores
        f"{normalized_title[:50]}.pdf",  # Truncated title
    ]

    # Try to find the PDF file
    for filename in possible_filenames:
        pdf_path = os.path.join(PDF_FOLDER_PATH, filename)
        if os.path.exists(pdf_path):
            return pdf_path  # Return the correct file path

    return None  # Return None if no matching file is found

def update_metadata_csv():
    """Reads PDFs from the folder, extracts text, classifies them, and updates metadata.csv."""
    if not os.path.exists(CSV_OUTPUT_PATH):
        print(f"Error: metadata.csv not found at {CSV_OUTPUT_PATH}")
        return
    
    # Read existing metadata
    df = pd.read_csv(CSV_OUTPUT_PATH)
    
    # Debug: Print DataFrame structure before adding the "Category" column
    print("DataFrame structure before adding 'Category' column:")
    print(df.columns)

    # Add "Category" column if it doesn't exist
    if "Category" not in df.columns:
        df["Category"] = ""  # Initialize with empty strings
        print("Added 'Category' column to DataFrame.")

    # Debug: Print DataFrame structure after adding the "Category" column
    print("DataFrame structure after adding 'Category' column:")
    print(df.columns)

    for index, row in df.iterrows():
        pdf_path = find_pdf_file(row["Paper Title"])  # Find correct PDF file

        if pdf_path is None:
            print(f"Warning: PDF file not found for '{row['Paper Title']}'")
            df.at[index, "Category"] = "Unknown"  # Mark as Unknown
        else:
            print(f"📄 Processing: {os.path.basename(pdf_path)}")

            # Extract text & classify
            extracted_text = extract_text_from_pdf(pdf_path)
            if extracted_text:
                category = classify_paper(extracted_text)
                df.at[index, "Category"] = category
                print(f"Updated: {os.path.basename(pdf_path)} -> {category}")

        # Save progress after processing each paper
        try:
            df.to_csv(CSV_OUTPUT_PATH, index=False)
            print(f"💾 Saved progress for '{row['Paper Title']}'")
        except Exception as e:
            print(f"Error saving CSV: {e}")

    print(f"✅ All papers processed and metadata.csv updated!")

if __name__ == "__main__":
    update_metadata_csv()