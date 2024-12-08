from flask import request
from flask_restful import Resource
from loguru import logger
from utils.llm_util import LLMService

class Chat(Resource):
    def __init__(self):
        """Initialize Chat resource with LLM service."""
        self.llm_service = LLMService()

    def post(self):
        """
        Handle POST requests for chat interactions.
        
        Expected request format:
        {
            "query": "user's question or prompt"
        }
        """
        try:
            data = request.get_json()
            if not data:
                return {"status": "error", "message": "Missing request data"}, 400

            query = data.get("query")
            if not query:
                return {"status": "error", "message": "Missing 'query' field"}, 400

            # Get response from LLM service
            response = self.llm_service.get_response(query)
            
            return {
                "status": "success",
                "response": response
            }, 200
            
        except Exception as e:
            logger.error(f"Error processing chat request: {e}")
            return {
                "status": "error",
                "message": "An error occurred while processing your request"
            }, 500






# from flask_restful import Resource, reqparse
# from typing import Dict, Any, Optional
# from loguru import logger
# from utils.llm_util import MultiAgentLLM
# from utils.trade_analysis import TradeAnalyzer
# from utils.market_analysis import MarketAnalyzer
# from utils.hyperliquid import HyperliquidClient

# class ChatSystem:
#     """
#     Centralized system for handling chat interactions and analysis.
#     """
#     def __init__(self):
#         """Initialize the chat system with required components."""
#         try:
#             self.llm = MultiAgentLLM()
#             self.trade_analyzer = TradeAnalyzer()
#             self.market_analyzer = MarketAnalyzer()
#             self.hyperliquid_client = HyperliquidClient()
            
#             # Define keyword mappings for different analysis types
#             self.trade_keywords = {
#                 'trade', 'buy', 'sell', 'position', 'entry', 'exit',
#                 'long', 'short', 'leverage', 'stop loss', 'take profit'
#             }
            
#             self.market_keywords = {
#                 'market', 'price', 'trend', 'volume', 'volatility',
#                 'resistance', 'support', 'momentum', 'analysis'
#             }
            
#             logger.info("ChatSystem initialized successfully")
#         except Exception as e:
#             logger.error(f"Error initializing ChatSystem: {e}")
#             raise

#     def needs_trade_analysis(self, query: str) -> bool:
#         """Determine if trade analysis is needed based on query content."""
#         return any(keyword in query.lower() for keyword in self.trade_keywords)

#     def needs_market_analysis(self, query: str) -> bool:
#         """Determine if market analysis is needed based on query content."""
#         return any(keyword in query.lower() for keyword in self.market_keywords)

#     def process_query(self, query: str) -> Dict[str, Any]:
#         """
#         Process a query and return comprehensive analysis.
        
#         Args:
#             query: User's input query
            
#         Returns:
#             Dictionary containing response and analysis results
#         """
#         try:
#             # Get base LLM response
#             response = self.llm.process_query(query)
            
#             # Enhance response with market data if needed
#             if self.needs_market_analysis(query):
#                 try:
#                     market_data = self.market_analyzer.analyze(query)
#                     response["market_analysis"] = {
#                         "data": market_data,
#                         "timestamp": self.market_analyzer.get_last_update_time(),
#                         "confidence_score": market_data.get("confidence", 0.0)
#                     }
#                 except Exception as e:
#                     logger.error(f"Market analysis failed: {e}")
#                     response["market_analysis_error"] = str(e)

#             # Add trade recommendations if needed
#             if self.needs_trade_analysis(query):
#                 try:
#                     trade_analysis = self.trade_analyzer.analyze(query, response)
#                     response["trade_analysis"] = {
#                         "recommendations": trade_analysis,
#                         "risk_score": trade_analysis.get("risk_score", 0.0),
#                         "confidence_score": trade_analysis.get("confidence", 0.0)
#                     }
                    
#                     # Add hyperliquid market data if available
#                     try:
#                         market_data = self.hyperliquid_client.get_market_data()
#                         response["trade_analysis"]["market_conditions"] = market_data
#                     except Exception as e:
#                         logger.warning(f"Hyperliquid data fetch failed: {e}")
                        
#                 except Exception as e:
#                     logger.error(f"Trade analysis failed: {e}")
#                     response["trade_analysis_error"] = str(e)

#             # Add metadata to response
#             response["metadata"] = {
#                 "query_type": self._determine_query_type(query),
#                 "analysis_performed": {
#                     "trade_analysis": self.needs_trade_analysis(query),
#                     "market_analysis": self.needs_market_analysis(query)
#                 },
#                 "response_quality_score": self._calculate_quality_score(response)
#             }

#             return response

#         except Exception as e:
#             logger.error(f"Error processing query: {e}")
#             raise

#     def _determine_query_type(self, query: str) -> str:
#         """Determine the primary type of the query."""
#         if self.needs_trade_analysis(query):
#             return "trade"
#         elif self.needs_market_analysis(query):
#             return "market"
#         return "general"

#     def _calculate_quality_score(self, response: Dict[str, Any]) -> float:
#         """Calculate overall quality score for the response."""
#         scores = []
        
#         # Base response confidence
#         if "confidence_score" in response:
#             scores.append(response["confidence_score"])
            
#         # Trade analysis confidence
#         if "trade_analysis" in response and "confidence_score" in response["trade_analysis"]:
#             scores.append(response["trade_analysis"]["confidence_score"])
            
#         # Market analysis confidence
#         if "market_analysis" in response and "confidence_score" in response["market_analysis"]:
#             scores.append(response["market_analysis"]["confidence_score"])
            
#         return round(sum(scores) / len(scores), 2) if scores else 0.5

# class Chat(Resource):
#     """RESTful resource for handling chat interactions."""
    
#     def __init__(self):
#         """Initialize the Chat resource."""
#         self.chat_system = ChatSystem()
#         self.parser = reqparse.RequestParser()
#         self.parser.add_argument(
#             "query",
#             type=str,
#             required=True,
#             help="Query is required"
#         )
        
#     def post(self) -> tuple[Dict[str, Any], int]:
#         """
#         Handle POST requests for chat interactions.
        
#         Returns:
#             Tuple of (response_dict, status_code)
#         """
#         try:
#             args = self.parser.parse_args()
#             query = args["query"]
            
#             # Log incoming request
#             logger.info(f"Processing chat request: {query[:50]}...")
            
#             # Process query and get response
#             response = self.chat_system.process_query(query)
            
#             # Log successful response
#             logger.info("Successfully processed chat request")
            
#             return response, 200
            
#         except Exception as e:
#             # Log error and return
#             logger.error(f"Error in chat endpoint: {str(e)}")
#             return {
#                 "error": "An error occurred while processing your request",
#                 "detail": str(e)
#             }, 500