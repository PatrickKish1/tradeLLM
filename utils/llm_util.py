import os
from groq import Groq
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

class LLMService:
    def __init__(self):
        """Initialize the LLM service with Groq client."""
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")
            
        self.client = Groq(api_key=self.api_key)
        self.model = os.getenv("MODEL", "mixtral-8x7b-32768")  # Default model if not specified
        
    def get_response(self, query: str) -> str:
        """
        Get response from Groq API for the given query.
        
        Args:
            query: User's input query
            
        Returns:
            Response from the LLM
        """
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful AI assistant. Provide clear, accurate, and informative responses."
                    },
                    {
                        "role": "user",
                        "content": query
                    }
                ],
                model=self.model
            )
            return chat_completion.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error getting LLM response: {e}")
            raise














# import os
# import json
# import time
# import requests
# import openai
# import copy
# from typing import Dict, List, Optional
# from dotenv import load_dotenv
# from groq import Groq
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# from loguru import logger

# # Load environment variables
# load_dotenv()

# # Debug configuration
# DEBUG = int(os.environ.get("DEBUG", "0"))

# class MultiAgentLLM:
#     def __init__(self):
#         """Initialize the MultiAgentLLM system with API keys and model configurations."""
#         api_key = os.getenv('GROQ_API_KEY')
#         if not api_key:
#             raise ValueError("GROQ_API_KEY environment variable is not set")
            
#         self.client = Groq(
#             api_key=api_key,
#             base_url="https://api.groq.com/openai/v1"  # Updated base URL
#         )
        
#         # Enhanced model selection with specialized roles
#         self.models = {
#             'analyst': 'mixtral-8x7b-32768',     # Market analysis
#             'trader': 'llama2-70b-4096',         # Trade execution
#             'researcher': 'mixtral-8x7b-32768',  # Deep research
#             'synthesizer': 'llama2-70b-4096'     # Response synthesis
#         }
        
#         # Knowledge mapping for intelligent agent selection
#         self.agent_keywords = {
#             'analyst': ['market', 'trend', 'analysis', 'overview', 'macro', 'performance'],
#             'trader': ['trade', 'buy', 'sell', 'position', 'entry', 'exit', 'strategy'],
#             'researcher': ['research', 'information', 'background', 'history', 'details', 'context']
#         }

# def generate_together(
#     model: str,
#     messages: List[Dict[str, str]],
#     max_tokens: int = 2048,
#     temperature: float = 0.7,
#     streaming: bool = False,
# ) -> Optional[str]:
#     """
#     Generate responses using the Groq API with retry mechanism.
    
#     Args:
#         model: The model identifier to use
#         messages: List of message dictionaries with role and content
#         max_tokens: Maximum number of tokens in the response
#         temperature: Temperature parameter for response generation
#         streaming: Whether to use streaming mode
    
#     Returns:
#         Generated text response or None if failed
#     """
#     output = None
#     for sleep_time in [1, 2, 4, 8, 16, 32]:
#         try:
#             endpoint = "https://api.groq.com/openai/v1/chat/completions"
            
#             if DEBUG:
#                 logger.debug(
#                     f"Sending messages ({len(messages)}) (last message: {messages[-1]['content'][:20]}...) to {model}."
#                 )
            
#             res = requests.post(
#                 endpoint,
#                 json={
#                     "model": model,
#                     "max_tokens": max_tokens,
#                     "temperature": (temperature if temperature > 1e-4 else 0),
#                     "messages": messages,
#                 },
#                 headers={
#                     "Authorization": f"Bearer {os.environ.get('GROQ_API_KEY')}",
#                 },
#             )
            
#             if "error" in res.json():
#                 logger.error(res.json())
#                 if res.json()["error"]["type"] == "invalid_request_error":
#                     logger.info("Input + output is longer than max_position_id.")
#                     return None
            
#             output = res.json()["choices"][0]["message"]["content"]
#             break
            
#         except Exception as e:
#             logger.error(e)
#             if DEBUG:
#                 logger.debug(f"Msgs: {messages}")
            
#             logger.info(f"Retry in {sleep_time}s..")
#             time.sleep(sleep_time)
    
#     if output is None:
#         return output
    
#     output = output.strip()
#     if DEBUG:
#         logger.debug(f"Output: {output[:20]}....")
    
#     return output

# def generate_together_stream(
#     model: str,
#     messages: List[Dict[str, str]],
#     max_tokens: int = 2048,
#     temperature: float = 0.7,
# ) -> openai.Stream:
#     """
#     Generate streaming responses using the Groq API.
    
