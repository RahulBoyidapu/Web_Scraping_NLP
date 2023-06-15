
# Data Extraction and Text Analysis

This project focuses on extracting textual data from given URLs and performing text analysis to compute various variables. It utilizes Python programming, along with libraries like BeautifulSoup, NLTK, and TextBlob, to extract the article text and analyze it.

## Installation

To use this project, follow these steps:

1. Clone the repository to your local machine.
2. Install the required dependencies by running `pip install -r requirements.txt`.

## Usage

1. Ensure that the URLs are provided in the "Input.xlsx" file, with each URL associated with a unique URL ID.
2. Run the main Python script, `data_extraction_and_analysis.py`, to extract the article content and perform text analysis.
3. The output will be saved in the "Output.xlsx" file, following the format specified in the output structure file.
4. View the generated output file to access the computed variables for each article.

## Data Extraction and Analysis

The project uses Python libraries such as BeautifulSoup, NLTK, and TextBlob for data extraction and text analysis. BeautifulSoup is employed to fetch the HTML content of the URLs and extract the article text, excluding any irrelevant sections like headers or footers. NLTK provides tools for tokenizing text, removing stopwords, stemming, and lemmatizing words. TextBlob is used for sentiment analysis and computing variables like polarity score, subjectivity score, and more.

## Input and Output Files

- **Input.xlsx**: This file contains the URLs and their corresponding URL IDs. Ensure that the URLs are listed in the "URL" column and the respective ID is in the "URL_ID" column.
- **Output.xlsx**: The output file will be generated after running the script, containing the computed variables for each article. The columns follow the structure defined in the output structure file.

## Examples

To extract data and analyze the articles, run the following command:

```
python data_extraction_and_analysis.py
```

Make sure to update the input file, "Input.xlsx", with the relevant URLs before running the script.

## Troubleshooting

If you encounter any issues or errors while running the script, consider the following:

- Check if all the necessary dependencies are installed by referring to the "requirements.txt" file.
- Ensure that the URLs in the input file are valid and accessible.
- Verify that the input and output files are in the correct format and located in the same directory as the script.

If you need further assistance or have any questions, feel free to reach out to Rahul Boyidapu at rahulboyidapu04@gmail.com
