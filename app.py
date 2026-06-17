"""
app.py

Gradio interface for FitFindr. The layout and wiring are already set up —
your job is to fill in handle_query() so it calls run_agent() and maps
the session results to the three output panels.

Run with:
    python app.py

Then open the localhost URL shown in your terminal (usually http://localhost:7860,
but check your terminal — the port may differ).
"""

import gradio as gr

from agent import run_agent
from utils.data_loader import get_example_wardrobe, get_empty_wardrobe


# ── helpers ───────────────────────────────────────────────────────────────────

def _parse_wardrobe_input(text: str) -> list[dict]:
    """Parse a comma or newline separated wardrobe description into item dicts."""
    import re
    items = []
    for i, raw in enumerate(re.split(r"[,\n]", text)):
        name = raw.strip()
        if not name:
            continue
        items.append({
            "id": f"user_{i}",
            "name": name,
            "category": "unknown",
            "colors": [],
            "style_tags": [],
            "notes": None,
        })
    return items


# ── query handler ─────────────────────────────────────────────────────────────

def handle_query(user_query: str, wardrobe_choice: str, wardrobe_input: str) -> tuple[str, str, str]:
    """
    Called by Gradio when the user submits a query.

    Args:
        user_query:     The text the user typed into the search box.
        wardrobe_choice: Either "Example wardrobe" or "Empty wardrobe (new user)".
        wardrobe_input: Optional comma/newline separated list of user's own wardrobe items.

    Returns:
        A tuple of three strings:
            (listing_text, outfit_suggestion, fit_card)
        Each string maps to one of the three output panels in the UI.
    """
    # Step 1: Guard against empty query
    if not user_query or not user_query.strip():
        return "Please enter a search query.", "", ""

    # Step 2: Select base wardrobe
    if wardrobe_choice == "Empty wardrobe (new user)":
        wardrobe = get_empty_wardrobe()
    else:
        wardrobe = get_example_wardrobe()

    # Merge user's own items at the front if provided
    if wardrobe_input and wardrobe_input.strip():
        user_items = _parse_wardrobe_input(wardrobe_input)
        wardrobe = {"items": user_items + wardrobe["items"]}

    # Step 3: Run agent
    session = run_agent(user_query, wardrobe)

    # Step 4: Return error in first panel if something went wrong
    if session["error"]:
        return session["error"], "", ""

    # Step 5: Format selected item and return all three outputs
    item = session["selected_item"]
    listing_text = (
        f"Title: {item['title']}\n"
        f"Price: ${item['price']}\n"
        f"Size: {item['size']}\n"
        f"Condition: {item['condition']}\n"
        f"Category: {item['category']}\n"
        f"Brand: {item.get('brand') or 'Unknown'}\n"
        f"Platform: {item['platform']}\n"
        f"Colors: {', '.join(item.get('colors', []))}\n"
        f"Style tags: {', '.join(item.get('style_tags', []))}\n\n"
        f"{item['description']}"
    )

    return listing_text, session["outfit_suggestion"], session["fit_card"]


# ── interface ─────────────────────────────────────────────────────────────────

EXAMPLE_QUERIES = [
    "vintage graphic tee under $30",
    "90s track jacket in size M",
    "flowy midi skirt under $40",
    "black combat boots size 8",
    "designer ballgown size XXS under $5",   # deliberate no-results test
]

def build_interface():
    with gr.Blocks(title="FitFindr") as demo:
        gr.Markdown("""
# FitFindr 🛍️
Find secondhand pieces and get outfit ideas based on your wardrobe.
Describe what you're looking for — include size and price if you want to filter.
        """)

        with gr.Row():
            query_input = gr.Textbox(
                label="What are you looking for?",
                placeholder="e.g. vintage graphic tee under $30, size M",
                lines=2,
                scale=3,
            )
            wardrobe_choice = gr.Radio(
                choices=["Example wardrobe", "Empty wardrobe (new user)"],
                value="Example wardrobe",
                label="Wardrobe",
                scale=1,
            )

        wardrobe_input = gr.Textbox(
            label="Your wardrobe items (optional — comma or line separated)",
            placeholder="e.g. black turtleneck, beige chinos, brown Chelsea boots, gold watch",
            lines=2,
        )

        submit_btn = gr.Button("Find it", variant="primary")

        with gr.Row():
            listing_output = gr.Textbox(
                label="🛍️ Top listing found",
                lines=8,
                interactive=False,
            )
            outfit_output = gr.Textbox(
                label="👗 Outfit idea",
                lines=8,
                interactive=False,
            )
            fitcard_output = gr.Textbox(
                label="✨ Your fit card",
                lines=8,
                interactive=False,
            )

        gr.Examples(
            examples=[[q, "Example wardrobe", ""] for q in EXAMPLE_QUERIES],
            inputs=[query_input, wardrobe_choice, wardrobe_input],
            label="Try these queries",
        )

        submit_btn.click(
            fn=handle_query,
            inputs=[query_input, wardrobe_choice, wardrobe_input],
            outputs=[listing_output, outfit_output, fitcard_output],
        )
        query_input.submit(
            fn=handle_query,
            inputs=[query_input, wardrobe_choice, wardrobe_input],
            outputs=[listing_output, outfit_output, fitcard_output],
        )

    return demo


if __name__ == "__main__":
    demo = build_interface()
    demo.launch()
