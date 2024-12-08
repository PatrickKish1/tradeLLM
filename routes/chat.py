from flask_restful import Resource, reqparse
from utils.llm_util import MultiAgentLLM
from utils.trade_analysis import TradeAnalyzer
from utils.market_analysis import MarketAnalyzer
from utils.hyperliquid import HyperliquidClient

# Initialize your utils
llm = MultiAgentLLM()
trade_analyzer = TradeAnalyzer()
market_analyzer = MarketAnalyzer()
hyperliquid_client = HyperliquidClient()


# Define a RESTful resource
class Chat(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument(
                "query", type=str, required=True, help="Query is required"
            )
            args = parser.parse_args()

            query = args["query"]
            response = llm.process_query(query)

            # Trade-related analysis
            if any(
                keyword in query.lower()
                for keyword in ["trade", "buy", "sell", "position"]
            ):
                trade_analysis = trade_analyzer.analyze(query, response)
                response["trade_recommendations"] = trade_analysis

            # Market-related analysis
            if any(
                keyword in query.lower() for keyword in ["market", "price", "trend"]
            ):
                market_data = market_analyzer.analyze(query)
                response["market_data"] = market_data

            return response, 200
        except Exception as e:
            return {"error": str(e)}, 500
