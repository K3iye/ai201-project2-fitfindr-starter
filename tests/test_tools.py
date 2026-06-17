from tools import search_listings, suggest_outfit, create_fit_card
from utils.data_loader import get_example_wardrobe, get_empty_wardrobe

# ── search_listings ───────────────────────────────────────────────────────────

def test_search_returns_results():
    results = search_listings("vintage graphic tee", size=None, max_price=50)
    assert isinstance(results, list)
    assert len(results) > 0

def test_search_empty_results():
    results = search_listings("designer ballgown", size="XXS", max_price=5)
    assert results == []

def test_search_price_filter():
    results = search_listings("jacket", size=None, max_price=10)
    assert all(item["price"] <= 10 for item in results)

def test_search_negative_price_returns_empty():
    results = search_listings("jeans", size=None, max_price=-1)
    assert results == []

# ── suggest_outfit ────────────────────────────────────────────────────────────

SAMPLE_ITEM = {
    "title": "Vintage Graphic Tee",
    "category": "tops",
    "colors": ["white", "black"],
    "style_tags": ["vintage", "streetwear"],
    "price": 18.0,
    "platform": "Depop",
}

def test_suggest_outfit_with_wardrobe():
    wardrobe = get_example_wardrobe()
    result = suggest_outfit(SAMPLE_ITEM, wardrobe)
    assert isinstance(result, str)
    assert len(result) > 0

def test_suggest_outfit_empty_wardrobe_returns_styling_advice():
    wardrobe = get_empty_wardrobe()
    result = suggest_outfit(SAMPLE_ITEM, wardrobe)
    assert isinstance(result, str)
    assert len(result) > 0

# ── create_fit_card ───────────────────────────────────────────────────────────

SAMPLE_OUTFIT = "Vintage graphic tee with baggy straight-leg jeans and chunky sneakers."

def test_create_fit_card_returns_caption():
    result = create_fit_card(SAMPLE_OUTFIT, SAMPLE_ITEM)
    assert isinstance(result, str)
    assert len(result) > 0

def test_create_fit_card_empty_outfit_returns_error():
    result = create_fit_card("", SAMPLE_ITEM)
    assert result.startswith("ERROR")

def test_create_fit_card_whitespace_outfit_returns_error():
    result = create_fit_card("   ", SAMPLE_ITEM)
    assert result.startswith("ERROR")