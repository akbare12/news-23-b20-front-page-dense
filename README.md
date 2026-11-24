[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/akbare12/news-23-b20-front-page-dense/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/akbare12/news-23-b20-front-page-dense/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

# THE WORLD TODAY — Monday 23 November 2026

A one-image front page summing up 23 November 2026's world news: 31 stories
in 6 regions, with 3 drawn hero scenes, 10 cards, a world map with numbered
pins, an ALSO list, and a DATE CHECK box that keeps out stories from other days.

## Heroes

1. **AI rout hits Asia** — Kospi −3.3% to 4,708.54, sheds 161 pts; intraday
   −5.8%. Samsung −3.1%, SK Hynix −2.5%.
2. **Guterres: regulate AI before it's too late** — UN chief urges global AI
   safety rules at the Bridgetown summit; 150 delegates back a risk framework.
3. **US lead over China at record low** — Asia Power Index 2026: US 78.9,
   China 73.6, gap 5.3, narrowest since 2018. India third at 40.5.

## How it is built

`draw.py` (PIL) renders `entry.png` at 1024×1024. `main.py` is stdlib-only:
it validates the PNG header (signature, IHDR 1024×1024, IEND trailer, ≤1 MiB)
and copies it to `$MAKEFUN_OUTPUT_DIR/entry.png`, never writing next to itself.

Run it:

```sh
python3 draw.py
MAKEFUN_OUTPUT_DIR=out python3 main.py
```
