# ResearchMind - Multi-Agent AI Research System

A sophisticated multi-agent AI system that automates research workflows using Groq's powerful LLMs. The system orchestrates multiple specialized agents to search the web, scrape content, synthesize reports, and provide critical evaluation.

## 🎯 Features

- **🔍 Search Agent**: Scours the web for recent, reliable sources on any topic
- **📄 Reader Agent**: Deep-scrapes selected URLs for rich content extraction
- **✍️ Writer Chain**: Synthesizes evidence into structured research reports
- **🧠 Critic Chain**: Evaluates reports for quality, gaps, and accuracy
- **🎨 Beautiful UI**: Modern Streamlit interface with real-time pipeline visualization

## 🛠️ Tech Stack

- **LLM**: Groq API (llama3-8b-8192)
- **Framework**: LangChain + Streamlit
- **Search**: Tavily API
- **Web Scraping**: BeautifulSoup + Requests

## 📋 Prerequisites

- Python 3.9+
- Groq API Key (get free at https://console.groq.com)
- Tavily API Key (get free at https://tavily.com)

## 🚀 Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/sawaraunakk31/ResearchMind---Multi-Agent-Research.git
cd "ResearchMind---Multi-Agent-Research"
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### 5. Run the App
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 🌐 Deploy on Streamlit Cloud (Free)

### 1. Prerequisites
- GitHub account with your code pushed

### 2. Deploy Steps
1. Go to https://share.streamlit.io/
2. Click **"Sign up with GitHub"** or **"Sign in"**
3. Click **"New app"**
4. Fill in:
   - **GitHub repo**: `sawaraunakk31/ResearchMind---Multi-Agent-Research`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. Click **"Deploy"** (takes 1-2 minutes)

### 3. Add Secrets
1. Once deployed, click ☰ menu → **Settings**
2. Go to **Secrets** tab
3. Add your API keys:
   ```
   GROQ_API_KEY=your_key_here
   TAVILY_API_KEY=your_key_here
   ```
4. Save - app will restart automatically

✅ Your app is now live!

## 📁 Project Structure

```
.
├── app.py              # Streamlit UI and pipeline orchestration
├── agents.py           # LLM agents and chains setup
├── tools.py            # Web search and scraping tools
├── pipeline.py         # Research pipeline execution
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (not in git)
└── .gitignore         # Git ignore file
```

## 🔄 How It Works

1. **User Input**: Enter a research topic
2. **Search Phase**: Search agent finds relevant sources via Tavily
3. **Scraping Phase**: Reader agent extracts detailed content from best URL
4. **Report Writing**: Writer chain synthesizes info into structured report
5. **Critical Review**: Critic chain evaluates quality and identifies gaps
6. **Output**: Complete research report with evaluation

## 📊 Output Components

- **Search Results**: Web search findings with URLs and snippets
- **Scraped Content**: Raw content from selected sources
- **Research Report**: Structured report (Introduction → Key Findings → Conclusion)
- **Critical Evaluation**: Expert assessment of report quality

## ⚙️ Configuration

### Available Models
Edit `agents.py` to change Groq models:
```python
llm = ChatGroq(model = "llama3-8b-8192", temperature=0)
```

Other available Groq models:
- `llama3-70b-8192` (larger, more accurate)
- `mixtral-8x7b-32768` (balanced)
- `gemma-7b-it` (faster)

### Adjust Settings
In `app.py` and `pipeline.py`, you can modify:
- Max search results
- Content scraping length
- Report structure
- Temperature (creativity level)

## 🐛 Troubleshooting

### API Key Errors
- Verify keys are in `.env` file (local) or Secrets (Streamlit Cloud)
- Check keys are not expired or revoked

### Tool Call Errors
- Ensure Groq has access to tool definitions
- Check that tool names match exactly in agents

### Memory/Timeout Issues on Cloud
- Reduce search results if hitting memory limits
- Consider upgrading Streamlit workspace

## 📝 Environment Variables

| Variable | Description | Where to Get |
|----------|-------------|------------|
| `GROQ_API_KEY` | Groq LLM API key | https://console.groq.com |
| `TAVILY_API_KEY` | Web search API key | https://tavily.com |

## 🔐 Security Notes

- **Never commit `.env` file** - it's in `.gitignore`
- Use Streamlit Secrets for cloud deployment
- Keep API keys confidential
- Rotate keys periodically

## 📚 Dependencies

See `requirements.txt` for complete list:
- `langchain>=0.2.0` - LLM orchestration
- `langchain-groq>=0.1.0` - Groq integration
- `streamlit>=1.28.0` - Web UI
- `tavily-python>=0.3.0` - Web search
- `beautifulsoup4>=4.12.0` - Web scraping

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📧 Support

For issues, questions, or suggestions:
- GitHub Issues: https://github.com/sawaraunakk31/ResearchMind---Multi-Agent-Research/issues
- Direct contact available via GitHub profile

---

**Last Updated**: April 2026  
**Status**: Active & Maintained
