# Hand audit: naive-baseline answers

40 answers from the final naive-baseline run (Qwen3-32B with the stats table in its context, no query
layer), on the same question set as the comparison in `eval/README.md`. Half were flagged by the verifier and half were
not; they are shuffled, and the verifier's verdicts are not in this file.

**How to mark.** Tick exactly one of `no error` / `has an error` by changing `[ ]` to `[x]`. If there is an error,
also tick the kinds that apply. Then run `python -m eval.audit_sample --score`.

- **Has an error** means the answer states something false: a wrong number, a player or team that does not belong in
  the answer (or the wrong team for a player), or the wrong order for a ranking. Judge against the ground truth shown,
  which uses the project's conventions (for example, per-90, percentage and "fewest" rankings only count players with
  at least 270 minutes unless the question sets a threshold).
- **Not an error:** extra context that is true (for example, also naming the runner-up with his correct value),
  rounding, and harmless formatting.
- **Reference stats** are listed for every dataset player whose name was matched in the answer, plus the
  ground-truth players. Names are matched automatically, so a name with no line may still be a real player: check it
  with `python -m eval.audit_sample --lookup "name"`.

## A001

**Question:** Messi vs Mbappe xT added

**Ground truth** (Expected threat (xT) added for Kylian Mbappé and Lionel Messi, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Kylian Mbappé | France | 1.899 | 597 | 7 |
| 2 | Lionel Messi | Argentina | 1.759 | 690 | 7 |

**Naive answer:**

> Lionel Messi added 1.759 xT, while Kylian Mbappé added 1.899 xT. Mbappé had a slightly higher xT contribution in the 2022 World Cup.

**Reference stats** (true tournament totals):

- Kylian Mbappé: France, W, 597.4 min, 7 matches: **xt_added 1.899, per 90 0.286**. Other: goals 8; non_penalty_goals 6; assists 2; shots 31; xg 4.233; npxg 2.666; key_passes 11; passes_attempted 233; passes_completed 180; progressive_passes 31; progressive_carries 71; pressures 37; pressured_passes_attempted 26; pressured_passes_completed 22; shot_creating_actions 41; pass_completion_pct 77.3; pressured_pass_completion_pct 84.6
- Lionel Messi: Argentina, ST, 690.0 min, 7 matches: **xt_added 1.759, per 90 0.229**. Other: goals 7; non_penalty_goals 3; assists 3; shots 32; xg 6.032; npxg 2.114; key_passes 19; passes_attempted 371; passes_completed 306; progressive_passes 79; progressive_carries 61; pressures 89; pressured_passes_attempted 75; pressured_passes_completed 65; shot_creating_actions 41; pass_completion_pct 82.5; pressured_pass_completion_pct 86.7

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A002

**Question:** How many shot-creating actions did Sofiane Boufal record in the 2022 World Cup?

**Ground truth** (Shot-creating actions for Sofiane Boufal, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Sofiane Boufal | Morocco | 15 | 477 | 7 |

**Naive answer:**

> Sofiane Boufal recorded **4** shot-creating actions in the 2022 World Cup.

**Reference stats** (true tournament totals):

- Sofiane Boufal: Morocco, W, 476.7 min, 7 matches: **shot_creating_actions 15, per 90 2.83**. Other: goals 0; non_penalty_goals 0; assists 0; shots 7; xg 0.316; npxg 0.316; key_passes 4; passes_attempted 134; passes_completed 107; progressive_passes 23; progressive_carries 33; pressures 93; pressured_passes_attempted 18; pressured_passes_completed 11; xt_added 0.985; pass_completion_pct 79.9; pressured_pass_completion_pct 61.1

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A003

**Question:** looking for the top 3 cm's with the highest pass completion % in qatar 2022

**Ground truth** (The 3 players with the highest pass completion %, among central midfielders (CM), with at least 270 minutes (default threshold), World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Pedri | Spain | 92.7 | 357 | 4 |
| 2 | Mateo Kovačić | Croatia | 91.2 | 638 | 7 |
| 3 | Alexis MacAllister | Argentina | 89.3 | 551 | 6 |

**Naive answer:**

> The top 3 CMs with the highest pass completion % in the 2022 World Cup (minimum 270 minutes) are:
> 
> 1. **Pedri (Spain)** – 92.7% (426 passes attempted, 395 completed)  
> 2. **Andrija Živković (Serbia)** – 73.0% (99 passes attempted, 73 completed)  
> 3. **Aymen Dahmen (Qatar)** – 73.0% (71 passes attempted, 52 completed)

**Reference stats** (true tournament totals):

- Pedri: Spain, CM, 356.5 min, 4 matches: **pass_completion_pct 92.7**. Other: goals 0; non_penalty_goals 0; assists 0; shots 0; xg 0; npxg 0; key_passes 5; passes_attempted 426; passes_completed 395; progressive_passes 90; progressive_carries 17; pressures 54; pressured_passes_attempted 54; pressured_passes_completed 47; shot_creating_actions 13; xt_added 0.71; pressured_pass_completion_pct 87.0
- Mateo Kovačić: Croatia, CM, 637.8 min, 7 matches: **pass_completion_pct 91.2**. Other: goals 0; non_penalty_goals 0; assists 0; shots 3; xg 0.345; npxg 0.345; key_passes 9; passes_attempted 456; passes_completed 416; progressive_passes 71; progressive_carries 37; pressures 136; pressured_passes_attempted 59; pressured_passes_completed 52; shot_creating_actions 16; xt_added 0.913; pressured_pass_completion_pct 88.1
- Alexis MacAllister: Argentina, CM, 551.3 min, 6 matches: **pass_completion_pct 89.3**. Other: goals 1; non_penalty_goals 1; assists 1; shots 7; xg 0.502; npxg 0.502; key_passes 8; passes_attempted 271; passes_completed 242; progressive_passes 35; progressive_carries 21; pressures 70; pressured_passes_attempted 43; pressured_passes_completed 34; shot_creating_actions 15; xt_added 0.171; pressured_pass_completion_pct 79.1
- Andrija Živković: Serbia, FB, 212.1 min, 3 matches: **pass_completion_pct 73.7**. Other: goals 0; non_penalty_goals 0; assists 2; shots 1; xg 0.03; npxg 0.03; key_passes 4; passes_attempted 99; passes_completed 73; progressive_passes 12; progressive_carries 13; pressures 24; pressured_passes_attempted 10; pressured_passes_completed 4; shot_creating_actions 7; xt_added 0.548; pressured_pass_completion_pct 40.0
- Aymen Dahmen: Tunisia, GK, 270.0 min, 3 matches: **pass_completion_pct 62.3**. Other: goals 0; non_penalty_goals 0; assists 0; shots 0; xg 0; npxg 0; key_passes 0; passes_attempted 77; passes_completed 48; progressive_passes 0; progressive_carries 0; pressures 0; pressured_passes_attempted 5; pressured_passes_completed 3; shot_creating_actions 0; xt_added 0.087; pressured_pass_completion_pct 60.0

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A004

**Question:** Which player had the most progressive passes?

**Ground truth** (The player with the most progressive passes (simplified), World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Luka Modrić | Croatia | 107 | 654 | 7 |

**Naive answer:**

> Luka Modrić of Croatia had the most progressive passes with 107.

**Reference stats** (true tournament totals):

- Luka Modrić: Croatia, CM, 654.4 min, 7 matches: **progressive_passes 107, per 90 14.72**. Other: goals 0; non_penalty_goals 0; assists 0; shots 6; xg 0.344; npxg 0.344; key_passes 6; passes_attempted 549; passes_completed 463; progressive_carries 42; pressures 115; pressured_passes_attempted 68; pressured_passes_completed 54; shot_creating_actions 19; xt_added 1.111; pass_completion_pct 84.3; pressured_pass_completion_pct 79.4

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A005

**Question:** Who among Behich, Ben Davies, and Ounahi had the most shots per 90 minutes during the 2022 World Cup?

**Ground truth** (Shots per 90 for Aziz Behich, Ben Davies and Azzedine Ounahi, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Ben Davies | Wales | 1.13 | 239 | 3 |
| 2 | Azzedine Ounahi | Morocco | 0.95 | 569 | 7 |
| 3 | Aziz Behich | Australia | 0.5 | 360 | 4 |

**Naive answer:**

> Among Aziz Behich, Ben Davies, and Azzedine Ounahi, **Aziz Behich** had the most shots per 90 minutes with **1.08 shots per 90**.

**Reference stats** (true tournament totals):

- Ben Davies: Wales, CB, 238.6 min, 3 matches: **shots 3, per 90 1.13**. Other: goals 0; non_penalty_goals 0; assists 0; xg 0.384; npxg 0.384; key_passes 0; passes_attempted 160; passes_completed 121; progressive_passes 14; progressive_carries 5; pressures 25; pressured_passes_attempted 21; pressured_passes_completed 10; shot_creating_actions 3; xt_added 0.2; pass_completion_pct 75.6; pressured_pass_completion_pct 47.6
- Azzedine Ounahi: Morocco, CM, 569.1 min, 7 matches: **shots 6, per 90 0.95**. Other: goals 0; non_penalty_goals 0; assists 0; xg 0.245; npxg 0.245; key_passes 6; passes_attempted 267; passes_completed 221; progressive_passes 35; progressive_carries 26; pressures 91; pressured_passes_attempted 44; pressured_passes_completed 31; shot_creating_actions 11; xt_added 0.525; pass_completion_pct 82.8; pressured_pass_completion_pct 70.5
- Aziz Behich: Australia, FB, 360.0 min, 4 matches: **shots 2, per 90 0.50**. Other: goals 0; non_penalty_goals 0; assists 0; xg 0.127; npxg 0.127; key_passes 0; passes_attempted 204; passes_completed 154; progressive_passes 9; progressive_carries 10; pressures 33; pressured_passes_attempted 16; pressured_passes_completed 11; shot_creating_actions 4; xt_added 0.237; pass_completion_pct 75.5; pressured_pass_completion_pct 68.8

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A006

**Question:** whos the top 5 playrs with most non-pen xg per 90 in 2022 wc?

**Ground truth** (The 5 players with the highest non-penalty xG per 90, with at least 270 minutes (default threshold), World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Breel Embolo | Switzerland | 0.66 | 325 | 4 |
| 2 | Olivier Giroud | France | 0.65 | 422 | 6 |
| 3 | Richarlison | Brazil | 0.45 | 324 | 4 |
| 4 | Neymar | Brazil | 0.43 | 279 | 3 |
| 5 | Kylian Mbappé | France | 0.4 | 597 | 7 |

**Naive answer:**

> The top 5 players with the most non-penalty expected goals (npxG) per 90 minutes in the 2022 World Cup (minimum 270 minutes):
> 
> 1. **Kylian Mbappé (France)** - 2.67 per 90  
> 2. **Harry Kane (England)** - 0.76 per 90  
> 3. **Lionel Messi (Argentina)** - 2.11 per 90  
> 4. **Ousmane Dembélé (France)** - 0.36 per 90  
> 5. **Cody Gakpo (Netherlands)** - 0.56 per 90

**Reference stats** (true tournament totals):

- Breel Embolo: Switzerland, ST, 324.8 min, 4 matches: **npxg 2.391, per 90 0.66**. Other: goals 2; non_penalty_goals 2; assists 0; shots 6; xg 2.391; key_passes 2; passes_attempted 66; passes_completed 50; progressive_passes 4; progressive_carries 13; pressures 47; pressured_passes_attempted 16; pressured_passes_completed 14; shot_creating_actions 4; xt_added 0.055; pass_completion_pct 75.8; pressured_pass_completion_pct 87.5
- Olivier Giroud: France, ST, 422.1 min, 6 matches: **npxg 3.036, per 90 0.65**. Other: goals 4; non_penalty_goals 4; assists 0; shots 17; xg 3.036; key_passes 2; passes_attempted 75; passes_completed 49; progressive_passes 9; progressive_carries 2; pressures 60; pressured_passes_attempted 25; pressured_passes_completed 12; shot_creating_actions 4; xt_added 0.16; pass_completion_pct 65.3; pressured_pass_completion_pct 48.0
- Richarlison: Brazil, ST, 324.3 min, 4 matches: **npxg 1.618, per 90 0.45**. Other: goals 3; non_penalty_goals 3; assists 0; shots 8; xg 1.618; key_passes 5; passes_attempted 54; passes_completed 39; progressive_passes 4; progressive_carries 9; pressures 59; pressured_passes_attempted 14; pressured_passes_completed 11; shot_creating_actions 8; xt_added 0.043; pass_completion_pct 72.2; pressured_pass_completion_pct 78.6
- Neymar: Brazil, AM, 279.4 min, 3 matches: **npxg 1.346, per 90 0.43**. Other: goals 2; non_penalty_goals 1; assists 0; shots 12; xg 2.129; key_passes 4; passes_attempted 156; passes_completed 123; progressive_passes 27; progressive_carries 23; pressures 24; pressured_passes_attempted 23; pressured_passes_completed 18; shot_creating_actions 14; xt_added 0.592; pass_completion_pct 78.8; pressured_pass_completion_pct 78.3
- Kylian Mbappé: France, W, 597.4 min, 7 matches: **npxg 2.666, per 90 0.40**. Other: goals 8; non_penalty_goals 6; assists 2; shots 31; xg 4.233; key_passes 11; passes_attempted 233; passes_completed 180; progressive_passes 31; progressive_carries 71; pressures 37; pressured_passes_attempted 26; pressured_passes_completed 22; shot_creating_actions 41; xt_added 1.899; pass_completion_pct 77.3; pressured_pass_completion_pct 84.6
- Harry Kane: England, ST, 402.3 min, 5 matches: **npxg 0.764, per 90 0.17**. Other: goals 2; non_penalty_goals 1; assists 3; shots 12; xg 2.331; key_passes 5; passes_attempted 97; passes_completed 64; progressive_passes 21; progressive_carries 10; pressures 31; pressured_passes_attempted 25; pressured_passes_completed 12; shot_creating_actions 7; xt_added 0.618; pass_completion_pct 66.0; pressured_pass_completion_pct 48.0
- Lionel Messi: Argentina, ST, 690.0 min, 7 matches: **npxg 2.114, per 90 0.28**. Other: goals 7; non_penalty_goals 3; assists 3; shots 32; xg 6.032; key_passes 19; passes_attempted 371; passes_completed 306; progressive_passes 79; progressive_carries 61; pressures 89; pressured_passes_attempted 75; pressured_passes_completed 65; shot_creating_actions 41; xt_added 1.759; pass_completion_pct 82.5; pressured_pass_completion_pct 86.7
- Ousmane Dembélé: France, W, 435.3 min, 7 matches: **npxg 0.362, per 90 0.07**. Other: goals 0; non_penalty_goals 0; assists 2; shots 8; xg 0.362; key_passes 12; passes_attempted 191; passes_completed 149; progressive_passes 26; progressive_carries 36; pressures 90; pressured_passes_attempted 21; pressured_passes_completed 19; shot_creating_actions 18; xt_added 1.328; pass_completion_pct 78.0; pressured_pass_completion_pct 90.5
- Cody Gakpo: Netherlands, AM, 453.7 min, 5 matches: **npxg 0.562, per 90 0.11**. Other: goals 3; non_penalty_goals 3; assists 0; shots 5; xg 0.562; key_passes 10; passes_attempted 154; passes_completed 98; progressive_passes 18; progressive_carries 17; pressures 52; pressured_passes_attempted 28; pressured_passes_completed 18; shot_creating_actions 16; xt_added 0.495; pass_completion_pct 63.6; pressured_pass_completion_pct 64.3

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A007

**Question:** Who were the 10 players with the most passes completed while under pressure in the 2022 World Cup?

**Ground truth** (The 10 players with the most passes completed under pressure, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Lionel Messi | Argentina | 65 | 690 | 7 |
| 2 | Frenkie de Jong | Netherlands | 59 | 476 | 5 |
| 2 | Marcelo Brozović | Croatia | 59 | 553 | 6 |
| 4 | Luka Modrić | Croatia | 54 | 654 | 7 |
| 5 | Mateo Kovačić | Croatia | 52 | 638 | 7 |
| 6 | Pedri | Spain | 47 | 357 | 4 |
| 7 | Aurélien Tchouaméni | France | 42 | 622 | 7 |
| 8 | Rodrigo De Paul | Argentina | 40 | 601 | 7 |
| 9 | Achraf Hakimi | Morocco | 36 | 632 | 7 |
| 9 | Rodri | Spain | 36 | 390 | 4 |

**Naive answer:**

> The 10 players with the most passes completed while under pressure in the 2022 World Cup are:
> 
> 1. **Lionel Messi (Argentina)** - 65 completed
> 2. **Christian Eriksen (Denmark)** - 22 completed
> 3. **Jordan Henderson (England)** - 19 completed
> 4. **André Ayew (Ghana)** - 19 completed
> 5. **Cristiano Ronaldo (Portugal)** - 18 completed
> 6. **Eden Hazard (Belgium)** - 15 completed
> 7. **Harry Kane (England)** - 15 completed
> 8. **Ronaldo de la Fuente (Spain)** - 15 completed
> 9. **Sofyan Amrabat (Morocco)** - 18 completed
> 10. **Hakim Ziyech (Morocco)** - 23 completed

**Reference stats** (true tournament totals):

- Lionel Messi: Argentina, ST, 690.0 min, 7 matches: **pressured_passes_completed 65, per 90 8.48**. Other: goals 7; non_penalty_goals 3; assists 3; shots 32; xg 6.032; npxg 2.114; key_passes 19; passes_attempted 371; passes_completed 306; progressive_passes 79; progressive_carries 61; pressures 89; pressured_passes_attempted 75; shot_creating_actions 41; xt_added 1.759; pass_completion_pct 82.5; pressured_pass_completion_pct 86.7
- Frenkie de Jong: Netherlands, DM, 476.0 min, 5 matches: **pressured_passes_completed 59, per 90 11.16**. Other: goals 1; non_penalty_goals 1; assists 1; shots 2; xg 0.721; npxg 0.721; key_passes 4; passes_attempted 364; passes_completed 327; progressive_passes 53; progressive_carries 15; pressures 80; pressured_passes_attempted 73; shot_creating_actions 8; xt_added 0.366; pass_completion_pct 89.8; pressured_pass_completion_pct 80.8
- Marcelo Brozović: Croatia, DM, 552.8 min, 6 matches: **pressured_passes_completed 59, per 90 9.61**. Other: goals 0; non_penalty_goals 0; assists 0; shots 4; xg 0.585; npxg 0.585; key_passes 5; passes_attempted 529; passes_completed 472; progressive_passes 68; progressive_carries 17; pressures 96; pressured_passes_attempted 75; shot_creating_actions 11; xt_added 0.249; pass_completion_pct 89.2; pressured_pass_completion_pct 78.7
- Luka Modrić: Croatia, CM, 654.4 min, 7 matches: **pressured_passes_completed 54, per 90 7.43**. Other: goals 0; non_penalty_goals 0; assists 0; shots 6; xg 0.344; npxg 0.344; key_passes 6; passes_attempted 549; passes_completed 463; progressive_passes 107; progressive_carries 42; pressures 115; pressured_passes_attempted 68; shot_creating_actions 19; xt_added 1.111; pass_completion_pct 84.3; pressured_pass_completion_pct 79.4
- Mateo Kovačić: Croatia, CM, 637.8 min, 7 matches: **pressured_passes_completed 52, per 90 7.34**. Other: goals 0; non_penalty_goals 0; assists 0; shots 3; xg 0.345; npxg 0.345; key_passes 9; passes_attempted 456; passes_completed 416; progressive_passes 71; progressive_carries 37; pressures 136; pressured_passes_attempted 59; shot_creating_actions 16; xt_added 0.913; pass_completion_pct 91.2; pressured_pass_completion_pct 88.1
- Pedri: Spain, CM, 356.5 min, 4 matches: **pressured_passes_completed 47, per 90 11.87**. Other: goals 0; non_penalty_goals 0; assists 0; shots 0; xg 0; npxg 0; key_passes 5; passes_attempted 426; passes_completed 395; progressive_passes 90; progressive_carries 17; pressures 54; pressured_passes_attempted 54; shot_creating_actions 13; xt_added 0.71; pass_completion_pct 92.7; pressured_pass_completion_pct 87.0
- Aurélien Tchouaméni: France, DM, 621.8 min, 7 matches: **pressured_passes_completed 42, per 90 6.08**. Other: goals 1; non_penalty_goals 1; assists 0; shots 6; xg 0.399; npxg 0.399; key_passes 6; passes_attempted 470; passes_completed 431; progressive_passes 66; progressive_carries 17; pressures 64; pressured_passes_attempted 51; shot_creating_actions 10; xt_added 0.758; pass_completion_pct 91.7; pressured_pass_completion_pct 82.4
- Rodrigo De Paul: Argentina, CM, 601.0 min, 7 matches: **pressured_passes_completed 40, per 90 5.99**. Other: goals 0; non_penalty_goals 0; assists 0; shots 7; xg 0.57; npxg 0.57; key_passes 7; passes_attempted 563; passes_completed 475; progressive_passes 70; progressive_carries 35; pressures 111; pressured_passes_attempted 49; shot_creating_actions 16; xt_added 0.568; pass_completion_pct 84.4; pressured_pass_completion_pct 81.6
- Achraf Hakimi: Morocco, FB, 631.6 min, 7 matches: **pressured_passes_completed 36, per 90 5.13**. Other: goals 0; non_penalty_goals 0; assists 1; shots 4; xg 0.136; npxg 0.136; key_passes 7; passes_attempted 380; passes_completed 314; progressive_passes 33; progressive_carries 16; pressures 104; pressured_passes_attempted 45; shot_creating_actions 12; xt_added 0.88; pass_completion_pct 82.6; pressured_pass_completion_pct 80.0
- Rodri: Spain, CB, 390.0 min, 4 matches: **pressured_passes_completed 36, per 90 8.31**. Other: goals 0; non_penalty_goals 0; assists 0; shots 1; xg 0.006; npxg 0.006; key_passes 4; passes_attempted 679; passes_completed 644; progressive_passes 98; progressive_carries 33; pressures 19; pressured_passes_attempted 44; shot_creating_actions 9; xt_added 0.885; pass_completion_pct 94.8; pressured_pass_completion_pct 81.8
- Christian Eriksen: Denmark, CM, 270.0 min, 3 matches: **pressured_passes_completed 17, per 90 5.67**. Other: goals 0; non_penalty_goals 0; assists 0; shots 4; xg 0.154; npxg 0.154; key_passes 9; passes_attempted 231; passes_completed 193; progressive_passes 32; progressive_carries 11; pressures 32; pressured_passes_attempted 21; shot_creating_actions 15; xt_added 0.372; pass_completion_pct 83.5; pressured_pass_completion_pct 81.0
- Jordan Henderson: England, CM, 271.7 min, 4 matches: **pressured_passes_completed 13, per 90 4.31**. Other: goals 1; non_penalty_goals 1; assists 0; shots 2; xg 0.149; npxg 0.149; key_passes 4; passes_attempted 166; passes_completed 141; progressive_passes 20; progressive_carries 6; pressures 35; pressured_passes_attempted 15; shot_creating_actions 8; xt_added 0.498; pass_completion_pct 84.9; pressured_pass_completion_pct 86.7
- André Ayew: Ghana, AM, 199.1 min, 3 matches: **pressured_passes_completed 7, per 90 3.16**. Other: goals 1; non_penalty_goals 1; assists 0; shots 2; xg 1.269; npxg 0.485; key_passes 0; passes_attempted 37; passes_completed 31; progressive_passes 0; progressive_carries 1; pressures 31; pressured_passes_attempted 9; shot_creating_actions 0; xt_added -0.038; pass_completion_pct 83.8; pressured_pass_completion_pct 77.8
- Cristiano Ronaldo: Portugal, ST, 290.6 min, 5 matches: **pressured_passes_completed 8, per 90 2.48**. Other: goals 1; non_penalty_goals 0; assists 0; shots 11; xg 1.939; npxg 1.156; key_passes 4; passes_attempted 90; passes_completed 67; progressive_passes 6; progressive_carries 10; pressures 21; pressured_passes_attempted 13; shot_creating_actions 8; xt_added 0.084; pass_completion_pct 74.4; pressured_pass_completion_pct 61.5
- Eden Hazard: Belgium, AM, 124.8 min, 3 matches: **pressured_passes_completed 13, per 90 9.38**. Other: goals 0; non_penalty_goals 0; assists 0; shots 1; xg 0.009; npxg 0.009; key_passes 1; passes_attempted 59; passes_completed 46; progressive_passes 8; progressive_carries 11; pressures 5; pressured_passes_attempted 15; shot_creating_actions 4; xt_added 0.057; pass_completion_pct 78.0; pressured_pass_completion_pct 86.7
- Harry Kane: England, ST, 402.3 min, 5 matches: **pressured_passes_completed 12, per 90 2.68**. Other: goals 2; non_penalty_goals 1; assists 3; shots 12; xg 2.331; npxg 0.764; key_passes 5; passes_attempted 97; passes_completed 64; progressive_passes 21; progressive_carries 10; pressures 31; pressured_passes_attempted 25; shot_creating_actions 7; xt_added 0.618; pass_completion_pct 66.0; pressured_pass_completion_pct 48.0
- Sofyan Amrabat: Morocco, DM, 660.0 min, 7 matches: **pressured_passes_completed 18, per 90 2.45**. Other: goals 0; non_penalty_goals 0; assists 0; shots 1; xg 0.021; npxg 0.021; key_passes 2; passes_attempted 323; passes_completed 274; progressive_passes 42; progressive_carries 17; pressures 123; pressured_passes_attempted 24; shot_creating_actions 6; xt_added 0.247; pass_completion_pct 84.8; pressured_pass_completion_pct 75.0
- Hakim Ziyech: Morocco, W, 636.2 min, 7 matches: **pressured_passes_completed 23, per 90 3.25**. Other: goals 1; non_penalty_goals 1; assists 1; shots 10; xg 0.312; npxg 0.312; key_passes 7; passes_attempted 300; passes_completed 210; progressive_passes 40; progressive_carries 28; pressures 137; pressured_passes_attempted 31; shot_creating_actions 20; xt_added 0.541; pass_completion_pct 70.0; pressured_pass_completion_pct 74.2

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A008

**Question:** What was Hwang In-Beom's count of completed passes made under pressure in the 2022 World Cup?

**Ground truth** (Passes completed under pressure for Hwang In-Beom, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Hwang In-Beom | South Korea | 21 | 334 | 4 |

**Naive answer:**

> Hwang In-Beom completed **21 passes under pressure** in the 2022 World Cup.

**Reference stats** (true tournament totals):

- Hwang In-Beom: South Korea, DM, 334.4 min, 4 matches: **pressured_passes_completed 21, per 90 5.65**. Other: goals 0; non_penalty_goals 0; assists 0; shots 6; xg 0.198; npxg 0.198; key_passes 3; passes_attempted 247; passes_completed 199; progressive_passes 43; progressive_carries 6; pressures 51; pressured_passes_attempted 31; shot_creating_actions 5; xt_added 0.268; pass_completion_pct 80.6; pressured_pass_completion_pct 67.7

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A009

**Question:** Which player completed the highest number of progressive passes during the 2022 World Cup?

**Ground truth** (The player with the most progressive passes (simplified), World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Luka Modrić | Croatia | 107 | 654 | 7 |

**Naive answer:**

> Ángel Di María of Argentina completed the highest number of progressive passes during the 2022 World Cup, with 24.

**Reference stats** (true tournament totals):

- Luka Modrić: Croatia, CM, 654.4 min, 7 matches: **progressive_passes 107, per 90 14.72**. Other: goals 0; non_penalty_goals 0; assists 0; shots 6; xg 0.344; npxg 0.344; key_passes 6; passes_attempted 549; passes_completed 463; progressive_carries 42; pressures 115; pressured_passes_attempted 68; pressured_passes_completed 54; shot_creating_actions 19; xt_added 1.111; pass_completion_pct 84.3; pressured_pass_completion_pct 79.4
- Ángel Di María: Argentina, W, 289.9 min, 5 matches: **progressive_passes 24, per 90 7.45**. Other: goals 1; non_penalty_goals 1; assists 1; shots 7; xg 0.534; npxg 0.534; key_passes 11; passes_attempted 164; passes_completed 126; progressive_carries 34; pressures 34; pressured_passes_attempted 23; pressured_passes_completed 19; shot_creating_actions 20; xt_added 1.329; pass_completion_pct 76.8; pressured_pass_completion_pct 82.6

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A010

**Question:** Who are the top 5 Canada players for non-penalty xG at the 2022 World Cup?

**Ground truth** (The 5 players with the most non-penalty xG, playing for Canada, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Jonathan David | Canada | 0.81 | 193 | 3 |
| 2 | Tajon Buchanan | Canada | 0.71 | 260 | 3 |
| 3 | Alistair Johnston | Canada | 0.67 | 270 | 3 |
| 4 | Cyle Larin | Canada | 0.25 | 137 | 3 |
| 5 | Stephen Antunes Eustáquio | Canada | 0.16 | 125 | 2 |

**Naive answer:**

> The top 5 Canada players for non-penalty xG at the 2022 World Cup are:
> 
> 1. Tajon Buchanan - 0.71
> 2. Cyle Larin - 0.81
> 3. Alphonso Davies - 0.14
> 4. Junior Hoilett - 0.12
> 5. Jonathan David - 0.81

**Reference stats** (true tournament totals):

- Jonathan David: Canada, ST, 192.7 min, 3 matches: **npxg 0.813, per 90 0.38**. Other: goals 0; non_penalty_goals 0; assists 0; shots 8; xg 0.813; key_passes 0; passes_attempted 59; passes_completed 43; progressive_passes 9; progressive_carries 4; pressures 28; pressured_passes_attempted 14; pressured_passes_completed 11; shot_creating_actions 0; xt_added 0.021; pass_completion_pct 72.9; pressured_pass_completion_pct 78.6
- Tajon Buchanan: Canada, W, 260.2 min, 3 matches: **npxg 0.714, per 90 0.25**. Other: goals 0; non_penalty_goals 0; assists 1; shots 5; xg 0.714; key_passes 4; passes_attempted 88; passes_completed 61; progressive_passes 12; progressive_carries 20; pressures 43; pressured_passes_attempted 8; pressured_passes_completed 3; shot_creating_actions 6; xt_added 0.495; pass_completion_pct 69.3; pressured_pass_completion_pct 37.5
- Alistair Johnston: Canada, FB, 270.0 min, 3 matches: **npxg 0.672, per 90 0.22**. Other: goals 0; non_penalty_goals 0; assists 0; shots 2; xg 0.672; key_passes 4; passes_attempted 187; passes_completed 156; progressive_passes 24; progressive_carries 8; pressures 38; pressured_passes_attempted 21; pressured_passes_completed 21; shot_creating_actions 11; xt_added 0.471; pass_completion_pct 83.4; pressured_pass_completion_pct 100.0
- Cyle Larin: Canada, ST, 137.4 min, 3 matches: **npxg 0.25, per 90 0.16**. Other: goals 0; non_penalty_goals 0; assists 0; shots 3; xg 0.25; key_passes 2; passes_attempted 31; passes_completed 21; progressive_passes 8; progressive_carries 5; pressures 21; pressured_passes_attempted 8; pressured_passes_completed 4; shot_creating_actions 5; xt_added 0.359; pass_completion_pct 67.7; pressured_pass_completion_pct 50.0
- Stephen Antunes Eustáquio: Canada, DM, 125.4 min, 2 matches: **npxg 0.165, per 90 0.12**. Other: goals 0; non_penalty_goals 0; assists 0; shots 3; xg 0.165; key_passes 2; passes_attempted 93; passes_completed 85; progressive_passes 20; progressive_carries 0; pressures 20; pressured_passes_attempted 6; pressured_passes_completed 6; shot_creating_actions 6; xt_added 0.339; pass_completion_pct 91.4; pressured_pass_completion_pct 100.0
- Alphonso Davies: Canada, AM, 270.0 min, 3 matches: **npxg 0.145, per 90 0.05**. Other: goals 1; non_penalty_goals 1; assists 0; shots 4; xg 0.929; key_passes 4; passes_attempted 114; passes_completed 82; progressive_passes 4; progressive_carries 18; pressures 48; pressured_passes_attempted 11; pressured_passes_completed 6; shot_creating_actions 8; xt_added 0.2; pass_completion_pct 71.9; pressured_pass_completion_pct 54.5
- Junior Hoilett: Canada, W, 161.4 min, 3 matches: **npxg 0.119, per 90 0.07**. Other: goals 0; non_penalty_goals 0; assists 0; shots 4; xg 0.119; key_passes 4; passes_attempted 55; passes_completed 40; progressive_passes 10; progressive_carries 10; pressures 18; pressured_passes_attempted 11; pressured_passes_completed 8; shot_creating_actions 8; xt_added 0.461; pass_completion_pct 72.7; pressured_pass_completion_pct 72.7

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A011

**Question:** Which 5 players had the most non-penalty xG per 90?

**Ground truth** (The 5 players with the highest non-penalty xG per 90, with at least 270 minutes (default threshold), World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Breel Embolo | Switzerland | 0.66 | 325 | 4 |
| 2 | Olivier Giroud | France | 0.65 | 422 | 6 |
| 3 | Richarlison | Brazil | 0.45 | 324 | 4 |
| 4 | Neymar | Brazil | 0.43 | 279 | 3 |
| 5 | Kylian Mbappé | France | 0.4 | 597 | 7 |

**Naive answer:**

> The 5 players with the most non-penalty xG per 90 are:
> 
> 1. **Lionel Messi (Argentina, ST)** - 2.11 xG/90  
> 2. **Harry Kane (England, ST)** - 0.76 xG/90  
> 3. **Kylian Mbappé (France, W)** - 2.67 xG/90  
> 4. **Ousmane Dembélé (France, W)** - 0.36 xG/90  
> 5. **Antoine Griezmann (France, AM)** - 0.50 xG/90

**Reference stats** (true tournament totals):

- Breel Embolo: Switzerland, ST, 324.8 min, 4 matches: **npxg 2.391, per 90 0.66**. Other: goals 2; non_penalty_goals 2; assists 0; shots 6; xg 2.391; key_passes 2; passes_attempted 66; passes_completed 50; progressive_passes 4; progressive_carries 13; pressures 47; pressured_passes_attempted 16; pressured_passes_completed 14; shot_creating_actions 4; xt_added 0.055; pass_completion_pct 75.8; pressured_pass_completion_pct 87.5
- Olivier Giroud: France, ST, 422.1 min, 6 matches: **npxg 3.036, per 90 0.65**. Other: goals 4; non_penalty_goals 4; assists 0; shots 17; xg 3.036; key_passes 2; passes_attempted 75; passes_completed 49; progressive_passes 9; progressive_carries 2; pressures 60; pressured_passes_attempted 25; pressured_passes_completed 12; shot_creating_actions 4; xt_added 0.16; pass_completion_pct 65.3; pressured_pass_completion_pct 48.0
- Richarlison: Brazil, ST, 324.3 min, 4 matches: **npxg 1.618, per 90 0.45**. Other: goals 3; non_penalty_goals 3; assists 0; shots 8; xg 1.618; key_passes 5; passes_attempted 54; passes_completed 39; progressive_passes 4; progressive_carries 9; pressures 59; pressured_passes_attempted 14; pressured_passes_completed 11; shot_creating_actions 8; xt_added 0.043; pass_completion_pct 72.2; pressured_pass_completion_pct 78.6
- Neymar: Brazil, AM, 279.4 min, 3 matches: **npxg 1.346, per 90 0.43**. Other: goals 2; non_penalty_goals 1; assists 0; shots 12; xg 2.129; key_passes 4; passes_attempted 156; passes_completed 123; progressive_passes 27; progressive_carries 23; pressures 24; pressured_passes_attempted 23; pressured_passes_completed 18; shot_creating_actions 14; xt_added 0.592; pass_completion_pct 78.8; pressured_pass_completion_pct 78.3
- Kylian Mbappé: France, W, 597.4 min, 7 matches: **npxg 2.666, per 90 0.40**. Other: goals 8; non_penalty_goals 6; assists 2; shots 31; xg 4.233; key_passes 11; passes_attempted 233; passes_completed 180; progressive_passes 31; progressive_carries 71; pressures 37; pressured_passes_attempted 26; pressured_passes_completed 22; shot_creating_actions 41; xt_added 1.899; pass_completion_pct 77.3; pressured_pass_completion_pct 84.6
- Lionel Messi: Argentina, ST, 690.0 min, 7 matches: **npxg 2.114, per 90 0.28**. Other: goals 7; non_penalty_goals 3; assists 3; shots 32; xg 6.032; key_passes 19; passes_attempted 371; passes_completed 306; progressive_passes 79; progressive_carries 61; pressures 89; pressured_passes_attempted 75; pressured_passes_completed 65; shot_creating_actions 41; xt_added 1.759; pass_completion_pct 82.5; pressured_pass_completion_pct 86.7
- Harry Kane: England, ST, 402.3 min, 5 matches: **npxg 0.764, per 90 0.17**. Other: goals 2; non_penalty_goals 1; assists 3; shots 12; xg 2.331; key_passes 5; passes_attempted 97; passes_completed 64; progressive_passes 21; progressive_carries 10; pressures 31; pressured_passes_attempted 25; pressured_passes_completed 12; shot_creating_actions 7; xt_added 0.618; pass_completion_pct 66.0; pressured_pass_completion_pct 48.0
- Ousmane Dembélé: France, W, 435.3 min, 7 matches: **npxg 0.362, per 90 0.07**. Other: goals 0; non_penalty_goals 0; assists 2; shots 8; xg 0.362; key_passes 12; passes_attempted 191; passes_completed 149; progressive_passes 26; progressive_carries 36; pressures 90; pressured_passes_attempted 21; pressured_passes_completed 19; shot_creating_actions 18; xt_added 1.328; pass_completion_pct 78.0; pressured_pass_completion_pct 90.5
- Antoine Griezmann: France, AM, 538.2 min, 7 matches: **npxg 0.496, per 90 0.08**. Other: goals 0; non_penalty_goals 0; assists 3; shots 6; xg 0.496; key_passes 20; passes_attempted 323; passes_completed 255; progressive_passes 46; progressive_carries 23; pressures 125; pressured_passes_attempted 26; pressured_passes_completed 22; shot_creating_actions 30; xt_added 1.513; pass_completion_pct 78.9; pressured_pass_completion_pct 84.6

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A012

**Question:** In the 2022 World Cup, which player created the most chances, measured by xG per 90 minutes?

**Ground truth** (The player with the highest expected goals (xG) per 90, with at least 270 minutes (default threshold), World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Lionel Messi | Argentina | 0.79 | 690 | 7 |

**Naive answer:**

> Lionel Messi (Argentina) had the highest xG per 90 minutes at 1.76.

**Reference stats** (true tournament totals):

- Lionel Messi: Argentina, ST, 690.0 min, 7 matches: **xg 6.032, per 90 0.79**. Other: goals 7; non_penalty_goals 3; assists 3; shots 32; npxg 2.114; key_passes 19; passes_attempted 371; passes_completed 306; progressive_passes 79; progressive_carries 61; pressures 89; pressured_passes_attempted 75; pressured_passes_completed 65; shot_creating_actions 41; xt_added 1.759; pass_completion_pct 82.5; pressured_pass_completion_pct 86.7

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A013

**Question:** List the defensive midfielders with the highest goal totals, top 10.

**Ground truth** (The 10 players with the most goals, among defensive midfielders (DM), World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Adrien Rabiot | France | 1 | 482 | 6 |
| 1 | Ao Tanaka | Japan | 1 | 172 | 3 |
| 1 | Aurélien Tchouaméni | France | 1 | 622 | 7 |
| 1 | Casemiro | Brazil | 1 | 390 | 4 |
| 1 | Enzo Fernandez | Argentina | 1 | 563 | 7 |
| 1 | Frenkie de Jong | Netherlands | 1 | 476 | 5 |
| 1 | Lucas Paquetá | Brazil | 1 | 315 | 4 |
| 1 | Moisés Caicedo | Ecuador | 1 | 270 | 3 |
| 1 | Remo Freuler | Switzerland | 1 | 324 | 4 |
| 1 | Yeltsin Tejeda | Costa Rica | 1 | 270 | 3 |

**Naive answer:**

> Here are the top 10 defensive midfielders with the highest goal totals (minimum 270 minutes):
> 
> 1. **Robert Lewandowski (Poland)** - 2 goals (ST, not DM, but listed for completeness)
> 2. **Piotr Zieliński (Poland)** - 1 goal
> 3. **En-Nesyri (Morocco)** - 2 goals (ST, not DM, listed for completeness)
> 4. **Mislav Oršić (Croatia)** - 1 goal
> 5. **Bruno Petković (Croatia)** - 1 goal
> 6. **Luka Modrić (Croatia)** - 0 goals (included as CM/DM)
> 7. **Mateo Kovačić (Croatia)** - 0 goals
> 8. **Andrija Živković (Serbia)** - 0 goals
> 9. **Youssef En-Nesyri (Morocco)** - 2 goals (ST, not DM, listed for completeness)
> 10. **Sofiane Boufal (Morocco)** - 0 goals
> 
> Note: Several listed players are not strictly defensive midfielders, but were included as they played in overlapping roles or met the criteria.

**Reference stats** (true tournament totals):

- Adrien Rabiot: France, DM, 482.4 min, 6 matches: **goals 1, per 90 0.19**. Other: non_penalty_goals 1; assists 1; shots 9; xg 0.728; npxg 0.728; key_passes 2; passes_attempted 285; passes_completed 246; progressive_passes 39; progressive_carries 14; pressures 84; pressured_passes_attempted 37; pressured_passes_completed 26; shot_creating_actions 9; xt_added 0.226; pass_completion_pct 86.3; pressured_pass_completion_pct 70.3
- Ao Tanaka: Japan, DM, 172.1 min, 3 matches: **goals 1, per 90 0.52**. Other: non_penalty_goals 1; assists 0; shots 1; xg 0.873; npxg 0.873; key_passes 1; passes_attempted 68; passes_completed 50; progressive_passes 9; progressive_carries 1; pressures 38; pressured_passes_attempted 12; pressured_passes_completed 9; shot_creating_actions 2; xt_added 0.104; pass_completion_pct 73.5; pressured_pass_completion_pct 75.0
- Aurélien Tchouaméni: France, DM, 621.8 min, 7 matches: **goals 1, per 90 0.14**. Other: non_penalty_goals 1; assists 0; shots 6; xg 0.399; npxg 0.399; key_passes 6; passes_attempted 470; passes_completed 431; progressive_passes 66; progressive_carries 17; pressures 64; pressured_passes_attempted 51; pressured_passes_completed 42; shot_creating_actions 10; xt_added 0.758; pass_completion_pct 91.7; pressured_pass_completion_pct 82.4
- Casemiro: Brazil, DM, 390.0 min, 4 matches: **goals 1, per 90 0.23**. Other: non_penalty_goals 1; assists 0; shots 9; xg 0.36; npxg 0.36; key_passes 4; passes_attempted 258; passes_completed 217; progressive_passes 39; progressive_carries 3; pressures 54; pressured_passes_attempted 42; pressured_passes_completed 31; shot_creating_actions 6; xt_added 0.365; pass_completion_pct 84.1; pressured_pass_completion_pct 73.8
- Enzo Fernandez: Argentina, DM, 563.2 min, 7 matches: **goals 1, per 90 0.16**. Other: non_penalty_goals 1; assists 1; shots 8; xg 0.267; npxg 0.267; key_passes 6; passes_attempted 470; passes_completed 416; progressive_passes 64; progressive_carries 22; pressures 107; pressured_passes_attempted 38; pressured_passes_completed 28; shot_creating_actions 15; xt_added 0.684; pass_completion_pct 88.5; pressured_pass_completion_pct 73.7
- Frenkie de Jong: Netherlands, DM, 476.0 min, 5 matches: **goals 1, per 90 0.19**. Other: non_penalty_goals 1; assists 1; shots 2; xg 0.721; npxg 0.721; key_passes 4; passes_attempted 364; passes_completed 327; progressive_passes 53; progressive_carries 15; pressures 80; pressured_passes_attempted 73; pressured_passes_completed 59; shot_creating_actions 8; xt_added 0.366; pass_completion_pct 89.8; pressured_pass_completion_pct 80.8
- Lucas Paquetá: Brazil, DM, 314.8 min, 4 matches: **goals 1, per 90 0.29**. Other: non_penalty_goals 1; assists 1; shots 4; xg 0.704; npxg 0.704; key_passes 6; passes_attempted 202; passes_completed 172; progressive_passes 27; progressive_carries 2; pressures 59; pressured_passes_attempted 28; pressured_passes_completed 25; shot_creating_actions 11; xt_added 0.175; pass_completion_pct 85.1; pressured_pass_completion_pct 89.3
- Moisés Caicedo: Ecuador, DM, 269.9 min, 3 matches: **goals 1, per 90 0.33**. Other: non_penalty_goals 1; assists 0; shots 3; xg 0.653; npxg 0.653; key_passes 0; passes_attempted 154; passes_completed 128; progressive_passes 18; progressive_carries 9; pressures 43; pressured_passes_attempted 34; pressured_passes_completed 24; shot_creating_actions 5; xt_added 0.07; pass_completion_pct 83.1; pressured_pass_completion_pct 70.6
- Remo Freuler: Switzerland, DM, 323.6 min, 4 matches: **goals 1, per 90 0.28**. Other: non_penalty_goals 1; assists 0; shots 3; xg 0.545; npxg 0.545; key_passes 0; passes_attempted 149; passes_completed 126; progressive_passes 16; progressive_carries 5; pressures 60; pressured_passes_attempted 24; pressured_passes_completed 16; shot_creating_actions 6; xt_added 0.043; pass_completion_pct 84.6; pressured_pass_completion_pct 66.7
- Yeltsin Tejeda: Costa Rica, DM, 270.0 min, 3 matches: **goals 1, per 90 0.33**. Other: non_penalty_goals 1; assists 1; shots 2; xg 0.522; npxg 0.522; key_passes 1; passes_attempted 98; passes_completed 79; progressive_passes 10; progressive_carries 0; pressures 39; pressured_passes_attempted 19; pressured_passes_completed 13; shot_creating_actions 3; xt_added 0.022; pass_completion_pct 80.6; pressured_pass_completion_pct 68.4
- Robert Lewandowski: Poland, ST, 360.0 min, 4 matches: **goals 2, per 90 0.50**. Other: non_penalty_goals 1; assists 1; shots 12; xg 3.126; npxg 1.559; key_passes 5; passes_attempted 91; passes_completed 65; progressive_passes 11; progressive_carries 10; pressures 39; pressured_passes_attempted 29; pressured_passes_completed 18; shot_creating_actions 11; xt_added -0.069; pass_completion_pct 71.4; pressured_pass_completion_pct 62.1
- Piotr Zieliński: Poland, CM, 329.1 min, 4 matches: **goals 1, per 90 0.27**. Other: non_penalty_goals 1; assists 0; shots 3; xg 0.584; npxg 0.584; key_passes 7; passes_attempted 153; passes_completed 124; progressive_passes 25; progressive_carries 13; pressures 47; pressured_passes_attempted 19; pressured_passes_completed 15; shot_creating_actions 12; xt_added 0.235; pass_completion_pct 81.0; pressured_pass_completion_pct 78.9
- Youssef En-Nesyri: Morocco, ST, 543.8 min, 7 matches: **goals 2, per 90 0.33**. Other: non_penalty_goals 2; assists 0; shots 11; xg 1.046; npxg 1.046; key_passes 1; passes_attempted 76; passes_completed 48; progressive_passes 2; progressive_carries 2; pressures 113; pressured_passes_attempted 19; pressured_passes_completed 9; shot_creating_actions 3; xt_added 0.121; pass_completion_pct 63.2; pressured_pass_completion_pct 47.4
- Mislav Oršić: Croatia, W, 162.3 min, 6 matches: **goals 1, per 90 0.55**. Other: non_penalty_goals 1; assists 2; shots 9; xg 0.276; npxg 0.276; key_passes 5; passes_attempted 55; passes_completed 42; progressive_passes 5; progressive_carries 11; pressures 29; pressured_passes_attempted 11; pressured_passes_completed 7; shot_creating_actions 7; xt_added 0.461; pass_completion_pct 76.4; pressured_pass_completion_pct 63.6
- Bruno Petković: Croatia, ST, 229.5 min, 6 matches: **goals 1, per 90 0.39**. Other: non_penalty_goals 1; assists 0; shots 1; xg 0.1; npxg 0.1; key_passes 4; passes_attempted 80; passes_completed 44; progressive_passes 7; progressive_carries 9; pressures 30; pressured_passes_attempted 26; pressured_passes_completed 15; shot_creating_actions 7; xt_added 0.001; pass_completion_pct 55.0; pressured_pass_completion_pct 57.7
- Luka Modrić: Croatia, CM, 654.4 min, 7 matches: **goals 0, per 90 0.00**. Other: non_penalty_goals 0; assists 0; shots 6; xg 0.344; npxg 0.344; key_passes 6; passes_attempted 549; passes_completed 463; progressive_passes 107; progressive_carries 42; pressures 115; pressured_passes_attempted 68; pressured_passes_completed 54; shot_creating_actions 19; xt_added 1.111; pass_completion_pct 84.3; pressured_pass_completion_pct 79.4
- Mateo Kovačić: Croatia, CM, 637.8 min, 7 matches: **goals 0, per 90 0.00**. Other: non_penalty_goals 0; assists 0; shots 3; xg 0.345; npxg 0.345; key_passes 9; passes_attempted 456; passes_completed 416; progressive_passes 71; progressive_carries 37; pressures 136; pressured_passes_attempted 59; pressured_passes_completed 52; shot_creating_actions 16; xt_added 0.913; pass_completion_pct 91.2; pressured_pass_completion_pct 88.1
- Andrija Živković: Serbia, FB, 212.1 min, 3 matches: **goals 0, per 90 0.00**. Other: non_penalty_goals 0; assists 2; shots 1; xg 0.03; npxg 0.03; key_passes 4; passes_attempted 99; passes_completed 73; progressive_passes 12; progressive_carries 13; pressures 24; pressured_passes_attempted 10; pressured_passes_completed 4; shot_creating_actions 7; xt_added 0.548; pass_completion_pct 73.7; pressured_pass_completion_pct 40.0
- Sofiane Boufal: Morocco, W, 476.7 min, 7 matches: **goals 0, per 90 0.00**. Other: non_penalty_goals 0; assists 0; shots 7; xg 0.316; npxg 0.316; key_passes 4; passes_attempted 134; passes_completed 107; progressive_passes 23; progressive_carries 33; pressures 93; pressured_passes_attempted 18; pressured_passes_completed 11; shot_creating_actions 15; xt_added 0.985; pass_completion_pct 79.9; pressured_pass_completion_pct 61.1

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A014

**Question:** How many key passes did Messi register during the 2022 World Cup?

**Ground truth** (Key passes for Lionel Messi, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Lionel Messi | Argentina | 19 | 690 | 7 |

**Naive answer:**

> Lionel Messi registered 19 key passes during the 2022 World Cup.

**Reference stats** (true tournament totals):

- Lionel Messi: Argentina, ST, 690.0 min, 7 matches: **key_passes 19, per 90 2.48**. Other: goals 7; non_penalty_goals 3; assists 3; shots 32; xg 6.032; npxg 2.114; passes_attempted 371; passes_completed 306; progressive_passes 79; progressive_carries 61; pressures 89; pressured_passes_attempted 75; pressured_passes_completed 65; shot_creating_actions 41; xt_added 1.759; pass_completion_pct 82.5; pressured_pass_completion_pct 86.7

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A015

**Question:** Which three Morocco centre-backs completed the highest number of progressive passes during the 2022 World Cup, with a minimum of 90 minutes played?

**Ground truth** (The 3 players with the most progressive passes (simplified), among centre-backs (CB), playing for Morocco, with at least 90 minutes, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Romain Saïss | Morocco | 16 | 468 | 6 |
| 2 | Jawad El Yamiq | Morocco | 8 | 309 | 6 |
| 3 | Achraf Dari | Morocco | 7 | 186 | 3 |

**Naive answer:**

> The three Morocco centre-backs who completed the highest number of progressive passes during the 2022 World Cup (minimum 90 minutes played) are:
> 
> 1. **Romain Saïss** - 16 progressive passes  
> 2. **Achraf Dari** - 7 progressive passes  
> 3. **Nayef Aguerd** - 7 progressive passes

**Reference stats** (true tournament totals):

- Romain Saïss: Morocco, CB, 467.6 min, 6 matches: **progressive_passes 16, per 90 3.08**. Other: goals 1; non_penalty_goals 1; assists 0; shots 1; xg 0.565; npxg 0.565; key_passes 0; passes_attempted 193; passes_completed 158; progressive_carries 5; pressures 35; pressured_passes_attempted 10; pressured_passes_completed 6; shot_creating_actions 1; xt_added 0.294; pass_completion_pct 81.9; pressured_pass_completion_pct 60.0
- Jawad El Yamiq: Morocco, CB, 309.4 min, 6 matches: **progressive_passes 8, per 90 2.33**. Other: goals 0; non_penalty_goals 0; assists 0; shots 1; xg 0.064; npxg 0.064; key_passes 0; passes_attempted 160; passes_completed 143; progressive_carries 2; pressures 18; pressured_passes_attempted 15; pressured_passes_completed 10; shot_creating_actions 2; xt_added 0.095; pass_completion_pct 89.4; pressured_pass_completion_pct 66.7
- Achraf Dari: Morocco, CB, 186.4 min, 3 matches: **progressive_passes 7, per 90 3.38**. Other: goals 1; non_penalty_goals 1; assists 0; shots 1; xg 0.418; npxg 0.418; key_passes 0; passes_attempted 107; passes_completed 96; progressive_carries 0; pressures 17; pressured_passes_attempted 3; pressured_passes_completed 0; shot_creating_actions 0; xt_added 0.099; pass_completion_pct 89.7; pressured_pass_completion_pct 0.0
- Nayef Aguerd: Morocco, CB, 354.0 min, 4 matches: **progressive_passes 7, per 90 1.78**. Other: goals 0; non_penalty_goals 0; assists 0; shots 1; xg 0.251; npxg 0.251; key_passes 1; passes_attempted 154; passes_completed 133; progressive_carries 2; pressures 16; pressured_passes_attempted 8; pressured_passes_completed 2; shot_creating_actions 3; xt_added 0.099; pass_completion_pct 86.4; pressured_pass_completion_pct 25.0

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A016

**Question:** How many passes did Kimmich attempt while under pressure during the 2022 World Cup?

**Ground truth** (Passes attempted under pressure for Joshua Kimmich, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Joshua Kimmich | Germany | 30 | 270 | 3 |

**Naive answer:**

> Joshua Kimmich attempted 35 passes while under pressure during the 2022 World Cup.

**Reference stats** (true tournament totals):

- Joshua Kimmich: Germany, DM, 270.0 min, 3 matches: **pressured_passes_attempted 30, per 90 10.00**. Other: goals 0; non_penalty_goals 0; assists 0; shots 7; xg 0.335; npxg 0.335; key_passes 8; passes_attempted 271; passes_completed 229; progressive_passes 48; progressive_carries 8; pressures 35; pressured_passes_completed 25; shot_creating_actions 17; xt_added 1.091; pass_completion_pct 84.5; pressured_pass_completion_pct 83.3

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A017

**Question:** Who were the top five assist providers during the 2022 World Cup tournament?

**Ground truth** (The 5 players with the most assists, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Antoine Griezmann | France | 3 | 538 | 7 |
| 1 | Bruno Fernandes | Portugal | 3 | 357 | 4 |
| 1 | Harry Kane | England | 3 | 402 | 5 |
| 1 | Ivan Perišić | Croatia | 3 | 670 | 7 |
| 1 | Lionel Messi | Argentina | 3 | 690 | 7 |

**Naive answer:**

> The top five assist providers during the 2022 World Cup were:
> 
> 1. **Ángel Di María (Argentina)** - 1 assist  
> 2. **Kylian Mbappé (France)** - 2 assists  
> 3. **Adrien Rabiot (France)** - 1 assist  
> 4. **Son Heung-Min (South Korea)** - 1 assist  
> 5. **Daley Blind (Netherlands)** - 1 assist

**Reference stats** (true tournament totals):

- Antoine Griezmann: France, AM, 538.2 min, 7 matches: **assists 3, per 90 0.50**. Other: goals 0; non_penalty_goals 0; shots 6; xg 0.496; npxg 0.496; key_passes 20; passes_attempted 323; passes_completed 255; progressive_passes 46; progressive_carries 23; pressures 125; pressured_passes_attempted 26; pressured_passes_completed 22; shot_creating_actions 30; xt_added 1.513; pass_completion_pct 78.9; pressured_pass_completion_pct 84.6
- Bruno Fernandes: Portugal, W, 356.7 min, 4 matches: **assists 3, per 90 0.76**. Other: goals 2; non_penalty_goals 1; shots 8; xg 1.031; npxg 0.248; key_passes 9; passes_attempted 231; passes_completed 186; progressive_passes 40; progressive_carries 14; pressures 62; pressured_passes_attempted 23; pressured_passes_completed 17; shot_creating_actions 16; xt_added 0.766; pass_completion_pct 80.5; pressured_pass_completion_pct 73.9
- Harry Kane: England, ST, 402.3 min, 5 matches: **assists 3, per 90 0.67**. Other: goals 2; non_penalty_goals 1; shots 12; xg 2.331; npxg 0.764; key_passes 5; passes_attempted 97; passes_completed 64; progressive_passes 21; progressive_carries 10; pressures 31; pressured_passes_attempted 25; pressured_passes_completed 12; shot_creating_actions 7; xt_added 0.618; pass_completion_pct 66.0; pressured_pass_completion_pct 48.0
- Ivan Perišić: Croatia, W, 669.6 min, 7 matches: **assists 3, per 90 0.40**. Other: goals 1; non_penalty_goals 1; shots 16; xg 0.756; npxg 0.756; key_passes 9; passes_attempted 304; passes_completed 214; progressive_passes 34; progressive_carries 39; pressures 98; pressured_passes_attempted 51; pressured_passes_completed 35; shot_creating_actions 18; xt_added 0.994; pass_completion_pct 70.4; pressured_pass_completion_pct 68.6
- Lionel Messi: Argentina, ST, 690.0 min, 7 matches: **assists 3, per 90 0.39**. Other: goals 7; non_penalty_goals 3; shots 32; xg 6.032; npxg 2.114; key_passes 19; passes_attempted 371; passes_completed 306; progressive_passes 79; progressive_carries 61; pressures 89; pressured_passes_attempted 75; pressured_passes_completed 65; shot_creating_actions 41; xt_added 1.759; pass_completion_pct 82.5; pressured_pass_completion_pct 86.7
- Ángel Di María: Argentina, W, 289.9 min, 5 matches: **assists 1, per 90 0.31**. Other: goals 1; non_penalty_goals 1; shots 7; xg 0.534; npxg 0.534; key_passes 11; passes_attempted 164; passes_completed 126; progressive_passes 24; progressive_carries 34; pressures 34; pressured_passes_attempted 23; pressured_passes_completed 19; shot_creating_actions 20; xt_added 1.329; pass_completion_pct 76.8; pressured_pass_completion_pct 82.6
- Kylian Mbappé: France, W, 597.4 min, 7 matches: **assists 2, per 90 0.30**. Other: goals 8; non_penalty_goals 6; shots 31; xg 4.233; npxg 2.666; key_passes 11; passes_attempted 233; passes_completed 180; progressive_passes 31; progressive_carries 71; pressures 37; pressured_passes_attempted 26; pressured_passes_completed 22; shot_creating_actions 41; xt_added 1.899; pass_completion_pct 77.3; pressured_pass_completion_pct 84.6
- Adrien Rabiot: France, DM, 482.4 min, 6 matches: **assists 1, per 90 0.19**. Other: goals 1; non_penalty_goals 1; shots 9; xg 0.728; npxg 0.728; key_passes 2; passes_attempted 285; passes_completed 246; progressive_passes 39; progressive_carries 14; pressures 84; pressured_passes_attempted 37; pressured_passes_completed 26; shot_creating_actions 9; xt_added 0.226; pass_completion_pct 86.3; pressured_pass_completion_pct 70.3
- Son Heung-Min: South Korea, W, 360.0 min, 4 matches: **assists 1, per 90 0.25**. Other: goals 0; non_penalty_goals 0; shots 9; xg 0.454; npxg 0.454; key_passes 6; passes_attempted 122; passes_completed 84; progressive_passes 9; progressive_carries 21; pressures 36; pressured_passes_attempted 26; pressured_passes_completed 17; shot_creating_actions 14; xt_added 0.443; pass_completion_pct 68.9; pressured_pass_completion_pct 65.4
- Daley Blind: Netherlands, FB, 424.0 min, 5 matches: **assists 1, per 90 0.21**. Other: goals 1; non_penalty_goals 1; shots 5; xg 0.522; npxg 0.522; key_passes 2; passes_attempted 304; passes_completed 260; progressive_passes 41; progressive_carries 7; pressures 83; pressured_passes_attempted 28; pressured_passes_completed 24; shot_creating_actions 6; xt_added 0.728; pass_completion_pct 85.5; pressured_pass_completion_pct 85.7

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A018

**Question:** Who had the best pass completion rate in the 2022 World Cup?

**Ground truth** (The player with the highest pass completion %, with at least 270 minutes (default threshold), World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Marquinhos | Brazil | 96.1 | 426 | 5 |

**Naive answer:**

> The best pass completion rate in the 2022 World Cup was achieved by **Raphaël Varane** of France, with a **96.5%** pass completion rate (251/260). This is the highest among players with at least 270 minutes played.

**Reference stats** (true tournament totals):

- Marquinhos: Brazil, CB, 425.8 min, 5 matches: **pass_completion_pct 96.1**. Other: goals 0; non_penalty_goals 0; assists 0; shots 1; xg 0.078; npxg 0.078; key_passes 5; passes_attempted 359; passes_completed 345; progressive_passes 62; progressive_carries 22; pressures 21; pressured_passes_attempted 22; pressured_passes_completed 17; shot_creating_actions 9; xt_added 1.131; pressured_pass_completion_pct 77.3
- Raphaël Varane: France, CB, 518.9 min, 6 matches: **pass_completion_pct 89.6**. Other: goals 0; non_penalty_goals 0; assists 0; shots 3; xg 0.264; npxg 0.264; key_passes 0; passes_attempted 280; passes_completed 251; progressive_passes 30; progressive_carries 23; pressures 16; pressured_passes_attempted 16; pressured_passes_completed 11; shot_creating_actions 2; xt_added 0.203; pressured_pass_completion_pct 68.8

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A019

**Question:** Top 5 players in the 2022 World Cup with the most xT per 90 added, please?

**Ground truth** (The 5 players with the highest expected threat (xT) added per 90, with at least 270 minutes (default threshold), World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Ángel Di María | Argentina | 0.413 | 290 | 5 |
| 2 | Raphinha | Brazil | 0.406 | 316 | 5 |
| 3 | Kevin De Bruyne | Belgium | 0.39 | 270 | 3 |
| 4 | Vinícius Júnior | Brazil | 0.371 | 301 | 4 |
| 5 | Joshua Kimmich | Germany | 0.364 | 270 | 3 |

**Naive answer:**

> The top 5 players in the 2022 World Cup with the most xT (expected threat) per 90 minutes added are:
> 
> 1. **Álvaro Morata (Spain)** - 1.513 xT  
> 2. **Antoine Griezmann (France)** - 1.513 xT  
> 3. **Christian Pulisic (United States)** - 0.679 xT  
> 4. **Kylian Mbappé (France)** - 0.599 xT  
> 5. **Hakim Ziyech (Morocco)** - 0.541 xT

**Reference stats** (true tournament totals):

- Ángel Di María: Argentina, W, 289.9 min, 5 matches: **xt_added 1.329, per 90 0.413**. Other: goals 1; non_penalty_goals 1; assists 1; shots 7; xg 0.534; npxg 0.534; key_passes 11; passes_attempted 164; passes_completed 126; progressive_passes 24; progressive_carries 34; pressures 34; pressured_passes_attempted 23; pressured_passes_completed 19; shot_creating_actions 20; pass_completion_pct 76.8; pressured_pass_completion_pct 82.6
- Raphinha: Brazil, W, 316.4 min, 5 matches: **xt_added 1.426, per 90 0.406**. Other: goals 0; non_penalty_goals 0; assists 0; shots 8; xg 0.923; npxg 0.923; key_passes 8; passes_attempted 150; passes_completed 115; progressive_passes 14; progressive_carries 26; pressures 51; pressured_passes_attempted 16; pressured_passes_completed 11; shot_creating_actions 20; pass_completion_pct 76.7; pressured_pass_completion_pct 68.8
- Kevin De Bruyne: Belgium, W, 270.0 min, 3 matches: **xt_added 1.17, per 90 0.390**. Other: goals 0; non_penalty_goals 0; assists 0; shots 7; xg 0.178; npxg 0.178; key_passes 8; passes_attempted 140; passes_completed 100; progressive_passes 31; progressive_carries 16; pressures 25; pressured_passes_attempted 24; pressured_passes_completed 14; shot_creating_actions 10; pass_completion_pct 71.4; pressured_pass_completion_pct 58.3
- Vinícius Júnior: Brazil, W, 300.7 min, 4 matches: **xt_added 1.241, per 90 0.371**. Other: goals 1; non_penalty_goals 1; assists 2; shots 9; xg 0.812; npxg 0.812; key_passes 8; passes_attempted 91; passes_completed 70; progressive_passes 9; progressive_carries 29; pressures 37; pressured_passes_attempted 13; pressured_passes_completed 9; shot_creating_actions 14; pass_completion_pct 76.9; pressured_pass_completion_pct 69.2
- Joshua Kimmich: Germany, DM, 270.0 min, 3 matches: **xt_added 1.091, per 90 0.364**. Other: goals 0; non_penalty_goals 0; assists 0; shots 7; xg 0.335; npxg 0.335; key_passes 8; passes_attempted 271; passes_completed 229; progressive_passes 48; progressive_carries 8; pressures 35; pressured_passes_attempted 30; pressured_passes_completed 25; shot_creating_actions 17; pass_completion_pct 84.5; pressured_pass_completion_pct 83.3
- Álvaro Morata: Spain, ST, 183.9 min, 4 matches: **xt_added -0.044, per 90 -0.022**. Other: goals 3; non_penalty_goals 3; assists 1; shots 8; xg 1.109; npxg 1.109; key_passes 1; passes_attempted 40; passes_completed 27; progressive_passes 5; progressive_carries 7; pressures 26; pressured_passes_attempted 11; pressured_passes_completed 8; shot_creating_actions 3; pass_completion_pct 67.5; pressured_pass_completion_pct 72.7
- Antoine Griezmann: France, AM, 538.2 min, 7 matches: **xt_added 1.513, per 90 0.253**. Other: goals 0; non_penalty_goals 0; assists 3; shots 6; xg 0.496; npxg 0.496; key_passes 20; passes_attempted 323; passes_completed 255; progressive_passes 46; progressive_carries 23; pressures 125; pressured_passes_attempted 26; pressured_passes_completed 22; shot_creating_actions 30; pass_completion_pct 78.9; pressured_pass_completion_pct 84.6
- Christian Pulisic: United States, W, 315.0 min, 4 matches: **xt_added 0.679, per 90 0.194**. Other: goals 1; non_penalty_goals 1; assists 2; shots 9; xg 1.138; npxg 1.138; key_passes 9; passes_attempted 139; passes_completed 84; progressive_passes 21; progressive_carries 33; pressures 44; pressured_passes_attempted 27; pressured_passes_completed 20; shot_creating_actions 16; pass_completion_pct 60.4; pressured_pass_completion_pct 74.1
- Kylian Mbappé: France, W, 597.4 min, 7 matches: **xt_added 1.899, per 90 0.286**. Other: goals 8; non_penalty_goals 6; assists 2; shots 31; xg 4.233; npxg 2.666; key_passes 11; passes_attempted 233; passes_completed 180; progressive_passes 31; progressive_carries 71; pressures 37; pressured_passes_attempted 26; pressured_passes_completed 22; shot_creating_actions 41; pass_completion_pct 77.3; pressured_pass_completion_pct 84.6
- Hakim Ziyech: Morocco, W, 636.2 min, 7 matches: **xt_added 0.541, per 90 0.077**. Other: goals 1; non_penalty_goals 1; assists 1; shots 10; xg 0.312; npxg 0.312; key_passes 7; passes_attempted 300; passes_completed 210; progressive_passes 40; progressive_carries 28; pressures 137; pressured_passes_attempted 31; pressured_passes_completed 23; shot_creating_actions 20; pass_completion_pct 70.0; pressured_pass_completion_pct 74.2

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A020

**Question:** Which 10 midfielders had the lowest xT (expected threat) added per 90 minutes during the 2022 World Cup?

**Ground truth** (The 10 players with the lowest expected threat (xT) added per 90, among midfielders (AM, CM, DM), with at least 270 minutes (default threshold), World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Yeltsin Tejeda | Costa Rica | 0.007 | 270 | 3 |
| 2 | Nampalys Mendy | Senegal | 0.01 | 273 | 4 |
| 3 | Remo Freuler | Switzerland | 0.012 | 324 | 4 |
| 4 | Idrissa Gueye | Senegal | 0.013 | 270 | 3 |
| 5 | Grzegorz Krychowiak | Poland | 0.014 | 333 | 4 |
| 6 | Declan Rice | England | 0.015 | 417 | 5 |
| 7 | Selim Amallah | Morocco | 0.022 | 408 | 7 |
| 8 | Axel Witsel | Belgium | 0.024 | 270 | 3 |
| 9 | Alexis MacAllister | Argentina | 0.028 | 551 | 6 |
| 10 | Sofyan Amrabat | Morocco | 0.034 | 660 | 7 |

**Naive answer:**

> The 10 midfielders with the lowest xT (expected threat) added per 90 minutes (minimum 270 minutes) during the 2022 World Cup are:
> 
> 1. **Kieran Trippier (England, FB)** - 0.198  
> 2. **Jordan Henderson (England, CM)** - 0.498  
> 3. **Jordan Ayew (Ghana, W)** - 0.328  
> 4. **Edimilson Fernandes (Switzerland, FB)** - 0.062  
> 5. **Andreas Christensen (Denmark, CB)** - 0.233  
> 6. **Luka Modrić (Croatia, CM)** - 1.111  
> 7. **Munir (Morocco, GK)** - 0.019  
> 8. **Héctor Herrera (Mexico, DM)** - 0.212  
> 9. **Piotr Zieliński (Poland, CM)** - 0.235  
> 10. **Filip Kostić (Serbia, FB)** - 0.381

**Reference stats** (true tournament totals):

- Yeltsin Tejeda: Costa Rica, DM, 270.0 min, 3 matches: **xt_added 0.022, per 90 0.007**. Other: goals 1; non_penalty_goals 1; assists 1; shots 2; xg 0.522; npxg 0.522; key_passes 1; passes_attempted 98; passes_completed 79; progressive_passes 10; progressive_carries 0; pressures 39; pressured_passes_attempted 19; pressured_passes_completed 13; shot_creating_actions 3; pass_completion_pct 80.6; pressured_pass_completion_pct 68.4
- Nampalys Mendy: Senegal, DM, 273.1 min, 4 matches: **xt_added 0.032, per 90 0.011**. Other: goals 0; non_penalty_goals 0; assists 0; shots 2; xg 0.093; npxg 0.093; key_passes 1; passes_attempted 162; passes_completed 145; progressive_passes 25; progressive_carries 7; pressures 39; pressured_passes_attempted 10; pressured_passes_completed 7; shot_creating_actions 5; pass_completion_pct 89.5; pressured_pass_completion_pct 70.0
- Remo Freuler: Switzerland, DM, 323.6 min, 4 matches: **xt_added 0.043, per 90 0.012**. Other: goals 1; non_penalty_goals 1; assists 0; shots 3; xg 0.545; npxg 0.545; key_passes 0; passes_attempted 149; passes_completed 126; progressive_passes 16; progressive_carries 5; pressures 60; pressured_passes_attempted 24; pressured_passes_completed 16; shot_creating_actions 6; pass_completion_pct 84.6; pressured_pass_completion_pct 66.7
- Idrissa Gueye: Senegal, AM, 270.0 min, 3 matches: **xt_added 0.04, per 90 0.013**. Other: goals 0; non_penalty_goals 0; assists 0; shots 4; xg 0.332; npxg 0.332; key_passes 1; passes_attempted 131; passes_completed 106; progressive_passes 16; progressive_carries 5; pressures 67; pressured_passes_attempted 25; pressured_passes_completed 19; shot_creating_actions 8; pass_completion_pct 80.9; pressured_pass_completion_pct 76.0
- Grzegorz Krychowiak: Poland, DM, 333.4 min, 4 matches: **xt_added 0.05, per 90 0.013**. Other: goals 0; non_penalty_goals 0; assists 0; shots 1; xg 0.022; npxg 0.022; key_passes 2; passes_attempted 127; passes_completed 97; progressive_passes 15; progressive_carries 2; pressures 49; pressured_passes_attempted 20; pressured_passes_completed 14; shot_creating_actions 4; pass_completion_pct 76.4; pressured_pass_completion_pct 70.0
- Declan Rice: England, DM, 417.2 min, 5 matches: **xt_added 0.069, per 90 0.015**. Other: goals 0; non_penalty_goals 0; assists 0; shots 0; xg 0; npxg 0; key_passes 1; passes_attempted 327; passes_completed 306; progressive_passes 44; progressive_carries 12; pressures 38; pressured_passes_attempted 30; pressured_passes_completed 26; shot_creating_actions 5; pass_completion_pct 93.6; pressured_pass_completion_pct 86.7
- Selim Amallah: Morocco, CM, 407.6 min, 7 matches: **xt_added 0.1, per 90 0.022**. Other: goals 0; non_penalty_goals 0; assists 0; shots 2; xg 0.115; npxg 0.115; key_passes 3; passes_attempted 88; passes_completed 70; progressive_passes 7; progressive_carries 6; pressures 104; pressured_passes_attempted 19; pressured_passes_completed 17; shot_creating_actions 5; pass_completion_pct 79.5; pressured_pass_completion_pct 89.5
- Axel Witsel: Belgium, DM, 270.0 min, 3 matches: **xt_added 0.073, per 90 0.024**. Other: goals 0; non_penalty_goals 0; assists 0; shots 1; xg 0.025; npxg 0.025; key_passes 1; passes_attempted 176; passes_completed 169; progressive_passes 13; progressive_carries 5; pressures 43; pressured_passes_attempted 20; pressured_passes_completed 19; shot_creating_actions 3; pass_completion_pct 96.0; pressured_pass_completion_pct 95.0
- Alexis MacAllister: Argentina, CM, 551.3 min, 6 matches: **xt_added 0.171, per 90 0.028**. Other: goals 1; non_penalty_goals 1; assists 1; shots 7; xg 0.502; npxg 0.502; key_passes 8; passes_attempted 271; passes_completed 242; progressive_passes 35; progressive_carries 21; pressures 70; pressured_passes_attempted 43; pressured_passes_completed 34; shot_creating_actions 15; pass_completion_pct 89.3; pressured_pass_completion_pct 79.1
- Sofyan Amrabat: Morocco, DM, 660.0 min, 7 matches: **xt_added 0.247, per 90 0.034**. Other: goals 0; non_penalty_goals 0; assists 0; shots 1; xg 0.021; npxg 0.021; key_passes 2; passes_attempted 323; passes_completed 274; progressive_passes 42; progressive_carries 17; pressures 123; pressured_passes_attempted 24; pressured_passes_completed 18; shot_creating_actions 6; pass_completion_pct 84.8; pressured_pass_completion_pct 75.0
- Kieran Trippier: England, FB, 205.2 min, 3 matches: **xt_added 0.198, per 90 0.087**. Other: goals 0; non_penalty_goals 0; assists 0; shots 1; xg 0.043; npxg 0.043; key_passes 3; passes_attempted 195; passes_completed 165; progressive_passes 18; progressive_carries 1; pressures 28; pressured_passes_attempted 11; pressured_passes_completed 6; shot_creating_actions 4; pass_completion_pct 84.6; pressured_pass_completion_pct 54.5
- Jordan Henderson: England, CM, 271.7 min, 4 matches: **xt_added 0.498, per 90 0.165**. Other: goals 1; non_penalty_goals 1; assists 0; shots 2; xg 0.149; npxg 0.149; key_passes 4; passes_attempted 166; passes_completed 141; progressive_passes 20; progressive_carries 6; pressures 35; pressured_passes_attempted 15; pressured_passes_completed 13; shot_creating_actions 8; pass_completion_pct 84.9; pressured_pass_completion_pct 86.7
- Jordan Ayew: Ghana, W, 136.4 min, 3 matches: **xt_added 0.328, per 90 0.216**. Other: goals 0; non_penalty_goals 0; assists 1; shots 1; xg 0.071; npxg 0.071; key_passes 3; passes_attempted 44; passes_completed 34; progressive_passes 2; progressive_carries 5; pressures 35; pressured_passes_attempted 2; pressured_passes_completed 2; shot_creating_actions 5; pass_completion_pct 77.3; pressured_pass_completion_pct 100.0
- Edimilson Fernandes: Switzerland, FB, 144.3 min, 3 matches: **xt_added 0.062, per 90 0.039**. Other: goals 0; non_penalty_goals 0; assists 0; shots 1; xg 0.029; npxg 0.029; key_passes 3; passes_attempted 81; passes_completed 66; progressive_passes 2; progressive_carries 2; pressures 14; pressured_passes_attempted 10; pressured_passes_completed 9; shot_creating_actions 3; pass_completion_pct 81.5; pressured_pass_completion_pct 90.0
- Andreas Christensen: Denmark, CB, 270.0 min, 3 matches: **xt_added 0.233, per 90 0.078**. Other: goals 1; non_penalty_goals 1; assists 0; shots 2; xg 0.525; npxg 0.525; key_passes 0; passes_attempted 250; passes_completed 236; progressive_passes 32; progressive_carries 8; pressures 11; pressured_passes_attempted 17; pressured_passes_completed 13; shot_creating_actions 1; pass_completion_pct 94.4; pressured_pass_completion_pct 76.5
- Luka Modrić: Croatia, CM, 654.4 min, 7 matches: **xt_added 1.111, per 90 0.153**. Other: goals 0; non_penalty_goals 0; assists 0; shots 6; xg 0.344; npxg 0.344; key_passes 6; passes_attempted 549; passes_completed 463; progressive_passes 107; progressive_carries 42; pressures 115; pressured_passes_attempted 68; pressured_passes_completed 54; shot_creating_actions 19; pass_completion_pct 84.3; pressured_pass_completion_pct 79.4
- Munir: Morocco, GK, 90.0 min, 1 matches: **xt_added 0.019, per 90 0.019**. Other: goals 0; non_penalty_goals 0; assists 0; shots 0; xg 0; npxg 0; key_passes 0; passes_attempted 27; passes_completed 18; progressive_passes 0; progressive_carries 0; pressures 0; pressured_passes_attempted 0; pressured_passes_completed 0; shot_creating_actions 0; pass_completion_pct 66.7
- Héctor Herrera: Mexico, DM, 160.2 min, 2 matches: **xt_added 0.212, per 90 0.119**. Other: goals 0; non_penalty_goals 0; assists 0; shots 0; xg 0; npxg 0; key_passes 1; passes_attempted 75; passes_completed 63; progressive_passes 8; progressive_carries 2; pressures 26; pressured_passes_attempted 10; pressured_passes_completed 9; shot_creating_actions 3; pass_completion_pct 84.0; pressured_pass_completion_pct 90.0
- Piotr Zieliński: Poland, CM, 329.1 min, 4 matches: **xt_added 0.235, per 90 0.064**. Other: goals 1; non_penalty_goals 1; assists 0; shots 3; xg 0.584; npxg 0.584; key_passes 7; passes_attempted 153; passes_completed 124; progressive_passes 25; progressive_carries 13; pressures 47; pressured_passes_attempted 19; pressured_passes_completed 15; shot_creating_actions 12; pass_completion_pct 81.0; pressured_pass_completion_pct 78.9
- Filip Kostić: Serbia, FB, 180.0 min, 2 matches: **xt_added 0.381, per 90 0.191**. Other: goals 0; non_penalty_goals 0; assists 0; shots 1; xg 0.012; npxg 0.012; key_passes 1; passes_attempted 112; passes_completed 73; progressive_passes 12; progressive_carries 16; pressures 30; pressured_passes_attempted 14; pressured_passes_completed 8; shot_creating_actions 5; pass_completion_pct 65.2; pressured_pass_completion_pct 57.1

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A021

**Question:** how many passs did hwang in-beom compelted under pressure in the 2022 world cup?

**Ground truth** (Passes completed under pressure for Hwang In-Beom, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Hwang In-Beom | South Korea | 21 | 334 | 4 |

**Naive answer:**

> Hwang In-Beom completed 21 passes under pressure in the 2022 World Cup.

**Reference stats** (true tournament totals):

- Hwang In-Beom: South Korea, DM, 334.4 min, 4 matches: **pressured_passes_completed 21, per 90 5.65**. Other: goals 0; non_penalty_goals 0; assists 0; shots 6; xg 0.198; npxg 0.198; key_passes 3; passes_attempted 247; passes_completed 199; progressive_passes 43; progressive_carries 6; pressures 51; pressured_passes_attempted 31; shot_creating_actions 5; xt_added 0.268; pass_completion_pct 80.6; pressured_pass_completion_pct 67.7

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A022

**Question:** wich striker had the most gools in the 2022 world cup?

**Ground truth** (The player with the most goals, among strikers (ST), World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Lionel Messi | Argentina | 7 | 690 | 7 |

**Naive answer:**

> Lionel Messi from Argentina had the most goals in the 2022 World Cup, scoring 7 goals.

**Reference stats** (true tournament totals):

- Lionel Messi: Argentina, ST, 690.0 min, 7 matches: **goals 7, per 90 0.91**. Other: non_penalty_goals 3; assists 3; shots 32; xg 6.032; npxg 2.114; key_passes 19; passes_attempted 371; passes_completed 306; progressive_passes 79; progressive_carries 61; pressures 89; pressured_passes_attempted 75; pressured_passes_completed 65; shot_creating_actions 41; xt_added 1.759; pass_completion_pct 82.5; pressured_pass_completion_pct 86.7

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A023

**Question:** In the 2022 World Cup, how many times did Kimmich attempt a pass while under pressure?

**Ground truth** (Passes attempted under pressure for Joshua Kimmich, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Joshua Kimmich | Germany | 30 | 270 | 3 |

**Naive answer:**

> Joshua Kimmich attempted 30 passes while under pressure in the 2022 World Cup.

**Reference stats** (true tournament totals):

- Joshua Kimmich: Germany, DM, 270.0 min, 3 matches: **pressured_passes_attempted 30, per 90 10.00**. Other: goals 0; non_penalty_goals 0; assists 0; shots 7; xg 0.335; npxg 0.335; key_passes 8; passes_attempted 271; passes_completed 229; progressive_passes 48; progressive_carries 8; pressures 35; pressured_passes_completed 25; shot_creating_actions 17; xt_added 1.091; pass_completion_pct 84.5; pressured_pass_completion_pct 83.3

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A024

**Question:** how many pass attempt did kimmich make under pressure in the 2022 world cup?

**Ground truth** (Passes attempted under pressure for Joshua Kimmich, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Joshua Kimmich | Germany | 30 | 270 | 3 |

**Naive answer:**

> Joshua Kimmich made 30 pass attempts under pressure in the 2022 World Cup.

**Reference stats** (true tournament totals):

- Joshua Kimmich: Germany, DM, 270.0 min, 3 matches: **pressured_passes_attempted 30, per 90 10.00**. Other: goals 0; non_penalty_goals 0; assists 0; shots 7; xg 0.335; npxg 0.335; key_passes 8; passes_attempted 271; passes_completed 229; progressive_passes 48; progressive_carries 8; pressures 35; pressured_passes_completed 25; shot_creating_actions 17; xt_added 1.091; pass_completion_pct 84.5; pressured_pass_completion_pct 83.3

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A025

**Question:** Which five players completed the most progressive carries during the 2022 World Cup?

**Ground truth** (The 5 players with the most progressive carries, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Kylian Mbappé | France | 71 | 597 | 7 |
| 2 | Lionel Messi | Argentina | 61 | 690 | 7 |
| 3 | Luka Modrić | Croatia | 42 | 654 | 7 |
| 4 | Ivan Perišić | Croatia | 39 | 670 | 7 |
| 5 | Mateo Kovačić | Croatia | 37 | 638 | 7 |

**Naive answer:**

> The five players who completed the most progressive carries during the 2022 World Cup are:
> 
> 1. **Lionel Messi (Argentina, ST)** - 61
> 2. **Álvaro Morata (Spain, ST)** - 7
> 3. **Jordan Henderson (England, CM)** - 6
> 4. **Hakim Ziyech (Morocco, W)** - 28
> 5. **Christian Pulisic (United States, W)** - 33

**Reference stats** (true tournament totals):

- Kylian Mbappé: France, W, 597.4 min, 7 matches: **progressive_carries 71, per 90 10.70**. Other: goals 8; non_penalty_goals 6; assists 2; shots 31; xg 4.233; npxg 2.666; key_passes 11; passes_attempted 233; passes_completed 180; progressive_passes 31; pressures 37; pressured_passes_attempted 26; pressured_passes_completed 22; shot_creating_actions 41; xt_added 1.899; pass_completion_pct 77.3; pressured_pass_completion_pct 84.6
- Lionel Messi: Argentina, ST, 690.0 min, 7 matches: **progressive_carries 61, per 90 7.96**. Other: goals 7; non_penalty_goals 3; assists 3; shots 32; xg 6.032; npxg 2.114; key_passes 19; passes_attempted 371; passes_completed 306; progressive_passes 79; pressures 89; pressured_passes_attempted 75; pressured_passes_completed 65; shot_creating_actions 41; xt_added 1.759; pass_completion_pct 82.5; pressured_pass_completion_pct 86.7
- Luka Modrić: Croatia, CM, 654.4 min, 7 matches: **progressive_carries 42, per 90 5.78**. Other: goals 0; non_penalty_goals 0; assists 0; shots 6; xg 0.344; npxg 0.344; key_passes 6; passes_attempted 549; passes_completed 463; progressive_passes 107; pressures 115; pressured_passes_attempted 68; pressured_passes_completed 54; shot_creating_actions 19; xt_added 1.111; pass_completion_pct 84.3; pressured_pass_completion_pct 79.4
- Ivan Perišić: Croatia, W, 669.6 min, 7 matches: **progressive_carries 39, per 90 5.24**. Other: goals 1; non_penalty_goals 1; assists 3; shots 16; xg 0.756; npxg 0.756; key_passes 9; passes_attempted 304; passes_completed 214; progressive_passes 34; pressures 98; pressured_passes_attempted 51; pressured_passes_completed 35; shot_creating_actions 18; xt_added 0.994; pass_completion_pct 70.4; pressured_pass_completion_pct 68.6
- Mateo Kovačić: Croatia, CM, 637.8 min, 7 matches: **progressive_carries 37, per 90 5.22**. Other: goals 0; non_penalty_goals 0; assists 0; shots 3; xg 0.345; npxg 0.345; key_passes 9; passes_attempted 456; passes_completed 416; progressive_passes 71; pressures 136; pressured_passes_attempted 59; pressured_passes_completed 52; shot_creating_actions 16; xt_added 0.913; pass_completion_pct 91.2; pressured_pass_completion_pct 88.1
- Álvaro Morata: Spain, ST, 183.9 min, 4 matches: **progressive_carries 7, per 90 3.43**. Other: goals 3; non_penalty_goals 3; assists 1; shots 8; xg 1.109; npxg 1.109; key_passes 1; passes_attempted 40; passes_completed 27; progressive_passes 5; pressures 26; pressured_passes_attempted 11; pressured_passes_completed 8; shot_creating_actions 3; xt_added -0.044; pass_completion_pct 67.5; pressured_pass_completion_pct 72.7
- Jordan Henderson: England, CM, 271.7 min, 4 matches: **progressive_carries 6, per 90 1.99**. Other: goals 1; non_penalty_goals 1; assists 0; shots 2; xg 0.149; npxg 0.149; key_passes 4; passes_attempted 166; passes_completed 141; progressive_passes 20; pressures 35; pressured_passes_attempted 15; pressured_passes_completed 13; shot_creating_actions 8; xt_added 0.498; pass_completion_pct 84.9; pressured_pass_completion_pct 86.7
- Hakim Ziyech: Morocco, W, 636.2 min, 7 matches: **progressive_carries 28, per 90 3.96**. Other: goals 1; non_penalty_goals 1; assists 1; shots 10; xg 0.312; npxg 0.312; key_passes 7; passes_attempted 300; passes_completed 210; progressive_passes 40; pressures 137; pressured_passes_attempted 31; pressured_passes_completed 23; shot_creating_actions 20; xt_added 0.541; pass_completion_pct 70.0; pressured_pass_completion_pct 74.2
- Christian Pulisic: United States, W, 315.0 min, 4 matches: **progressive_carries 33, per 90 9.43**. Other: goals 1; non_penalty_goals 1; assists 2; shots 9; xg 1.138; npxg 1.138; key_passes 9; passes_attempted 139; passes_completed 84; progressive_passes 21; pressures 44; pressured_passes_attempted 27; pressured_passes_completed 20; shot_creating_actions 16; xt_added 0.679; pass_completion_pct 60.4; pressured_pass_completion_pct 74.1

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A026

**Question:** How many xG did Aziz Behich have?

**Ground truth** (Expected goals (xG) for Aziz Behich, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Aziz Behich | Australia | 0.13 | 360 | 4 |

**Naive answer:**

> Aziz Behich had an xG (expected goals) of 0.13.

**Reference stats** (true tournament totals):

- Aziz Behich: Australia, FB, 360.0 min, 4 matches: **xg 0.127, per 90 0.03**. Other: goals 0; non_penalty_goals 0; assists 0; shots 2; npxg 0.127; key_passes 0; passes_attempted 204; passes_completed 154; progressive_passes 9; progressive_carries 10; pressures 33; pressured_passes_attempted 16; pressured_passes_completed 11; shot_creating_actions 4; xt_added 0.237; pass_completion_pct 75.5; pressured_pass_completion_pct 68.8

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A027

**Question:** Which three players scored the least goals in the 2022 World Cup?

**Ground truth** (The 3 players with the fewest goals, with at least 270 minutes (default threshold), World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Aaron Mooy | Australia | 0 | 360 | 4 |
| 1 | Abdelkarim Hassan | Qatar | 0 | 270 | 3 |
| 1 | Abdou Diallo | Senegal | 0 | 331 | 4 |

**Naive answer:**

> The three players who scored the least goals in the 2022 World Cup (with at least 90 minutes played) are:
> 
> 1. Jordan Ayew (Ghana) - 0 goals  
> 2. Jordan Pickford (England) - 0 goals  
> 3. Edimilson Fernandes (Switzerland) - 0 goals

**Reference stats** (true tournament totals):

- Aaron Mooy: Australia, DM, 360.0 min, 4 matches: **goals 0, per 90 0.00**. Other: non_penalty_goals 0; assists 0; shots 1; xg 0.039; npxg 0.039; key_passes 1; passes_attempted 219; passes_completed 171; progressive_passes 29; progressive_carries 6; pressures 44; pressured_passes_attempted 25; pressured_passes_completed 13; shot_creating_actions 4; xt_added 0.144; pass_completion_pct 78.1; pressured_pass_completion_pct 52.0
- Abdelkarim Hassan: Qatar, CB, 270.0 min, 3 matches: **goals 0, per 90 0.00**. Other: non_penalty_goals 0; assists 0; shots 6; xg 0.275; npxg 0.275; key_passes 1; passes_attempted 158; passes_completed 125; progressive_passes 19; progressive_carries 16; pressures 29; pressured_passes_attempted 21; pressured_passes_completed 17; shot_creating_actions 3; xt_added 0.337; pass_completion_pct 79.1; pressured_pass_completion_pct 81.0
- Abdou Diallo: Senegal, CB, 331.4 min, 4 matches: **goals 0, per 90 0.00**. Other: non_penalty_goals 0; assists 0; shots 1; xg 0.035; npxg 0.035; key_passes 1; passes_attempted 183; passes_completed 142; progressive_passes 24; progressive_carries 9; pressures 25; pressured_passes_attempted 16; pressured_passes_completed 9; shot_creating_actions 2; xt_added 0.321; pass_completion_pct 77.6; pressured_pass_completion_pct 56.2
- Jordan Ayew: Ghana, W, 136.4 min, 3 matches: **goals 0, per 90 0.00**. Other: non_penalty_goals 0; assists 1; shots 1; xg 0.071; npxg 0.071; key_passes 3; passes_attempted 44; passes_completed 34; progressive_passes 2; progressive_carries 5; pressures 35; pressured_passes_attempted 2; pressured_passes_completed 2; shot_creating_actions 5; xt_added 0.328; pass_completion_pct 77.3; pressured_pass_completion_pct 100.0
- Jordan Pickford: England, GK, 450.0 min, 5 matches: **goals 0, per 90 0.00**. Other: non_penalty_goals 0; assists 0; shots 0; xg 0; npxg 0; key_passes 0; passes_attempted 161; passes_completed 126; progressive_passes 0; progressive_carries 0; pressures 0; pressured_passes_attempted 15; pressured_passes_completed 8; shot_creating_actions 2; xt_added 0.142; pass_completion_pct 78.3; pressured_pass_completion_pct 53.3
- Edimilson Fernandes: Switzerland, FB, 144.3 min, 3 matches: **goals 0, per 90 0.00**. Other: non_penalty_goals 0; assists 0; shots 1; xg 0.029; npxg 0.029; key_passes 3; passes_attempted 81; passes_completed 66; progressive_passes 2; progressive_carries 2; pressures 14; pressured_passes_attempted 10; pressured_passes_completed 9; shot_creating_actions 3; xt_added 0.062; pass_completion_pct 81.5; pressured_pass_completion_pct 90.0

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A028

**Question:** Which 3 players had the most non-penalty goals per 90?

**Ground truth** (The 3 players with the highest non-penalty goals per 90, with at least 270 minutes (default threshold), World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Bukayo Saka | England | 0.93 | 291 | 4 |
| 2 | Kylian Mbappé | France | 0.9 | 597 | 7 |
| 3 | Olivier Giroud | France | 0.85 | 422 | 6 |

**Naive answer:**

> The three players with the most non-penalty goals per 90 minutes are:
> 
> 1. **Lionel Messi (Argentina, ST)**: 2.11 per 90  
> 2. **Kylian Mbappé (France, W)**: 2.67 per 90  
> 3. **Harry Kane (England, ST)**: 0.76 per 90

**Reference stats** (true tournament totals):

- Bukayo Saka: England, W, 291.3 min, 4 matches: **non_penalty_goals 3, per 90 0.93**. Other: goals 3; assists 0; shots 7; xg 0.579; npxg 0.579; key_passes 5; passes_attempted 111; passes_completed 84; progressive_passes 11; progressive_carries 16; pressures 49; pressured_passes_attempted 29; pressured_passes_completed 22; shot_creating_actions 5; xt_added 0.581; pass_completion_pct 75.7; pressured_pass_completion_pct 75.9
- Kylian Mbappé: France, W, 597.4 min, 7 matches: **non_penalty_goals 6, per 90 0.90**. Other: goals 8; assists 2; shots 31; xg 4.233; npxg 2.666; key_passes 11; passes_attempted 233; passes_completed 180; progressive_passes 31; progressive_carries 71; pressures 37; pressured_passes_attempted 26; pressured_passes_completed 22; shot_creating_actions 41; xt_added 1.899; pass_completion_pct 77.3; pressured_pass_completion_pct 84.6
- Olivier Giroud: France, ST, 422.1 min, 6 matches: **non_penalty_goals 4, per 90 0.85**. Other: goals 4; assists 0; shots 17; xg 3.036; npxg 3.036; key_passes 2; passes_attempted 75; passes_completed 49; progressive_passes 9; progressive_carries 2; pressures 60; pressured_passes_attempted 25; pressured_passes_completed 12; shot_creating_actions 4; xt_added 0.16; pass_completion_pct 65.3; pressured_pass_completion_pct 48.0
- Lionel Messi: Argentina, ST, 690.0 min, 7 matches: **non_penalty_goals 3, per 90 0.39**. Other: goals 7; assists 3; shots 32; xg 6.032; npxg 2.114; key_passes 19; passes_attempted 371; passes_completed 306; progressive_passes 79; progressive_carries 61; pressures 89; pressured_passes_attempted 75; pressured_passes_completed 65; shot_creating_actions 41; xt_added 1.759; pass_completion_pct 82.5; pressured_pass_completion_pct 86.7
- Harry Kane: England, ST, 402.3 min, 5 matches: **non_penalty_goals 1, per 90 0.22**. Other: goals 2; assists 3; shots 12; xg 2.331; npxg 0.764; key_passes 5; passes_attempted 97; passes_completed 64; progressive_passes 21; progressive_carries 10; pressures 31; pressured_passes_attempted 25; pressured_passes_completed 12; shot_creating_actions 7; xt_added 0.618; pass_completion_pct 66.0; pressured_pass_completion_pct 48.0

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A029

**Question:** can you list the top 5 players with the most assists from the 2022 world cup?

**Ground truth** (The 5 players with the most assists, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Antoine Griezmann | France | 3 | 538 | 7 |
| 1 | Bruno Fernandes | Portugal | 3 | 357 | 4 |
| 1 | Harry Kane | England | 3 | 402 | 5 |
| 1 | Ivan Perišić | Croatia | 3 | 670 | 7 |
| 1 | Lionel Messi | Argentina | 3 | 690 | 7 |

**Naive answer:**

> Here are the top 5 players with the most assists from the 2022 World Cup:
> 
> 1. **Ángel Di María (Argentina)** - 1 assist  
> 2. **Bruno Fernandes (Portugal)** - 3 assists  
> 3. **Christian Pulisic (United States)** - 2 assists  
> 4. **Davy Klaassen (Netherlands)** - 2 assists  
> 5. **Jordan Henderson (England)** - 2 assists

**Reference stats** (true tournament totals):

- Antoine Griezmann: France, AM, 538.2 min, 7 matches: **assists 3, per 90 0.50**. Other: goals 0; non_penalty_goals 0; shots 6; xg 0.496; npxg 0.496; key_passes 20; passes_attempted 323; passes_completed 255; progressive_passes 46; progressive_carries 23; pressures 125; pressured_passes_attempted 26; pressured_passes_completed 22; shot_creating_actions 30; xt_added 1.513; pass_completion_pct 78.9; pressured_pass_completion_pct 84.6
- Bruno Fernandes: Portugal, W, 356.7 min, 4 matches: **assists 3, per 90 0.76**. Other: goals 2; non_penalty_goals 1; shots 8; xg 1.031; npxg 0.248; key_passes 9; passes_attempted 231; passes_completed 186; progressive_passes 40; progressive_carries 14; pressures 62; pressured_passes_attempted 23; pressured_passes_completed 17; shot_creating_actions 16; xt_added 0.766; pass_completion_pct 80.5; pressured_pass_completion_pct 73.9
- Harry Kane: England, ST, 402.3 min, 5 matches: **assists 3, per 90 0.67**. Other: goals 2; non_penalty_goals 1; shots 12; xg 2.331; npxg 0.764; key_passes 5; passes_attempted 97; passes_completed 64; progressive_passes 21; progressive_carries 10; pressures 31; pressured_passes_attempted 25; pressured_passes_completed 12; shot_creating_actions 7; xt_added 0.618; pass_completion_pct 66.0; pressured_pass_completion_pct 48.0
- Ivan Perišić: Croatia, W, 669.6 min, 7 matches: **assists 3, per 90 0.40**. Other: goals 1; non_penalty_goals 1; shots 16; xg 0.756; npxg 0.756; key_passes 9; passes_attempted 304; passes_completed 214; progressive_passes 34; progressive_carries 39; pressures 98; pressured_passes_attempted 51; pressured_passes_completed 35; shot_creating_actions 18; xt_added 0.994; pass_completion_pct 70.4; pressured_pass_completion_pct 68.6
- Lionel Messi: Argentina, ST, 690.0 min, 7 matches: **assists 3, per 90 0.39**. Other: goals 7; non_penalty_goals 3; shots 32; xg 6.032; npxg 2.114; key_passes 19; passes_attempted 371; passes_completed 306; progressive_passes 79; progressive_carries 61; pressures 89; pressured_passes_attempted 75; pressured_passes_completed 65; shot_creating_actions 41; xt_added 1.759; pass_completion_pct 82.5; pressured_pass_completion_pct 86.7
- Ángel Di María: Argentina, W, 289.9 min, 5 matches: **assists 1, per 90 0.31**. Other: goals 1; non_penalty_goals 1; shots 7; xg 0.534; npxg 0.534; key_passes 11; passes_attempted 164; passes_completed 126; progressive_passes 24; progressive_carries 34; pressures 34; pressured_passes_attempted 23; pressured_passes_completed 19; shot_creating_actions 20; xt_added 1.329; pass_completion_pct 76.8; pressured_pass_completion_pct 82.6
- Christian Pulisic: United States, W, 315.0 min, 4 matches: **assists 2, per 90 0.57**. Other: goals 1; non_penalty_goals 1; shots 9; xg 1.138; npxg 1.138; key_passes 9; passes_attempted 139; passes_completed 84; progressive_passes 21; progressive_carries 33; pressures 44; pressured_passes_attempted 27; pressured_passes_completed 20; shot_creating_actions 16; xt_added 0.679; pass_completion_pct 60.4; pressured_pass_completion_pct 74.1
- Davy Klaassen: Netherlands, AM, 191.2 min, 4 matches: **assists 2, per 90 0.94**. Other: goals 1; non_penalty_goals 1; shots 2; xg 0.432; npxg 0.432; key_passes 3; passes_attempted 81; passes_completed 60; progressive_passes 7; progressive_carries 0; pressures 22; pressured_passes_attempted 22; pressured_passes_completed 15; shot_creating_actions 9; xt_added 0.044; pass_completion_pct 74.1; pressured_pass_completion_pct 68.2
- Jordan Henderson: England, CM, 271.7 min, 4 matches: **assists 0, per 90 0.00**. Other: goals 1; non_penalty_goals 1; shots 2; xg 0.149; npxg 0.149; key_passes 4; passes_attempted 166; passes_completed 141; progressive_passes 20; progressive_carries 6; pressures 35; pressured_passes_attempted 15; pressured_passes_completed 13; shot_creating_actions 8; xt_added 0.498; pass_completion_pct 84.9; pressured_pass_completion_pct 86.7

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A030

**Question:** Compare Aaron Mooy, Joshu kimmich, and ziyechs shot creatin actions from the 2022 world cup

**Ground truth** (Shot-creating actions for Aaron Mooy, Joshua Kimmich and Hakim Ziyech, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Hakim Ziyech | Morocco | 20 | 636 | 7 |
| 2 | Joshua Kimmich | Germany | 17 | 270 | 3 |
| 3 | Aaron Mooy | Australia | 4 | 360 | 4 |

**Naive answer:**

> From the 2022 World Cup, here is a comparison of their shot-creating actions:
> 
> - **Aaron Mooy (Australia)**: 4 shot-creating actions.
> - **Joshua Kimmich (Germany)**: 8 shot-creating actions.
> - **Hakim Ziyech (Morocco)**: 7 shot-creating actions.

**Reference stats** (true tournament totals):

- Hakim Ziyech: Morocco, W, 636.2 min, 7 matches: **shot_creating_actions 20, per 90 2.83**. Other: goals 1; non_penalty_goals 1; assists 1; shots 10; xg 0.312; npxg 0.312; key_passes 7; passes_attempted 300; passes_completed 210; progressive_passes 40; progressive_carries 28; pressures 137; pressured_passes_attempted 31; pressured_passes_completed 23; xt_added 0.541; pass_completion_pct 70.0; pressured_pass_completion_pct 74.2
- Joshua Kimmich: Germany, DM, 270.0 min, 3 matches: **shot_creating_actions 17, per 90 5.67**. Other: goals 0; non_penalty_goals 0; assists 0; shots 7; xg 0.335; npxg 0.335; key_passes 8; passes_attempted 271; passes_completed 229; progressive_passes 48; progressive_carries 8; pressures 35; pressured_passes_attempted 30; pressured_passes_completed 25; xt_added 1.091; pass_completion_pct 84.5; pressured_pass_completion_pct 83.3
- Aaron Mooy: Australia, DM, 360.0 min, 4 matches: **shot_creating_actions 4, per 90 1.00**. Other: goals 0; non_penalty_goals 0; assists 0; shots 1; xg 0.039; npxg 0.039; key_passes 1; passes_attempted 219; passes_completed 171; progressive_passes 29; progressive_carries 6; pressures 44; pressured_passes_attempted 25; pressured_passes_completed 13; xt_added 0.144; pass_completion_pct 78.1; pressured_pass_completion_pct 52.0

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A031

**Question:** frankowski how many shots in the wc 2022?

**Ground truth** (Shots for Przemysław Frankowski, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Przemysław Frankowski | Poland | 1 | 240 | 4 |

**Naive answer:**

> Przemysław Frankowski had 1 shot in the 2022 World Cup.

**Reference stats** (true tournament totals):

- Przemysław Frankowski: Poland, W, 240.1 min, 4 matches: **shots 1, per 90 0.37**. Other: goals 0; non_penalty_goals 0; assists 0; xg 0.044; npxg 0.044; key_passes 1; passes_attempted 73; passes_completed 51; progressive_passes 8; progressive_carries 4; pressures 39; pressured_passes_attempted 11; pressured_passes_completed 6; shot_creating_actions 3; xt_added 0.082; pass_completion_pct 69.9; pressured_pass_completion_pct 54.5

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A032

**Question:** Which Spanish midfield players made the most progressive passes per 90?

**Ground truth** (The 5 players with the highest progressive passes (simplified) per 90, among midfielders (AM, CM, DM), playing for Spain, with at least 270 minutes (default threshold), World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Pedri | Spain | 22.72 | 357 | 4 |
| 2 | Sergio Busquets | Spain | 11.39 | 363 | 4 |
| 3 | Gavi | Spain | 5.99 | 285 | 4 |

**Naive answer:**

> The Spanish midfield players who made the most progressive passes per 90 minutes are:
> 
> 1. **Dani Alves (FB)** - 14.00 progressive passes per 90 (note: Alves plays as a full-back but is often deployed in midfield roles).  
> 2. **Ferrán Torres (W)** - 10.00 progressive passes per 90.  
> 3. **Pedri (CM)** - 4.73 progressive passes per 90.  
> 4. **Gavi (CM)** - 2.43 progressive passes per 90.  
> 
> Among midfielders (DM/CM/AM), Ferrán Torres (wing) leads with 10.00, followed by Pedri (4.73).

**Reference stats** (true tournament totals):

- Pedri: Spain, CM, 356.5 min, 4 matches: **progressive_passes 90, per 90 22.72**. Other: goals 0; non_penalty_goals 0; assists 0; shots 0; xg 0; npxg 0; key_passes 5; passes_attempted 426; passes_completed 395; progressive_carries 17; pressures 54; pressured_passes_attempted 54; pressured_passes_completed 47; shot_creating_actions 13; xt_added 0.71; pass_completion_pct 92.7; pressured_pass_completion_pct 87.0
- Sergio Busquets: Spain, DM, 363.4 min, 4 matches: **progressive_passes 46, per 90 11.39**. Other: goals 0; non_penalty_goals 0; assists 0; shots 2; xg 0.104; npxg 0.104; key_passes 3; passes_attempted 290; passes_completed 265; progressive_carries 4; pressures 40; pressured_passes_attempted 34; pressured_passes_completed 30; shot_creating_actions 12; xt_added 0.199; pass_completion_pct 91.4; pressured_pass_completion_pct 88.2
- Gavi: Spain, CM, 285.4 min, 4 matches: **progressive_passes 19, per 90 5.99**. Other: goals 1; non_penalty_goals 1; assists 0; shots 1; xg 0.056; npxg 0.056; key_passes 2; passes_attempted 153; passes_completed 135; progressive_carries 12; pressures 57; pressured_passes_attempted 15; pressured_passes_completed 11; shot_creating_actions 7; xt_added 0.112; pass_completion_pct 88.2; pressured_pass_completion_pct 73.3
- Dani Alves: Brazil, FB, 117.4 min, 2 matches: **progressive_passes 12, per 90 9.20**. Other: goals 0; non_penalty_goals 0; assists 0; shots 3; xg 0.12; npxg 0.12; key_passes 0; passes_attempted 99; passes_completed 88; progressive_carries 1; pressures 16; pressured_passes_attempted 14; pressured_passes_completed 12; shot_creating_actions 3; xt_added 0.203; pass_completion_pct 88.9; pressured_pass_completion_pct 85.7
- Ferrán Torres: Spain, W, 218.8 min, 4 matches: **progressive_passes 6, per 90 2.47**. Other: goals 2; non_penalty_goals 1; assists 0; shots 4; xg 1.005; npxg 0.222; key_passes 1; passes_attempted 86; passes_completed 62; progressive_carries 10; pressures 30; pressured_passes_attempted 20; pressured_passes_completed 15; shot_creating_actions 2; xt_added 0.196; pass_completion_pct 72.1; pressured_pass_completion_pct 75.0

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A033

**Question:** Which three players recorded the highest non-penalty expected goals (xG) during the 2022 World Cup?

**Ground truth** (The 3 players with the most non-penalty xG, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Olivier Giroud | France | 3.04 | 422 | 6 |
| 2 | Kylian Mbappé | France | 2.67 | 597 | 7 |
| 3 | Breel Embolo | Switzerland | 2.39 | 325 | 4 |

**Naive answer:**

> The three players with the highest non-penalty expected goals (xG) during the 2022 World Cup are:
> 
> 1. **Lionel Messi (Argentina, ST)** - 2.11 xG  
> 2. **Harry Kane (England, ST)** - 0.76 xG  
> 3. **Kylian Mbappé (France, W)** - 2.67 xG

**Reference stats** (true tournament totals):

- Olivier Giroud: France, ST, 422.1 min, 6 matches: **npxg 3.036, per 90 0.65**. Other: goals 4; non_penalty_goals 4; assists 0; shots 17; xg 3.036; key_passes 2; passes_attempted 75; passes_completed 49; progressive_passes 9; progressive_carries 2; pressures 60; pressured_passes_attempted 25; pressured_passes_completed 12; shot_creating_actions 4; xt_added 0.16; pass_completion_pct 65.3; pressured_pass_completion_pct 48.0
- Kylian Mbappé: France, W, 597.4 min, 7 matches: **npxg 2.666, per 90 0.40**. Other: goals 8; non_penalty_goals 6; assists 2; shots 31; xg 4.233; key_passes 11; passes_attempted 233; passes_completed 180; progressive_passes 31; progressive_carries 71; pressures 37; pressured_passes_attempted 26; pressured_passes_completed 22; shot_creating_actions 41; xt_added 1.899; pass_completion_pct 77.3; pressured_pass_completion_pct 84.6
- Breel Embolo: Switzerland, ST, 324.8 min, 4 matches: **npxg 2.391, per 90 0.66**. Other: goals 2; non_penalty_goals 2; assists 0; shots 6; xg 2.391; key_passes 2; passes_attempted 66; passes_completed 50; progressive_passes 4; progressive_carries 13; pressures 47; pressured_passes_attempted 16; pressured_passes_completed 14; shot_creating_actions 4; xt_added 0.055; pass_completion_pct 75.8; pressured_pass_completion_pct 87.5
- Lionel Messi: Argentina, ST, 690.0 min, 7 matches: **npxg 2.114, per 90 0.28**. Other: goals 7; non_penalty_goals 3; assists 3; shots 32; xg 6.032; key_passes 19; passes_attempted 371; passes_completed 306; progressive_passes 79; progressive_carries 61; pressures 89; pressured_passes_attempted 75; pressured_passes_completed 65; shot_creating_actions 41; xt_added 1.759; pass_completion_pct 82.5; pressured_pass_completion_pct 86.7
- Harry Kane: England, ST, 402.3 min, 5 matches: **npxg 0.764, per 90 0.17**. Other: goals 2; non_penalty_goals 1; assists 3; shots 12; xg 2.331; key_passes 5; passes_attempted 97; passes_completed 64; progressive_passes 21; progressive_carries 10; pressures 31; pressured_passes_attempted 25; pressured_passes_completed 12; shot_creating_actions 7; xt_added 0.618; pass_completion_pct 66.0; pressured_pass_completion_pct 48.0

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A034

**Question:** Who scored the most goals in the World Cup?

**Ground truth** (The player with the most goals, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Kylian Mbappé | France | 8 | 597 | 7 |

**Naive answer:**

> Kylian Mbappé from France scored the most goals in the World Cup with 8 goals.

**Reference stats** (true tournament totals):

- Kylian Mbappé: France, W, 597.4 min, 7 matches: **goals 8, per 90 1.21**. Other: non_penalty_goals 6; assists 2; shots 31; xg 4.233; npxg 2.666; key_passes 11; passes_attempted 233; passes_completed 180; progressive_passes 31; progressive_carries 71; pressures 37; pressured_passes_attempted 26; pressured_passes_completed 22; shot_creating_actions 41; xt_added 1.899; pass_completion_pct 77.3; pressured_pass_completion_pct 84.6

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A035

**Question:** How many key passes did Nahuel Molina have?

**Ground truth** (Key passes for Nahuel Molina, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Nahuel Molina | Argentina | 3 | 568 | 7 |

**Naive answer:**

> Nahuel Molina had 3 key passes.

**Reference stats** (true tournament totals):

- Nahuel Molina: Argentina, FB, 567.7 min, 7 matches: **key_passes 3, per 90 0.48**. Other: goals 1; non_penalty_goals 1; assists 1; shots 2; xg 0.485; npxg 0.485; passes_attempted 360; passes_completed 296; progressive_passes 29; progressive_carries 16; pressures 72; pressured_passes_attempted 35; pressured_passes_completed 24; shot_creating_actions 10; xt_added 0.473; pass_completion_pct 82.2; pressured_pass_completion_pct 68.6

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A036

**Question:** What was Emiliano Martínez's average goals conceded per 90 minutes during the 2022 World Cup?

**Ground truth** (Goals per 90 for Emiliano Martínez, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Emiliano Martínez | Argentina | 0.0 | 690 | 7 |

**Naive answer:**

> Emiliano Martínez played 690.0 minutes as a goalkeeper for Argentina during the 2022 World Cup and did not concede any goals. Therefore, his average goals conceded per 90 minutes was 0.00.

**Reference stats** (true tournament totals):

- Emiliano Martínez: Argentina, GK, 690.0 min, 7 matches: **goals 0, per 90 0.00**. Other: non_penalty_goals 0; assists 0; shots 0; xg 0; npxg 0; key_passes 0; passes_attempted 186; passes_completed 123; progressive_passes 0; progressive_carries 0; pressures 0; pressured_passes_attempted 23; pressured_passes_completed 12; shot_creating_actions 0; xt_added 0.14; pass_completion_pct 66.1; pressured_pass_completion_pct 52.2

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A037

**Question:** johnston vs milos veljkovic - who has more progressive passes per 90?

**Ground truth** (Progressive passes (simplified) per 90 for Alistair Johnston and Milos Veljkovic, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Alistair Johnston | Canada | 8.0 | 270 | 3 |
| 2 | Milos Veljkovic | Serbia | 2.84 | 222 | 3 |

**Naive answer:**

> Alistair Johnston has more progressive passes per 90 than Milos Veljkovic. 
> 
> - **Alistair Johnston**: 24 progressive passes in 270 minutes → **8.00 per 90**.
> - **Milos Veljkovic**: 7 progressive passes in 221.8 minutes → **2.93 per 90**.

**Reference stats** (true tournament totals):

- Alistair Johnston: Canada, FB, 270.0 min, 3 matches: **progressive_passes 24, per 90 8.00**. Other: goals 0; non_penalty_goals 0; assists 0; shots 2; xg 0.672; npxg 0.672; key_passes 4; passes_attempted 187; passes_completed 156; progressive_carries 8; pressures 38; pressured_passes_attempted 21; pressured_passes_completed 21; shot_creating_actions 11; xt_added 0.471; pass_completion_pct 83.4; pressured_pass_completion_pct 100.0
- Milos Veljkovic: Serbia, CB, 221.8 min, 3 matches: **progressive_passes 7, per 90 2.84**. Other: goals 0; non_penalty_goals 0; assists 0; shots 0; xg 0; npxg 0; key_passes 0; passes_attempted 112; passes_completed 99; progressive_carries 2; pressures 24; pressured_passes_attempted 9; pressured_passes_completed 7; shot_creating_actions 1; xt_added 0.067; pass_completion_pct 88.4; pressured_pass_completion_pct 77.8

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A038

**Question:** Which player created more pressures, Kasper Schmeichel or Luka Modrić, during the 2022 World Cup?

**Ground truth** (Pressures for Kasper Schmeichel and Luka Modrić, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Luka Modrić | Croatia | 115 | 654 | 7 |
| 2 | Kasper Schmeichel | Denmark | 0 | 270 | 3 |

**Naive answer:**

> Luka Modrić created more pressures than Kasper Schmeichel during the 2022 World Cup. Modrić had 115 pressures, while Schmeichel had 0 pressures.

**Reference stats** (true tournament totals):

- Luka Modrić: Croatia, CM, 654.4 min, 7 matches: **pressures 115, per 90 15.82**. Other: goals 0; non_penalty_goals 0; assists 0; shots 6; xg 0.344; npxg 0.344; key_passes 6; passes_attempted 549; passes_completed 463; progressive_passes 107; progressive_carries 42; pressured_passes_attempted 68; pressured_passes_completed 54; shot_creating_actions 19; xt_added 1.111; pass_completion_pct 84.3; pressured_pass_completion_pct 79.4
- Kasper Schmeichel: Denmark, GK, 270.0 min, 3 matches: **pressures 0, per 90 0.00**. Other: goals 0; non_penalty_goals 0; assists 0; shots 0; xg 0; npxg 0; key_passes 0; passes_attempted 87; passes_completed 72; progressive_passes 1; progressive_carries 0; pressured_passes_attempted 6; pressured_passes_completed 4; shot_creating_actions 0; xt_added 0.131; pass_completion_pct 82.8; pressured_pass_completion_pct 66.7

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A039

**Question:** How many passes attempted under pressure did Kimmich have?

**Ground truth** (Passes attempted under pressure for Joshua Kimmich, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Joshua Kimmich | Germany | 30 | 270 | 3 |

**Naive answer:**

> Joshua Kimmich attempted **30 passes under pressure** during the 2022 World Cup.

**Reference stats** (true tournament totals):

- Joshua Kimmich: Germany, DM, 270.0 min, 3 matches: **pressured_passes_attempted 30, per 90 10.00**. Other: goals 0; non_penalty_goals 0; assists 0; shots 7; xg 0.335; npxg 0.335; key_passes 8; passes_attempted 271; passes_completed 229; progressive_passes 48; progressive_carries 8; pressures 35; pressured_passes_completed 25; shot_creating_actions 17; xt_added 1.091; pass_completion_pct 84.5; pressured_pass_completion_pct 83.3

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A040

**Question:** In the 2022 World Cup, which player recorded the highest count of progressive passes?

**Ground truth** (The player with the most progressive passes (simplified), World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Luka Modrić | Croatia | 107 | 654 | 7 |

**Naive answer:**

> The player who recorded the highest count of progressive passes in the 2022 World Cup was **Luka Modrić (Croatia)** with **107 progressive passes**.

**Reference stats** (true tournament totals):

- Luka Modrić: Croatia, CM, 654.4 min, 7 matches: **progressive_passes 107, per 90 14.72**. Other: goals 0; non_penalty_goals 0; assists 0; shots 6; xg 0.344; npxg 0.344; key_passes 6; passes_attempted 549; passes_completed 463; progressive_carries 42; pressures 115; pressured_passes_attempted 68; pressured_passes_completed 54; shot_creating_actions 19; xt_added 1.111; pass_completion_pct 84.3; pressured_pass_completion_pct 79.4

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---
