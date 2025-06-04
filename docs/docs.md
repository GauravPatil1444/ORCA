<h1> 1. Introduction </h1>
ORCA is a no-code AI chatbot-building platform designed to enable users to effortlessly create and deploy intelligent question-and-answer chatbots. It leverages Large Language Models (LLMs) along with Groq's high-speed inference engine to ensure seamless performance and efficiency.   

## 1.1 Problem Statement 
Creating AI-driven chatbots typically requires extensive technical knowledge in machine 
learning and natural language processing (NLP). Many businesses and individuals face 
challenges when attempting to develop and deploy intelligent Q&A systems without the 
necessary coding skills. Existing platforms either demand coding expertise or are limited in functionality. The lack of a user-friendly, no-code solution hinders the potential for widespread adoption and usability of AI-powered chatbots. 

## 1.2 Objectives 
The goal of this project is to develop ORCA, a no-code AI chatbot-building platform that 
allows users to effortlessly create, configure, and deploy AI-powered Q&A chatbots without 
requiring programming skills. The specific objectives are: 

1. To create an intuitive, user-friendly platform for building AI chatbots. 
2. To enable real-time, context-aware conversations using large language models (LLMs). 
3. To allow easy integration with external systems via API endpoints. 
4. To provide scalability for hosting multiple chatbot instances. 
5. To support diverse input formats like blogs, websites, PDFs, JSON and images for chatbot training. 

## 1.3 Application 
ORCA can be applied across various domains such as:

**• Customer Support:** Automating responses to frequently asked questions and assisting 
customers with product inquiries. 

**• Education:** Building interactive chatbots that guide students through educational 
content and answer academic questions. 

**• Research:** Creating chatbots to facilitate research by providing users with relevant
information based on a set of documents or queries.

**• Business Automation:** Streamlining business processes by enabling efficient retrieval of essential information through chatbot interactions.

<h1>2. Literature Survey</h1>

<h2>2.1 Background</h2

Over the past few years, chatbots have become increasingly popular for automating interactions, with applications ranging from customer service to healthcare support. These systems traditionally rely on rule-based algorithms or machine learning models, such as Long Short-Term Memory (LSTM) and transformers, to generate responses. However, deploying and managing these models usually requires significant coding expertise.
The shift toward no-code platforms and the integration of Large Language Models (LLMs) like GPT-3/4 has democratized AI. This has made AI chatbots more accessible to users without deep technical knowledge. With platforms like ORCA, users can now leverage sophisticated AI for chatbot creation with a user-friendly interface, boosting both functionality and accessibility.

<h2>2.2 Existing Systems</h2>

**1. Dialogflow by Google (2019):** Provides a cloud-based framework for building conversational agents. Users can train bots with pre-built templates and manage them without coding, but the customization options can be limited.

**2. IBM Watson Assistant (2018):** A popular AI tool for building conversational agents that supports voice input and integrates with various business systems. However, users still need basic programming knowledge for optimal customization.

**3. Rasa (2020):** An open-source conversational AI platform designed for developers who need more control over their chatbots. Although powerful, it requires coding skills and is less suitable for non-technical users.

**4. ChatGPT (2023):** OpenAI's conversational AI model, capable of generating detailed and contextually relevant answers. Though it is a cutting-edge model, it requires developers to integrate it into systems or build apps around it.

<h1>3. Methodology </h1>

## 3.1 Hardware and Software Requirements 
**Hardware:**  
• Minimum 2GB RAM.  
• Minimum 500MB Internal Storage.  
• Multi-core processor.  

**Software:**   
• Backend: Python, FastAPI.  
• Frontend: Minimum Android 7.0.      
• Database & Hosting: DataStax, Firebase.     
• Deployment & Scaling: Docker, Google Cloud Run.  
• AI Processing: Groq LPU.     

## 3.2 System Design 
The system will follow a modular design that supports cloud deployment. Here’s an 
overview of the architecture: 