#     Args:
#         model: The model identifier to use
#         messages: List of message dictionaries with role and content
#         max_tokens: Maximum number of tokens in the response
#         temperature: Temperature parameter for response generation
    
#     Returns:
#         Streaming response object
#     """
#     endpoint = "https://api.groq.com/openai/v1"
#     client = openai.OpenAI(
#         api_key=os.environ.get("GROQ_API_KEY"),
#         base_url=endpoint
#     )
    
#     response = client.chat.completions.create(
#         model=model,
#         messages=messages,
#         temperature=temperature if temperature > 1e-4 else 0,
#         max_tokens=max_tokens,
#         stream=True,
#     )
    
#     return response

# def generate_openai(
#     model: str,
#     messages: List[Dict[str, str]],
#     max_tokens: int = 2048,
#     temperature: float = 0.7,
# ) -> str:
#     """
#     Generate responses using the OpenAI API with retry mechanism.
    
#     Args:
#         model: The model identifier to use
#         messages: List of message dictionaries with role and content
#         max_tokens: Maximum number of tokens in the response
#         temperature: Temperature parameter for response generation
    
#     Returns:
#         Generated text response
#     """
#     client = openai.OpenAI(
#         api_key=os.environ.get("OPENAI_API_KEY"),
#     )
    
#     output = None
#     for sleep_time in [1, 2, 4, 8, 16, 32]:
#         try:
#             if DEBUG:
#                 logger.debug(
#                     f"Sending messages ({len(messages)}) (last message: {messages[-1]['content'][:20]}) to {model}."
#                 )
            
#             completion = client.chat.completions.create(
#                 model=model,
#                 messages=messages,
#                 temperature=temperature,
#                 max_tokens=max_tokens,
#             )
#             output = completion.choices[0].message.content
#             break
            
#         except Exception as e:
#             logger.error(e)
#             logger.info(f"Retry in {sleep_time}s..")
#             time.sleep(sleep_time)
    
#     return output.strip()

# def inject_references_to_messages(
#     messages: List[Dict[str, str]],
#     references: List[str],
# ) -> List[Dict[str, str]]:
#     """
#     Inject reference responses into the system message.
    
#     Args:
#         messages: Original list of message dictionaries
#         references: List of reference responses to inject
    
#     Returns:
#         Updated list of messages with injected references
#     """
#     messages = copy.deepcopy(messages)
#     system = """You have been provided with a set of responses from various open-source models to the latest user query. 
#     Your task is to synthesize these responses into a single, high-quality response. It is crucial to critically evaluate 
#     the information provided in these responses, recognizing that some of it may be biased or incorrect. Your response 
#     should not simply replicate the given answers but should offer a refined, accurate, and comprehensive reply to the 
#     instruction. Ensure your response is well-structured, coherent, and adheres to the highest standards of accuracy 
#     and reliability.

#     Responses from models:"""
    
#     for i, reference in enumerate(references):
#         system += f"\n{i+1}. {reference}"
    
#     if messages[0]["role"] == "system":
#         messages[0]["content"] += "\n\n" + system
#     else:
#         messages = [{"role": "system", "content": system}] + messages
    
#     return messages

# def generate_with_references(
#     model: str,
#     messages: List[Dict[str, str]],
#     references: List[str] = [],
#     max_tokens: int = 2048,
#     temperature: float = 0.7,
#     generate_fn: callable = generate_together,
# ) -> Optional[str]:
#     """
#     Generate a response with reference responses injected into the prompt.
    
#     Args:
#         model: The model identifier to use
#         messages: List of message dictionaries with role and content
#         references: List of reference responses to consider
#         max_tokens: Maximum number of tokens in the response
#         temperature: Temperature parameter for response generation
#         generate_fn: Function to use for generation (default: generate_together)
    
#     Returns:
#         Generated text response or None if failed
#     """
#     if len(references) > 0:
#         messages = inject_references_to_messages(messages, references)
    
#     return generate_fn(
#         model=model,
#         messages=messages,
#         temperature=temperature,
#         max_tokens=max_tokens,
#     )

# # Complete the MultiAgentLLM class methods
# def process_query(self, query: str) -> Dict:
#     """Process a query using multiple specialized agents."""
#     active_agents = self._select_agents(query)
#     responses = {}
    
