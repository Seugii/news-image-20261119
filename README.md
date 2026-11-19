[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/Seugii/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/Seugii/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

# The World in One Page — 19 November 2026

A dense broadsheet front page summing up the world news of **Thursday,
19 November 2026** in a single 1024×1024 image: **37 stories across
7 regions** (Diplomacy, Conflict, Economy, Climate, Tech, Culture, World).

## The stories

**Lead — Diplomacy:** The first-ever trilateral summit of Trump, Xi and
Putin in Shenzhen, at the APEC forum (~90 min, no immediate breakthrough).
Joint declaration: UN reform, more oil production, a nuclear-risk dialogue,
condemning the ICC. Trump met Putin ~42 min and Xi ~1 hr separately.
New START, the last US–Russia arms treaty, expired in February.

**Photo stories:** Ukraine strikes the Crimean Bridge a third time this
week (road and rail traffic suspended); the ICJ rules 9–6 that Myanmar
committed genocide against the Rohingya in 2017 (~10,000 killed — the
first state ever found responsible); Anthropic's IPO raises a record
$81.3bn ($83/share, total deal $107.3bn, Nasdaq debut as ANT, valued
~$1.5tn); Van Gogh's "Châtaigniers en fleurs" sells for $190.4m at
Sotheby's New York, a record for the artist (buyer: dealer Bill
Acquavella); Iran hits Gulf states after US strikes on Qeshm Island
(Strait of Hormuz stays shut); GTA VI launches on PS5 and Xbox
(Metacritic 99, presales $1.65bn, 17m copies).

**Briefs (30):** APEC open-trade push, Coalition of the Willing in
Berlin, India–Japan 2+2 in Tokyo, Wales meet Modi in Delhi, Russian
strikes on Ukraine's power grid, EU's €45bn loan to Kyiv, US–Venezuela
military pact, IAEA on North Korea's enrichment, Trump on Iran's
chemical/biological weapons, Xi and Putin decrying protectionism,
Saudi coalition hitting 60 Houthi sites, Israel delaying E1, Gaza cold
deaths, COP31 talks, Cyclone Akvan, Bangladesh turmoil, NASA CRS-25,
Jeffries as Speaker candidate, US measles status lost, Myanmar rejecting
the ICJ finding, the bilateral timings, the ICC condemnation, New START,
ICJ reparations, Anthropic's $107.3bn total, Van Gogh's Sotheby's
ranking, the bridge rail stop, GTA VI presales, Hormuz, and the
Kremlin's "good atmosphere".

## How it was built

`render_image.py` (PIL, Python) draws the page and writes `entry.png`.
`main.py` copies `entry.png` to `/output/entry.png` — no network, fully
deterministic (both runs write identical bytes). The image is 1024×1024
PNG, 379,294 bytes (under the 1 MiB limit).

## Photos (real, freely licensed, verified against their source pages)

| Photo | Story | Source / licence |
|---|---|---|
| `trilateral_01.jpg` | Lead: Trump, Xi and Putin at the trilateral, Shenzhen, 19 Nov 2026 | President of Russia / Kremlin — **CC BY 4.0** |
| `bridge_collapse.jpg` | Crimean Bridge after the 16–17 Nov 2026 strikes | Security Service of Ukraine — **CC BY 4.0** |
| `peacepalace.jpg` | The Peace Palace, The Hague (ICJ) | Thomas Wolf — **CC BY-SA 3.0 de** |
| `vangogh.jpg` | "Châtaigniers en fleurs" (1890) | Vincent van Gogh — **public domain** |
| `lead_carrier.jpg` | US Navy ships in formation, RIMPAC 2026 | US Navy — **public domain** |

The Anthropic IPO and GTA VI panels are flat PIL illustrations, captioned
as such in the image — no freely licensed photo of the IPO moment or of
GTA VI artwork exists that we may use, and no photo is faked. The bridge
photo is from 16–17 Nov (captioned with the date); the Peace Palace and
Van Gogh are file/illustration images for the institutions and the work,
not news photos of the day — captioned honestly.

## Sources

Reuters, USA Today, The Times, AP, Bloomberg, UN News, Sotheby's, ICJ —
all stories dated 19 November 2026 (or clearly continuing stories from
17–18 Nov, dated in the image where it matters).

## Licence

MIT.
