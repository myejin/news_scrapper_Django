import csv
import urls


def get_stopwords():
    stopwords = ["특파원", "현지시간", "현지시각", "현지", "기자", "단독", "한편"]
    f = open("./korean_stopwords.tsv", "r", encoding="UTF-8")
    while True:
        line = f.readline()
        if not line:
            break
        stopwords.append(line.rstrip())
    return set(stopwords)


def preprocessing(url_list, stopwords, keywords, dummy_title="각캭콕쿅 눈누날라"):
    # 불용어 + 기업이름 삭제
    from newspaper import Article

    titles = []
    for i, url in enumerate(url_list):
        try:
            article = Article(url, language="ko")
            article.download()
            article.parse()
            if not article.title or not article.text:
                raise (Exception)

            words = ""
            for word in article.title.split():
                is_included = True
                for keyword in keywords:
                    if keyword in word:  # 기업이름
                        is_included = False
                        break
                if not is_included:
                    continue
                if word not in stopwords:
                    words += word + " "
            titles.append(words.rstrip())

        except Exception:
            titles.append(dummy_title)
            print(f"{i}번 문서 dummy 값으로 처리")
            continue

    return titles


def get_cos_sim(corpus):
    from KoSentenceBERT_SKTBERT.sentence_transformers import SentenceTransformer, util
    import numpy as np

    model_path = "KoSentenceBERT_SKTBERT/output/training_sts"
    embedder = SentenceTransformer(model_path)

    embeddings = embedder.encode(corpus, convert_to_tensor=True)
    cos_scores = util.pytorch_cos_sim(embeddings, embeddings)

    labels = [i for i in range(len(corpus))]

    def find(x):
        if labels[x] != x:
            labels[x] = find(labels[x])
        return labels[x]

    for i in range(len(corpus)):
        for j in range(len(corpus)):
            if cos_scores[i, j] > 0.75:
                fi, fj = find(i), find(j)
                if fi < fj:
                    labels[fj] = fi
                elif fj < fi:
                    labels[fi] = fj
    for x in range(len(corpus)):
        find(x)
    return labels


def classifier(titles, labels, dummy_title="각캭콕쿅 눈누날라"):
    result = {}
    for idx in labels:
        if titles[idx] == dummy_title:
            continue
        result[idx] = result.get(idx, 0) + 1
    return result


if __name__ == "__main__":
    stopwords = get_stopwords()
    url_list = urls.lgchem1 + urls.lgchem2
    keywords = ["LG", "lg"]

    titles = preprocessing(url_list, stopwords, keywords)
    labels = get_cos_sim(titles)
    K = len(urls.lgchem1)

    print("\n[라벨링]")
    print(f"lgchem1 : {labels[:K]}")
    print(f"lgchem2 : {labels[K:]}")

    print("\n[분류 결과]")
    result = classifier(titles, labels)
    print(result)
    for idx in result:
        print(f"- {titles[idx]}")
