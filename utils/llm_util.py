from typing import Dict, List, Optional
import os
from dotenv import load_dotenv
from groq import Groq

def MultiAgentLLM():
    def __init__(self):
        load_dotenv()
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")
            
        self.client = Groq(
            api_key=api_key,
            base_url="https://api.groq.com/v1"
        )
        self.models = {
            'analyst': 'mixtral-8x7b-32768',  # For market analysis
            'trader': 'llama2-70b-4096',      # For trade execution
            'researcher': 'mixtral-8x7b-32768' # For deep research
        }
        
    def process_query(self, query: str) -> Dict:
        responses = {}
        
        # Determine which agents should process the query
        active_agents = self._select_agents(query)
        
        # Process through each relevant agent
        for agent_name in active_agents:
            response = self._get_completion(query, agent_name)
            responses[agent_name] = response
            
        return self._synthesize_responses(responses)
    
    def _select_agents(self, query: str) -> List[str]:
        # Simple keyword-based agent selection
        agents = []
        if any(word in query.lower() for word in ['market', 'trend', 'analysis']):
            agents.append('analyst')
        if any(word in query.lower() for word in ['trade', 'buy', 'sell']):
            agents.append('trader')
        if any(word in query.lower() for word in ['research', 'information', 'background']):
            agents.append('researcher')
        
        # Default to analyst if no specific agent is selected
        return agents if agents else ['analyst']
    
    def _get_completion(self, query: str, agent_name: str) -> str:
        # Prepare the prompt based on agent role
        prompts = {
            'analyst': "As a market analyst, analyze the following query: ",
            'trader': "As a professional trader, provide trading advice for: ",
            'researcher': "As a market researcher, investigate the following: "
        }
        
        full_prompt = f"{prompts[agent_name]}{query}"
        
        completion = self.client.chat.completions.create(
            model=self.models[agent_name],
            messages=[
                {"role": "system", "content": "You are a professional trading assistant."},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        return completion.choices[0].message.content
    
    def _synthesize_responses(self, responses: Dict[str, str]) -> Dict:
        # Combine responses from multiple agents into a coherent output
        synthesized = {
            "summary": "",
            "detailed_responses": responses,
            "confidence_score": 0.0
        }
        
        # Create a summary from all responses
        all_responses = " ".join(responses.values())
        summary_prompt = f"Synthesize this information into a brief summary: {all_responses}"
        
        summary_completion = self.client.chat.completions.create(
            model=self.models['analyst'],
            messages=[
                {"role": "system", "content": "Create a brief summary of the following analysis."},
                {"role": "user", "content": summary_prompt}
            ],
            temperature=0.5,
            max_tokens=200
        )
        
        synthesized["summary"] = summary_completion.choices[0].message.content
        
        # Calculate confidence score based on agreement between agents
        if len(responses) > 1:
            # Simple agreement metric
            synthesized["confidence_score"] = self._calculate_confidence(responses)
        else:
            synthesized["confidence_score"] = 0.8  # Default for single agent
            
        return synthesized
    
    def _calculate_confidence(self, responses: Dict[str, str]) -> float:
        # Simplified confidence calculation
        # Could be enhanced with more sophisticated NLP comparison
        return 0.85  # Placeholder for demonstration