
-----

# HSE Compliance RAG Assistant ⚖️

This project is a sophisticated AI-powered chat assistant designed to help employees of "PetroSafe Global Holdings" understand and comply with the company's Health, Safety, and Environment (HSE) policies.

It uses a **Retrieval-Augmented Generation (RAG)** architecture to provide reliable, accurate, and context-aware answers grounded in a specific policy document. This approach minimizes AI "hallucinations" and ensures that all responses are based on the official source of truth.

The application is built with Python and Streamlit, powered by Azure AI Services for the backend, and deployed live on Render.

## 🏛️ Architecture Overview

The application follows a modern RAG pattern:

1.  **Frontend**: A user-friendly chat interface built with **Streamlit**.
2.  **Backend Logic**: The Streamlit app orchestrates the RAG process.
3.  **AI Services (Azure)**:
      * **Azure OpenAI**: Provides the embedding model (`text-embedding-ada-002`) to convert text to vectors and the chat model (`gpt-4o`) for generating answers.
      * **Azure AI Search**: Stores the indexed policy document and performs rapid vector searches to find relevant information.
4.  **Deployment**: The final application is hosted as a Web Service on **Render**.

-----

##  Features

  * **Grounded Answers**: Responses are based solely on the provided HSE policy document, ensuring accuracy.
  * **Intuitive Chat Interface**: A simple, interactive UI for asking compliance questions.
  * **Secure Configuration**: All API keys and endpoints are managed securely using environment variables.
  * **Scalable Deployment**: Hosted on Render for reliable, continuous access.
  * **Built-in Safety**: The assistant includes guardrails to prevent it from giving unauthorized advice and directs users to supervisors for complex issues.

-----

##  Tech Stack

  * **Language**: Python 3.9+
  * **Frontend**: Streamlit
  * **Cloud & AI**: Microsoft Azure
      * Azure AI Studio (for management)
      * Azure OpenAI Service
      * Azure AI Search
  * **Deployment**: Render, Git & GitHub

-----

##  Part 1: Setting Up the Azure Backend

This is the foundation of the project. Follow these steps to set up all the necessary Azure services using Azure AI Studio.

**Prerequisites:** An active Azure Subscription.

### Step 1: Create an Azure AI Studio Project

1.  Navigate to the [Azure Portal](https://portal.azure.com/).
2.  Create a new **Azure AI Hub** resource. This will serve as a container for your AI projects.
3.  Once the AI Hub is created, navigate to **Azure AI Studio** and create a new **Project** within your Hub. This project will be your workspace.

### Step 2: Deploy the AI Models

You need two types of models: one for generating text (chat) and one for creating embeddings (understanding text).

1.  In your AI Studio Project, go to the **Model catalog**.
2.  Find and select the **`gpt-4o`** model. Click **Deploy** and choose the "Pay-as-you-go" option.
3.  On the deployment screen, give it a clear **Deployment name** (e.g., `my-chat-model`). **This name is your `CHAT_MODEL` value.**
4.  Repeat the process for the embedding model. Go back to the **Model catalog**, find **`text-embedding-ada-002`**, and deploy it.
5.  Give it a unique **Deployment name** (e.g., `my-embedding-model`). **This name is your `EMBEDDING_MODEL` value.**

### Step 3: Create the Azure AI Search Service

1.  In the Azure Portal, search for and create a new **Azure AI Search** resource.
2.  Choose a pricing tier (the "Basic" or "Free" tier is sufficient for this project).
3.  Once created, this service will have a **URL** and **Admin keys**. You will need these later.

### Step 4: Create the Vector Index

This step involves uploading your policy document and having Azure AI Search index it.

1.  Prepare your knowledge base document (e.g., `HSE_Policy.pdf`).
2.  In Azure AI Studio, go to the **Indexes** tab in the left menu.
3.  Click **+ Create index**.
4.  **Source data**: Choose to upload your policy document.
5.  **Index store**: Select the Azure AI Search service you created in the previous step.
6.  Give your index a memorable name (e.g., `hse-policy-index`). **This is your `INDEX_NAME` value.**
7.  The wizard will automatically handle chunking the document and creating vector embeddings using the model you deployed. Let the indexing job complete.

-----

## 💻 Part 2: Running the Streamlit App Locally

Now that the Azure backend is ready, you can run the Streamlit application on your local machine.

### Step 1: Clone the Repository

```bash
git clone <your-repository-url>
cd <your-repository-folder>
```

### Step 2: Set Up a Virtual Environment (Recommended)

```bash
# Using Conda
conda create -n hse-app python=3.9
conda activate hse-app
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Your Environment Variables

1.  Create a new file in the root of your project named `.env`.
2.  Add the credentials for the Azure services you created in Part 1. **Do not use quotes.**

<!-- end list -->

```env
# .env file
# Get these from your Azure OpenAI resource in the Azure Portal
OPEN_AI_ENDPOINT="https://your-openai-endpoint.openai.azure.com/"
OPEN_AI_KEY="your_secret_openai_key"

# These are the DEPLOYMENT NAMES you chose in Step 2
CHAT_MODEL="my-chat-model"
EMBEDDING_MODEL="my-embedding-model"

# Get these from your Azure AI Search resource in the Azure Portal
SEARCH_ENDPOINT="https://your-search-service.search.windows.net"
SEARCH_KEY="your_secret_search_admin_key"

# This is the Index Name you chose in Step 4
INDEX_NAME="hse-policy-index"
```

### Step 5: Run the Application

```bash
streamlit run app.py
```

Your application should now be running in a new browser tab\!

-----

## 🌐 Part 3: Deploying to Render

The final step is to deploy your application to make it publicly accessible.

### Step 1: Prepare Your Repository

Ensure your project has the following four files at the root level:

  * `app.py` (your application code)
  * `requirements.txt` (your dependencies)
  * `.gitignore` (to exclude `.env`, `__pycache__/`, etc.)
 



### Step 2: Create a New Web Service on Render

1.  Log in to your Render account and create a **New Web Service**.
2.  Connect your GitHub repository.
3.  Configure the settings:
      * **Name**: A unique name for your app (e.g., `hse-assist`).
      * **Build Command**: `pip install -r requirements.txt`
      

### Step 3: Add Environment Variables

This is the most critical step. You must add the same key-value pairs from your local `.env` file to Render's secure environment variable manager.

1.  In your service dashboard, go to the **Environment** tab.
2.  Click **Add Environment Variable** for each key-value pair.
3.  Enter the keys and values exactly as they are in your `.env` file, **without quotes**.

### Step 4: Deploy

Click **Create Web Service**. Render will build and deploy your application. Once complete, you'll have a public URL to access your HSE Compliance Assistant.

-----

## 📂 Project Structure

```
.
├── .gitignore
├── Ragapp.py
├── requirements.txt
├── .streamlit
└── README.md
```