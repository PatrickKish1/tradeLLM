# tradeLLM

# Trading AI Assistant API Documentation

## Chat Endpoints

### 1. Send Chat Message

**Endpoint:** `POST /api/chat`

#### Example Requests:

a) Basic Market Question:

```json
{
  "message": "What's the current price of (X:BTCUSD)?",
  "threadId": "optional-thread-id-here"
}
```

b) Technical Analysis Request:

```json
{
  "message": "Can you do a technical analysis of (S:AAPL) focusing on support and resistance levels?",
  "threadId": "optional-thread-id-here"
}
```

c) Multi-Asset Comparison:

```json
{
  "message": "Compare the performance of (S:MSFT) and (S:GOOGL) over the last trading day",
  "threadId": "optional-thread-id-here"
}
```

d) Forex Analysis:

```json
{
  "message": "What's your analysis on (C:EURUSD) current market conditions?",
  "threadId": "optional-thread-id-here"
}
```

#### Example Response:

```json
{
  "response": {
    "content": "Based on the current market data for Bitcoin (BTCUSD), the price is trading at $44,250 with a 24-hour change of +2.3%. The volume remains strong at 12,345 BTC...",
    "role": "assistant"
  },
  "marketData": {
    "symbol": "BTCUSD",
    "price": 44250,
    "change": 997.5,
    "volume": 12345,
    "marketType": "crypto"
  },
  "threadId": "123e4567-e89b-12d3-a456-426614174000",
  "timestamp": "2024-01-16T10:30:00Z",
  "requestId": "req_789xyz"
}
```

### 2. Get Chat History

**Endpoint:** `GET /api/chat/history/:threadId`

#### Example Request:

```
GET /api/chat/history/123e4567-e89b-12d3-a456-426614174000
```

#### Example Response:

```json
{
  "history": [
    {
      "role": "user",
      "content": "What's the current price of (X:BTCUSD)?"
    },
    {
      "role": "assistant",
      "content": "Bitcoin is currently trading at $44,250..."
    },
    {
      "role": "user",
      "content": "What's the technical outlook?"
    },
    {
      "role": "assistant",
      "content": "Looking at the technical indicators..."
    }
  ],
  "requestId": "req_789xyz"
}
```

### 3. Clear Chat History

**Endpoint:** `DELETE /api/chat/history/:threadId`

#### Example Request:

```
DELETE /api/chat/history/123e4567-e89b-12d3-a456-426614174000
```

#### Example Response:

```json
{
  "message": "Conversation history cleared",
  "requestId": "req_789xyz"
}
```

## Market Data Endpoints

### 1. Get Current Market Data

**Endpoint:** `GET /api/market/current/:symbol`

#### Example Request:

```
GET /api/market/current/BTCUSD?marketType=crypto
```

#### Example Response:

```json
{
  "data": {
    "ticker": "X:BTCUSD",
    "results": [
      {
        "c": 44250,
        "h": 44500,
        "l": 43800,
        "o": 43900,
        "v": 12345,
        "vw": 44150.25,
        "t": 1673308799999
      }
    ],
    "status": "OK"
  },
  "requestId": "req_789xyz"
}
```

### 2. Get Historical Data

**Endpoint:** `GET /api/market/historical/:symbol`

#### Example Request:

```
GET /api/market/historical/AAPL?marketType=stocks&timeframe=1/day&from=2024-01-01&to=2024-01-15
```

#### Example Response:

```json
{
  "data": {
    "ticker": "AAPL",
    "results": [
      {
        "c": 185.92,
        "h": 186.74,
        "l": 185.19,
        "o": 186.54,
        "v": 55123456,
        "vw": 185.965,
        "t": 1704153600000
      }
      // ... more daily entries
    ],
    "status": "OK"
  },
  "requestId": "req_789xyz"
}
```

### 3. Get Day Data

**Endpoint:** `GET /api/market/day/:symbol/:date`

#### Example Request:

```
GET /api/market/day/EURUSD/2024-01-15?marketType=forex
```

#### Example Response:

```json
{
  "data": {
    "ticker": "C:EURUSD",
    "results": [
      {
        "c": 1.095,
        "h": 1.0975,
        "l": 1.0925,
        "o": 1.0945,
        "v": 123456,
        "vw": 1.0955,
        "t": 1705276799999
      }
    ],
    "status": "OK"
  },
  "requestId": "req_789xyz"
}
```

### 4. Get Grouped Daily Data

**Endpoint:** `GET /api/market/grouped/:marketType/:date`

#### Example Request:

```
GET /api/market/grouped/crypto/2024-01-15
```

#### Example Response:

```json
{
  "data": {
    "queryCount": 687,
    "results": [
      {
        "T": "X:BTCUSD",
        "c": 44250,
        "h": 44500,
        "l": 43800,
        "o": 43900,
        "v": 12345,
        "vw": 44150.25,
        "t": 1705276799999
      }
      // ... more crypto pairs
    ],
    "status": "OK"
  },
  "requestId": "req_789xyz"
}
```

### 5. Search Symbols

**Endpoint:** `GET /api/market/search`

#### Example Request:

```
GET /api/market/search?query=APPLE&marketType=stocks
```

#### Example Response:

```json
{
  "data": {
    "results": [
      {
        "ticker": "AAPL",
        "name": "Apple Inc.",
        "market": "stocks",
        "locale": "us",
        "active": true
      }
      // ... more matching symbols
    ],
    "status": "OK"
  },
  "requestId": "req_789xyz"
}
```

## Symbol Format Guide

When sending messages to the chat endpoint, use the following format for symbols:

- Stocks: `(S:SYMBOL)` - Example: `(S:AAPL)`
- Crypto: `(X:SYMBOL)` - Example: `(X:BTCUSD)`
- Forex: `(C:SYMBOL)` - Example: `(C:EURUSD)`

## Key Features of the LLM Integration:

1. **Context Awareness**: The LLM maintains conversation context within a thread, remembering previous discussions about specific assets.

2. **Market Data Integration**: Automatically fetches and incorporates real-time market data when symbols are mentioned in the format `(X:SYMBOL)`.

3. **Analysis Types**:

   - Technical Analysis: Triggered by keywords like "technical", "chart", "indicator"
   - Fundamental Analysis: Triggered by keywords like "fundamental", "company", "value"
   - Market Sentiment: Triggered by keywords like "sentiment", "feeling", "mood"

4. **Multi-Asset Analysis**: Can analyze multiple assets in a single query when multiple symbols are provided.

5. **Conversation Memory**: Maintains thread-based conversation history for contextual responses.

## Example Complex Queries:

1. **Technical Analysis with Multiple Timeframes**:

```json
{
  "message": "Compare the technical indicators for (S:AAPL) on both daily and weekly timeframes, focusing on RSI and MACD."
}
```

2. **Cross-Market Analysis**:

```json
{
  "message": "How is (X:BTCUSD) performing compared to tech stocks like (S:NVDA) and (S:AMD)? Are there any correlations?"
}
```

3. **Market Sentiment and Technical Analysis**:

```json
{
  "message": "What's the current market sentiment for (S:TSLA), and how does it align with the technical indicators?"
}
```

4. **Portfolio Analysis**:

```json
{
  "message": "Analyze the potential risks and rewards of a portfolio containing (S:MSFT), (X:ETHUSD), and (C:GBPUSD)."
}
```
