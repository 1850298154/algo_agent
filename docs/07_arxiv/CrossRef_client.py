import requests
import json

def get_bibtex_by_title_crossref(title, limit=1):
    """
    根据论文标题从CrossRef获取BibTeX
    :param title: 论文标题（字符串）
    :param limit: 返回结果数量（默认1，取最匹配的）
    :return: 匹配的BibTeX字符串
    """
    # 构造请求URL
    url = "https://api.crossref.org/works"
    params = {
        "query.title": title,
        "rows": limit,
        "sort": "score",  # 按匹配度排序
        "order": "desc"
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # 抛出HTTP错误
        data = response.json()
        
        # 提取第一个匹配结果的DOI，再获取BibTeX
        if data["message"]["items"]:
            first_item = data["message"]["items"][0]
            doi = first_item["DOI"]
            # 通过DOI获取BibTeX
            bibtex_url = f"https://api.crossref.org/works/{doi}/transform/application/x-bibtex"
            bibtex_response = requests.get(bibtex_url)
            r"""
            https://api.crossref.org/works/10.65215/nxvz2v36/transform/application/x-bibtex
            
             @article{Vaswani_2025, title={Attention Is All You Need}, url={http://dx.doi.org/10.65215/nxvz2v36}, DOI={10.65215/nxvz2v36}, publisher={Shenzhen Medical Academy of Research and Translation}, author={Vaswani, Ashish and Shazeer, Noam and Parmar, Niki and Uszkoreit, Jakob and Jones, Llion and N.Gomez, Aidan and Kaiser, Lukasz and Polosukhin, Illia}, year={2025}, month=aug }
             
            https://api.crossref.org/works/10.65215/nxvz2v36/
            
            {"status":"ok","message-type":"work","message-version":"1.0.0","message":{"indexed":{"date-parts":[[2026,1,31]],"date-time":"2026-01-31T10:10:02Z","timestamp":1769854202153,"version":"3.49.0"},"posted":{"date-parts":[[2025,8,23]]},"reference-count":0,"publisher":"Shenzhen Medical Academy of Research and Translation","content-domain":{"domain":[],"crossmark-restriction":false},"short-container-title":[],"abstract":"<jats:p>The dominant sequence transduction models are based on complex recurrent or convolutional neural networks in an encoder-decoder configuration. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. Experiments on two machine translation tasks show these models to be superior in quality while being more parallelizable and requiring significantly less time to train. Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task, improving over the existing best results, including ensembles by over 2 BLEU. On the WMT 2014 English-to-French translation task, our model establishes a new single-model state-of-the-art BLEU score of 41.8 after training for 3.5 days on eight GPUs, a small fraction of the training costs of the best models from the literature. We show that the Transformer generalizes well to other tasks by applying it successfully to English constituency parsing both with large and limited training data.<\/jats:p>","DOI":"10.65215\/nxvz2v36","type":"posted-content","created":{"date-parts":[[2025,11,12]],"date-time":"2025-11-12T09:40:48Z","timestamp":1762940448000},"source":"Crossref","is-referenced-by-count":3,"title":["Attention Is All You Need"],"prefix":"10.65215","author":[{"given":"Ashish","family":"Vaswani","sequence":"first","affiliation":[{"name":"Google Brain"}]},{"given":"Noam","family":"Shazeer","sequence":"additional","affiliation":[{"name":"Google Brain"}]},{"given":"Niki","family":"Parmar","sequence":"additional","affiliation":[{"name":"Google Research"}]},{"given":"Jakob","family":"Uszkoreit","sequence":"additional","affiliation":[{"name":"Google Research"}]},{"given":"Llion","family":"Jones","sequence":"additional","affiliation":[{"name":"Google Research"}]},{"given":"Aidan","family":"N.Gomez","sequence":"additional","affiliation":[{"name":"University of Toronto"}]},{"given":"Lukasz","family":"Kaiser","sequence":"additional","affiliation":[{"name":"Google Brain"}]},{"given":"Illia","family":"Polosukhin","sequence":"additional","affiliation":[]}],"member":"54718","container-title":[],"original-title":[],"deposited":{"date-parts":[[2025,11,13]],"date-time":"2025-11-13T02:40:32Z","timestamp":1763001632000},"score":1,"resource":{"primary":{"URL":"https:\/\/langtaosha.org.cn\/index.php\/lts\/preprint\/view\/10"}},"subtitle":[],"short-title":[],"issued":{"date-parts":[[2025,8,23]]},"references-count":0,"URL":"https:\/\/doi.org\/10.65215\/nxvz2v36","relation":{"is-version-of":[{"id-type":"doi","id":"10.65215\/r5bs2d54","asserted-by":"subject"}]},"subject":[],"published":{"date-parts":[[2025,8,23]]},"subtype":"preprint"}}

            
            """
            return bibtex_response.text
        else:
            return "未找到匹配的论文"
    except Exception as e:
        return f"获取失败：{str(e)}"

# 测试示例
if __name__ == "__main__":
    paper_title = "Attention Is All You Need"  # 经典论文标题
    bibtex = get_bibtex_by_title_crossref(paper_title)
    print("BibTeX结果：")
    print(bibtex)
