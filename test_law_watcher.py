from backend.law_watcher import fetch_kvkk_updates, summarize

text = fetch_kvkk_updates()
summary = summarize(text)
print("SUMMARY:\n", summary)
