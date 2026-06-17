# FitFindr — Starter Kit

This starter kit contains everything you need to begin Project 2.

## What's Included

```
ai201-project2-fitfindr-starter/
├── data/
│   ├── listings.json          # 40 mock secondhand listings
│   └── wardrobe_schema.json   # Wardrobe format + example wardrobe
├── utils/
│   └── data_loader.py         # Helper functions for loading the data
├── planning.md                # Your planning template — fill this out first
└── requirements.txt           # Python dependencies
```

## Setup

**macOS / Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Windows:**
```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

Set your Groq API key in a `.env` file (get a free key at [console.groq.com](https://console.groq.com)):
```
GROQ_API_KEY=your_key_here
```

## The Mock Listings Dataset

`data/listings.json` contains 40 mock secondhand listings across categories (tops, bottoms, outerwear, shoes, accessories) and styles (vintage, y2k, grunge, cottagecore, streetwear, and more).

Each listing has: `id`, `title`, `description`, `category`, `style_tags`, `size`, `condition`, `price`, `colors`, `brand`, and `platform`.

Load it with:
```python
from utils.data_loader import load_listings
listings = load_listings()
```

## The Wardrobe Schema

`data/wardrobe_schema.json` defines the format your agent uses to represent a user's existing wardrobe. It includes:

- `schema`: field definitions for a wardrobe item
- `example_wardrobe`: a sample wardrobe with 10 items you can use for testing
- `empty_wardrobe`: a starting template for a new user

Load an example wardrobe with:
```python
from utils.data_loader import get_example_wardrobe
wardrobe = get_example_wardrobe()
```

## Tool Inventory

Your README submission must document each tool's name, inputs, and return value. **These must exactly match your actual function signatures in `tools.py`.** Your documented interfaces will be checked against your actual function signatures in `tools.py` — if the parameter count or types contradict what's in the code, you may not receive full credit for that tool.

---

## Interaction Walkthrough

<!-- Walk through a complete interaction step by step: natural language query → each tool call (and why) → final fit card.
     Walk through this carefully — it's how graders follow your agent's reasoning without a live demo.
     Use a specific example — do not leave this as a template. -->

**User query:**

I am looking for a 90s track jacket in size M that I can wear during my track practice. Empty wardrobe was selected.

**Step 1 — Tool called:**

- Tool: search_listings
- Input: description = "90s track jacket track practice", size = "M", max_price = None
- Why this tool: This tool is used to find relevant clothing options for the user based on the description they recieved. This filters and sorts for most relevant options.
- Output: A list of dicts with the most relevant clothing items for the user.

**Step 2 — Tool called:**
- Tool: suggest_outfit
- Input: new_item is the most relevant item in the list of dictionarys from tool 1 call, and wardrobe is empty wardrobe since thats what the user selected.
- Why this tool: This tool suggests different outfits for the user based on the new item and their wardrobe, if wardrobe is empty then it will give styling advice.
- Output: This 90s track jacket is a versatile and nostalgic piece that can add a sporty touch to any outfit. To style it, pair it with distressed denim jeans, graphic t-shirts, and sleek sneakers for a casual, streetwear-inspired look that suits a relaxed, everyday vibe. You can also layer it over a hoodie or a simple white tee for a more athletic look, and don't be afraid to experiment with different accessories, such as baseball caps or chunky jewelry, to add a personal touch.

**Step 3 — Tool called:**
- Tool: create_fit_card
- Input: outfit = session["outfit_suggestion"], new_item = session["selected_item"]
- Why this tool: This is the final tool used to create the caption talking about the outfit for social media. 
- Output: Just scored this sick 90s Track Jacket for $45.0 on Poshmark and I'm obsessed with how it adds a sporty touch to my everyday look. Paired it with distressed denim and sleek sneakers for a casual, streetwear vibe that's perfect for running errands or grabbing brunch. The navy and white stripes are giving me major nostalgic feels - highly recommend snagging unique pieces like this to elevate your wardrobe.

**Final output to user:**

Just scored this sick 90s Track Jacket for $45.0 on Poshmark and I'm obsessed with how it adds a sporty touch to my everyday look. Paired it with distressed denim and sleek sneakers for a casual, streetwear vibe that's perfect for running errands or grabbing brunch. The navy and white stripes are giving me major nostalgic feels - highly recommend snagging unique pieces like this to elevate your wardrobe.

---

## Error Handling and Fail Points

<!-- For each tool, describe the specific failure mode and what your agent does in response.
     This maps to the error handling section of the rubric (F5-C1). -->

| Tool | Failure mode | Agent response |
|------|-------------|----------------|
| search_listings | No results match the query | No items found. Then prompt the user to retry |
| suggest_outfit | Wardrobe is empty | Return styling advice to the user for the selected item|
| create_fit_card | Outfit input is missing or incomplete |  ERROR: Outfit suggestion is missing. Try searching for a different item.|

---

## Spec Reflection

<!-- Answer both questions with at least 2–3 sentences each. -->

**One way planning.md helped during implementation:**

The planning.md helped greatly during implementation by giving me a step-by-step guide on how my workflow should be. It also allowed me to stop and truly think about what needs to be done and how the tools need to function. I also really enjoyed having to make the mermaid diagrams since they help me visually see the process.

**One divergence from your spec, and why:**

Originally my spec called for the user to interactively select which listing they wanted and which outfit suggestion they preferreed before generating the fit card. While implementing this was changed because run_agent is called directly and expects an immediate return value, which blocks input. Instead the agent auto-selects the top-ranked result from search_listings and passes the outfit suggestion directly into create_fit_card.

---

## Where to Start

1. **Read `planning.md` and fill it out before writing any code.**
2. Verify the data loads correctly by running `python utils/data_loader.py`.
3. Build and test each tool individually before connecting them through your planning loop.

Your implementation files go in this same directory. There's no required file structure for your agent code — organize it however makes sense for your design.
