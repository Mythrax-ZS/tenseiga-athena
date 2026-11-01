# The Twin Flames Saga

The Samurai's quest line, adapted from the user's *Twin Flames Saga* (see
[samurai.md](samurai.md) for the job, its blades and skills). It follows Hayate Yoshida's story
in ten chapters: the player, a Samurai, takes Hayate's road from the burned village of Kagemori
to the First Forge. Along the way they receive **Muramasa** (Chapter I) and **Kusanagi**
(Chapter V), then forge **Tenseiga-no-Hayate** and learn **Mortal Flame** (Chapter X). Only
Samurai can take it.

The set pieces are **memorial dungeons**: solo instances with stages, scripted scenes,
companions who speak and help, and bosses with phases, built the way the official memorials
are (Old Glast Heim, Faceworm's Nest, Sealed Shrine). Between them, the field chapters keep
the companions' trials, with the companion at the Samurai's side.

Masaru no longer forges Tenseiga on request in Prontera; the forging is Chapter X. Samurai who
forged Tenseiga before the saga existed keep it, and Masaru still grants them Mortal Flame.

## Files

| What | Where |
| --- | --- |
| Chapters and their NPCs | `npc/custom/twin_flames/` (`tf_common.txt`, `tf_ch01_03.txt`, `tf_tetsuya.txt`, `tf_ch04_06.txt`, `tf_ch07_10.txt`), and Masaru in `npc/custom/samurai_tenseiga.txt` |
| Memorial dungeons | `npc/custom/twin_flames/tf_md_*.txt`; `db/custom/samurai/instance_db.yml` (900-907), imported by `db/instance_db.yml` |
| Memorial maps | stock maps copied under saga names by `tools/twin_flames_maps.py` (see Setup) |
| Quests | `db/custom/samurai/quest_db.yml` (900101-900192), imported by `db/quest_db.yml` |
| Monsters | `db/custom/samurai/mob_db.yml` (31900-31933), imported by `db/mob_db.yml` |
| Monster skills | `db/custom/samurai/mob_skill_db.txt`, read after db/import (`src/map/mob.cpp`, `mob_load`) |
| Relics and quest items | `db/custom/samurai/item_db.yml` (900010-900021) |
| Client: monster looks, map copies | roclient `crates/ro-client/src/saga.rs`; `MAP_COPIES` in `crates/ro-client/src/app.rs` |
| Client: quest log, item names | roclient `overlays/samurai/System/samurai_questinfo.lua`, `samurai_iteminfo.lua` |

## Setup

The memorials are instances of saga maps: stock maps under their own names, so that their NPCs
stay out of the stock maps. Run once, from the rathena folder, then restart the map server:

```
python tools/twin_flames_maps.py
```

It copies each source map's cells into `db/import/map_cache.dat` and lists the copy in
`db/import/map_index.txt` and `conf/import/map_conf.txt` (all three are local files). Running it
again changes nothing. The Tenseiga client draws each copy from its source map's files.

| Copy | Source | Memorial |
| --- | --- | --- |
| `tf_kagemori` | amatsu (drawn at night) | Kagemori Burning |
| `tf_fortress` | ama_dun02 | Kurogane's Fortress |
| `tf_crimson` | ama_fild01 | The Crimson Fields |
| `tf_shrine` | ama_dun03 | The Shrine of Seals |
| `tf_palace` | ama_in02 | The Palace of Masks |
| `tf_abyss` | thor_v03 | The Abyssal Pit |
| `tf_trial` | job_ko | The Trial of Balance |
| `tf_goddess` | herosria | The Celestial Veil |

## The chapters

`TF_STEP` (a character variable) records progress. `TF_BOND` holds a bit for each finished
side trial: 1 Kiyoshi, 2 Renga, 4 Ayame, 8 Taro and Jiro, 16 Hanae, 32 the Herald, 64 Masaru.
`TF_MERCY`, `TF_TRUST` and `TF_DUEL` remember choices and change Tetsuya's last words.

| Chapter | Steps | Where | What happens |
| --- | --- | --- | --- |
| I Ashes of Honor | 0-10 | Ashigaru Courier, Prontera 158,179; Oharu, Amatsu 192,94; the Hooded Kami, ama_in01 175,176 | The kami's vision, **Kagemori Burning**. Muramasa is given inside it. Then hunt 20 Ashigaru Raiders. |
| II The Wandering Ronin | 10-20 | Elder Genzo, Amatsu 185,160; the Captured Raider, 187,158 | Drive back 30 Kapha. Spare or cut down the raider; his daughter sees which. |
| III The Trickster's Tail | 20-30 | Tetsuya, Amatsu 192,163; Iron Gate, ama_dun02 45,50 | Three riddles, then **Kurogane's Fortress**. |
| IV Whispers in Steel | 30-51 | Scorched War Banner, ama_fild01 200,291; Kiyoshi 198,151, Renga 200,140, Ayame 215,140 | **The Crimson Fields**. Three trials in the field, each companion at the arena: **General Mibu** (ice_dun02), **Fallen Monk Genkai** (prt_monk), **Kage** (ama_dun02). |
| V The Shrine of Seals | 51-60 | Sealed Gate, ama_dun03 120,30 | **The Shrine of Seals**: Kusanagi, then Sayo with Chiyo. |
| VI Chains of Light | 60-71 | Tetsuya; Taro and Jiro, Amatsu 225/227,150; Lady Hanae, ama_in02 196,172 | Trust the goddess or Tetsuya; trusting her brings the **Clash of Brothers**, a duel of stances. The **Glacial Yokai** (ice_dun03): the twins' ritual falters and only the Samurai can talk them round. **The Palace of Masks**. |
| VII Return of the Ashes | 71-81 | Altar of Ashes, thor_v02 90,199; Masaru, Prontera 161,179 | 30 Cultists of Ashes and the **Herald of Ashes** (Twin Flames: both blades dual wielded, and both pull). Five ledger pages for Masaru. |
| VIII The Fall of Yami | 81-90 | Kohaku, pay_fild08 40,80; Abyssal Gate, thor_v03 49,250 | The **Contract Binder** frees Kohaku. **The Abyssal Pit**; the goddess's false blessing. |
| IX The Weaver Unmasked | 90-100 | Tetsuya | The fall was a trap. Bring all eight relics, then **The Trial of Balance** for the Sarugami Essence. |
| X The Mortal Flame | 100-120 | Masaru and Tetsuya at the First Forge, mag_dun02 49,40 / 53,44 | Forge **Tenseiga-no-Hayate** (Twin Flames, 9 relics, 10 Oridecon, 10 Burning Hearts) with every companion watching their relic go into the fire, and learn **Mortal Flame**. Then **The Celestial Veil**. |

The forge keeps the lower refine of the two blades and refuses blades with cards in them.

## The memorial dungeons

Each memorial is a solo instance (`IM_CHAR`) that lasts an hour, so a Samurai who falls inside
can go back to it through the NPC that opened it. `F_TF_Memorial` (`tf_common.txt`) opens and
enters them. Scenes begin when the Samurai loads the map (`loadevent`, then a one-second player
timer, so that the map-load scripts finish first); each memorial marks its next objective on
the minimap and says it in an announcement.

| Memorial | Opened by | Stages and mechanics |
| --- | --- | --- |
| Kagemori Burning (I) | the Hooded Kami | Free four trapped villagers (the fire at the manor gate dies down); save Oharu from the raiders in the courtyard; the lord's last words; **Torch Captain Gonza**, who sets the hall burning and calls his men. At 15% the vision stops, he is lifted out of it, and the kami offers Muramasa. |
| Kurogane's Fortress (III) | the Iron Gate | Cut down three Iron Banners; **Warlord Kurogane** calls his retainers, then banner bearers who restore him if they reach him (Tetsuya trips one). At 20% he begs; whatever the Samurai answers, Muramasa answers first. |
| The Crimson Fields (IV) | the Scorched War Banner | Thirty soldiers among cowering villagers. Each villager cut down strengthens the **Shade of Yami** and is remembered; sparing them all counts as mercy. The Shade's pull confuses the Samurai and brings villagers into reach. Yami speaks, the blade will not leave the hand, Tetsuya's tail. |
| The Shrine of Seals (V) | the Sealed Gate | The seals of the Curse (it drinks HP through Muramasa), the Blood (Tetsuya bleeds) and the Truth (a riddle) open the way up; the **Guardian of the Seal** is shielded by Seal Lanterns that mend it; Kusanagi in its hall of moonlight; **High Priestess Sayo**, shielded while her acolytes pray, with Chiyo healing the Samurai. |
| The Palace of Masks (VI) | Lady Hanae | Search six chests for the cult's three sealed letters (some hide guards); each letter rules out one of four masked stewards, and the guilty one is drawn anew each time. The wrong accusation brings assassins; the right one unmasks **Daimyo Kurozane**, who hides behind masked doubles. |
| The Abyssal Pit (VIII) | the Abyssal Gate | Four Chain Anchors on the way down; **Kagutsuchi-no-Yami** rains meteors on the Samurai, calls cultists to be devoured (each that arrives mends him), and at the last reaches for Muramasa through a chain of fire until Kohaku burns it. |
| The Trial of Balance (IX) | Tetsuya | Sarugami spirits test the path; pillars of light and shadow must fall within five seconds of each other or both are restored; the **Sarugami Judge** hides behind one more pair. |
| The Celestial Veil (X) | Tetsuya at the forge | Three echoes of the companions guard the outer platforms and the bridge to the throne. The Weaver as **Radiant** (the sun's judgement scorches anyone not beside a Stone of Shade), **Eclipsed** (Moon Shards mend her) and **Amaterasu-no-Mikazuki** (both, and a seal that Tetsuya tears open). Then the ending and what became of everyone. |

## Field bosses

Six bosses are called in the field (`TF_Arenas` in `tf_common.txt`): Mibu, Genkai, Kage, the
Glacial Yokai, the Herald and the Contract Binder. Each is called by the quest's own player at
an arena NPC, on that quest step and with the blade it needs, and leaves after 15 minutes if it
still stands. The companion whose trial it is appears at the caller's side (seen only by them),
and boss and companion speak as it weakens. The Herald's two blades pull at the Samurai at
half health. Quest kill credit goes to the killer and to party members on the map.

## Monsters

| Id | Monster | Lv | HP | Notes |
| --- | --- | --- | --- | --- |
| 31900 | Ashigaru Raider | 110 | 45k | Amatsu fields (25), Kagemori, the fortress |
| 31901 | Crimson Fields Soldier | 125 | 90k | Amatsu fields, north (30); the Crimson Fields |
| 31902 | Cultist of Ashes | 140 | 160k | Thor's volcano, first level (20); the pit |
| 31903 | Warlord Kurogane | 145 | 3M | Kurogane's Fortress |
| 31904 | Shade of Yami | 150 | 4M | The Crimson Fields |
| 31905 | Usurper General Mibu | 150 | 5M | |
| 31906 | Fallen Monk Genkai | 150 | 5M | |
| 31907 | Kage, Assassin of Ashes | 155 | 5.5M | |
| 31908 | Guardian of the Seal | 160 | 9M | The Shrine of Seals |
| 31909 | High Priestess Sayo | 160 | 9M | The Shrine of Seals |
| 31910 | Glacial Yokai | 165 | 12M | |
| 31911 | Daimyo Kurozane | 165 | 12M | The Palace of Masks |
| 31912 | Herald of Ashes | 175 | 20M | |
| 31913 | Contract Binder | 170 | 15M | |
| 31914 | Kagutsuchi-no-Yami | 185 | 50M | MVP; the Abyssal Pit |
| 31915 | Radiant Amaterasu | 195 | 35M | Holy; the Celestial Veil |
| 31916 | Eclipsed Amaterasu | 195 | 35M | Dark |
| 31917 | Amaterasu-no-Mikazuki | 200 | 60M | MVP, Neutral |
| 31918 | Torch Captain Gonza | 125 | 1.2M | Kagemori Burning |
| 31919 | Iron Retainer | 135 | 120k | |
| 31920 | Iron Banner | 130 | 400k | object |
| 31921 | Banner Bearer | 130 | 80k | walks to Kurogane |
| 31922, 31933 | Cowering Villager | 50 | 15k | passive, never moves |
| 31923 | Sarugami Spirit | 150 | 150k | |
| 31924 | Seal Lantern | 150 | 600k | object; also the Pillar of Light |
| 31925 | Acolyte of the Veil | 155 | 200k | heals Sayo |
| 31926 | Masked Guard | 160 | 250k | |
| 31927 | Masked Double | 165 | 800k | |
| 31928 | Chain Anchor | 170 | 2M | object |
| 31929 | Ash Wraith | 170 | 300k | |
| 31930 | Echo | 185 | 3M | named for the companion it mimics |
| 31931 | Moon Shard | 190 | 1.5M | object; also the Pillar of Shadow |
| 31932 | Sarugami Judge | 175 | 18M | The Trial of Balance |

They are tuned against the Samurai's 4th-job-strength skills. The ids are this server's own,
so the official client has no sprite for them; Tenseiga draws each from a stock monster or NPC
sprite, recoloured, resized and tinted, with code-drawn auras for Yami (embers over a black
pool) and the Weaver (sun gold and moon silver).

## Testing

`@set TF_STEP <n>` with `@setquest` / `@completequest` jumps to a chapter; `@item 900010`..`900018`
gives the relics. A memorial lasts an hour, and five minutes once nobody is inside; restarting
the map server clears them. Every memorial, the duel and the First Forge were played through in
Tenseiga on 2026-11-02. The Glacial Yokai's mediation was not reached in a scripted run (its
auto-attack picked the dungeon's own monsters).
