# routes/chat.py
from flask import Blueprint, request, jsonify
from utils.llm_util import MultiAgentLLM
from utils.trade_analysis import TradeAnalyzer
from utils.market_analysis import MarketAnalyzer
from utils.hyperliquid import HyperliquidClient

Chat = Blueprint('chat', __name__)
llm = MultiAgentLLM()
trade_analyzer = TradeAnalyzer()
market_analyzer = MarketAnalyzer()
hyperliquid_client = HyperliquidClient()

@Chat.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        if not data or 'query' not in data:
            return jsonify({"error": "Missing query parameter"}), 400

        query = data['query']
        
        # Process the query through multi-agent LLM
        response = llm.process_query(query)
        
        # Analyze if trade-related
        if any(keyword in query.lower() for keyword in ['trade', 'buy', 'sell', 'position']):
            trade_analysis = trade_analyzer.analyze(query, response)
            response['trade_recommendations'] = trade_analysis
            
        # Analyze if market-related
        if any(keyword in query.lower() for keyword in ['market', 'price', 'trend']):
            market_data = market_analyzer.analyze(query)
            response['market_data'] = market_data
            
        return jsonify(response)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500