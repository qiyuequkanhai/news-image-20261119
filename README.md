# news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/qiyuequkanhai/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/qiyuequkanhai/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

A one-page newspaper front page, "THE WORLD TODAY", summing up the world news of Thursday 19 November 2026 in a single 1024x1024 image. The headline is Denmark's parliament voting 109-0 to ratify the US-Denmark-Greenland defence agreement. Below it: Voyager 1 phoning home from one light-day away, GTA VI's estimated $2.36 billion first day, Iran's claim that five tankers struck mines in the Strait of Hormuz, and Mongolia's parliament accepting its president's resignation. Every story was checked against several news sources before it went on the page.

## Run it

```sh
python3 tools/build_image.py
MAKEFUN_OUTPUT_DIR=./output python3 main.py
```

`tools/build_image.py` draws the front page with Pillow (DejaVu fonts, standard on most Linux systems) and writes `entry.png`. `main.py` is the entrypoint: it copies `entry.png` into the output directory, nothing else, using only the Python standard library.

## Stories and sources

- Denmark ratifies the US-Greenland defence deal, 109-0 — Al Jazeera, AP via Military.com, The Straits Times
- Voyager 1 crosses one light-day from Earth — NASA, AP via Phys.org, Reuters via Channel News Asia
- GTA VI launch: an estimated 24.58 million copies and $2.36 billion on day one (Sensor Tower estimate; Take-Two has not confirmed a figure) — Reuters, BBC via NME, The Straits Times
- Iran says five tankers struck naval mines in the Strait of Hormuz — IRGC Navy via ISNA/IRNA, UK Maritime Trade Operations
- Mongolia's parliament accepts President Khurelsukh's resignation, 96-104 — MONTSAME, AP

---

<sub>Entered on [make.fun](https://make.fun/?ref=qvhhz6jz&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