#     # Parallel processing of relevant agents
#     for agent_name in active_agents:
#         try:
#             response = self._get_completion(query, agent_name)
#             responses[agent_name] = response
#         except Exception as e:
#             logger.error(f"Error processing query with {agent_name}: {e}")
    
#     # Advanced response synthesis
#     return self._synthesize_responses(query, responses)

# def _select_agents(self, query: str) -> List[str]:
#     """Select appropriate agents based on query content."""
#     query_lower = query.lower()
#     selected_agents = set()
    
#     # Score-based agent selection
#     for agent, keywords in self.agent_keywords.items():
#         if any(keyword in query_lower for keyword in keywords):
#             selected_agents.add(agent)
    
#     # Fallback mechanism
#     if not selected_agents:
#         selected_agents.add('analyst')
    
#     return list(selected_agents)

# def _get_completion(self, query: str, agent_name: str) -> str:
#     """Get completion from a specific agent."""
#     system_prompts = {
#         'analyst': "You are an expert market analyst providing comprehensive insights. Analyze the query with data-driven perspectives.",
#         'trader': "You are a professional quantitative trader. Provide strategic trading insights and risk-aware recommendations.",
#         'researcher': "You are a meticulous market researcher. Investigate the query thoroughly, providing deep contextual information."
#     }
    
#     try:
#         completion = self.client.chat.completions.create(
#             model=self.models[agent_name],
#             messages=[
#                 {"role": "system", "content": system_prompts[agent_name]},
#                 {"role": "user", "content": query}
#             ],
#             temperature=0.7,
#             max_tokens=2000
#         )
#         return completion.choices[0].message.content
#     except Exception as e:
#         logger.error(f"Error getting completion for {agent_name}: {e}")
#         return ""

# def _synthesize_responses(self, query: str, responses: Dict[str, str]) -> Dict:
#     """Synthesize multiple agent responses into a coherent output."""
#     synthesized_response = {
#         "summary": "",
#         "detailed_responses": responses,
#         "confidence_score": 0.0,
#         "relevance_scores": {}
#     }
    
#     # Compute relevance scores
#     for agent, response in responses.items():
#         relevance_score = self._calculate_relevance(query, response)
#         synthesized_response['relevance_scores'][agent] = relevance_score
    
#     # Sort responses by relevance
#     sorted_responses = sorted(
#         responses.items(),
#         key=lambda x: synthesized_response['relevance_scores'][x[0]],
#         reverse=True
#     )
    
#     # Synthesize comprehensive summary
#     summary_prompt = "Synthesize the following responses into a concise, coherent summary:\n\n" + \
#                      "\n\n".join([f"{agent}: {response}" for agent, response in sorted_responses])
    
#     try:
#         summary_completion = self.client.chat.completions.create(
#             model=self.models['synthesizer'],
#             messages=[
#                 {"role": "system", "content": "Create a precise, informative summary that captures key insights."},
#                 {"role": "user", "content": summary_prompt}
#             ],
#             temperature=0.5,
#             max_tokens=300
#         )
#         synthesized_response["summary"] = summary_completion.choices[0].message.content
#     except Exception as e:
#         logger.error(f"Error generating summary: {e}")
    
#     # Confidence calculation based on response agreement and relevance
#     synthesized_response["confidence_score"] = self._calculate_confidence(synthesized_response)
    
#     return synthesized_response

# def _calculate_relevance(self, query: str, response: str) -> float:
#     """Calculate relevance score between query and response."""
#     vectorizer = TfidfVectorizer()
    
#     try:
#         tfidf_matrix = vectorizer.fit_transform([query, response])
#         cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
#         return cosine_sim
#     except Exception as e:
#         logger.error(f"Relevance calculation error: {e}")
#         return 0.5

# def _calculate_confidence(self, synthesized_response: Dict) -> float:
#     """Calculate confidence score based on response agreement and relevance."""
#     relevance_scores = list(synthesized_response['relevance_scores'].values())
    
#     if not relevance_scores:
#         return 0.5
    
#     avg_relevance = sum(relevance_scores) / len(relevance_scores)
#     confidence = min(max(avg_relevance * 1.2, 0.3), 0.95)
#     return round(confidence, 2)

# MultiAgentLLM.process_query = process_query
# MultiAgentLLM._select_agents = _select_agents
# MultiAgentLLM._get_completion = _get_completion
# MultiAgentLLM._synthesize_responses = _synthesize_responses
# MultiAgentLLM._calculate_relevance = _calculate_relevance
# MultiAgentLLM._calculate_confidence = _calculate_confidence