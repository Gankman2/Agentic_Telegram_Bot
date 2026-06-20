from ddgs import DDGS

def web_search(query: str) -> str:
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
        if not results:
            return "No results found."
        return "\n\n".join(
            f"{r['title']}\n{r['body']}\n{r['href']}" for r in results
        )
    except Exception as e:
        return f"Search error: {e}"