import pandas as pd
import json

INPUT_CSV = "static/imdb.csv"  
OUTPUT_JSON = "similarity.json"  
df = pd.read_csv(INPUT_CSV)
df = df.fillna('')

def compute_score(movie, candidate):
    score = 0.0
    # Same Genre
    if movie['Genre'] == candidate['Genre']:
        score += 1.0
    # Same Director
    if movie['Director'] == candidate['Director']:
        score += 0.5
    # Shared Stars
    movie_stars = [movie['Star1'], movie['Star2'], movie['Star3'], movie['Star4']]
    candidate_stars = [candidate['Star1'], candidate['Star2'], candidate['Star3'], candidate['Star4']]
    shared_stars = len(set(movie_stars) & set(candidate_stars))
    score += shared_stars * 0.2
    # IMDB Rating boost
    try:
        score += (float(candidate['IMDB_Rating']) - 7.0) * 0.1
    except ValueError:
        pass
    return score

similarity_dict = {}
for idx, movie in df.iterrows():
    similarities = []
    for idx2, candidate in df.iterrows():
        if movie['Series_Title'] == candidate['Series_Title']:
            continue
        score = compute_score(movie, candidate)
        similarities.append({"title": candidate['Series_Title'], "score": score})
    similarities = sorted(similarities, key=lambda x: x['score'], reverse=True)[:10]
    similarity_dict[movie['Series_Title']] = similarities
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(similarity_dict, f, indent=2)

print(f"Similarity JSON saved to {OUTPUT_JSON}")