**Retrieval Augmented Generation (RAG) Architecture:**
<h1 align="center">  
  <img src="https://github.com/GauravPatil1444/Projects/blob/master/RAG%20Architecture.png?raw=true" width="fit-content">
</h1>
 
**Organizational Website Search Tool (OWST) Architecture:**
<h1 align="center">  
  <img src="https://github.com/GauravPatil1444/Projects/blob/master/OWST%20Architecture.png?raw=true" width="fit-content">
</h1>

**1. User Interface (Mobile):** 
Interface to create and configure the chatbot, manage knowledge sources, and 
deploy the bot. 

**2. Backend System (FastAPI):**
Manages interactions between the UI, the AI processing layer, and external 
systems. 

**3. AI Engine (Groq Inference):** 
Responsible for processing user queries and providing responses using pre
configured LLMs. 

**4. Database (DataStax, Firebase-Firestore):**
Stores user-defined configurations, chatbot data, knowledge bases, and 
interaction logs. 

**5. API Integration:** 
Allows external services to connect with ORCA-powered chatbots via REST 
APIs.

**6. Containerization (Docker):** 
Ensures easy deployment and scaling in both cloud and on-premise 
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

**• Step 3:** Select the response with the highest similarity score as the response-context for LLM.

<h1> 4. Implementation Details </h1>  

## 4.1 Frontend Development - Mar 28, 2025 to Apr 15, 2025

<h3>Modules Implemented:</h3> 

<h4>Module 1 - Mar 28, 2025</h4> 

• Animated splash screen implementation - enhance user experience.   
• Chat interface implementatation - seamless interaction with the backend chatbot system.    
• Integration of API calls to connect with backend services.  
• Testing UI elements across different screen sizes and devices.  

<h6>Splash Screen:</h6>

<h1 align="center">  
  <img src="https://github.com/GauravPatil1444/Projects/blob/master/Splash%20Screen.jpg?raw=true" width="340" height="640">
</h1>

<h6>Chat Screen:</h6>
<h1 align="center">  
  <img src="https://github.com/GauravPatil1444/Projects/blob/master/Chat%20Screen.jpg?raw=true" width="340" height="640">
</h1>

<h4>Module 2 - Apr 2, 2025</h4> 

• New screen addition to drawer navigation.     
• Chat interface improvement.      

<h4>Module 3 - Apr 4, 2025</h4> 

• AgentSelector screen implementation - select agent type (Document or URL).       
• File picker implementation - data ingestion for supported file types.  

<h6>AgentSelector Screen:</h6>

<h1 align="center">  
  <img src="https://github.com/GauravPatil1444/Projects/blob/master/Screenshot_2025-04-18-10-58-57-50_15f99a7ff97e9b752efb3734a54866e0.jpg?raw=true" width="340" height="640">
</h1>

<h6>File picker:</h6>
<h1 align="center">  
  <img src="https://github.com/GauravPatil1444/Projects/blob/master/Screenshot_2025-04-18-10-59-09-16_15f99a7ff97e9b752efb3734a54866e0.jpg?raw=true" width="340" height="640">
</h1>

<h4>Module 4 - Apr 5, 2025</h4> 

• File upload implementation - upload file to backend services for processing.  

<h4>Module 5 - Apr 6, 2025</h4> 

• Agent metadata persistence implementation.  

<h4>Module 6 - Apr 8, 2025</h4> 

• Advance pdf tool implementation - configuration settings for data extraction. 
• Update UI and Navigation.  

<h6>Advance pdf tool:</h6>
<h1 align="center">  
  <img src="https://github.com/GauravPatil1444/Projects/blob/master/Screenshot_2025-04-18-10-59-24-49_15f99a7ff97e9b752efb3734a54866e0.jpg?raw=true" width="340" height="640">
</h1>

<h4>Module 7 - Apr 10, 2025</h4> 

