# Polymarket Trade Tracker

A free, open-source web tool for analyzing Polymarket trading activities.

## What Can This Tool Do?

**For any Polymarket wallet address, you can:**

- 📊 **View complete trade history** - See all buy/sell records with timestamps, prices, and amounts
- 💰 **Calculate profit & loss** - Know exactly how much you earned or lost (realized + unrealized PnL)
- 🏷️ **Identify Maker/Taker roles** - Determine if you provided liquidity (Maker) or took liquidity (Taker) in each trade
- 📈 **Generate visual charts** - Price charts, position changes, cumulative PnL over time
- 🔗 **Detect on-chain operations** - Track Split, Merge, Redeem, and Convert activities
- 📥 **Export data** - Download trade data as JSON for further analysis

**Supports two query modes:**

1. **Quick Query** - Analyze a single market
2. **Multi-Market Query** - Batch analyze all sub-markets within an event (e.g., election predictions with multiple candidates)

## Features

- **Maker/Taker Analysis**: Uses on-chain transaction receipts to accurately determine your role
- **Multi-Source Detection**: Identifies trade sources (Direct, Neg-Risk, Split, Merge, Transfer, Redeem)
- **Real-time Positions**: Shows current holdings and unrealized gains/losses
- **Multi-language**: English and Chinese interface
- **No Login Required**: Just enter a wallet address and market URL
- **100% Free**: No paid APIs used, all data from public endpoints

## ⚠️ Performance Note

This tool uses **free public RPC endpoints** (polygon-rpc.com) for on-chain data queries. 

- Query speed may be **slow** for wallets with many transactions (e.g., 500 trades could take 5-10 minutes)
- No API keys required, but public RPC has rate limits
- For better performance, you can replace `POLYGON_RPC_URL` in the code with a paid RPC provider (Alchemy, Infura, etc.)

## Screenshots

(Add your screenshots here)

## Installation

### Prerequisites

- Python 3.8+
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/polymarket-trade-tracker.git
cd polymarket-trade-tracker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Set environment variables:
```bash
# Linux/macOS
export ADMIN_PATH='your_custom_admin_path'

# Windows
set ADMIN_PATH=your_custom_admin_path
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and visit: `http://127.0.0.1:5000`

## Usage

### Quick Query (Single Market)

1. Enter the Polymarket market URL
2. Enter the wallet address to analyze
3. Click "Start Analysis"
4. View the generated report with charts and statistics

### Multi-Market Query

1. Enter the Polymarket event URL (with multiple sub-markets)
2. Enter the wallet address
3. Select the sub-markets to analyze
4. Click "Start Analysis"
5. View batch analysis results

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, Tailwind CSS, JavaScript
- **Charts**: Matplotlib
- **Data Sources**: 
  - Polymarket Gamma API
  - Polymarket CLOB API
  - Polygon RPC (for on-chain data)

## API Usage

This tool uses the following public APIs:

- `gamma-api.polymarket.com` - Market data
- `data-api.polymarket.com` - Trading activity
- `clob.polymarket.com` - Order book data
- `polygon-rpc.com` - Blockchain data

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is for informational purposes only. It is not financial advice. Always do your own research before making any trading decisions.

## Acknowledgments

- [Polymarket](https://polymarket.com) for providing the prediction market platform
- [Gnosis Conditional Tokens](https://github.com/gnosis/conditional-tokens-contracts) for the underlying protocol
