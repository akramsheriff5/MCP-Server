## Features
Lightweight programs that each expose specific capabilities through the standardized Model Context Protocol


### Weather Server
- **Weather Alerts**: Fetch active weather alerts for a specific US state.
- **Weather Forecast**: Retrieve detailed weather forecasts for a given location.
- **Freshdesk Integration**: Create support tickets in Freshdesk.

### Finance Module
- **Intraday Market Data**: Fetch intraday stock market data using the AlphaVantage API.
- **Technical Analysis**:
  - Calculate moving averages (short and long periods).
  - Compute Relative Strength Index (RSI).
- **Trade Recommendations**: Generate comprehensive trade recommendations based on technical indicators.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/mcp-weather-server.git
   cd mcp-weather-server
   ```

2. Set up a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Navigate to the `finance` module and install its dependencies:
   ```bash
   cd finance
   pip install -r requirements.txt
   ```

## Running the Project

### Weather Server
Run the weather server:
```bash
python main.py
```

### Finance Server
Run the finance server:
```bash
cd finance
python finance_server.py
```

### Weather Demo
Run the weather demo server:
```bash
python weather-demo.py
```