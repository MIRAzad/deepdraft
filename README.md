# DeepDraft

DeepDraft is a Streamlit-based application designed to facilitate proposal management tasks by extracting requirements from Request for Proposal (RFP) documents and generating responses to user queries.

## Overview

DeepDraft utilizes OpenAI's language models to extract relevant information from RFP documents and provide responses to user queries. It offers a user-friendly interface for uploading PDF files, inputting queries, and viewing generated responses.

## Features

- Extract key information from RFP documents.
- Generate responses to user queries based on extracted information.
- Store and manage generated responses for future reference.
- Support for different language models, including GPT-3.5 Turbo and GPT-4.

## Getting Started

To get started with DeepDraft, follow these steps:

1. **Clone the Repository**: Clone this repository to your local machine.
git clone https://github.com/your_username/DeepDraft.git

2. **Install Dependencies**: Navigate to the project directory and install the required dependencies.
pip install -r requirements.txt

3. **Set Up Environment Variables**: Ensure you have the necessary environment variables set up, including OpenAI API key and Streamlit secrets.

4. **Run the Application**: Execute the main script to run the DeepDraft application.
streamlit run main.py

5. **Use the Application**: Upload RFP PDF files, input queries, and explore generated responses using the provided interface.

## Contributing

Contributions to DeepDraft are welcome! If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix: `git checkout -b feature-name`.
3. Make your changes and commit them: `git commit -m 'Description of changes'`.
4. Push to your branch: `git push origin feature-name`.
5. Submit a pull request detailing your changes.

Please ensure that your contributions adhere to the project's coding standards and include appropriate documentation where necessary.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
