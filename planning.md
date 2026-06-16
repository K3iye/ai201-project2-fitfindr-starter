# FitFindr — planning.md

> Complete this document before writing any implementation code.
> Your spec and agent diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Your planning.md will be reviewed as part of your submission.
> Update it before starting any stretch features.

---

## Tools

List every tool your agent will use. For each tool, fill in all four fields.
You must have at least 3 tools. The three required tools are listed — add any additional tools below them.

### Tool 1: search_listings

**What it does:**
<!-- Describe what this tool does in 1–2 sentences -->

This searches using keywords to find items that match the parameters used. It returns a dictionary of the relevant items with all their information like id, title, description, category, and more.

**Input parameters:**
<!-- List each parameter, its type, and what it represents -->

- `description` (str): category of clothing
- `size` (str): Optional input, represents size of the clothing 
- `max_price` (float): Optional input, represents inclusive max price of the clothing item

**What it returns:**
<!-- Describe the return value — what fields does a result contain? -->

Returns a list of dicts that are sorted by relevance, where most relevant is the first item. Each of these dicts contain all the fields that are listed in listing.json, such as (id, title, description , category, etc.)

**What happens if it fails or returns nothing:**
<!-- What should the agent do if no listings match? -->

It should return an empty list and tell the user that no clothing can be found with the search results used. This should then prompt the user to search again using something else.

---

### Tool 2: suggest_outfit

**What it does:**
<!-- Describe what this tool does in 1–2 sentences -->

This tool looks at any new thrifted clothing items the user has purchased and compares it with their wardrobe. It then suggests 1-2 outfits for the user that has this new clothing item included in it. If the wardrobe is empty it instead suggests styling advice.

**Input parameters:**
<!-- List each parameter, its type, and what it represents -->

- `new_item` (dict): Contains the information on the item the user wants to purchase next
- `wardrobe` (dict): a dict with an items key that has a list of item dicts.

**What it returns:**
<!-- Describe the return value -->

Returns a string with outfit suggestions using the new item and the wardrobe, if the wardrobe is empty it instead returns styling advice using the new item.

**What happens if it fails or returns nothing:**
<!-- What should the agent do if the wardrobe is empty or no outfit can be suggested? -->

It  should return a string that gives styling advice for the new item that the user wants to purchase.

---

### Tool 3: create_fit_card

**What it does:**
<!-- Describe what this tool does in 1–2 sentences -->

This tool should take the outfit that was suggested from the suggest_outfit function and the new item the user purchased, to then create a 2-4 sentence social media caption for the user to post.

**Input parameters:**
<!-- List each parameter, its type, and what it represents -->

- `outfit` (str):  One of the outfits suggested from suggest_outfit function
- `new_item` (dict):  The new thrifted item that the user purchased 

**What it returns:**
<!-- Describe the return value -->

Returns a 2-4 sentence message that the user can put on a social media caption for their new outfit that was made using the new thrifted item. 

**What happens if it fails or returns nothing:**
<!-- What should the agent do if the outfit data is incomplete? -->

If the outfit data is incomplete the agent should return a message to the user that states what is missing.

---

### Additional Tools (if any)

<!-- Copy the block above for any tools beyond the required three -->

---

## Planning Loop

**How does your agent decide which tool to call next?**
<!-- Describe the logic your planning loop uses. What does it look at? What conditions change its behavior? How does it know when it's done? -->



---

## State Management

**How does information from one tool get passed to the next?**
<!-- Describe how your agent stores and accesses state within a session. What data is tracked? How is it passed between tool calls? -->

---

## Error Handling

For each tool, describe the specific failure mode you're handling and what the agent does in response.

| Tool | Failure mode | Agent response |
|------|-------------|----------------|
| search_listings | No results match the query | |
| suggest_outfit | Wardrobe is empty | |
| create_fit_card | Outfit input is missing or incomplete | |

---

## Architecture

<!-- Draw a diagram of your agent showing how the components connect:
     User input → Planning Loop → Tools (search_listings, suggest_outfit, create_fit_card)
                                                                          ↕
                                                                   State / Session
     Show what triggers each tool, how state flows between them, and where error paths branch off.
     Use ASCII art or a Mermaid diagram (https://mermaid.js.org/syntax/flowchart.html).
     Do NOT embed an image — graders need to read your diagram directly in the file;
     an embedded image or screenshot cannot be evaluated.
     You'll share this diagram with an AI tool when asking it to implement
     the planning loop and each individual tool. -->

---

## AI Tool Plan

<!-- For each part of the implementation below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, your agent diagram)
     - What you expect it to produce
     - How you'll verify the output matches your spec before moving on

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Tool 1 spec (inputs, return value, failure mode) and ask it to implement
     search_listings() using load_listings() from the data loader — then test it against 3 queries
     before trusting it" is a plan. -->

**Milestone 3 — Individual tool implementations:**

**Milestone 4 — Planning loop and state management:**

---

## A Complete Interaction (Step by Step)

Write out what a full user interaction looks like from start to finish — tool call by tool call. Use a specific example query.

**Example user query:** "I'm looking for a vintage graphic tee under $30. I mostly wear baggy jeans and chunky sneakers. What's out there and how would I style it?"

**Step 1:**
<!-- What does the agent do first? Which tool is called? With what input? -->

The agent should first use the search_listing function based on the users query. This is to find relevant clothing options for the user.

**Step 2:**
<!-- What happens next? What was returned from step 1? What tool is called now? -->

Step 1 returns a list of dicts that are sorted by relevance where most relevant is the first. The agent should display all the items and after the user choses an item it should then call the suggest_outfit function using that item to then create outfits based on the new piece.

**Step 3:**
<!-- Continue until the full interaction is complete -->

Step 2 returns a string of outfit suggestions or ways to style the new thrifted clothing piece. After this the user can select which outfit they like more and create_fit_card function should be called on that outfit to create a social media caption for a post.

**Final output to user:**
<!-- What does the user actually see at the end? -->

The user should see the outfit with their social media caption at the end.