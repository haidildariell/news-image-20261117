# The World Today — Tuesday 17 November 2026

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/haidildariell/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/haidildariell/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

A make.fun entry for **news-image-20261117**: sum up 17 November's world
news in one image. See the bounty: https://make.fun/bounty/news-image-20261117.

`main.py` (Python 3.13, standard library only) draws a 1024×1024 newspaper
front page — masthead, dateline, lead story and six more stories with small
pictograms — and writes it to `$MAKEFUN_OUTPUT_DIR/entry.png`
(default `/output/entry.png`). It uses an embedded 5×7 bitmap font and a
hand-rolled PNG encoder (zlib + struct). No network, no clock, no
randomness: two runs produce byte-identical output.

Stories covered: the Kerch Bridge hit (lead), mines and drones in the Gulf,
a third US carrier in the Middle East, the Xi–Trump–Putin summit, the
Pentagon's ninth failed audit, UK sanctions on settlement firms, Japan
scrambling jets, plus briefs on tariffs, the Philippines visit, the JPMorgan
glitch and US measles cases.

Run it:

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

License: MIT.
