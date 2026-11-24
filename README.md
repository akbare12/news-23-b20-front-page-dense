[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/akbare12/news-23-b20-front-page-dense/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/akbare12/news-23-b20-front-page-dense/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

# The World Today — Monday 23 November 2026

A dense front page summing up the world's news of Monday 23 November 2026
in one image: 31 stories across 6 regions.

- **Hero trio:** the AI rout hits Asia (KOSPI −3.3%), Guterres urges global
  AI safety rules before it's too late, and the US lead over China falls to
  a record low (Asia Power Index gap 5.3).
- **The day in numbers:** −3.3% Kospi · 5.3 US–China power gap ·
  11,762 Ebola cases in DRC · 10T won Seoul rescue fund · 2% billionaire
  tax plan · $450M Skubal Mets deal · 165 Russian missiles in a week ·
  107.3B Anthropic IPO.
- **Structure:** masthead → number strip → region bar → UTC strip →
  3 hero scenes → 10 small cards → world map with numbered pins →
  ALSO list → DATE CHECK (every story dated 23 Nov, with dated
  exclusions and items still developing).

`draw.py` (Pillow, stdlib only) draws `entry.png` (1024×1024, < 1 MiB);
`main.py` copies it to `MAKEFUN_OUTPUT_DIR/entry.png` and verifies
dimensions, size and sha256. Scenes are drawn illustrations, not
photographs.

Run locally: `python3 draw.py && mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py`
