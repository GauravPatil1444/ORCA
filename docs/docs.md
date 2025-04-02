<h1> 1. Introduction </h1>
ORCA is a no-code AI chatbot-building platform designed to enable users to create and deploy 
intelligent question-and-answer chatbots effortlessly. It leverages Large Language Models 
(LLMs) and Groq's high-speed inference engine to ensure adaptability and efficiency. 

## 1.1 Problem Statement 
Creating AI-driven chatbots typically requires extensive technical knowledge in machine 
learning and natural language processing (NLP). Many businesses and individuals face 
challenges when attempting to develop and deploy intelligent Q&A systems without the 
necessary coding skills. Existing platforms either demand coding expertise or are limited in 
functionality. The lack of a user-friendly, no-code solution hinders the potential for widespread 
adoption and usability of AI-powered chatbots. 

## 1.2 Objectives 
The goal of this project is to develop ORCA, a no-code AI chatbot-building platform that 
allows users to effortlessly create, configure, and deploy AI-powered Q&A chatbots without 
requiring programming skills. The specific objectives are: 

1. To create an intuitive, user-friendly platform for building AI chatbots. 
2. To enable real-time, context-aware conversations using large language models (LLMs) 
and Groq’s inference engine. 
3. To allow easy integration with external systems via API endpoints. 
4. To provide scalability for hosting multiple chatbot instances. 
5. To support diverse input formats like blogs, websites, PDFs, JSON, images, and voice 
inputs for chatbot training. 
6. To facilitate the sharing of custom chatbots via API, increasing the platform’s 
accessibility. 

## 1.3 Application 
ORCA can be applied across various domains such as:

**• Customer Support:** Automating responses to frequently asked questions and assisting 
customers with product inquiries. 

**• Education:** Building interactive chatbots that guide students through educational 
content and answer academic questions. 

**• Research:** Creating chatbots to facilitate research by providing users with relevant
information based on a set of documents or queries.

**• Business Automation:** Streamlining business processes like feedback collection, 
scheduling, and information dissemination via chatbot interactions.

<h1>2. Literature Survey</h1>

<h2>2.1 Background</h2

Over the past few years, chatbots have become increasingly popular for automating interactions, with applications ranging from customer service to healthcare support. These systems traditionally rely on rule-based algorithms or machine learning models, such as Long Short-Term Memory (LSTM) and transformers, to generate responses. However, deploying and managing these models usually requires significant coding expertise.

The shift toward no-code platforms and the integration of Large Language Models (LLMs) like GPT-3/4 has democratized AI. This has made AI chatbots more accessible to users without deep technical knowledge. With platforms like ORCA, users can now leverage sophisticated AI for chatbot creation with a user-friendly interface, boosting both functionality and acces
sibility.

<h2>2.2 Existing Systems</h2>

**1. Dialogflow by Google (2019):** Provides a cloud-based framework for building conversational agents. Users can train bots with pre-built templates and manage them without coding, but the customization options can be limited.

**o Citation: Gamboa, R. and Lima, P., 2019. Dialogflow:** Google’s conversational platform for artificial intelligence chatbots. Journal of AI Research, 67, pp. 55-61.

**2. IBM Watson Assistant (2018):** A popular AI tool for building conversational agents that supports voice input and integrates with various business systems. However, users still need basic programming knowledge for optimal customization.

**o Citation: Wu, F., Zhao, Y., and Zhang, M., 2018. IBM Watson Assistant:** Integrating AI into the customer service experience. Business AI Review, 10(2), pp. 42-47.

**3. Rasa (2020):** An open-source conversational AI platform designed for developers who need more control over their chatbots. Although powerful, it requires coding skills and is less suitable for non-technical users.

**o Citation: Zhang, D., and Tang, X., 2020. Rasa:** Open-source conversational AI for developers. AI Communication, 12(4), pp. 102-110.

**4. ChatGPT (2023):** OpenAI's conversational AI model, capable of generating detailed and contextually relevant answers. Though it is a cutting-edge model, it requires developers to integrate it into systems or build apps around it.

**o Citation: Brown, T., and Dempsey, L., 2023. GPT-3 and Beyond:** The evolution of conversational AI. AI Models Journal, 8(3), pp. 27-34.
nal, 8(3), pp. 27-34.

