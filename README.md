# sbert container version

### 1) 디렉토리 구조

- `sts` 폴더 위치를 명시하는 목적이기 때문에, 일부 기재하지 않았습니다.
- 타 개발자 분의 pre-trained 모델을 링크에서 다운 받고, `sbert` 내부에 추가해주세요.
  - <a href="https://drive.google.com/drive/folders/1fLYRi7W6J3rxt-KdGALBXMUS2W4Re7II">`모델 다운 링크`</a> 

```
sbert
+-- Dockerfile
+-- news_classifier.py
+-- urls.py
+-- sts
    +-- result.pt
```

### 2) 실행방법
- 패키지 설치가 오래 걸릴 수 있습니다. (빌드된 모델 사이즈: 11.5GB) 
```
$ docker build -t sbert:<version> .
$ docker run -it --name=<name> sbert:<version>
```

### 3) 결과이미지
- <a href="https://github.com/myejin/news_scrapper_Django/tree/feature/bert-test/tests/news_classify/ko_sbert_test_result">`링크 이동`</a>
<br>

### :clipboard: 참고

- <a href="https://github.com/BM-K/KoSentenceBERT_SKT">`BM-K/KoSentenceBERT_SKT`</a>

