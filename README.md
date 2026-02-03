## Channel3 Take Home Assignment
Hi Channel3 Team, this is Michael Moran and this is my writeup on the take-home assignment for the Backend dev role. I also did the Frontend code and writeup as a bonus for fun, feel free to ignore those if you desire

First things first:
### How to Run

**Backend (Extract products from HTML):**
```powershell
cd take-home-2026-moran-main
pip install python-dotenv openai pydantic beautifulsoup4
python extract.py
```

**Frontend (View product catalog):**
```powershell
cd frontend
npm install
npm run dev
```
Then open http://localhost:5173 in your browser.

**Run both together:**
```powershell
# Terminal 1 - Backend
python extract.py

# Terminal 2 - Frontend
cd frontend && npm run dev
```
Hopefully this is working for you! Let's get into the system design:

The core of designing any scalable system is understanding what the tradeoffs you make will mean as the workload increases in orders of magnitude. For this project and Channel3's mission generally of indexing the internet, the key thing to understand is cost per token and number of tokens used. In this project those are the primary considerations to consider for both the amount of money and time consumed. In order to get both the time and money consumed to a minimum, this project takes a few crucial steps that will work at scale:
1. A preprocessing step that reduces token usage in the extract step by 98% but may lose small amounts of product data, such as extra images in the cotton pants. This would mean $519K ? $11K at 50M scale
2. Utilizing the cheapest and fastest LLM model we have access to alongside a prompt that uses specific examples to work as quickly as possible on the most common html layouts
3. A fuzzy match catching step that doesn't use an LLM on html that doesn't quite fit what we are looking for, instead of rechecking with an LLM

All of these steps are taken with a primary goal in mind: how do we take this same logic from 5 to 50 million without costing too much time or money? The preprocessing is the most crucial by far as it saw a 98%(!) reduction in used tokens at the extract step by using BeautifulSoup to shave down what the LLM needs to process. Using a super cheap model is good here but we could probably push it down even more with a local model depending on the hardware available

Of course some of the assumptions made in this project will not hold as you scale:
1. The clearest one is storing the data as JSON in a folder inside the code. In a production setting you would use PostgreSQL alongside a cache like Redis to both store and serve the data for both the extractor and frontend better.
2. The extraction uses asyncio, but single-process concurrency has limits. At scale, you'd add
a job queue (Redis/RabbitMQ) with multiple worker processes, each running async extractions
with semaphores for API rate limits. Database writes would be batched to reduce I/O overhead.


### Optional Frontend System Design

When thinking about what API to provide for agentic shopping apps, the key insight is that AI agents need structured data they can reason about:
1. A semantic search endpoint where agents can search not based on exact or fuzzy match but rather based on a more ambiguous meaning
2. A product details endpoint that returns the full structured object we extract here.Potentially with a guide for the agent to know what to look for
3. A price history endpoint so agents can say "this is 20% below average" and comparisons to products in the same or similar category

For developer tools, the goal is making this data easy to build on. Nobody wants to parse JSON by hand or guess at field names:
1. Python and JavaScript SDKs with typed responses so devs get autocomplete and catch errors before runtime
2. Webhooks for "price dropped" or "back in stock" events instead of forcing developers to poll constantly
3. A sandbox environment for testing without rate limits so you can iterate fast without worrying about hitting quotas

The theme here is the same as the backend: give developers the building blocks without making them do the hard work themselves.
