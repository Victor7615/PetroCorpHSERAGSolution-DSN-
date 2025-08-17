-----

# HSE Compliance RAG Assistant ⚖️

This project is a sophisticated AI-powered chat assistant designed to help employees of "PetroSafe Global Holdings" understand and comply with the company's Health, Safety, and Environment (HSE) policies.

It uses a **Retrieval-Augmented Generation (RAG)** architecture to provide reliable, accurate, and context-aware answers grounded in a specific policy document. This approach minimizes AI "hallucinations" and ensures that all responses are based on the official source of truth.

The application is built with Python and Streamlit, powered by Azure AI Services for the backend, and deployed live on Render.

##  Architecture Overview

The application follows a modern RAG pattern:

1.  **Frontend**: A user-friendly chat interface built with **Streamlit**.
2.  **Backend Logic**: The Streamlit app orchestrates the RAG process.
3.  **AI Services (Azure)**:
      * **Azure OpenAI**: Provides the embedding model (`text-embedding-ada-002`) to convert text to vectors and the chat model (`gpt-4o`) for generating answers.
      * **Azure AI Search**: Stores the indexed policy document and performs rapid vector searches to find relevant information.
4.  **Deployment**: The final application is hosted as a Web Service on **Render**.

-----

## Features

  * **Grounded Answers**: Responses are based solely on the provided HSE policy document, ensuring accuracy.
  * **Intuitive Chat Interface**: A simple, interactive UI for asking compliance questions.
  * **Secure Configuration**: All API keys and endpoints are managed securely using environment variables.
  * **Scalable Deployment**: Hosted on Render for reliable, continuous access.
  * **Built-in Safety**: The assistant includes guardrails to prevent it from giving unauthorized advice and directs users to supervisors for complex issues.

-----

## Tech Stack

  * **Language**: Python 3.9+
  * **Frontend**: Streamlit
  * **Cloud & AI**: Microsoft Azure
      * **Azure AI Foundry** (for management)
      * Azure OpenAI Service
      * Azure AI Search
  * **Deployment**: Render, Git & GitHub

-----

##  Part 1: Setting Up the Azure Backend with Azure AI Foundry

This is the foundation of the project. Follow these steps to set up all necessary Azure services.

**Prerequisites:** An active Azure Subscription.

### Step 1: Create an Azure AI Foundry Hub and Project

1.  In a web browser, open the **Azure AI Foundry portal** at `https://ai.azure.com` and sign in.
2.  Navigate to the management center (`https://ai.azure.com/managementCenter/allResources`) and select **Create new**. Choose the option to create a new **AI hub resource**.
3.  In the creation wizard, select your subscription and resource group, and give your new **Azure AI Foundry hub** a unique name in a supported region (e.g., East US 2).
4.  Once the hub is created, navigate to it and create a new **Project**. This project will be your primary workspace for deploying models and creating indexes.

### Step 2: Deploy the AI Models

You need two models: one for generating text (chat) and one for creating embeddings (understanding text).

1.  In your AI Foundry project, go to the **Models + endpoints** page in the left navigation pane.
2.  Deploy the **`text-embedding-ada-002`** model. Give it a clear **Deployment name** (e.g., `my-embedding-model`). **This name is your `EMBEDDING_MODEL` value.**
3.  Return to the **Models + endpoints** page and repeat the process to deploy the **`gpt-4o`** model. Give it a unique **Deployment name** (e.g., `my-chat-model`). **This name is your `CHAT_MODEL` value.**

### Step 3: Add the Knowledge Base Data

1.  Prepare your knowledge base document. For this project, it's the `HSE_Policy.pdf` or a similar text file.
2.  In your AI Foundry project, navigate to the **Data + indexes** page.
3.  Select **+ New data**. In the wizard, choose **Upload files/folders**.
4.  Upload your policy document. Give the data asset a name, such as `hse-policy-data`.

### Step 4: Create the Vector Index

This step involves indexing your policy document so it can be searched efficiently.

1.  On the **Data + indexes** page, select the **Indexes** tab.
2.  Click **+ New index** and configure it with the following settings:
      * **Source location**: Select "Data in Azure AI Foundry" and choose the `hse-policy-data` asset you just created.
      * **Index configuration**:
          * **Select Azure AI Search service**: Choose to **Create a new Azure AI Search resource**.
          * Provide a unique **Service name**, and ensure the **Location** and **Resource group** match your AI Foundry hub.
          * Select the **Basic** pricing tier.
      * **Vector index**: Give your index a memorable name (e.g., `hse-policy-index`). **This is your `INDEX_NAME` value.**
      * **Search settings**:
          * Ensure **Add vector search to this search resource** is enabled.
          * For the **Azure OpenAI connection**, select the default resource for your hub.
          * For the **Embedding model**, choose `text-embedding-ada-002` and select the deployment you created in Step 2.
3.  Click **Create** and wait for the indexing process to complete.

-----

## Part 2: Running the Streamlit App Locally

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

Create a file named `.env` in the root of your project and add the credentials for the Azure services you created in Part 1. **Do not use quotes.**

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
streamlit run Ragapp.py
```

-----

##  Part 3: Deploying to Render

The final step is to deploy your application to make it publicly accessible.

### Step 1: Prepare Your Repository

Ensure your project has the `Ragapp.py`, `requirements.txt`, `.gitignore`.

The `startup.sh` file should contain:


### Step 2: Create a New Web Service on Render

1.  Log in to your Render account and create a **New Web Service**.
2.  Connect your GitHub repository.
3.  Configure the settings:
      * **Name**: A unique name for your app (e.g., `hse-assist`).
      * **Build Command**: `pip install -r requirements.txt`
      * **Start Command**: `bash startup.sh`

### Step 3: Add Environment Variables

In the **Environment** tab on Render, add the same key-value pairs from your local `.env` file. **Do not use quotes.**

### Step 4: Deploy

Click **Create Web Service**. Render will build and deploy your application, providing you with a public URL.

-----

## 📂 Project Structure

```
.
Of course. Adding a UI theme configuration is a great way to customize your application's appearance.

Here are the updated sections for your `README.md` file to reflect this change.

-----

### \#\# Updated Section: `Part 2: Running the Streamlit App Locally`

I've added a new optional step explaining the theme configuration.

#### Step 6 (Optional): Customize the UI Theme

This project includes a `.streamlit/config.toml` file to customize the application's appearance. You can modify this file to change colors, fonts, and more to match your brand.

1.  Create a folder named `.streamlit` in your project's root directory.
2.  Inside this folder, create a file named `config.toml`.
3.  Add your theme settings. For example:

<!-- end list -->

```toml
# .streamlit/config.toml

[theme]
# Primary accent color for interactive elements.
primaryColor = "#d33682"

# Background color for the main content area.
backgroundColor = "#031F54"

# Background color used for the sidebar and most interactive widgets.
secondaryBackgroundColor = "#213C56"

# Color used for almost all text.
textColor = "#fff"
```

Streamlit will automatically apply these settings when you run the app.

-----

### \#\# Updated Section: `Project Structure`

The project structure has been updated to include the new `.streamlit` directory and `config.toml` file.

```
.
├── .streamlit/
│   └── config.toml
├── .gitignore
├── Ragapp.py
├── requirements.txt
└── README.md

```