• Delete Agent Implementation - delete deployed agents from local as well as cloud environment.  

<h6>Delete Agent:</h6>
<h1 align="center">  
  <img src="https://github.com/GauravPatil1444/Projects/blob/master/Screenshot_2025-04-18-10-59-52-85_15f99a7ff97e9b752efb3734a54866e0.jpg?raw=true" width="340" height="640">
</h1>

<h4>Module 8 - Apr 13, 2025</h4> 

• URL Agent Implementation - website & web page chatbot configuration.  

<h6>URL Agent:</h6>
<h1 align="center">  
  <img src="https://github.com/GauravPatil1444/Projects/blob/master/Screenshot_2025-04-18-11-00-43-74_15f99a7ff97e9b752efb3734a54866e0.jpg?raw=true" width="340" height="640">
</h1>

<h4>Module 9 - Apr 14, 2025</h4> 

• Update UI.  

<h4>Module 10 - Apr 15, 2025</h4> 

• Beta release v1.0.0 - Performance & Bug testing in production environment.  

## 4.2 Backend Development - Mar 19, 2025 to Apr 17, 2025

<h3>Modules Implemented:</h3>  

<h4>Module 1 - Mar 19, 2025</h4> 

• API Gateway to route services.    
• Datastax AstraDB operations i.e. Creation, Updation, Retrieval.     
<h6>API Testing:</h6>
<h1 align="center">  
  <img src="https://github.com/GauravPatil1444/Projects/blob/master/API%20Testing.png?raw=true" width="fit-content">
</h1> 
  
<h4>Module 2 - Mar 20, 2025</h4> 

• Dual-Agent implementation for handling out-of-context queries.    
• Chatbot interaction handling (query processing & response retrieval).   

<h4>Module 3 - Apr 5, 2025</h4> 

• PDF tool implementation.   
• Updated other services with respect to pdf tool.   

<h4>Module 4 - Apr 8, 2025</h4> 

• Advance PDF tool implementation.   
• Client prompt implementation.   
• Updated other services with respect to Advance pdf tool.   

<h4>Module 5 - Apr 10, 2025</h4> 

• Delete Agent implementation.    

<h4>Module 6 - Apr 13, 2025</h4> 

• OWST implementation.  
• JSON_CSV tool implementation.  
• PDF_WEB tool implementation.  

<h4>Module 7 - Apr 17, 2025</h4> 

• Beta release v1.0.0 - Performance & Bug testing in production environment.   

## 4.3 DevOps

<h3>Modules Implemented:</h3>  

<h4>Module 1 - Apr 15, 2025</h4>  

• Containerization - dockerized backend services (v1.0.0-beta).     
• Deployment - deployed to google cloud run (v1.0.0-beta).   

<h6>Containerization:</h6>
<h1 align="center">  
  <img src="https://github.com/GauravPatil1444/Projects/blob/master/Screenshot%202025-04-18%20105526.png?raw=true" width="fit-content">
</h1>

<h6>Deployment:</h6>
<h1 align="center">  
  <img src="https://github.com/GauravPatil1444/Projects/blob/master/Screenshot%202025-04-18%20105719.png?raw=true" width="fit-content">
</h1>

<h1> Conclusion </h1>   
ORCA Beta v1.0.0 underwent extensive testing across multiple real-world use cases to evaluate its performance, adaptability, and user experience. The testing phase focused on diverse applications including e-commerce, general website assistance, legal help, and academic knowledge support.
E-commerce Chatbot: Delivered fast, relevant responses for product queries, improving customer engagement.
Website Chatbot: Handled real-time user queries, navigation support, and general assistance effectively on dynamic websites.
Legal Assistance: Accurately interpreted legal documents and provided clear answers to legal questions, showing strong domain understanding.
Academic Books: Served as a reliable virtual tutor, answering subject-specific queries based on academic content with clarity and precision. 




