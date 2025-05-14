# TenderPilot

TenderPilot is an AI-powered tool that streamlines the tendering process for businesses and procurement professionals. It automatically matches tender requirements to your product list, optimizes pricing for maximum profit, and generates polished tender documents—all with an intuitive chat interface.

---

## ✨ Features

- **AI-Powered Matching:**
  - Instantly matches tender requirements to your available products using smart keyword and specification analysis.
- **Automated Pricing Optimization:**
  - Calculates optimal selling prices based on your desired profit margin.
- **One-Click Tender Document Generation:**
  - Produces professional Excel tender documents, complete with item details, pricing, and profit margin breakdowns.
- **Persistent Database:**
  - Securely stores your product and tender data for easy reuse and future reference.
- **Interactive Chat Interface:**
  - Simple CLI-based chat for entering requirements and generating tenders in seconds.

---

## 🚀 Quick Start

1. **Install Requirements**
   ```sh
   pip install -r requirements.txt
   ```
2. **Initialize the Database**
   ```sh
   python dbgen.py
   ```
3. **Run the Chatbot**
   ```sh
   python ui/chatbot.py
   ```

---

## 📦 Project Structure

```
TenderPilot/
├── dbgen.py                # Database initialization script
├── requirements.txt        # Python dependencies
├── db/                     # SQLite database folder
│   └── items.db            # Main database file
├── data/                   # Output folder for generated tenders
│   └── Tender_Output.xlsx  # Example output file
├── modules/                # Core logic modules
│   ├── loader.py           # Excel/database loader
│   ├── matcher.py          # Item matching logic
│   ├── pricing.py          # Pricing calculations
│   └── generator.py        # Excel file generator
├── ui/
│   └── chatbot.py          # CLI chat interface
└── README.md
```

---

## 🛠️ How It Works

1. **Input Requirements:**
   - Enter your tender requirements and desired profit margin via the chat interface.
2. **AI Matching:**
   - The system finds the best-matching items from your product database.
3. **Pricing Optimization:**
   - Calculates selling prices to maximize your profit.
4. **Tender Generation:**
   - Exports a ready-to-submit Excel tender document to the `data/` folder.

---

## 📋 Example Usage

```
$ python ui/chatbot.py
=== Tender Recommendation System ===
Enter tender requirements (keywords, specs, etc.): security camera motion detector
Enter desired profit margin percentage (e.g., 20): 15
3 items recommended. Generating Excel file...
Tender document saved to data/Tender_Output.xlsx
```

---

## 🤖 Technologies Used
- Python 3.8+
- pandas
- SQLite3
- xlsxwriter

---

## 📞 Support & Contributions
- Issues and pull requests are welcome!
- For questions, contact the maintainer or open an issue on GitHub.

---

## License
This project is licensed under the MIT License.
