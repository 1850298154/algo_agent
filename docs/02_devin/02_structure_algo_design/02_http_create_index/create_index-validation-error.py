import requests

url = "https://api.devin.ai/ada/index_public_repo"

# 从 URL 中提取的查询参数
# 注意：requests 会自动处理 URL 编码（例如 %2F 变为 /，%40 变为 @）
params = {
    "repo_name": "streamlit/docs",
    "email_to_notify": "1850298154@qq.com",
    "recaptcha_token": "0cAFcWeA7o0VEEvRe88cp2vp9ooyxGy5PKx6j7NykEjArP5WoqxHWibh6V8gCb7zEhlOWZC_Rke-Fz4kKSiOGRUi70rRI1qOIfvig_7vpqRIudykB5PQjkwXoeN377X4Bqew6QbDChTP1_jQtuAp3Hl5cNCB_JdWJfBxTjjSNnuOFYO3LzWRFXhSyeZIzpj2_bbv-QE902hSUTBNaZSdpfUGaPwKgTwM7HR1zRJdq6m84ofLeQ41nKasp5rW6a6gEkFSsFGz572lVTJi6N9Pq9eAmQAXOv4AB1VBXeK9oNFy16zmSKJ2ml5SWK2P45mdjumwDxniCkPHCL13EOAVeqKnxZGbdHuscKHhyz26clfcelRuHx8F4e97dA03XND8sXJVX0U16ZLYUokCSVuGSgTm1sUFTssEOTmLkmH1sfFaDOPlwfVwi36MO4wKq1QGcbiar9x10SUA-1SrQ0W-JEEYg53tDQ1TU5qSF5zHDcckRa6sg014cz97tDUnGRy63RGF-pG3cY4059ugliw6Et4Am-KG_XOh37B_9UFxrrxzdZ1e5QjsTNWAdTKihAkhqQsPmLdspSocul0Hlb0BR-FsM0nCIm1qyx4n_KDHP8DUWV-jDz430Fn9Jbg1Ub124v9UhiXcLLMP0sK5OgLaKnqN4lABqEjup6Sd6Z-pNn4wQ0npLIccCjMpwihVr9KRJ9MgRdpuA1d3pz5o77BS9nublv9GSvT-Ivl4nYfHfdbNDlPupIN-L4CMLzpUwpcNmUjfV81QDKqsPGV3McL6VSPGZKZnNFYcL0AGQf3CNEHzYWPi1IGi46yIygCO5WsfSXaLJN63e1y22wZ-ENcIPZh2oALQFbEVWzu8DwDcNxkkZF8r3tG68OpOwsG7SywchWfMEHfpJSAlVXB9WZTGVR2PfTJHd1HGsoBPve8rOwXOpNu7TnpxzkA1R0GOqfDQN4U9q75ZvKfgSTKb7Ht-QbUT3WjmV3V_iL206pJkvvRLcuacZTDFOGKdgU_NBhvS_OnCI6r9v4aw4bnMZX4hCIF-qdD9MlX7dDB7xtVTDd81-7KkPvWlMzKiSV-jyCddtsmlfuWpkFrmkIOvm9nvFKbp_dTllwizA1L-_j7KrckpVC84s6dUa-dJraVb1uj7FxYHc0J1NHE5i2pwTbptRw_el6U9r2pyGLSii8ZuuxSRCI-L3IVv5d4-hv_B87cZDoYCON2PvkuDqnsGM9gpl5v1t7kYYVcQMF5-L4G_ur6S0jwnoxhEvEdUgtB0OHdSXKNmH7_eaTSJTtsV72h1XhaSwmqgLjEjed7fr8JAkfcf7m54uMzOen3mHg2PX8yF7etAJXFH-4IFm7XEwc7YQybM7G4X_dmEyg17YX58tbav1bzq-tF-6HZ8YZ3IE-Hf6kZH5rNfPDOmRP_zNKnbYnI2YiPs6UNTRl3E2CBNeGhImWwww73EPl97TKihFn1EkeY3jzGi0TFlZbiVnwh1McqsViEXiUL5ExqXxQtFxcJ-z519tUnBYsYmhi8pjmgekBmmg_VNNX51HySo3GbeFejR6ukeyq4ewW2FtxEu_D8nbixsI2Hyk5Wc_lZqzqV9xmZmKrEkvIUFxguMrFE-XnozT3ClVgpzElNIPNYzqwns1tbUNDgv4IW-ItJWzipLnXURg6Of6bdu_k26MLqXjLZj5IDYTYDN9ANzZaEuC3r1FWzeEmPXlvTa2bHp8-oO2pA4myKRQTZzG2M5uh2NppKUsoFnDdRn7yeiRAV_bPFAvlcYTEtUhlFkt-tHdsWwNbsmxYn-RqOQLt4c22fvzouSDvbC-xQyoJRpRc1UuOUoa3tk2R7cgN2oJpHHA-fztTZ6ZBpI0c-YB6Y4Ij4zTYu5MkZJ63q9l-uC90emuKMwyCYgRBgX04D5MJKyG32tIsGr4RXawDpojaTl3J55Qcn6lc7fLX-on-2UcfUpQqn-vf3EJEtzEVq8MyEhjFSEJTaK7OtT_N4KjZQTV8SoFP6CIzmQmcjFgp-sNLsgZJ1l46jB7U2Wtjmb-G4fUek2d7Pm_iGZvyYB46CZYc3oLCeM35T06WoENkmtH9bhcbf99xHilWQM_XFY3DD27m8SYANj8TInipG5fNM885cn2_JCN0sFETL8u8mwtbskGZPVNy59wYOCqc_jTaIoP2jv15TP2WPPNgQGimb8HsWixezVkaAr8Df2eASP_opGZhuO9ojmvrzqJVJoQ"
}

headers = {
    "accept": "*/*",
    "accept-language": "zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6,en-GB;q=0.5",
    "content-length": "0",
    "origin": "https://deepwiki.com",
    "priority": "u=1, i",
    "referer": "https://deepwiki.com/",
    "sec-ch-ua": '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
}

try:
    # 这是一个 POST 请求，但参数是在 URL 中的 (Query params)，所以使用 params=params
    response = requests.post(url, headers=headers, params=params)
    
    # 打印结果
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
    
except Exception as e:
    print(f"An error occurred: {e}")
    
'''
Status Code: 400
Response Body: {"detail":"reCAPTCHA validation failed"}
'''