<h1>3.Methodology </h1>

## 3.1 Hardware and Software Requirements 
**Hardware:**  
• Minimum 4GB RAM.  
• Multi-core processor (Intel i3 or equivalent).  
• Local deployment support via standard desktop/laptop.   
• Cloud-based hosting for scalability (e.g., AWS, Google Cloud, or Microsoft Azure).  

**Software:**   
• Backend: Python, FastAPI/Flask.  
• Frontend: React/React Native.      
• Database & Hosting: Firebase.     
• Deployment & Scaling: Docker.  
• AI Processing: Integration with Groq's inference engine for LLM-based responses.   
• Third-party Integrations: API connectors for third-party service integration.  

## 3.2 System Design 
The system will follow a modular design that supports both cloud deployment. Here’s an 
overview of the architecture: 

**Retrieval Augmented Generation (RAG) Architecture:**
<h1 align="center">  
  <img src="https://github.com/GauravPatil1444/Projects/blob/master/RAG%20Architecture.png?raw=true" width="fit-content">
</h1>
 
**Organizational Website Search Tool (OWST) Architecture:**
<h1 align="center">  
  <img src="https://github.com/GauravPatil1444/Projects/blob/master/OWST%20Architecture.png?raw=true" width="fit-content">
</h1>

**1. User Interface (Web, Mobile, Desktop):** 
o Interface to create and configure the chatbot, manage knowledge sources, and 
deploy the bot. 

**2. Backend System (FastAPI):**
o Manages interactions between the UI, the AI processing layer, and external 
systems. 

**3. AI Engine (Groq Inference):** 
o Responsible for processing user queries and providing responses using pre
configured LLMs. 

**4. Database (Firebase-Firestore):**
o Stores user-defined configurations, chatbot data, knowledge bases, and 
interaction logs. 

**5. API Integration:** 
o Allows external services to connect with ORCA-powered chatbots via REST 
APIs.

**6. Containerization (Docker):** 
o Ensures easy deployment and scaling in both cloud and on-premise 
environments. 

## 3.3 Algorithm 
Cosine-Similarity Retrieval Algorithm: This algorithm measures the similarity between a 
query and a set of possible responses by calculating the cosine of the angle between their 
vector representations. By utilizing embeddings from pre-trained language models, the 
system can rank responses based on relevance, improving the chatbot's contextual 
understanding. 

**• Step 1:** Extract the text embeddings of the user query and possible response 
candidates. 

**• Step 2:** Compute the cosine similarity between the query embedding and each 
response embedding. 

**• Step 3:** Select the response with the highest similarity score as the chatbot’s answer.

<h1> 4. Implementation Details </h1>

## 4.1 Backend Development

**Current Status: API Testing Phase**

We have started building the backend services, focusing on designing and implementing API endpoints that will handle chatbot interactions and database operations.

**Implementation Details**

Frameworks & Technologies: Python, Langchain, FastAPI, Groq LLM Integration, Datastax AstraDB

**Modules Implemented:**

• API Gateway to route services.  
• Dual-Agent implementation for handling out-of-context queries.  
• Chatbot interaction handling (query processing & response retrieval).  
• Datastax AstraDB operations i.e. Creation, Updation, Retrieval.  

**API Testing:**
<h1 align="center">  
  <img src="https://github.com/GauravPatil1444/Projects/blob/master/OWST%20Architecture.png?raw=true" width="fit-content">
</h1>

## 4.2 Frontend Development

**Current Status: UI Testing and Improvements**

We have started building the frontend for ORCA, focusing on a smooth user experience and interactive design elements.

**Implementation Details**

Frameworks & Technologies: React Native.

**Modules Implemented:**

• Animated splash screen for enhanced user experience.  
• Chat interface designed for seamless interaction with the backend chatbot system.  
• Integration of API calls to connect with backend services.  
• Testing UI elements across different screen sizes and devices.  

**Splash Screen:**
<h1 align="center">  
  <img src="https://github.com/GauravPatil1444/Projects/blob/master/Splash%20Screen.jpg?raw=true" width="340" height="640">
</h1>

**Chat Screen:**
<h1 align="center">  
  <img src="https://github.com/GauravPatil1444/Projects/blob/master/Chat%20Screen.jpg?raw=true" width="340" height="640">
</h1>
