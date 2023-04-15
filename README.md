# news-reader

Prepare data:

```
poetry install
poetry run python crawl.py
```

Read daily summary:

```
poetry run python summary.py
```

## Example

```
❯ poetry run python summary.py
Title: G7気候・エネルギー・環境相会合 初日終了 共同声明案明らかに
URL: https://www3.nhk.or.jp/news/html/20230415/k10014039591000.html
Summary:
- 世界的な気候変動の課題に対し、G7の気候・エネルギー・環境相会合が開催され、各国共同の声明案が明らかになった。
- 重要鉱物の確保に関する激しい獲得競争がある。
- 合成燃料の技術開発が進められ、早期の商用化を目指すなど、各国が自動車分野の脱炭素化に向けて取り組んでいる。
Reason: This article covers an international event related to climate change and energy, which aligns with the customer's interest in international and business news.

Title: 陸自ヘリ事故 天候不良で「飽和潜水」実施せず 16日以降再開へ
URL: https://www3.nhk.or.jp/news/html/20230415/k10014039651000.html
Summary:
- 6月6日に陸上自衛隊のヘリコプターが宮古島と伊良部島の間で消息を絶ち、乗っていた隊員10人が行方不明となっている。
- 13日に海上自衛隊の掃海艦が、北北東におよそ4キロの海中で機体の一部とみられるものと、隊員の可能性がある人の姿を複数見つけたということが明らかになった。
- 自衛隊は、深い海で活動する「飽和潜水」と呼ばれる特殊な潜り方ができる潜水員を乗せた専用のカプセルを海に入れたが、作業中に不具合が起きて中止され、16日以降再開する予定となっている。
Reason: This article reports on a military helicopter accident, which may have implications for the defense industry and military relations, aligning with the customer's interest in business and international news.

Title: ChatGPT 各国で規制検討の動き 個人情報保護などの懸念から
URL: https://www3.nhk.or.jp/news/html/20230415/k10014039621000.html
Summary:
- 「ChatGPT」による個人情報の保護や情報流出の懸念から、各国で規制検討の動きが広がっている。
- アメリカ商務省はAIの評価や認証制度などについて一般からの意見募集を開始した。
- イタリアが「ChatGPT」の一時使用禁止に踏み切り、また欧州の国々でも規制を設けるか検討中。専門家は政治レベルでの対応を求めている。
Reason: This article discusses the global trend of regulating personal information protection, which is relevant to the customer's interest in business news.
```
