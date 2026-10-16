# Hand audit: naive-baseline answers

100 answers from the final naive-baseline run (Qwen3-32B with the stats table in its context, no query
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

**Question:** How many passes completed under pressure did Hwang In-Beom have?

**Ground truth** (Passes completed under pressure for Hwang In-Beom, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Hwang In-Beom | South Korea | 21 | 334 | 4 |

**Naive answer:**

> Hwang In-Beom had 21 passes completed under pressure.

**Reference stats** (true tournament totals):

- Hwang In-Beom: South Korea, DM, 334.4 min, 4 matches: **pressured_passes_completed 21, per 90 5.65**. Other: goals 0; non_penalty_goals 0; assists 0; shots 6; xg 0.198; npxg 0.198; key_passes 3; passes_attempted 247; passes_completed 199; progressive_passes 43; progressive_carries 6; pressures 51; pressured_passes_attempted 31; shot_creating_actions 5; xt_added 0.268; pass_completion_pct 80.6; pressured_pass_completion_pct 67.7

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A002

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

## A003

**Question:** messi how many key passes in world cup 2022?

**Ground truth** (Key passes for Lionel Messi, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Lionel Messi | Argentina | 19 | 690 | 7 |

**Naive answer:**

> Lionel Messi had 19 key passes in the 2022 World Cup.

**Reference stats** (true tournament totals):

- Lionel Messi: Argentina, ST, 690.0 min, 7 matches: **key_passes 19, per 90 2.48**. Other: goals 7; non_penalty_goals 3; assists 3; shots 32; xg 6.032; npxg 2.114; passes_attempted 371; passes_completed 306; progressive_passes 79; progressive_carries 61; pressures 89; pressured_passes_attempted 75; pressured_passes_completed 65; shot_creating_actions 41; xt_added 1.759; pass_completion_pct 82.5; pressured_pass_completion_pct 86.7

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A004

**Question:** whic 3 centra midfieders ha de most progresive passes in de 2022 world cug?

**Ground truth** (The 3 players with the most progressive passes (simplified), among central midfielders (CM), World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Luka Modrić | Croatia | 107 | 654 | 7 |
| 2 | Pedri | Spain | 90 | 357 | 4 |
| 3 | Mateo Kovačić | Croatia | 71 | 638 | 7 |

**Naive answer:**

> The three central midfielders with the most progressive passes in the 2022 World Cup are:
> 
> 1. **Luka Modrić (Croatia)** - 107 progressive passes  
> 2. **Mateo Kovačić (Croatia)** - 71 progressive passes  
> 3. **Kevin De Bruyne (Belgium)** - 31 progressive passes

**Reference stats** (true tournament totals):

- Luka Modrić: Croatia, CM, 654.4 min, 7 matches: **progressive_passes 107, per 90 14.72**. Other: goals 0; non_penalty_goals 0; assists 0; shots 6; xg 0.344; npxg 0.344; key_passes 6; passes_attempted 549; passes_completed 463; progressive_carries 42; pressures 115; pressured_passes_attempted 68; pressured_passes_completed 54; shot_creating_actions 19; xt_added 1.111; pass_completion_pct 84.3; pressured_pass_completion_pct 79.4
- Pedri: Spain, CM, 356.5 min, 4 matches: **progressive_passes 90, per 90 22.72**. Other: goals 0; non_penalty_goals 0; assists 0; shots 0; xg 0; npxg 0; key_passes 5; passes_attempted 426; passes_completed 395; progressive_carries 17; pressures 54; pressured_passes_attempted 54; pressured_passes_completed 47; shot_creating_actions 13; xt_added 0.71; pass_completion_pct 92.7; pressured_pass_completion_pct 87.0
- Mateo Kovačić: Croatia, CM, 637.8 min, 7 matches: **progressive_passes 71, per 90 10.02**. Other: goals 0; non_penalty_goals 0; assists 0; shots 3; xg 0.345; npxg 0.345; key_passes 9; passes_attempted 456; passes_completed 416; progressive_carries 37; pressures 136; pressured_passes_attempted 59; pressured_passes_completed 52; shot_creating_actions 16; xt_added 0.913; pass_completion_pct 91.2; pressured_pass_completion_pct 88.1
- Kevin De Bruyne: Belgium, W, 270.0 min, 3 matches: **progressive_passes 31, per 90 10.33**. Other: goals 0; non_penalty_goals 0; assists 0; shots 7; xg 0.178; npxg 0.178; key_passes 8; passes_attempted 140; passes_completed 100; progressive_carries 16; pressures 25; pressured_passes_attempted 24; pressured_passes_completed 14; shot_creating_actions 10; xt_added 1.17; pass_completion_pct 71.4; pressured_pass_completion_pct 58.3

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A005

**Question:** Out of all players in the 2022 World Cup, which three had the most passes attempted, provided they met the 450-minute threshold?

**Ground truth** (The 3 players with the most passes attempted, with at least 450 minutes, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Nicolás Otamendi | Argentina | 565 | 690 | 7 |
| 2 | Rodrigo De Paul | Argentina | 563 | 601 | 7 |
| 3 | Luka Modrić | Croatia | 549 | 654 | 7 |

**Naive answer:**

> The three players with the most passes attempted (minimum 450 minutes) are:
> 
> 1. **Rodri (Spain, CB)** – 679 passes attempted  
> 2. **Luka Modrić (Croatia, CM)** – 549 passes attempted  
> 3. **Kylian Mbappé (France, W)** – 233 passes attempted

**Reference stats** (true tournament totals):

- Nicolás Otamendi: Argentina, CB, 690.0 min, 7 matches: **passes_attempted 565, per 90 73.70**. Other: goals 0; non_penalty_goals 0; assists 1; shots 1; xg 0.048; npxg 0.048; key_passes 2; passes_completed 528; progressive_passes 53; progressive_carries 15; pressures 54; pressured_passes_attempted 35; pressured_passes_completed 20; shot_creating_actions 6; xt_added 0.477; pass_completion_pct 93.5; pressured_pass_completion_pct 57.1
- Rodrigo De Paul: Argentina, CM, 601.0 min, 7 matches: **passes_attempted 563, per 90 84.31**. Other: goals 0; non_penalty_goals 0; assists 0; shots 7; xg 0.57; npxg 0.57; key_passes 7; passes_completed 475; progressive_passes 70; progressive_carries 35; pressures 111; pressured_passes_attempted 49; pressured_passes_completed 40; shot_creating_actions 16; xt_added 0.568; pass_completion_pct 84.4; pressured_pass_completion_pct 81.6
- Luka Modrić: Croatia, CM, 654.4 min, 7 matches: **passes_attempted 549, per 90 75.50**. Other: goals 0; non_penalty_goals 0; assists 0; shots 6; xg 0.344; npxg 0.344; key_passes 6; passes_completed 463; progressive_passes 107; progressive_carries 42; pressures 115; pressured_passes_attempted 68; pressured_passes_completed 54; shot_creating_actions 19; xt_added 1.111; pass_completion_pct 84.3; pressured_pass_completion_pct 79.4
- Rodri: Spain, CB, 390.0 min, 4 matches: **passes_attempted 679, per 90 156.69**. Other: goals 0; non_penalty_goals 0; assists 0; shots 1; xg 0.006; npxg 0.006; key_passes 4; passes_completed 644; progressive_passes 98; progressive_carries 33; pressures 19; pressured_passes_attempted 44; pressured_passes_completed 36; shot_creating_actions 9; xt_added 0.885; pass_completion_pct 94.8; pressured_pass_completion_pct 81.8
- Kylian Mbappé: France, W, 597.4 min, 7 matches: **passes_attempted 233, per 90 35.10**. Other: goals 8; non_penalty_goals 6; assists 2; shots 31; xg 4.233; npxg 2.666; key_passes 11; passes_completed 180; progressive_passes 31; progressive_carries 71; pressures 37; pressured_passes_attempted 26; pressured_passes_completed 22; shot_creating_actions 41; xt_added 1.899; pass_completion_pct 77.3; pressured_pass_completion_pct 84.6

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A006

**Question:** How do Koopmeiners and Widmer compare in terms of shot-creating actions during the 2022 World Cup?

**Ground truth** (Shot-creating actions for Teun Koopmeiners and Silvan Widmer, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Silvan Widmer | Switzerland | 5 | 265 | 3 |
| 1 | Teun Koopmeiners | Netherlands | 5 | 219 | 5 |

**Naive answer:**

> Teun Koopmeiners had 2 shot-creating actions in 218.6 minutes (0.91 per 90), while Silvan Widmer had 2 shot-creating actions in 265.3 minutes (0.68 per 90).

**Reference stats** (true tournament totals):

- Silvan Widmer: Switzerland, FB, 265.3 min, 3 matches: **shot_creating_actions 5, per 90 1.70**. Other: goals 0; non_penalty_goals 0; assists 1; shots 1; xg 0.051; npxg 0.051; key_passes 2; passes_attempted 164; passes_completed 127; progressive_passes 20; progressive_carries 8; pressures 37; pressured_passes_attempted 13; pressured_passes_completed 9; xt_added 0.673; pass_completion_pct 77.4; pressured_pass_completion_pct 69.2
- Teun Koopmeiners: Netherlands, DM, 218.6 min, 5 matches: **shot_creating_actions 5, per 90 2.06**. Other: goals 0; non_penalty_goals 0; assists 1; shots 2; xg 0.09; npxg 0.09; key_passes 2; passes_attempted 120; passes_completed 95; progressive_passes 18; progressive_carries 4; pressures 55; pressured_passes_attempted 22; pressured_passes_completed 16; xt_added 0.122; pass_completion_pct 79.2; pressured_pass_completion_pct 72.7

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A007

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

## A008

**Question:** Which 3 players had the fewest goals?

**Ground truth** (The 3 players with the fewest goals, with at least 270 minutes (default threshold), World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Aaron Mooy | Australia | 0 | 360 | 4 |
| 1 | Abdelkarim Hassan | Qatar | 0 | 270 | 3 |
| 1 | Abdou Diallo | Senegal | 0 | 331 | 4 |

**Naive answer:**

> The 3 players with the fewest goals (0 goals) are:
> 1. Youri Tielemans (Belgium, 0 goals)
> 2. Alexander Djiku (Ghana, 0 goals)
> 3. Christian Eriksen (Denmark, 0 goals)

**Reference stats** (true tournament totals):

- Aaron Mooy: Australia, DM, 360.0 min, 4 matches: **goals 0, per 90 0.00**. Other: non_penalty_goals 0; assists 0; shots 1; xg 0.039; npxg 0.039; key_passes 1; passes_attempted 219; passes_completed 171; progressive_passes 29; progressive_carries 6; pressures 44; pressured_passes_attempted 25; pressured_passes_completed 13; shot_creating_actions 4; xt_added 0.144; pass_completion_pct 78.1; pressured_pass_completion_pct 52.0
- Abdelkarim Hassan: Qatar, CB, 270.0 min, 3 matches: **goals 0, per 90 0.00**. Other: non_penalty_goals 0; assists 0; shots 6; xg 0.275; npxg 0.275; key_passes 1; passes_attempted 158; passes_completed 125; progressive_passes 19; progressive_carries 16; pressures 29; pressured_passes_attempted 21; pressured_passes_completed 17; shot_creating_actions 3; xt_added 0.337; pass_completion_pct 79.1; pressured_pass_completion_pct 81.0
- Abdou Diallo: Senegal, CB, 331.4 min, 4 matches: **goals 0, per 90 0.00**. Other: non_penalty_goals 0; assists 0; shots 1; xg 0.035; npxg 0.035; key_passes 1; passes_attempted 183; passes_completed 142; progressive_passes 24; progressive_carries 9; pressures 25; pressured_passes_attempted 16; pressured_passes_completed 9; shot_creating_actions 2; xt_added 0.321; pass_completion_pct 77.6; pressured_pass_completion_pct 56.2
- Youri Tielemans: Belgium, DM, 93.7 min, 3 matches: **goals 0, per 90 0.00**. Other: non_penalty_goals 0; assists 0; shots 0; xg 0; npxg 0; key_passes 1; passes_attempted 61; passes_completed 51; progressive_passes 5; progressive_carries 1; pressures 17; pressured_passes_attempted 8; pressured_passes_completed 7; shot_creating_actions 1; xt_added 0.017; pass_completion_pct 83.6; pressured_pass_completion_pct 87.5
- Alexander Djiku: Ghana, CB, 97.9 min, 2 matches: **goals 0, per 90 0.00**. Other: non_penalty_goals 0; assists 0; shots 0; xg 0; npxg 0; key_passes 0; passes_attempted 27; passes_completed 23; progressive_passes 1; progressive_carries 0; pressures 5; pressured_passes_attempted 0; pressured_passes_completed 0; shot_creating_actions 1; xt_added 0.012; pass_completion_pct 85.2
- Christian Eriksen: Denmark, CM, 270.0 min, 3 matches: **goals 0, per 90 0.00**. Other: non_penalty_goals 0; assists 0; shots 4; xg 0.154; npxg 0.154; key_passes 9; passes_attempted 231; passes_completed 193; progressive_passes 32; progressive_carries 11; pressures 32; pressured_passes_attempted 21; pressured_passes_completed 17; shot_creating_actions 15; xt_added 0.372; pass_completion_pct 83.5; pressured_pass_completion_pct 81.0

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A009

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

## A010

**Question:** how many key passes did messi have in the 2022 world cup?

**Ground truth** (Key passes for Lionel Messi, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Lionel Messi | Argentina | 19 | 690 | 7 |

**Naive answer:**

> Lionel Messi had 19 key passes in the 2022 World Cup.

**Reference stats** (true tournament totals):

- Lionel Messi: Argentina, ST, 690.0 min, 7 matches: **key_passes 19, per 90 2.48**. Other: goals 7; non_penalty_goals 3; assists 3; shots 32; xg 6.032; npxg 2.114; passes_attempted 371; passes_completed 306; progressive_passes 79; progressive_carries 61; pressures 89; pressured_passes_attempted 75; pressured_passes_completed 65; shot_creating_actions 41; xt_added 1.759; pass_completion_pct 82.5; pressured_pass_completion_pct 86.7

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A011

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

## A012

**Question:** How many key passes did Messi have?

**Ground truth** (Key passes for Lionel Messi, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Lionel Messi | Argentina | 19 | 690 | 7 |

**Naive answer:**

> Lionel Messi had 19 key passes in the 2022 World Cup.

**Reference stats** (true tournament totals):

- Lionel Messi: Argentina, ST, 690.0 min, 7 matches: **key_passes 19, per 90 2.48**. Other: goals 7; non_penalty_goals 3; assists 3; shots 32; xg 6.032; npxg 2.114; passes_attempted 371; passes_completed 306; progressive_passes 79; progressive_carries 61; pressures 89; pressured_passes_attempted 75; pressured_passes_completed 65; shot_creating_actions 41; xt_added 1.759; pass_completion_pct 82.5; pressured_pass_completion_pct 86.7

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A013

**Question:** Which player scored the highest number of non-penalty goals in the 2022 World Cup?

**Ground truth** (The player with the most non-penalty goals, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Kylian Mbappé | France | 6 | 597 | 7 |

**Naive answer:**

> Kylian Mbappé (France) scored the highest number of non-penalty goals in the 2022 World Cup, with 6 non-penalty goals.

**Reference stats** (true tournament totals):

- Kylian Mbappé: France, W, 597.4 min, 7 matches: **non_penalty_goals 6, per 90 0.90**. Other: goals 8; assists 2; shots 31; xg 4.233; npxg 2.666; key_passes 11; passes_attempted 233; passes_completed 180; progressive_passes 31; progressive_carries 71; pressures 37; pressured_passes_attempted 26; pressured_passes_completed 22; shot_creating_actions 41; xt_added 1.899; pass_completion_pct 77.3; pressured_pass_completion_pct 84.6

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A014

**Question:** Compare Aurélien Tchouaméni and Costa on progressive passes.

**Ground truth** (Progressive passes (simplified) for Aurélien Tchouaméni and Diogo Costa, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Aurélien Tchouaméni | France | 66 | 622 | 7 |
| 2 | Diogo Costa | Portugal | 0 | 450 | 5 |

**Naive answer:**

> Aurélien Tchouaméni made 66 progressive passes in 621.8 minutes, which is 9.69 per 90. Costa Rica's Celso Borges made 21 progressive passes in 250.0 minutes, which is 7.56 per 90. Tchouaméni outperformed Borges in progressive passes per 90.

**Reference stats** (true tournament totals):

- Aurélien Tchouaméni: France, DM, 621.8 min, 7 matches: **progressive_passes 66, per 90 9.55**. Other: goals 1; non_penalty_goals 1; assists 0; shots 6; xg 0.399; npxg 0.399; key_passes 6; passes_attempted 470; passes_completed 431; progressive_carries 17; pressures 64; pressured_passes_attempted 51; pressured_passes_completed 42; shot_creating_actions 10; xt_added 0.758; pass_completion_pct 91.7; pressured_pass_completion_pct 82.4
- Diogo Costa: Portugal, GK, 450.0 min, 5 matches: **progressive_passes 0, per 90 0.00**. Other: goals 0; non_penalty_goals 0; assists 0; shots 0; xg 0; npxg 0; key_passes 1; passes_attempted 159; passes_completed 111; progressive_carries 0; pressures 1; pressured_passes_attempted 20; pressured_passes_completed 10; shot_creating_actions 1; xt_added 0.128; pass_completion_pct 69.8; pressured_pass_completion_pct 50.0
- Celso Borges: Costa Rica, DM, 250.0 min, 3 matches: **progressive_passes 21, per 90 7.56**. Other: goals 0; non_penalty_goals 0; assists 0; shots 0; xg 0; npxg 0; key_passes 1; passes_attempted 113; passes_completed 94; progressive_carries 0; pressures 33; pressured_passes_attempted 22; pressured_passes_completed 18; shot_creating_actions 1; xt_added 0.097; pass_completion_pct 83.2; pressured_pass_completion_pct 81.8

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A015

**Question:** which serbia center back had the most passes under pressure at the world cup 2022?

**Ground truth** (The player with the most passes attempted under pressure, among centre-backs (CB), playing for Serbia, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Nikola Milenković | Serbia | 21 | 270 | 3 |

**Naive answer:**

> The Serbian center back with the most passes under pressure at the World Cup 2022 was **Nikola Milenković**, with **28 pressured passes attempted**.

**Reference stats** (true tournament totals):

- Nikola Milenković: Serbia, CB, 270.0 min, 3 matches: **pressured_passes_attempted 21, per 90 7.00**. Other: goals 0; non_penalty_goals 0; assists 0; shots 3; xg 0.123; npxg 0.123; key_passes 0; passes_attempted 157; passes_completed 136; progressive_passes 19; progressive_carries 4; pressures 28; pressured_passes_completed 16; shot_creating_actions 0; xt_added 0.175; pass_completion_pct 86.6; pressured_pass_completion_pct 76.2

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A016

**Question:** Who had the highest number of shot-creating actions among Aaron Mooy, Joshua Kimmich, and Hakim Ziyech in the 2022 World Cup?

**Ground truth** (Shot-creating actions for Aaron Mooy, Hakim Ziyech and Joshua Kimmich, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Hakim Ziyech | Morocco | 20 | 636 | 7 |
| 2 | Joshua Kimmich | Germany | 17 | 270 | 3 |
| 3 | Aaron Mooy | Australia | 4 | 360 | 4 |

**Naive answer:**

> Hakim Ziyech had the highest number of shot-creating actions among Aaron Mooy, Joshua Kimmich, and Hakim Ziyech in the 2022 World Cup with 7 shot-creating actions.

**Reference stats** (true tournament totals):

- Hakim Ziyech: Morocco, W, 636.2 min, 7 matches: **shot_creating_actions 20, per 90 2.83**. Other: goals 1; non_penalty_goals 1; assists 1; shots 10; xg 0.312; npxg 0.312; key_passes 7; passes_attempted 300; passes_completed 210; progressive_passes 40; progressive_carries 28; pressures 137; pressured_passes_attempted 31; pressured_passes_completed 23; xt_added 0.541; pass_completion_pct 70.0; pressured_pass_completion_pct 74.2
- Joshua Kimmich: Germany, DM, 270.0 min, 3 matches: **shot_creating_actions 17, per 90 5.67**. Other: goals 0; non_penalty_goals 0; assists 0; shots 7; xg 0.335; npxg 0.335; key_passes 8; passes_attempted 271; passes_completed 229; progressive_passes 48; progressive_carries 8; pressures 35; pressured_passes_attempted 30; pressured_passes_completed 25; xt_added 1.091; pass_completion_pct 84.5; pressured_pass_completion_pct 83.3
- Aaron Mooy: Australia, DM, 360.0 min, 4 matches: **shot_creating_actions 4, per 90 1.00**. Other: goals 0; non_penalty_goals 0; assists 0; shots 1; xg 0.039; npxg 0.039; key_passes 1; passes_attempted 219; passes_completed 171; progressive_passes 29; progressive_carries 6; pressures 44; pressured_passes_attempted 25; pressured_passes_completed 13; xt_added 0.144; pass_completion_pct 78.1; pressured_pass_completion_pct 52.0

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A017

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

## A018

**Question:** What was the xG value for Aziz Behich in the 2022 World Cup?

**Ground truth** (Expected goals (xG) for Aziz Behich, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Aziz Behich | Australia | 0.13 | 360 | 4 |

**Naive answer:**

> Aziz Behich had an xG value of 0.13 in the 2022 World Cup.

**Reference stats** (true tournament totals):

- Aziz Behich: Australia, FB, 360.0 min, 4 matches: **xg 0.127, per 90 0.03**. Other: goals 0; non_penalty_goals 0; assists 0; shots 2; npxg 0.127; key_passes 0; passes_attempted 204; passes_completed 154; progressive_passes 9; progressive_carries 10; pressures 33; pressured_passes_attempted 16; pressured_passes_completed 11; shot_creating_actions 4; xt_added 0.237; pass_completion_pct 75.5; pressured_pass_completion_pct 68.8

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A019

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

## A020

**Question:** How many key passes did Nahuel Molina register during the 2022 World Cup?

**Ground truth** (Key passes for Nahuel Molina, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Nahuel Molina | Argentina | 3 | 568 | 7 |

**Naive answer:**

> Nahuel Molina registered 3 key passes during the 2022 World Cup.

**Reference stats** (true tournament totals):

- Nahuel Molina: Argentina, FB, 567.7 min, 7 matches: **key_passes 3, per 90 0.48**. Other: goals 1; non_penalty_goals 1; assists 1; shots 2; xg 0.485; npxg 0.485; passes_attempted 360; passes_completed 296; progressive_passes 29; progressive_carries 16; pressures 72; pressured_passes_attempted 35; pressured_passes_completed 24; shot_creating_actions 10; xt_added 0.473; pass_completion_pct 82.2; pressured_pass_completion_pct 68.6

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A021

**Question:** Looking at the 2022 World Cup, which five players made the most progressive carries?

**Ground truth** (The 5 players with the most progressive carries, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Kylian Mbappé | France | 71 | 597 | 7 |
| 2 | Lionel Messi | Argentina | 61 | 690 | 7 |
| 3 | Luka Modrić | Croatia | 42 | 654 | 7 |
| 4 | Ivan Perišić | Croatia | 39 | 670 | 7 |
| 5 | Mateo Kovačić | Croatia | 37 | 638 | 7 |

**Naive answer:**

> The five players who made the most progressive carries at the 2022 World Cup are:
> 
> 1. **Luka Modrić (Croatia, CM)** - 42 progressive carries  
> 2. **Christian Pulisic (United States, W)** - 33 progressive carries  
> 3. **Álvaro Morata (Spain, ST)** - 14 progressive carries  
> 4. **Kylian Mbappé (France, W)** - 71 progressive carries  
> 5. **Harry Kane (England, ST)** - 10 progressive carries

**Reference stats** (true tournament totals):

- Kylian Mbappé: France, W, 597.4 min, 7 matches: **progressive_carries 71, per 90 10.70**. Other: goals 8; non_penalty_goals 6; assists 2; shots 31; xg 4.233; npxg 2.666; key_passes 11; passes_attempted 233; passes_completed 180; progressive_passes 31; pressures 37; pressured_passes_attempted 26; pressured_passes_completed 22; shot_creating_actions 41; xt_added 1.899; pass_completion_pct 77.3; pressured_pass_completion_pct 84.6
- Lionel Messi: Argentina, ST, 690.0 min, 7 matches: **progressive_carries 61, per 90 7.96**. Other: goals 7; non_penalty_goals 3; assists 3; shots 32; xg 6.032; npxg 2.114; key_passes 19; passes_attempted 371; passes_completed 306; progressive_passes 79; pressures 89; pressured_passes_attempted 75; pressured_passes_completed 65; shot_creating_actions 41; xt_added 1.759; pass_completion_pct 82.5; pressured_pass_completion_pct 86.7
- Luka Modrić: Croatia, CM, 654.4 min, 7 matches: **progressive_carries 42, per 90 5.78**. Other: goals 0; non_penalty_goals 0; assists 0; shots 6; xg 0.344; npxg 0.344; key_passes 6; passes_attempted 549; passes_completed 463; progressive_passes 107; pressures 115; pressured_passes_attempted 68; pressured_passes_completed 54; shot_creating_actions 19; xt_added 1.111; pass_completion_pct 84.3; pressured_pass_completion_pct 79.4
- Ivan Perišić: Croatia, W, 669.6 min, 7 matches: **progressive_carries 39, per 90 5.24**. Other: goals 1; non_penalty_goals 1; assists 3; shots 16; xg 0.756; npxg 0.756; key_passes 9; passes_attempted 304; passes_completed 214; progressive_passes 34; pressures 98; pressured_passes_attempted 51; pressured_passes_completed 35; shot_creating_actions 18; xt_added 0.994; pass_completion_pct 70.4; pressured_pass_completion_pct 68.6
- Mateo Kovačić: Croatia, CM, 637.8 min, 7 matches: **progressive_carries 37, per 90 5.22**. Other: goals 0; non_penalty_goals 0; assists 0; shots 3; xg 0.345; npxg 0.345; key_passes 9; passes_attempted 456; passes_completed 416; progressive_passes 71; pressures 136; pressured_passes_attempted 59; pressured_passes_completed 52; shot_creating_actions 16; xt_added 0.913; pass_completion_pct 91.2; pressured_pass_completion_pct 88.1
- Christian Pulisic: United States, W, 315.0 min, 4 matches: **progressive_carries 33, per 90 9.43**. Other: goals 1; non_penalty_goals 1; assists 2; shots 9; xg 1.138; npxg 1.138; key_passes 9; passes_attempted 139; passes_completed 84; progressive_passes 21; pressures 44; pressured_passes_attempted 27; pressured_passes_completed 20; shot_creating_actions 16; xt_added 0.679; pass_completion_pct 60.4; pressured_pass_completion_pct 74.1
- Álvaro Morata: Spain, ST, 183.9 min, 4 matches: **progressive_carries 7, per 90 3.43**. Other: goals 3; non_penalty_goals 3; assists 1; shots 8; xg 1.109; npxg 1.109; key_passes 1; passes_attempted 40; passes_completed 27; progressive_passes 5; pressures 26; pressured_passes_attempted 11; pressured_passes_completed 8; shot_creating_actions 3; xt_added -0.044; pass_completion_pct 67.5; pressured_pass_completion_pct 72.7
- Harry Kane: England, ST, 402.3 min, 5 matches: **progressive_carries 10, per 90 2.24**. Other: goals 2; non_penalty_goals 1; assists 3; shots 12; xg 2.331; npxg 0.764; key_passes 5; passes_attempted 97; passes_completed 64; progressive_passes 21; pressures 31; pressured_passes_attempted 25; pressured_passes_completed 12; shot_creating_actions 7; xt_added 0.618; pass_completion_pct 66.0; pressured_pass_completion_pct 48.0

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A022

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

## A023

**Question:** Which Croatian midfielders completed the most passes under pressure?

**Ground truth** (The 5 players with the most passes completed under pressure, among midfielders (AM, CM, DM), playing for Croatia, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Marcelo Brozović | Croatia | 59 | 553 | 6 |
| 2 | Luka Modrić | Croatia | 54 | 654 | 7 |
| 3 | Mateo Kovačić | Croatia | 52 | 638 | 7 |

**Naive answer:**

> The Croatian midfielder who completed the most passes under pressure is **Luka Modrić**, with **54 completed passes under pressure**. 
> 
> Other Croatian midfielders with notable pass completions under pressure include:
> - **Mateo Kovačić** – 52 completed passes under pressure.
> - **Marcelo Brozović** – 59 completed passes under pressure.
> - **Mario Pašalić** – 16 completed passes under pressure.
> 
> Brozović completed the most, with **59 completed passes under pressure**.

**Reference stats** (true tournament totals):

- Marcelo Brozović: Croatia, DM, 552.8 min, 6 matches: **pressured_passes_completed 59, per 90 9.61**. Other: goals 0; non_penalty_goals 0; assists 0; shots 4; xg 0.585; npxg 0.585; key_passes 5; passes_attempted 529; passes_completed 472; progressive_passes 68; progressive_carries 17; pressures 96; pressured_passes_attempted 75; shot_creating_actions 11; xt_added 0.249; pass_completion_pct 89.2; pressured_pass_completion_pct 78.7
- Luka Modrić: Croatia, CM, 654.4 min, 7 matches: **pressured_passes_completed 54, per 90 7.43**. Other: goals 0; non_penalty_goals 0; assists 0; shots 6; xg 0.344; npxg 0.344; key_passes 6; passes_attempted 549; passes_completed 463; progressive_passes 107; progressive_carries 42; pressures 115; pressured_passes_attempted 68; shot_creating_actions 19; xt_added 1.111; pass_completion_pct 84.3; pressured_pass_completion_pct 79.4
- Mateo Kovačić: Croatia, CM, 637.8 min, 7 matches: **pressured_passes_completed 52, per 90 7.34**. Other: goals 0; non_penalty_goals 0; assists 0; shots 3; xg 0.345; npxg 0.345; key_passes 9; passes_attempted 456; passes_completed 416; progressive_passes 71; progressive_carries 37; pressures 136; pressured_passes_attempted 59; shot_creating_actions 16; xt_added 0.913; pass_completion_pct 91.2; pressured_pass_completion_pct 88.1
- Mario Pašalić: Croatia, W, 268.0 min, 7 matches: **pressured_passes_completed 16, per 90 5.37**. Other: goals 0; non_penalty_goals 0; assists 0; shots 3; xg 0.167; npxg 0.167; key_passes 1; passes_attempted 93; passes_completed 77; progressive_passes 12; progressive_carries 6; pressures 53; pressured_passes_attempted 25; shot_creating_actions 4; xt_added 0.177; pass_completion_pct 82.8; pressured_pass_completion_pct 64.0

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A024

**Question:** Which 5 strikers had the most xT added?

**Ground truth** (The 5 players with the most expected threat (xT) added, among strikers (ST), World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Lionel Messi | Argentina | 1.759 | 690 | 7 |
| 2 | Julián Álvarez | Argentina | 0.676 | 465 | 7 |
| 3 | Harry Kane | England | 0.618 | 402 | 5 |
| 4 | Gareth Bale | Wales | 0.37 | 225 | 3 |
| 5 | Kai Havertz | Germany | 0.362 | 102 | 2 |

**Naive answer:**

> The 5 strikers with the most xT (expected threat) added in the 2022 World Cup are:
> 
> 1. **Lionel Messi (Argentina)** - 1.759 xT  
> 2. **Harry Kane (England)** - 0.618 xT  
> 3. **Kylian Mbappé (France)** - 0.1899 xT  
> 4. **Cristiano Ronaldo (Portugal)** - 0.084 xT  
> 5. **Raphinha (Brazil)** - 0.1426 xT

**Reference stats** (true tournament totals):

- Lionel Messi: Argentina, ST, 690.0 min, 7 matches: **xt_added 1.759, per 90 0.229**. Other: goals 7; non_penalty_goals 3; assists 3; shots 32; xg 6.032; npxg 2.114; key_passes 19; passes_attempted 371; passes_completed 306; progressive_passes 79; progressive_carries 61; pressures 89; pressured_passes_attempted 75; pressured_passes_completed 65; shot_creating_actions 41; pass_completion_pct 82.5; pressured_pass_completion_pct 86.7
- Julián Álvarez: Argentina, ST, 464.9 min, 7 matches: **xt_added 0.676, per 90 0.131**. Other: goals 4; non_penalty_goals 4; assists 0; shots 11; xg 1.908; npxg 1.908; key_passes 2; passes_attempted 124; passes_completed 93; progressive_passes 5; progressive_carries 17; pressures 118; pressured_passes_attempted 27; pressured_passes_completed 18; shot_creating_actions 7; pass_completion_pct 75.0; pressured_pass_completion_pct 66.7
- Harry Kane: England, ST, 402.3 min, 5 matches: **xt_added 0.618, per 90 0.138**. Other: goals 2; non_penalty_goals 1; assists 3; shots 12; xg 2.331; npxg 0.764; key_passes 5; passes_attempted 97; passes_completed 64; progressive_passes 21; progressive_carries 10; pressures 31; pressured_passes_attempted 25; pressured_passes_completed 12; shot_creating_actions 7; pass_completion_pct 66.0; pressured_pass_completion_pct 48.0
- Gareth Bale: Wales, ST, 225.0 min, 3 matches: **xt_added 0.37, per 90 0.148**. Other: goals 1; non_penalty_goals 0; assists 0; shots 2; xg 0.805; npxg 0.022; key_passes 2; passes_attempted 55; passes_completed 34; progressive_passes 6; progressive_carries 2; pressures 17; pressured_passes_attempted 16; pressured_passes_completed 9; shot_creating_actions 3; pass_completion_pct 61.8; pressured_pass_completion_pct 56.2
- Kai Havertz: Germany, ST, 102.4 min, 2 matches: **xt_added 0.362, per 90 0.318**. Other: goals 2; non_penalty_goals 2; assists 0; shots 5; xg 1.155; npxg 1.155; key_passes 2; passes_attempted 33; passes_completed 26; progressive_passes 6; progressive_carries 3; pressures 19; pressured_passes_attempted 8; pressured_passes_completed 6; shot_creating_actions 6; pass_completion_pct 78.8; pressured_pass_completion_pct 75.0
- Kylian Mbappé: France, W, 597.4 min, 7 matches: **xt_added 1.899, per 90 0.286**. Other: goals 8; non_penalty_goals 6; assists 2; shots 31; xg 4.233; npxg 2.666; key_passes 11; passes_attempted 233; passes_completed 180; progressive_passes 31; progressive_carries 71; pressures 37; pressured_passes_attempted 26; pressured_passes_completed 22; shot_creating_actions 41; pass_completion_pct 77.3; pressured_pass_completion_pct 84.6
- Cristiano Ronaldo: Portugal, ST, 290.6 min, 5 matches: **xt_added 0.084, per 90 0.026**. Other: goals 1; non_penalty_goals 0; assists 0; shots 11; xg 1.939; npxg 1.156; key_passes 4; passes_attempted 90; passes_completed 67; progressive_passes 6; progressive_carries 10; pressures 21; pressured_passes_attempted 13; pressured_passes_completed 8; shot_creating_actions 8; pass_completion_pct 74.4; pressured_pass_completion_pct 61.5
- Raphinha: Brazil, W, 316.4 min, 5 matches: **xt_added 1.426, per 90 0.406**. Other: goals 0; non_penalty_goals 0; assists 0; shots 8; xg 0.923; npxg 0.923; key_passes 8; passes_attempted 150; passes_completed 115; progressive_passes 14; progressive_carries 26; pressures 51; pressured_passes_attempted 16; pressured_passes_completed 11; shot_creating_actions 20; pass_completion_pct 76.7; pressured_pass_completion_pct 68.8

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A025

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

## A026

**Question:** How many pressures did Julián Álvarez make?

**Ground truth** (Pressures for Julián Álvarez, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Julián Álvarez | Argentina | 118 | 465 | 7 |

**Naive answer:**

> Julián Álvarez made 118 pressures.

**Reference stats** (true tournament totals):

- Julián Álvarez: Argentina, ST, 464.9 min, 7 matches: **pressures 118, per 90 22.84**. Other: goals 4; non_penalty_goals 4; assists 0; shots 11; xg 1.908; npxg 1.908; key_passes 2; passes_attempted 124; passes_completed 93; progressive_passes 5; progressive_carries 17; pressured_passes_attempted 27; pressured_passes_completed 18; shot_creating_actions 7; xt_added 0.676; pass_completion_pct 75.0; pressured_pass_completion_pct 66.7

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A027

**Question:** Which five players recorded the highest expected goals (xG) during the 2022 World Cup?

**Ground truth** (The 5 players with the most expected goals (xG), World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Lionel Messi | Argentina | 6.03 | 690 | 7 |
| 2 | Kylian Mbappé | France | 4.23 | 597 | 7 |
| 3 | Robert Lewandowski | Poland | 3.13 | 360 | 4 |
| 4 | Olivier Giroud | France | 3.04 | 422 | 6 |
| 5 | Breel Embolo | Switzerland | 2.39 | 325 | 4 |

**Naive answer:**

> The five players with the highest expected goals (xG) during the 2022 World Cup are:
> 
> 1. **Kylian Mbappé** (France) - 4.23  
> 2. **Ousmane Dembélé** (France) - 3.6  
> 3. **Harry Kane** (England) - 2.33  
> 4. **Lionel Messi** (Argentina) - 6.03  
> 5. **Neymar** (Brazil) - 2.13

**Reference stats** (true tournament totals):

- Lionel Messi: Argentina, ST, 690.0 min, 7 matches: **xg 6.032, per 90 0.79**. Other: goals 7; non_penalty_goals 3; assists 3; shots 32; npxg 2.114; key_passes 19; passes_attempted 371; passes_completed 306; progressive_passes 79; progressive_carries 61; pressures 89; pressured_passes_attempted 75; pressured_passes_completed 65; shot_creating_actions 41; xt_added 1.759; pass_completion_pct 82.5; pressured_pass_completion_pct 86.7
- Kylian Mbappé: France, W, 597.4 min, 7 matches: **xg 4.233, per 90 0.64**. Other: goals 8; non_penalty_goals 6; assists 2; shots 31; npxg 2.666; key_passes 11; passes_attempted 233; passes_completed 180; progressive_passes 31; progressive_carries 71; pressures 37; pressured_passes_attempted 26; pressured_passes_completed 22; shot_creating_actions 41; xt_added 1.899; pass_completion_pct 77.3; pressured_pass_completion_pct 84.6
- Robert Lewandowski: Poland, ST, 360.0 min, 4 matches: **xg 3.126, per 90 0.78**. Other: goals 2; non_penalty_goals 1; assists 1; shots 12; npxg 1.559; key_passes 5; passes_attempted 91; passes_completed 65; progressive_passes 11; progressive_carries 10; pressures 39; pressured_passes_attempted 29; pressured_passes_completed 18; shot_creating_actions 11; xt_added -0.069; pass_completion_pct 71.4; pressured_pass_completion_pct 62.1
- Olivier Giroud: France, ST, 422.1 min, 6 matches: **xg 3.036, per 90 0.65**. Other: goals 4; non_penalty_goals 4; assists 0; shots 17; npxg 3.036; key_passes 2; passes_attempted 75; passes_completed 49; progressive_passes 9; progressive_carries 2; pressures 60; pressured_passes_attempted 25; pressured_passes_completed 12; shot_creating_actions 4; xt_added 0.16; pass_completion_pct 65.3; pressured_pass_completion_pct 48.0
- Breel Embolo: Switzerland, ST, 324.8 min, 4 matches: **xg 2.391, per 90 0.66**. Other: goals 2; non_penalty_goals 2; assists 0; shots 6; npxg 2.391; key_passes 2; passes_attempted 66; passes_completed 50; progressive_passes 4; progressive_carries 13; pressures 47; pressured_passes_attempted 16; pressured_passes_completed 14; shot_creating_actions 4; xt_added 0.055; pass_completion_pct 75.8; pressured_pass_completion_pct 87.5
- Ousmane Dembélé: France, W, 435.3 min, 7 matches: **xg 0.362, per 90 0.07**. Other: goals 0; non_penalty_goals 0; assists 2; shots 8; npxg 0.362; key_passes 12; passes_attempted 191; passes_completed 149; progressive_passes 26; progressive_carries 36; pressures 90; pressured_passes_attempted 21; pressured_passes_completed 19; shot_creating_actions 18; xt_added 1.328; pass_completion_pct 78.0; pressured_pass_completion_pct 90.5
- Harry Kane: England, ST, 402.3 min, 5 matches: **xg 2.331, per 90 0.52**. Other: goals 2; non_penalty_goals 1; assists 3; shots 12; npxg 0.764; key_passes 5; passes_attempted 97; passes_completed 64; progressive_passes 21; progressive_carries 10; pressures 31; pressured_passes_attempted 25; pressured_passes_completed 12; shot_creating_actions 7; xt_added 0.618; pass_completion_pct 66.0; pressured_pass_completion_pct 48.0
- Neymar: Brazil, AM, 279.4 min, 3 matches: **xg 2.129, per 90 0.69**. Other: goals 2; non_penalty_goals 1; assists 0; shots 12; npxg 1.346; key_passes 4; passes_attempted 156; passes_completed 123; progressive_passes 27; progressive_carries 23; pressures 24; pressured_passes_attempted 23; pressured_passes_completed 18; shot_creating_actions 14; xt_added 0.592; pass_completion_pct 78.8; pressured_pass_completion_pct 78.3

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A028

**Question:** Which three defenders in central positions recorded the lowest number of pressures in the 2022 World Cup?

**Ground truth** (The 3 players with the fewest pressures, among centre-backs (CB), with at least 270 minutes (default threshold), World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Andreas Christensen | Denmark | 11 | 270 | 3 |
| 1 | Aymeric Laporte | Spain | 11 | 300 | 3 |
| 3 | Félix Torres | Ecuador | 12 | 270 | 3 |

**Naive answer:**

> The three central defenders (CBs) who recorded the lowest number of pressures (minimum 270 minutes played) in the 2022 World Cup are:
> 
> 1. **Ederson Moraes** (Brazil, GK) - 0 pressures (only 90 minutes played, not eligible for per-90 stats).
> 2. **Pape Gueye** (Senegal, DM) - 22 pressures in 151.8 minutes.
> 3. **António Silva** (Portugal, CB) - 2 pressures in 90 minutes (not eligible for per-90 stats). 
> 
> Note: Only players with at least 270 minutes are considered for per-90 comparisons.

**Reference stats** (true tournament totals):

- Andreas Christensen: Denmark, CB, 270.0 min, 3 matches: **pressures 11, per 90 3.67**. Other: goals 1; non_penalty_goals 1; assists 0; shots 2; xg 0.525; npxg 0.525; key_passes 0; passes_attempted 250; passes_completed 236; progressive_passes 32; progressive_carries 8; pressured_passes_attempted 17; pressured_passes_completed 13; shot_creating_actions 1; xt_added 0.233; pass_completion_pct 94.4; pressured_pass_completion_pct 76.5
- Aymeric Laporte: Spain, CB, 300.0 min, 3 matches: **pressures 11, per 90 3.30**. Other: goals 0; non_penalty_goals 0; assists 0; shots 1; xg 0.041; npxg 0.041; key_passes 1; passes_attempted 429; passes_completed 404; progressive_passes 53; progressive_carries 19; pressured_passes_attempted 17; pressured_passes_completed 10; shot_creating_actions 3; xt_added 0.525; pass_completion_pct 94.2; pressured_pass_completion_pct 58.8
- Félix Torres: Ecuador, CB, 270.0 min, 3 matches: **pressures 12, per 90 4.00**. Other: goals 0; non_penalty_goals 0; assists 0; shots 1; xg 0.154; npxg 0.154; key_passes 0; passes_attempted 199; passes_completed 159; progressive_passes 8; progressive_carries 2; pressured_passes_attempted 10; pressured_passes_completed 7; shot_creating_actions 1; xt_added 0.177; pass_completion_pct 79.9; pressured_pass_completion_pct 70.0
- Ederson Moraes: Brazil, GK, 90.0 min, 1 matches: **pressures 0, per 90 0.00**. Other: goals 0; non_penalty_goals 0; assists 0; shots 0; xg 0; npxg 0; key_passes 0; passes_attempted 30; passes_completed 28; progressive_passes 0; progressive_carries 0; pressured_passes_attempted 1; pressured_passes_completed 1; shot_creating_actions 0; xt_added 0.039; pass_completion_pct 93.3; pressured_pass_completion_pct 100.0
- Pape Gueye: Senegal, DM, 151.8 min, 3 matches: **pressures 22, per 90 13.04**. Other: goals 0; non_penalty_goals 0; assists 0; shots 4; xg 0.094; npxg 0.094; key_passes 2; passes_attempted 61; passes_completed 46; progressive_passes 9; progressive_carries 3; pressured_passes_attempted 15; pressured_passes_completed 8; shot_creating_actions 4; xt_added 0.086; pass_completion_pct 75.4; pressured_pass_completion_pct 53.3
- António Silva: Portugal, CB, 90.0 min, 1 matches: **pressures 2, per 90 2.00**. Other: goals 0; non_penalty_goals 0; assists 0; shots 0; xg 0; npxg 0; key_passes 0; passes_attempted 58; passes_completed 57; progressive_passes 6; progressive_carries 1; pressured_passes_attempted 4; pressured_passes_completed 4; shot_creating_actions 1; xt_added 0.025; pass_completion_pct 98.3; pressured_pass_completion_pct 100.0

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A029

**Question:** Who had the most progressive passes in the 2022 World Cup?

**Ground truth** (The player with the most progressive passes (simplified), World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Luka Modrić | Croatia | 107 | 654 | 7 |

**Naive answer:**

> Luka Modrić of Croatia had the most progressive passes in the 2022 World Cup with 107.

**Reference stats** (true tournament totals):

- Luka Modrić: Croatia, CM, 654.4 min, 7 matches: **progressive_passes 107, per 90 14.72**. Other: goals 0; non_penalty_goals 0; assists 0; shots 6; xg 0.344; npxg 0.344; key_passes 6; passes_attempted 549; passes_completed 463; progressive_carries 42; pressures 115; pressured_passes_attempted 68; pressured_passes_completed 54; shot_creating_actions 19; xt_added 1.111; pass_completion_pct 84.3; pressured_pass_completion_pct 79.4

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A030

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

## A031

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

## A032

**Question:** What was Emiliano Martínez's goals per 90?

**Ground truth** (Goals per 90 for Emiliano Martínez, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Emiliano Martínez | Argentina | 0.0 | 690 | 7 |

**Naive answer:**

> Emiliano Martínez did not score any goals in the 2022 World Cup, so his goals per 90 is 0.00.

**Reference stats** (true tournament totals):

- Emiliano Martínez: Argentina, GK, 690.0 min, 7 matches: **goals 0, per 90 0.00**. Other: non_penalty_goals 0; assists 0; shots 0; xg 0; npxg 0; key_passes 0; passes_attempted 186; passes_completed 123; progressive_passes 0; progressive_carries 0; pressures 0; pressured_passes_attempted 23; pressured_passes_completed 12; shot_creating_actions 0; xt_added 0.14; pass_completion_pct 66.1; pressured_pass_completion_pct 52.2

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A033

**Question:** Who was the top non-penalty goal scorer at the 2022 World Cup?

**Ground truth** (The player with the most non-penalty goals, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Kylian Mbappé | France | 6 | 597 | 7 |

**Naive answer:**

> Kylian Mbappé was the top non-penalty goal scorer at the 2022 World Cup with 6 non-penalty goals.

**Reference stats** (true tournament totals):

- Kylian Mbappé: France, W, 597.4 min, 7 matches: **non_penalty_goals 6, per 90 0.90**. Other: goals 8; assists 2; shots 31; xg 4.233; npxg 2.666; key_passes 11; passes_attempted 233; passes_completed 180; progressive_passes 31; progressive_carries 71; pressures 37; pressured_passes_attempted 26; pressured_passes_completed 22; shot_creating_actions 41; xt_added 1.899; pass_completion_pct 77.3; pressured_pass_completion_pct 84.6

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A034

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

## A035

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

## A036

**Question:** how did koopmeiners an widmer do in shot creating actions in the 2022 world cup?

**Ground truth** (Shot-creating actions for Teun Koopmeiners and Silvan Widmer, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Silvan Widmer | Switzerland | 5 | 265 | 3 |
| 1 | Teun Koopmeiners | Netherlands | 5 | 219 | 5 |

**Naive answer:**

> Teun Koopmeiners made 3 shot-creating actions (per 90: 1.22) in 4 matches (198.6 minutes).  
> Silvan Widmer made 2 shot-creating actions (per 90: 0.67) in 3 matches (265.3 minutes).

**Reference stats** (true tournament totals):

- Silvan Widmer: Switzerland, FB, 265.3 min, 3 matches: **shot_creating_actions 5, per 90 1.70**. Other: goals 0; non_penalty_goals 0; assists 1; shots 1; xg 0.051; npxg 0.051; key_passes 2; passes_attempted 164; passes_completed 127; progressive_passes 20; progressive_carries 8; pressures 37; pressured_passes_attempted 13; pressured_passes_completed 9; xt_added 0.673; pass_completion_pct 77.4; pressured_pass_completion_pct 69.2
- Teun Koopmeiners: Netherlands, DM, 218.6 min, 5 matches: **shot_creating_actions 5, per 90 2.06**. Other: goals 0; non_penalty_goals 0; assists 1; shots 2; xg 0.09; npxg 0.09; key_passes 2; passes_attempted 120; passes_completed 95; progressive_passes 18; progressive_carries 4; pressures 55; pressured_passes_attempted 22; pressured_passes_completed 16; xt_added 0.122; pass_completion_pct 79.2; pressured_pass_completion_pct 72.7

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A037

**Question:** Who were the five wingers who contributed the most shot-creating actions in the 2022 World Cup, having played at least 300 minutes?

**Ground truth** (The 5 players with the most shot-creating actions, among wingers (W), with at least 300 minutes, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Kylian Mbappé | France | 41 | 597 | 7 |
| 2 | Hakim Ziyech | Morocco | 20 | 636 | 7 |
| 2 | Raphinha | Brazil | 20 | 316 | 5 |
| 4 | Ivan Perišić | Croatia | 18 | 670 | 7 |
| 4 | Ousmane Dembélé | France | 18 | 435 | 7 |

**Naive answer:**

> The five wingers who contributed the most shot-creating actions (minimum 300 minutes played) in the 2022 World Cup were:
> 
> 1. **Kylian Mbappé (France)** – 41 shot-creating actions  
> 2. **Lionel Messi (Argentina)** – 41 shot-creating actions  
> 3. **André Ayew (Ghana)** – 6 shot-creating actions  
> 4. **Hakim Ziyech (Morocco)** – 7 shot-creating actions  
> 5. **Álvaro Morata (Spain)** – 3 shot-creating actions  
> 
> Note: Only players with at least 300 minutes were considered, and the list is based on the raw total of shot-creating actions.

**Reference stats** (true tournament totals):

- Kylian Mbappé: France, W, 597.4 min, 7 matches: **shot_creating_actions 41, per 90 6.18**. Other: goals 8; non_penalty_goals 6; assists 2; shots 31; xg 4.233; npxg 2.666; key_passes 11; passes_attempted 233; passes_completed 180; progressive_passes 31; progressive_carries 71; pressures 37; pressured_passes_attempted 26; pressured_passes_completed 22; xt_added 1.899; pass_completion_pct 77.3; pressured_pass_completion_pct 84.6
- Hakim Ziyech: Morocco, W, 636.2 min, 7 matches: **shot_creating_actions 20, per 90 2.83**. Other: goals 1; non_penalty_goals 1; assists 1; shots 10; xg 0.312; npxg 0.312; key_passes 7; passes_attempted 300; passes_completed 210; progressive_passes 40; progressive_carries 28; pressures 137; pressured_passes_attempted 31; pressured_passes_completed 23; xt_added 0.541; pass_completion_pct 70.0; pressured_pass_completion_pct 74.2
- Raphinha: Brazil, W, 316.4 min, 5 matches: **shot_creating_actions 20, per 90 5.69**. Other: goals 0; non_penalty_goals 0; assists 0; shots 8; xg 0.923; npxg 0.923; key_passes 8; passes_attempted 150; passes_completed 115; progressive_passes 14; progressive_carries 26; pressures 51; pressured_passes_attempted 16; pressured_passes_completed 11; xt_added 1.426; pass_completion_pct 76.7; pressured_pass_completion_pct 68.8
- Ivan Perišić: Croatia, W, 669.6 min, 7 matches: **shot_creating_actions 18, per 90 2.42**. Other: goals 1; non_penalty_goals 1; assists 3; shots 16; xg 0.756; npxg 0.756; key_passes 9; passes_attempted 304; passes_completed 214; progressive_passes 34; progressive_carries 39; pressures 98; pressured_passes_attempted 51; pressured_passes_completed 35; xt_added 0.994; pass_completion_pct 70.4; pressured_pass_completion_pct 68.6
- Ousmane Dembélé: France, W, 435.3 min, 7 matches: **shot_creating_actions 18, per 90 3.72**. Other: goals 0; non_penalty_goals 0; assists 2; shots 8; xg 0.362; npxg 0.362; key_passes 12; passes_attempted 191; passes_completed 149; progressive_passes 26; progressive_carries 36; pressures 90; pressured_passes_attempted 21; pressured_passes_completed 19; xt_added 1.328; pass_completion_pct 78.0; pressured_pass_completion_pct 90.5
- Lionel Messi: Argentina, ST, 690.0 min, 7 matches: **shot_creating_actions 41, per 90 5.35**. Other: goals 7; non_penalty_goals 3; assists 3; shots 32; xg 6.032; npxg 2.114; key_passes 19; passes_attempted 371; passes_completed 306; progressive_passes 79; progressive_carries 61; pressures 89; pressured_passes_attempted 75; pressured_passes_completed 65; xt_added 1.759; pass_completion_pct 82.5; pressured_pass_completion_pct 86.7
- André Ayew: Ghana, AM, 199.1 min, 3 matches: **shot_creating_actions 0, per 90 0.00**. Other: goals 1; non_penalty_goals 1; assists 0; shots 2; xg 1.269; npxg 0.485; key_passes 0; passes_attempted 37; passes_completed 31; progressive_passes 0; progressive_carries 1; pressures 31; pressured_passes_attempted 9; pressured_passes_completed 7; xt_added -0.038; pass_completion_pct 83.8; pressured_pass_completion_pct 77.8
- Álvaro Morata: Spain, ST, 183.9 min, 4 matches: **shot_creating_actions 3, per 90 1.47**. Other: goals 3; non_penalty_goals 3; assists 1; shots 8; xg 1.109; npxg 1.109; key_passes 1; passes_attempted 40; passes_completed 27; progressive_passes 5; progressive_carries 7; pressures 26; pressured_passes_attempted 11; pressured_passes_completed 8; xt_added -0.044; pass_completion_pct 67.5; pressured_pass_completion_pct 72.7

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A038

**Question:** Which Serbia centre-back had the most passes attempted under pressure?

**Ground truth** (The player with the most passes attempted under pressure, among centre-backs (CB), playing for Serbia, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Nikola Milenković | Serbia | 21 | 270 | 3 |

**Naive answer:**

> The Serbia centre-back with the most passes attempted under pressure is Nikola Milenković, with 21 passes attempted under pressure.

**Reference stats** (true tournament totals):

- Nikola Milenković: Serbia, CB, 270.0 min, 3 matches: **pressured_passes_attempted 21, per 90 7.00**. Other: goals 0; non_penalty_goals 0; assists 0; shots 3; xg 0.123; npxg 0.123; key_passes 0; passes_attempted 157; passes_completed 136; progressive_passes 19; progressive_carries 4; pressures 28; pressured_passes_completed 16; shot_creating_actions 0; xt_added 0.175; pass_completion_pct 86.6; pressured_pass_completion_pct 76.2

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A039

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

## A040

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

## A041

**Question:** how do hassan mohammed al tambakti and timothy castagne stack up in non-penalty xg?

**Ground truth** (Non-penalty xG for Hassan Mohammed Al Tambakti and Timothy Castagne, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Hassan Mohammed Al Tambakti | Saudi Arabia | 0.0 | 180 | 2 |
| 1 | Timothy Castagne | Belgium | 0.0 | 270 | 3 |

**Naive answer:**

> Hassan Mohammed Al Tambakti (Saudi Arabia, CB) has 0.0 xG (non-penalty xG) in 180.0 minutes. Timothy Castagne (Belgium, FB) has 0.0 xG in 270.0 minutes. Both players have 0.0 non-penalty xG.

**Reference stats** (true tournament totals):

- Hassan Mohammed Al Tambakti: Saudi Arabia, CB, 180.0 min, 2 matches: **npxg 0, per 90 0.00**. Other: goals 0; non_penalty_goals 0; assists 0; shots 0; xg 0; key_passes 0; passes_attempted 49; passes_completed 37; progressive_passes 4; progressive_carries 1; pressures 18; pressured_passes_attempted 6; pressured_passes_completed 2; shot_creating_actions 0; xt_added -0.075; pass_completion_pct 75.5; pressured_pass_completion_pct 33.3
- Timothy Castagne: Belgium, FB, 270.0 min, 3 matches: **npxg 0, per 90 0.00**. Other: goals 0; non_penalty_goals 0; assists 0; shots 0; xg 0; key_passes 0; passes_attempted 201; passes_completed 176; progressive_passes 30; progressive_carries 3; pressures 31; pressured_passes_attempted 29; pressured_passes_completed 19; shot_creating_actions 0; xt_added 0.147; pass_completion_pct 87.6; pressured_pass_completion_pct 65.5

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A042

**Question:** What was Frankowski's total shot count in the 2022 World Cup?

**Ground truth** (Shots for Przemysław Frankowski, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Przemysław Frankowski | Poland | 1 | 240 | 4 |

**Naive answer:**

> Przemysław Frankowski had a total shot count of 1 in the 2022 World Cup.

**Reference stats** (true tournament totals):

- Przemysław Frankowski: Poland, W, 240.1 min, 4 matches: **shots 1, per 90 0.37**. Other: goals 0; non_penalty_goals 0; assists 0; xg 0.044; npxg 0.044; key_passes 1; passes_attempted 73; passes_completed 51; progressive_passes 8; progressive_carries 4; pressures 39; pressured_passes_attempted 11; pressured_passes_completed 6; shot_creating_actions 3; xt_added 0.082; pass_completion_pct 69.9; pressured_pass_completion_pct 54.5

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A043

**Question:** Which five Canadian players recorded the highest non-penalty expected goals during the 2022 World Cup?

**Ground truth** (The 5 players with the most non-penalty xG, playing for Canada, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Jonathan David | Canada | 0.81 | 193 | 3 |
| 2 | Tajon Buchanan | Canada | 0.71 | 260 | 3 |
| 3 | Alistair Johnston | Canada | 0.67 | 270 | 3 |
| 4 | Cyle Larin | Canada | 0.25 | 137 | 3 |
| 5 | Stephen Antunes Eustáquio | Canada | 0.16 | 125 | 2 |

**Naive answer:**

> The five Canadian players with the highest non-penalty expected goals (npxG) during the 2022 World Cup are:
> 
> 1. Tajon Buchanan - 0.71  
> 2. Cyle Larin - 0.81  
> 3. Alphonso Davies - 0.14  
> 4. Richie Laryea - 0.51  
> 5. Junior Hoilett - 0.12

**Reference stats** (true tournament totals):

- Jonathan David: Canada, ST, 192.7 min, 3 matches: **npxg 0.813, per 90 0.38**. Other: goals 0; non_penalty_goals 0; assists 0; shots 8; xg 0.813; key_passes 0; passes_attempted 59; passes_completed 43; progressive_passes 9; progressive_carries 4; pressures 28; pressured_passes_attempted 14; pressured_passes_completed 11; shot_creating_actions 0; xt_added 0.021; pass_completion_pct 72.9; pressured_pass_completion_pct 78.6
- Tajon Buchanan: Canada, W, 260.2 min, 3 matches: **npxg 0.714, per 90 0.25**. Other: goals 0; non_penalty_goals 0; assists 1; shots 5; xg 0.714; key_passes 4; passes_attempted 88; passes_completed 61; progressive_passes 12; progressive_carries 20; pressures 43; pressured_passes_attempted 8; pressured_passes_completed 3; shot_creating_actions 6; xt_added 0.495; pass_completion_pct 69.3; pressured_pass_completion_pct 37.5
- Alistair Johnston: Canada, FB, 270.0 min, 3 matches: **npxg 0.672, per 90 0.22**. Other: goals 0; non_penalty_goals 0; assists 0; shots 2; xg 0.672; key_passes 4; passes_attempted 187; passes_completed 156; progressive_passes 24; progressive_carries 8; pressures 38; pressured_passes_attempted 21; pressured_passes_completed 21; shot_creating_actions 11; xt_added 0.471; pass_completion_pct 83.4; pressured_pass_completion_pct 100.0
- Cyle Larin: Canada, ST, 137.4 min, 3 matches: **npxg 0.25, per 90 0.16**. Other: goals 0; non_penalty_goals 0; assists 0; shots 3; xg 0.25; key_passes 2; passes_attempted 31; passes_completed 21; progressive_passes 8; progressive_carries 5; pressures 21; pressured_passes_attempted 8; pressured_passes_completed 4; shot_creating_actions 5; xt_added 0.359; pass_completion_pct 67.7; pressured_pass_completion_pct 50.0
- Stephen Antunes Eustáquio: Canada, DM, 125.4 min, 2 matches: **npxg 0.165, per 90 0.12**. Other: goals 0; non_penalty_goals 0; assists 0; shots 3; xg 0.165; key_passes 2; passes_attempted 93; passes_completed 85; progressive_passes 20; progressive_carries 0; pressures 20; pressured_passes_attempted 6; pressured_passes_completed 6; shot_creating_actions 6; xt_added 0.339; pass_completion_pct 91.4; pressured_pass_completion_pct 100.0
- Alphonso Davies: Canada, AM, 270.0 min, 3 matches: **npxg 0.145, per 90 0.05**. Other: goals 1; non_penalty_goals 1; assists 0; shots 4; xg 0.929; key_passes 4; passes_attempted 114; passes_completed 82; progressive_passes 4; progressive_carries 18; pressures 48; pressured_passes_attempted 11; pressured_passes_completed 6; shot_creating_actions 8; xt_added 0.2; pass_completion_pct 71.9; pressured_pass_completion_pct 54.5
- Richie Laryea: Canada, FB, 159.6 min, 3 matches: **npxg 0.057, per 90 0.03**. Other: goals 0; non_penalty_goals 0; assists 0; shots 2; xg 0.057; key_passes 4; passes_attempted 45; passes_completed 35; progressive_passes 3; progressive_carries 11; pressures 25; pressured_passes_attempted 4; pressured_passes_completed 2; shot_creating_actions 5; xt_added 0.518; pass_completion_pct 77.8; pressured_pass_completion_pct 50.0
- Junior Hoilett: Canada, W, 161.4 min, 3 matches: **npxg 0.119, per 90 0.07**. Other: goals 0; non_penalty_goals 0; assists 0; shots 4; xg 0.119; key_passes 4; passes_attempted 55; passes_completed 40; progressive_passes 10; progressive_carries 10; pressures 18; pressured_passes_attempted 11; pressured_passes_completed 8; shot_creating_actions 8; xt_added 0.461; pass_completion_pct 72.7; pressured_pass_completion_pct 72.7

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A044

**Question:** whicg 3 forwards attemped most passis undr pressur in 2022 world cup?

**Ground truth** (The 3 players with the most passes attempted under pressure, among forwards (ST, W), World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Lionel Messi | Argentina | 75 | 690 | 7 |
| 2 | Ivan Perišić | Croatia | 51 | 670 | 7 |
| 3 | Mathew Leckie | Australia | 36 | 334 | 4 |

**Naive answer:**

> The three forwards who attempted the most passes under pressure in the 2022 World Cup are:
> 
> 1. **Christian Pulisic (United States, W)** - 44 passes under pressure  
> 2. **Lionel Messi (Argentina, ST)** - 89 passes under pressure  
> 3. **Hakim Ziyech (Morocco, W)** - 137 passes under pressure

**Reference stats** (true tournament totals):

- Lionel Messi: Argentina, ST, 690.0 min, 7 matches: **pressured_passes_attempted 75, per 90 9.78**. Other: goals 7; non_penalty_goals 3; assists 3; shots 32; xg 6.032; npxg 2.114; key_passes 19; passes_attempted 371; passes_completed 306; progressive_passes 79; progressive_carries 61; pressures 89; pressured_passes_completed 65; shot_creating_actions 41; xt_added 1.759; pass_completion_pct 82.5; pressured_pass_completion_pct 86.7
- Ivan Perišić: Croatia, W, 669.6 min, 7 matches: **pressured_passes_attempted 51, per 90 6.85**. Other: goals 1; non_penalty_goals 1; assists 3; shots 16; xg 0.756; npxg 0.756; key_passes 9; passes_attempted 304; passes_completed 214; progressive_passes 34; progressive_carries 39; pressures 98; pressured_passes_completed 35; shot_creating_actions 18; xt_added 0.994; pass_completion_pct 70.4; pressured_pass_completion_pct 68.6
- Mathew Leckie: Australia, W, 334.4 min, 4 matches: **pressured_passes_attempted 36, per 90 9.69**. Other: goals 1; non_penalty_goals 1; assists 1; shots 1; xg 0.114; npxg 0.114; key_passes 2; passes_attempted 103; passes_completed 69; progressive_passes 14; progressive_carries 10; pressures 68; pressured_passes_completed 20; shot_creating_actions 5; xt_added 0.113; pass_completion_pct 67.0; pressured_pass_completion_pct 55.6
- Christian Pulisic: United States, W, 315.0 min, 4 matches: **pressured_passes_attempted 27, per 90 7.71**. Other: goals 1; non_penalty_goals 1; assists 2; shots 9; xg 1.138; npxg 1.138; key_passes 9; passes_attempted 139; passes_completed 84; progressive_passes 21; progressive_carries 33; pressures 44; pressured_passes_completed 20; shot_creating_actions 16; xt_added 0.679; pass_completion_pct 60.4; pressured_pass_completion_pct 74.1
- Hakim Ziyech: Morocco, W, 636.2 min, 7 matches: **pressured_passes_attempted 31, per 90 4.39**. Other: goals 1; non_penalty_goals 1; assists 1; shots 10; xg 0.312; npxg 0.312; key_passes 7; passes_attempted 300; passes_completed 210; progressive_passes 40; progressive_carries 28; pressures 137; pressured_passes_completed 23; shot_creating_actions 20; xt_added 0.541; pass_completion_pct 70.0; pressured_pass_completion_pct 74.2

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A045

**Question:** What was Sofiane Boufal's total shot-creating actions count in the 2022 World Cup?

**Ground truth** (Shot-creating actions for Sofiane Boufal, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Sofiane Boufal | Morocco | 15 | 477 | 7 |

**Naive answer:**

> Sofiane Boufal had a total of **4 shot-creating actions** in the 2022 World Cup.

**Reference stats** (true tournament totals):

- Sofiane Boufal: Morocco, W, 476.7 min, 7 matches: **shot_creating_actions 15, per 90 2.83**. Other: goals 0; non_penalty_goals 0; assists 0; shots 7; xg 0.316; npxg 0.316; key_passes 4; passes_attempted 134; passes_completed 107; progressive_passes 23; progressive_carries 33; pressures 93; pressured_passes_attempted 18; pressured_passes_completed 11; xt_added 0.985; pass_completion_pct 79.9; pressured_pass_completion_pct 61.1

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A046

**Question:** Who was the top-scoring striker in the 2022 World Cup?

**Ground truth** (The player with the most goals, among strikers (ST), World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Lionel Messi | Argentina | 7 | 690 | 7 |

**Naive answer:**

> Kylian Mbappé from France was the top-scoring striker in the 2022 World Cup, scoring 8 goals (7 non-penalty goals) in 7 matches.

**Reference stats** (true tournament totals):

- Lionel Messi: Argentina, ST, 690.0 min, 7 matches: **goals 7, per 90 0.91**. Other: non_penalty_goals 3; assists 3; shots 32; xg 6.032; npxg 2.114; key_passes 19; passes_attempted 371; passes_completed 306; progressive_passes 79; progressive_carries 61; pressures 89; pressured_passes_attempted 75; pressured_passes_completed 65; shot_creating_actions 41; xt_added 1.759; pass_completion_pct 82.5; pressured_pass_completion_pct 86.7
- Kylian Mbappé: France, W, 597.4 min, 7 matches: **goals 8, per 90 1.21**. Other: non_penalty_goals 6; assists 2; shots 31; xg 4.233; npxg 2.666; key_passes 11; passes_attempted 233; passes_completed 180; progressive_passes 31; progressive_carries 71; pressures 37; pressured_passes_attempted 26; pressured_passes_completed 22; shot_creating_actions 41; xt_added 1.899; pass_completion_pct 77.3; pressured_pass_completion_pct 84.6

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A047

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

## A048

**Question:** How many shots did Frankowski have?

**Ground truth** (Shots for Przemysław Frankowski, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Przemysław Frankowski | Poland | 1 | 240 | 4 |

**Naive answer:**

> Przemysław Frankowski had 1 shot.

**Reference stats** (true tournament totals):

- Przemysław Frankowski: Poland, W, 240.1 min, 4 matches: **shots 1, per 90 0.37**. Other: goals 0; non_penalty_goals 0; assists 0; xg 0.044; npxg 0.044; key_passes 1; passes_attempted 73; passes_completed 51; progressive_passes 8; progressive_carries 4; pressures 39; pressured_passes_attempted 11; pressured_passes_completed 6; shot_creating_actions 3; xt_added 0.082; pass_completion_pct 69.9; pressured_pass_completion_pct 54.5

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A049

**Question:** which 3 belgium players had the most passes tried under pressure in the 2022 world cup?

**Ground truth** (The 3 players with the most passes attempted under pressure, playing for Belgium, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Timothy Castagne | Belgium | 29 | 270 | 3 |
| 2 | Kevin De Bruyne | Belgium | 24 | 270 | 3 |
| 3 | Toby Alderweireld | Belgium | 23 | 270 | 3 |

**Naive answer:**

> The three Belgium players with the most passes attempted under pressure in the 2022 World Cup are:
> 
> 1. Kevin De Bruyne - 24 passes attempted under pressure  
> 2. Thomas Meunier - 19 passes attempted under pressure  
> 3. Thorgan Hazard - 6 passes attempted under pressure

**Reference stats** (true tournament totals):

- Timothy Castagne: Belgium, FB, 270.0 min, 3 matches: **pressured_passes_attempted 29, per 90 9.67**. Other: goals 0; non_penalty_goals 0; assists 0; shots 0; xg 0; npxg 0; key_passes 0; passes_attempted 201; passes_completed 176; progressive_passes 30; progressive_carries 3; pressures 31; pressured_passes_completed 19; shot_creating_actions 0; xt_added 0.147; pass_completion_pct 87.6; pressured_pass_completion_pct 65.5
- Kevin De Bruyne: Belgium, W, 270.0 min, 3 matches: **pressured_passes_attempted 24, per 90 8.00**. Other: goals 0; non_penalty_goals 0; assists 0; shots 7; xg 0.178; npxg 0.178; key_passes 8; passes_attempted 140; passes_completed 100; progressive_passes 31; progressive_carries 16; pressures 25; pressured_passes_completed 14; shot_creating_actions 10; xt_added 1.17; pass_completion_pct 71.4; pressured_pass_completion_pct 58.3
- Toby Alderweireld: Belgium, CB, 270.0 min, 3 matches: **pressured_passes_attempted 23, per 90 7.67**. Other: goals 0; non_penalty_goals 0; assists 1; shots 0; xg 0; npxg 0; key_passes 1; passes_attempted 267; passes_completed 244; progressive_passes 25; progressive_carries 2; pressures 13; pressured_passes_completed 21; shot_creating_actions 3; xt_added 0.347; pass_completion_pct 91.4; pressured_pass_completion_pct 91.3
- Thomas Meunier: Belgium, FB, 212.3 min, 3 matches: **pressured_passes_attempted 19, per 90 8.05**. Other: goals 0; non_penalty_goals 0; assists 0; shots 3; xg 0.119; npxg 0.119; key_passes 2; passes_attempted 142; passes_completed 109; progressive_passes 10; progressive_carries 8; pressures 24; pressured_passes_completed 13; shot_creating_actions 7; xt_added 0.171; pass_completion_pct 76.8; pressured_pass_completion_pct 68.4
- Thorgan Hazard: Belgium, W, 106.0 min, 2 matches: **pressured_passes_attempted 6, per 90 5.09**. Other: goals 0; non_penalty_goals 0; assists 0; shots 0; xg 0; npxg 0; key_passes 5; passes_attempted 59; passes_completed 41; progressive_passes 5; progressive_carries 2; pressures 31; pressured_passes_completed 4; shot_creating_actions 7; xt_added 0.379; pass_completion_pct 69.5; pressured_pass_completion_pct 66.7

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A050

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

## A051

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

## A052

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

## A053

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

## A054

**Question:** Which player had the most non-penalty goals?

**Ground truth** (The player with the most non-penalty goals, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Kylian Mbappé | France | 6 | 597 | 7 |

**Naive answer:**

> Lionel Messi from Argentina had the most non-penalty goals with 7.

**Reference stats** (true tournament totals):

- Kylian Mbappé: France, W, 597.4 min, 7 matches: **non_penalty_goals 6, per 90 0.90**. Other: goals 8; assists 2; shots 31; xg 4.233; npxg 2.666; key_passes 11; passes_attempted 233; passes_completed 180; progressive_passes 31; progressive_carries 71; pressures 37; pressured_passes_attempted 26; pressured_passes_completed 22; shot_creating_actions 41; xt_added 1.899; pass_completion_pct 77.3; pressured_pass_completion_pct 84.6
- Lionel Messi: Argentina, ST, 690.0 min, 7 matches: **non_penalty_goals 3, per 90 0.39**. Other: goals 7; assists 3; shots 32; xg 6.032; npxg 2.114; key_passes 19; passes_attempted 371; passes_completed 306; progressive_passes 79; progressive_carries 61; pressures 89; pressured_passes_attempted 75; pressured_passes_completed 65; shot_creating_actions 41; xt_added 1.759; pass_completion_pct 82.5; pressured_pass_completion_pct 86.7

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A055

**Question:** whos the player wid the most non penalty goals in the 2022 world cup?

**Ground truth** (The player with the most non-penalty goals, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Kylian Mbappé | France | 6 | 597 | 7 |

**Naive answer:**

> Kylian Mbappé of France had the most non-penalty goals in the 2022 World Cup, with 6 non-penalty goals.

**Reference stats** (true tournament totals):

- Kylian Mbappé: France, W, 597.4 min, 7 matches: **non_penalty_goals 6, per 90 0.90**. Other: goals 8; assists 2; shots 31; xg 4.233; npxg 2.666; key_passes 11; passes_attempted 233; passes_completed 180; progressive_passes 31; progressive_carries 71; pressures 37; pressured_passes_attempted 26; pressured_passes_completed 22; shot_creating_actions 41; xt_added 1.899; pass_completion_pct 77.3; pressured_pass_completion_pct 84.6

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A056

**Question:** Compare Hassan Mohammed Al Tambakti and Timothy Castagne on non-penalty xG.

**Ground truth** (Non-penalty xG for Hassan Mohammed Al Tambakti and Timothy Castagne, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Hassan Mohammed Al Tambakti | Saudi Arabia | 0.0 | 180 | 2 |
| 1 | Timothy Castagne | Belgium | 0.0 | 270 | 3 |

**Naive answer:**

> Hassan Mohammed Al Tambakti (Saudi Arabia, CB) has 0.0 xG, while Timothy Castagne (Belgium, FB) has 0.0 xG. Both have 0.0 non-penalty xG.

**Reference stats** (true tournament totals):

- Hassan Mohammed Al Tambakti: Saudi Arabia, CB, 180.0 min, 2 matches: **npxg 0, per 90 0.00**. Other: goals 0; non_penalty_goals 0; assists 0; shots 0; xg 0; key_passes 0; passes_attempted 49; passes_completed 37; progressive_passes 4; progressive_carries 1; pressures 18; pressured_passes_attempted 6; pressured_passes_completed 2; shot_creating_actions 0; xt_added -0.075; pass_completion_pct 75.5; pressured_pass_completion_pct 33.3
- Timothy Castagne: Belgium, FB, 270.0 min, 3 matches: **npxg 0, per 90 0.00**. Other: goals 0; non_penalty_goals 0; assists 0; shots 0; xg 0; key_passes 0; passes_attempted 201; passes_completed 176; progressive_passes 30; progressive_carries 3; pressures 31; pressured_passes_attempted 29; pressured_passes_completed 19; shot_creating_actions 0; xt_added 0.147; pass_completion_pct 87.6; pressured_pass_completion_pct 65.5

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A057

**Question:** how many times did frankowski shoot in the 2022 world cup

**Ground truth** (Shots for Przemysław Frankowski, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Przemysław Frankowski | Poland | 1 | 240 | 4 |

**Naive answer:**

> Przemysław Frankowski shot 1 time in the 2022 World Cup.

**Reference stats** (true tournament totals):

- Przemysław Frankowski: Poland, W, 240.1 min, 4 matches: **shots 1, per 90 0.37**. Other: goals 0; non_penalty_goals 0; assists 0; xg 0.044; npxg 0.044; key_passes 1; passes_attempted 73; passes_completed 51; progressive_passes 8; progressive_carries 4; pressures 39; pressured_passes_attempted 11; pressured_passes_completed 6; shot_creating_actions 3; xt_added 0.082; pass_completion_pct 69.9; pressured_pass_completion_pct 54.5

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A058

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

## A059

**Question:** What was Nahuel Molina's key passes tally at the 2022 World Cup?

**Ground truth** (Key passes for Nahuel Molina, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Nahuel Molina | Argentina | 3 | 568 | 7 |

**Naive answer:**

> Nahuel Molina's key passes tally at the 2022 World Cup was **3**.

**Reference stats** (true tournament totals):

- Nahuel Molina: Argentina, FB, 567.7 min, 7 matches: **key_passes 3, per 90 0.48**. Other: goals 1; non_penalty_goals 1; assists 1; shots 2; xg 0.485; npxg 0.485; passes_attempted 360; passes_completed 296; progressive_passes 29; progressive_carries 16; pressures 72; pressured_passes_attempted 35; pressured_passes_completed 24; shot_creating_actions 10; xt_added 0.473; pass_completion_pct 82.2; pressured_pass_completion_pct 68.6

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A060

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

## A061

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

## A062

**Question:** Which 5 United States players had the most xG?

**Ground truth** (The 5 players with the most expected goals (xG), playing for United States, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Christian Pulisic | United States | 1.14 | 315 | 4 |
| 2 | Haji Wright | United States | 0.66 | 135 | 4 |
| 3 | Timothy Weah | United States | 0.44 | 318 | 4 |
| 4 | Weston McKennie | United States | 0.38 | 274 | 4 |
| 5 | Josh Sargent | United States | 0.36 | 158 | 3 |

**Naive answer:**

> The 5 United States players with the most xG (expected goals) are:
> 
> 1. Christian Pulisic - 1.14 xG  
> 2. Weston McKennie - 0.38 xG  
> 3. Walker Zimmerman - 0.06 xG  
> 4. Harry Souttar - 0.06 xG  
> 5. Brenden Aaronson - 0.09 xG

**Reference stats** (true tournament totals):

- Christian Pulisic: United States, W, 315.0 min, 4 matches: **xg 1.138, per 90 0.33**. Other: goals 1; non_penalty_goals 1; assists 2; shots 9; npxg 1.138; key_passes 9; passes_attempted 139; passes_completed 84; progressive_passes 21; progressive_carries 33; pressures 44; pressured_passes_attempted 27; pressured_passes_completed 20; shot_creating_actions 16; xt_added 0.679; pass_completion_pct 60.4; pressured_pass_completion_pct 74.1
- Haji Wright: United States, ST, 135.2 min, 4 matches: **xg 0.658, per 90 0.44**. Other: goals 1; non_penalty_goals 1; assists 0; shots 7; npxg 0.658; key_passes 1; passes_attempted 27; passes_completed 20; progressive_passes 3; progressive_carries 4; pressures 25; pressured_passes_attempted 7; pressured_passes_completed 3; shot_creating_actions 3; xt_added 0.026; pass_completion_pct 74.1; pressured_pass_completion_pct 42.9
- Timothy Weah: United States, W, 317.9 min, 4 matches: **xg 0.44, per 90 0.12**. Other: goals 1; non_penalty_goals 1; assists 0; shots 5; npxg 0.44; key_passes 6; passes_attempted 109; passes_completed 91; progressive_passes 11; progressive_carries 11; pressures 26; pressured_passes_attempted 20; pressured_passes_completed 17; shot_creating_actions 8; xt_added 0.188; pass_completion_pct 83.5; pressured_pass_completion_pct 85.0
- Weston McKennie: United States, CM, 273.6 min, 4 matches: **xg 0.376, per 90 0.12**. Other: goals 0; non_penalty_goals 0; assists 0; shots 5; npxg 0.376; key_passes 3; passes_attempted 146; passes_completed 117; progressive_passes 30; progressive_carries 17; pressures 40; pressured_passes_attempted 20; pressured_passes_completed 14; shot_creating_actions 11; xt_added 0.423; pass_completion_pct 80.1; pressured_pass_completion_pct 70.0
- Josh Sargent: United States, ST, 157.9 min, 3 matches: **xg 0.362, per 90 0.21**. Other: goals 0; non_penalty_goals 0; assists 0; shots 4; npxg 0.362; key_passes 1; passes_attempted 34; passes_completed 30; progressive_passes 1; progressive_carries 3; pressures 26; pressured_passes_attempted 7; pressured_passes_completed 6; shot_creating_actions 3; xt_added -0.013; pass_completion_pct 88.2; pressured_pass_completion_pct 85.7
- Walker Zimmerman: United States, CB, 278.9 min, 4 matches: **xg 0.057, per 90 0.02**. Other: goals 0; non_penalty_goals 0; assists 0; shots 1; npxg 0.057; key_passes 0; passes_attempted 233; passes_completed 212; progressive_passes 19; progressive_carries 1; pressures 17; pressured_passes_attempted 10; pressured_passes_completed 8; shot_creating_actions 4; xt_added 0.141; pass_completion_pct 91.0; pressured_pass_completion_pct 80.0
- Harry Souttar: Australia, CB, 360.0 min, 4 matches: **xg 0.068, per 90 0.02**. Other: goals 0; non_penalty_goals 0; assists 0; shots 1; npxg 0.068; key_passes 1; passes_attempted 163; passes_completed 135; progressive_passes 8; progressive_carries 0; pressures 28; pressured_passes_attempted 20; pressured_passes_completed 17; shot_creating_actions 2; xt_added 0.261; pass_completion_pct 82.8; pressured_pass_completion_pct 85.0
- Brenden Aaronson: United States, W, 106.2 min, 4 matches: **xg 0.094, per 90 0.08**. Other: goals 0; non_penalty_goals 0; assists 0; shots 1; npxg 0.094; key_passes 3; passes_attempted 48; passes_completed 41; progressive_passes 6; progressive_carries 5; pressures 32; pressured_passes_attempted 4; pressured_passes_completed 3; shot_creating_actions 3; xt_added 0.125; pass_completion_pct 85.4; pressured_pass_completion_pct 75.0

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A063

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

## A064

**Question:** Top 5 players with the most shots in the 2022 World Cup?

**Ground truth** (The 5 players with the most shots, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Lionel Messi | Argentina | 32 | 690 | 7 |
| 2 | Kylian Mbappé | France | 31 | 597 | 7 |
| 3 | Olivier Giroud | France | 17 | 422 | 6 |
| 4 | Ivan Perišić | Croatia | 16 | 670 | 7 |
| 5 | Lautaro Martínez | Argentina | 14 | 241 | 6 |

**Naive answer:**

> 1. **Christian Pulisic** (United States, W) - 9 shots  
> 2. **Ousmane Dembélé** (France, W) - 8 shots  
> 3. **Richarlison** (Brazil, ST) - 8 shots  
> 4. **Salem Al Dawsari** (Saudi Arabia, W) - 7 shots  
> 5. **Kylian Mbappé** (France, W) - 7 shots

**Reference stats** (true tournament totals):

- Lionel Messi: Argentina, ST, 690.0 min, 7 matches: **shots 32, per 90 4.17**. Other: goals 7; non_penalty_goals 3; assists 3; xg 6.032; npxg 2.114; key_passes 19; passes_attempted 371; passes_completed 306; progressive_passes 79; progressive_carries 61; pressures 89; pressured_passes_attempted 75; pressured_passes_completed 65; shot_creating_actions 41; xt_added 1.759; pass_completion_pct 82.5; pressured_pass_completion_pct 86.7
- Kylian Mbappé: France, W, 597.4 min, 7 matches: **shots 31, per 90 4.67**. Other: goals 8; non_penalty_goals 6; assists 2; xg 4.233; npxg 2.666; key_passes 11; passes_attempted 233; passes_completed 180; progressive_passes 31; progressive_carries 71; pressures 37; pressured_passes_attempted 26; pressured_passes_completed 22; shot_creating_actions 41; xt_added 1.899; pass_completion_pct 77.3; pressured_pass_completion_pct 84.6
- Olivier Giroud: France, ST, 422.1 min, 6 matches: **shots 17, per 90 3.62**. Other: goals 4; non_penalty_goals 4; assists 0; xg 3.036; npxg 3.036; key_passes 2; passes_attempted 75; passes_completed 49; progressive_passes 9; progressive_carries 2; pressures 60; pressured_passes_attempted 25; pressured_passes_completed 12; shot_creating_actions 4; xt_added 0.16; pass_completion_pct 65.3; pressured_pass_completion_pct 48.0
- Ivan Perišić: Croatia, W, 669.6 min, 7 matches: **shots 16, per 90 2.15**. Other: goals 1; non_penalty_goals 1; assists 3; xg 0.756; npxg 0.756; key_passes 9; passes_attempted 304; passes_completed 214; progressive_passes 34; progressive_carries 39; pressures 98; pressured_passes_attempted 51; pressured_passes_completed 35; shot_creating_actions 18; xt_added 0.994; pass_completion_pct 70.4; pressured_pass_completion_pct 68.6
- Lautaro Martínez: Argentina, ST, 240.6 min, 6 matches: **shots 14, per 90 5.24**. Other: goals 0; non_penalty_goals 0; assists 0; xg 2.122; npxg 2.122; key_passes 0; passes_attempted 63; passes_completed 46; progressive_passes 2; progressive_carries 6; pressures 20; pressured_passes_attempted 18; pressured_passes_completed 10; shot_creating_actions 9; xt_added 0.248; pass_completion_pct 73.0; pressured_pass_completion_pct 55.6
- Christian Pulisic: United States, W, 315.0 min, 4 matches: **shots 9, per 90 2.57**. Other: goals 1; non_penalty_goals 1; assists 2; xg 1.138; npxg 1.138; key_passes 9; passes_attempted 139; passes_completed 84; progressive_passes 21; progressive_carries 33; pressures 44; pressured_passes_attempted 27; pressured_passes_completed 20; shot_creating_actions 16; xt_added 0.679; pass_completion_pct 60.4; pressured_pass_completion_pct 74.1
- Ousmane Dembélé: France, W, 435.3 min, 7 matches: **shots 8, per 90 1.65**. Other: goals 0; non_penalty_goals 0; assists 2; xg 0.362; npxg 0.362; key_passes 12; passes_attempted 191; passes_completed 149; progressive_passes 26; progressive_carries 36; pressures 90; pressured_passes_attempted 21; pressured_passes_completed 19; shot_creating_actions 18; xt_added 1.328; pass_completion_pct 78.0; pressured_pass_completion_pct 90.5
- Richarlison: Brazil, ST, 324.3 min, 4 matches: **shots 8, per 90 2.22**. Other: goals 3; non_penalty_goals 3; assists 0; xg 1.618; npxg 1.618; key_passes 5; passes_attempted 54; passes_completed 39; progressive_passes 4; progressive_carries 9; pressures 59; pressured_passes_attempted 14; pressured_passes_completed 11; shot_creating_actions 8; xt_added 0.043; pass_completion_pct 72.2; pressured_pass_completion_pct 78.6
- Salem Al Dawsari: Saudi Arabia, W, 270.0 min, 3 matches: **shots 7, per 90 2.33**. Other: goals 2; non_penalty_goals 2; assists 0; xg 1.564; npxg 0.781; key_passes 6; passes_attempted 117; passes_completed 92; progressive_passes 18; progressive_carries 13; pressures 42; pressured_passes_attempted 16; pressured_passes_completed 11; shot_creating_actions 14; xt_added 0.613; pass_completion_pct 78.6; pressured_pass_completion_pct 68.8

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A065

**Question:** Looking at the 2022 World Cup, which Serbia central defender had the highest total of passes attempted under pressure?

**Ground truth** (The player with the most passes attempted under pressure, among centre-backs (CB), playing for Serbia, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Nikola Milenković | Serbia | 21 | 270 | 3 |

**Naive answer:**

> The Serbian central defender with the highest total of passes attempted under pressure was **Nikola Milenković**, with **21 passes attempted under pressure.**

**Reference stats** (true tournament totals):

- Nikola Milenković: Serbia, CB, 270.0 min, 3 matches: **pressured_passes_attempted 21, per 90 7.00**. Other: goals 0; non_penalty_goals 0; assists 0; shots 3; xg 0.123; npxg 0.123; key_passes 0; passes_attempted 157; passes_completed 136; progressive_passes 19; progressive_carries 4; pressures 28; pressured_passes_completed 16; shot_creating_actions 0; xt_added 0.175; pass_completion_pct 86.6; pressured_pass_completion_pct 76.2

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A066

**Question:** Top 5 CBs with the most goals per 90, 2022 WC, min 180 mins played

**Ground truth** (The 5 players with the highest goals per 90, among centre-backs (CB), with at least 180 minutes, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Jean-Charles Castelletto | Cameroon | 0.5 | 180 | 2 |
| 2 | Achraf Dari | Morocco | 0.48 | 186 | 3 |
| 3 | Strahinja Pavlović | Serbia | 0.38 | 235 | 3 |
| 4 | Andreas Christensen | Denmark | 0.33 | 270 | 3 |
| 4 | Mohamed Salisu | Ghana | 0.33 | 270 | 3 |

**Naive answer:**

> The top 5 centre-backs (CBs) with the most goals per 90 minutes in the 2022 World Cup (minimum 180 minutes played) are:
> 
> 1. **Kalidou Koulibaly (Senegal)** – 0.23 g/90  
> 2. **Mohamed Salisu (Ghana)** – 0.43 g/90  
> 3. **Youssef En-Nesyri (Morocco)** – 0.35 g/90  
> 4. **Abdou Diallo (Senegal)** – 0.04 g/90  
> 5. **Jean-Charles Castelletto (Cameroon)** – 0.90 g/90  
> 
> *Note: Only 4 CBs met the criteria for goals, with Jean-Charles Castelletto (Cameroon) being the only one with multiple goals in limited minutes.*

**Reference stats** (true tournament totals):

- Jean-Charles Castelletto: Cameroon, CB, 180.0 min, 2 matches: **goals 1, per 90 0.50**. Other: non_penalty_goals 1; assists 1; shots 1; xg 0.895; npxg 0.895; key_passes 1; passes_attempted 78; passes_completed 63; progressive_passes 10; progressive_carries 4; pressures 20; pressured_passes_attempted 17; pressured_passes_completed 14; shot_creating_actions 1; xt_added 0.088; pass_completion_pct 80.8; pressured_pass_completion_pct 82.4
- Achraf Dari: Morocco, CB, 186.4 min, 3 matches: **goals 1, per 90 0.48**. Other: non_penalty_goals 1; assists 0; shots 1; xg 0.418; npxg 0.418; key_passes 0; passes_attempted 107; passes_completed 96; progressive_passes 7; progressive_carries 0; pressures 17; pressured_passes_attempted 3; pressured_passes_completed 0; shot_creating_actions 0; xt_added 0.099; pass_completion_pct 89.7; pressured_pass_completion_pct 0.0
- Strahinja Pavlović: Serbia, CB, 235.4 min, 3 matches: **goals 1, per 90 0.38**. Other: non_penalty_goals 1; assists 0; shots 2; xg 0.178; npxg 0.178; key_passes 0; passes_attempted 152; passes_completed 121; progressive_passes 29; progressive_carries 12; pressures 33; pressured_passes_attempted 19; pressured_passes_completed 11; shot_creating_actions 2; xt_added 0.285; pass_completion_pct 79.6; pressured_pass_completion_pct 57.9
- Andreas Christensen: Denmark, CB, 270.0 min, 3 matches: **goals 1, per 90 0.33**. Other: non_penalty_goals 1; assists 0; shots 2; xg 0.525; npxg 0.525; key_passes 0; passes_attempted 250; passes_completed 236; progressive_passes 32; progressive_carries 8; pressures 11; pressured_passes_attempted 17; pressured_passes_completed 13; shot_creating_actions 1; xt_added 0.233; pass_completion_pct 94.4; pressured_pass_completion_pct 76.5
- Mohamed Salisu: Ghana, CB, 270.0 min, 3 matches: **goals 1, per 90 0.33**. Other: non_penalty_goals 1; assists 0; shots 2; xg 0.428; npxg 0.428; key_passes 0; passes_attempted 149; passes_completed 106; progressive_passes 23; progressive_carries 6; pressures 20; pressured_passes_attempted 16; pressured_passes_completed 7; shot_creating_actions 3; xt_added 0.185; pass_completion_pct 71.1; pressured_pass_completion_pct 43.8
- Kalidou Koulibaly: Senegal, CB, 360.0 min, 4 matches: **goals 1, per 90 0.25**. Other: non_penalty_goals 1; assists 0; shots 1; xg 0.234; npxg 0.234; key_passes 1; passes_attempted 196; passes_completed 152; progressive_passes 21; progressive_carries 6; pressures 34; pressured_passes_attempted 18; pressured_passes_completed 10; shot_creating_actions 5; xt_added 0.149; pass_completion_pct 77.6; pressured_pass_completion_pct 55.6
- Youssef En-Nesyri: Morocco, ST, 543.8 min, 7 matches: **goals 2, per 90 0.33**. Other: non_penalty_goals 2; assists 0; shots 11; xg 1.046; npxg 1.046; key_passes 1; passes_attempted 76; passes_completed 48; progressive_passes 2; progressive_carries 2; pressures 113; pressured_passes_attempted 19; pressured_passes_completed 9; shot_creating_actions 3; xt_added 0.121; pass_completion_pct 63.2; pressured_pass_completion_pct 47.4
- Abdou Diallo: Senegal, CB, 331.4 min, 4 matches: **goals 0, per 90 0.00**. Other: non_penalty_goals 0; assists 0; shots 1; xg 0.035; npxg 0.035; key_passes 1; passes_attempted 183; passes_completed 142; progressive_passes 24; progressive_carries 9; pressures 25; pressured_passes_attempted 16; pressured_passes_completed 9; shot_creating_actions 2; xt_added 0.321; pass_completion_pct 77.6; pressured_pass_completion_pct 56.2

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A067

**Question:** What was Aziz Behich's expected goals (xG) total during the 2022 World Cup?

**Ground truth** (Expected goals (xG) for Aziz Behich, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Aziz Behich | Australia | 0.13 | 360 | 4 |

**Naive answer:**

> Aziz Behich's expected goals (xG) total during the 2022 World Cup was 0.13.

**Reference stats** (true tournament totals):

- Aziz Behich: Australia, FB, 360.0 min, 4 matches: **xg 0.127, per 90 0.03**. Other: goals 0; non_penalty_goals 0; assists 0; shots 2; npxg 0.127; key_passes 0; passes_attempted 204; passes_completed 154; progressive_passes 9; progressive_carries 10; pressures 33; pressured_passes_attempted 16; pressured_passes_completed 11; shot_creating_actions 4; xt_added 0.237; pass_completion_pct 75.5; pressured_pass_completion_pct 68.8

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A068

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

## A069

**Question:** which three full-backs had the lowest progressive carries in the 2022 world cup?

**Ground truth** (The 3 players with the fewest progressive carries, among full-backs (FB), with at least 270 minutes (default threshold), World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Noussair Mazraoui | Morocco | 3 | 368 | 5 |
| 1 | Timothy Castagne | Belgium | 3 | 270 | 3 |
| 3 | Nicolás Tagliafico | Argentina | 4 | 373 | 6 |

**Naive answer:**

> The three full-backs with the lowest progressive carries in the 2022 World Cup (minimum 270 minutes) are:
> 
> 1. **Yassine Meriah (Tunisia)** – 0.0 progressive carries per 90 (0 total)
> 2. **Ali Gholizadeh (Iran)** – 0.11 progressive carries per 90 (2 total)
> 3. **Nico Elvedi (Switzerland)** – 0.11 progressive carries per 90 (2 total)

**Reference stats** (true tournament totals):

- Noussair Mazraoui: Morocco, FB, 367.7 min, 5 matches: **progressive_carries 3, per 90 0.73**. Other: goals 0; non_penalty_goals 0; assists 0; shots 4; xg 0.151; npxg 0.151; key_passes 1; passes_attempted 121; passes_completed 103; progressive_passes 9; pressures 44; pressured_passes_attempted 12; pressured_passes_completed 9; shot_creating_actions 2; xt_added 0.108; pass_completion_pct 85.1; pressured_pass_completion_pct 75.0
- Timothy Castagne: Belgium, FB, 270.0 min, 3 matches: **progressive_carries 3, per 90 1.00**. Other: goals 0; non_penalty_goals 0; assists 0; shots 0; xg 0; npxg 0; key_passes 0; passes_attempted 201; passes_completed 176; progressive_passes 30; pressures 31; pressured_passes_attempted 29; pressured_passes_completed 19; shot_creating_actions 0; xt_added 0.147; pass_completion_pct 87.6; pressured_pass_completion_pct 65.5
- Nicolás Tagliafico: Argentina, FB, 373.1 min, 6 matches: **progressive_carries 4, per 90 0.96**. Other: goals 0; non_penalty_goals 0; assists 0; shots 3; xg 0.912; npxg 0.912; key_passes 2; passes_attempted 182; passes_completed 153; progressive_passes 9; pressures 56; pressured_passes_attempted 23; pressured_passes_completed 18; shot_creating_actions 5; xt_added 0.183; pass_completion_pct 84.1; pressured_pass_completion_pct 78.3
- Yassine Meriah: Tunisia, CB, 270.0 min, 3 matches: **progressive_carries 0, per 90 0.00**. Other: goals 0; non_penalty_goals 0; assists 0; shots 1; xg 0.046; npxg 0.046; key_passes 1; passes_attempted 168; passes_completed 138; progressive_passes 18; pressures 29; pressured_passes_attempted 12; pressured_passes_completed 8; shot_creating_actions 3; xt_added 0.168; pass_completion_pct 82.1; pressured_pass_completion_pct 66.7
- Ali Gholizadeh: Iran, W, 197.6 min, 3 matches: **progressive_carries 4, per 90 1.82**. Other: goals 0; non_penalty_goals 0; assists 1; shots 1; xg 0.043; npxg 0.043; key_passes 2; passes_attempted 73; passes_completed 47; progressive_passes 8; pressures 28; pressured_passes_attempted 6; pressured_passes_completed 5; shot_creating_actions 8; xt_added 0.339; pass_completion_pct 64.4; pressured_pass_completion_pct 83.3
- Nico Elvedi: Switzerland, CB, 180.0 min, 2 matches: **progressive_carries 10, per 90 5.00**. Other: goals 0; non_penalty_goals 0; assists 0; shots 1; xg 0.19; npxg 0.19; key_passes 0; passes_attempted 141; passes_completed 132; progressive_passes 11; pressures 15; pressured_passes_attempted 10; pressured_passes_completed 7; shot_creating_actions 0; xt_added 0.11; pass_completion_pct 93.6; pressured_pass_completion_pct 70.0

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A070

**Question:** Looking at shot-creating actions in the 2022 World Cup, how do Aaron Mooy, Joshua Kimmich, and Ziyech compare?

**Ground truth** (Shot-creating actions for Aaron Mooy, Joshua Kimmich and Hakim Ziyech, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Hakim Ziyech | Morocco | 20 | 636 | 7 |
| 2 | Joshua Kimmich | Germany | 17 | 270 | 3 |
| 3 | Aaron Mooy | Australia | 4 | 360 | 4 |

**Naive answer:**

> Aaron Mooy, Joshua Kimmich, and Hakim Ziyech were all notable contributors in shot creation during the 2022 World Cup. 
> 
> - **Aaron Mooy (Australia, DM)**: 1 shot-creating action per 90 minutes (2 total in 360 minutes).  
> - **Joshua Kimmich (Germany, DM)**: 8 shot-creating actions per 90 minutes (8 total in 270 minutes).  
> - **Hakim Ziyech (Morocco, W)**: 7 shot-creating actions per 90 minutes (10 total in 636.2 minutes).  
> 
> Joshua Kimmich was the most active in creating shots, while Ziyech had the highest total despite playing significantly more minutes than the others.

**Reference stats** (true tournament totals):

- Hakim Ziyech: Morocco, W, 636.2 min, 7 matches: **shot_creating_actions 20, per 90 2.83**. Other: goals 1; non_penalty_goals 1; assists 1; shots 10; xg 0.312; npxg 0.312; key_passes 7; passes_attempted 300; passes_completed 210; progressive_passes 40; progressive_carries 28; pressures 137; pressured_passes_attempted 31; pressured_passes_completed 23; xt_added 0.541; pass_completion_pct 70.0; pressured_pass_completion_pct 74.2
- Joshua Kimmich: Germany, DM, 270.0 min, 3 matches: **shot_creating_actions 17, per 90 5.67**. Other: goals 0; non_penalty_goals 0; assists 0; shots 7; xg 0.335; npxg 0.335; key_passes 8; passes_attempted 271; passes_completed 229; progressive_passes 48; progressive_carries 8; pressures 35; pressured_passes_attempted 30; pressured_passes_completed 25; xt_added 1.091; pass_completion_pct 84.5; pressured_pass_completion_pct 83.3
- Aaron Mooy: Australia, DM, 360.0 min, 4 matches: **shot_creating_actions 4, per 90 1.00**. Other: goals 0; non_penalty_goals 0; assists 0; shots 1; xg 0.039; npxg 0.039; key_passes 1; passes_attempted 219; passes_completed 171; progressive_passes 29; progressive_carries 6; pressures 44; pressured_passes_attempted 25; pressured_passes_completed 13; xt_added 0.144; pass_completion_pct 78.1; pressured_pass_completion_pct 52.0

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A071

**Question:** top 3 morroco center backs with most progressve passes (min 90 mins) in world cup 2022?

**Ground truth** (The 3 players with the most progressive passes (simplified), among centre-backs (CB), playing for Morocco, with at least 90 minutes, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Romain Saïss | Morocco | 16 | 468 | 6 |
| 2 | Jawad El Yamiq | Morocco | 8 | 309 | 6 |
| 3 | Achraf Dari | Morocco | 7 | 186 | 3 |

**Naive answer:**

> The top 3 Morocco center backs with the most progressive passes (minimum 90 minutes) in the 2022 World Cup are:
> 
> 1. **Romain Saïss** - 16 progressive passes (6 matches, 467.6 minutes)  
> 2. **Achraf Dari** - 7 progressive passes (3 matches, 186.4 minutes)  
> 3. **Yassine Meriah** - 18 progressive passes (3 matches, 270.0 minutes)

**Reference stats** (true tournament totals):

- Romain Saïss: Morocco, CB, 467.6 min, 6 matches: **progressive_passes 16, per 90 3.08**. Other: goals 1; non_penalty_goals 1; assists 0; shots 1; xg 0.565; npxg 0.565; key_passes 0; passes_attempted 193; passes_completed 158; progressive_carries 5; pressures 35; pressured_passes_attempted 10; pressured_passes_completed 6; shot_creating_actions 1; xt_added 0.294; pass_completion_pct 81.9; pressured_pass_completion_pct 60.0
- Jawad El Yamiq: Morocco, CB, 309.4 min, 6 matches: **progressive_passes 8, per 90 2.33**. Other: goals 0; non_penalty_goals 0; assists 0; shots 1; xg 0.064; npxg 0.064; key_passes 0; passes_attempted 160; passes_completed 143; progressive_carries 2; pressures 18; pressured_passes_attempted 15; pressured_passes_completed 10; shot_creating_actions 2; xt_added 0.095; pass_completion_pct 89.4; pressured_pass_completion_pct 66.7
- Achraf Dari: Morocco, CB, 186.4 min, 3 matches: **progressive_passes 7, per 90 3.38**. Other: goals 1; non_penalty_goals 1; assists 0; shots 1; xg 0.418; npxg 0.418; key_passes 0; passes_attempted 107; passes_completed 96; progressive_carries 0; pressures 17; pressured_passes_attempted 3; pressured_passes_completed 0; shot_creating_actions 0; xt_added 0.099; pass_completion_pct 89.7; pressured_pass_completion_pct 0.0
- Yassine Meriah: Tunisia, CB, 270.0 min, 3 matches: **progressive_passes 18, per 90 6.00**. Other: goals 0; non_penalty_goals 0; assists 0; shots 1; xg 0.046; npxg 0.046; key_passes 1; passes_attempted 168; passes_completed 138; progressive_carries 0; pressures 29; pressured_passes_attempted 12; pressured_passes_completed 8; shot_creating_actions 3; xt_added 0.168; pass_completion_pct 82.1; pressured_pass_completion_pct 66.7

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A072

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

## A073

**Question:** How many times did Sofiane Boufal create shots in the 2022 World Cup?

**Ground truth** (Shot-creating actions for Sofiane Boufal, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Sofiane Boufal | Morocco | 15 | 477 | 7 |

**Naive answer:**

> Sofiane Boufal created 7 shots in the 2022 World Cup.

**Reference stats** (true tournament totals):

- Sofiane Boufal: Morocco, W, 476.7 min, 7 matches: **shot_creating_actions 15, per 90 2.83**. Other: goals 0; non_penalty_goals 0; assists 0; shots 7; xg 0.316; npxg 0.316; key_passes 4; passes_attempted 134; passes_completed 107; progressive_passes 23; progressive_carries 33; pressures 93; pressured_passes_attempted 18; pressured_passes_completed 11; xt_added 0.985; pass_completion_pct 79.9; pressured_pass_completion_pct 61.1

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A074

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

## A075

**Question:** How many minutes did Bellingham play?

**Ground truth** (Minutes played for Jude Bellingham, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Jude Bellingham | England | 414 | 414 | 5 |

**Naive answer:**

> Jude Bellingham played 414.2 minutes in the 2022 World Cup.

**Reference stats** (true tournament totals):

- Jude Bellingham: England, CM, 414.2 min, 5 matches: **minutes 414, per 90 90.00**. Other: goals 1; non_penalty_goals 1; assists 1; shots 5; xg 0.841; npxg 0.841; key_passes 4; passes_attempted 275; passes_completed 242; progressive_passes 43; progressive_carries 20; pressures 70; pressured_passes_attempted 38; pressured_passes_completed 31; shot_creating_actions 14; xt_added 0.355; pass_completion_pct 88.0; pressured_pass_completion_pct 81.6

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A076

**Question:** Which three full-backs recorded the lowest number of progressive carries during the 2022 World Cup?

**Ground truth** (The 3 players with the fewest progressive carries, among full-backs (FB), with at least 270 minutes (default threshold), World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Noussair Mazraoui | Morocco | 3 | 368 | 5 |
| 1 | Timothy Castagne | Belgium | 3 | 270 | 3 |
| 3 | Nicolás Tagliafico | Argentina | 4 | 373 | 6 |

**Naive answer:**

> The three full-backs with the lowest number of progressive carries during the 2022 World Cup were:
> 
> 1. **Ederson Moraes (Brazil)** – 0 progressive carries  
> 2. **Hugo Lloris (France)** – 0 progressive carries  
> 3. **Kevin De Bruyne (Belgium)** – 0 progressive carries  
> 
> Note: These players are listed as full-backs (FB) in the dataset, though some (e.g., De Bruyne, Lloris) are more commonly associated with other roles.

**Reference stats** (true tournament totals):

- Noussair Mazraoui: Morocco, FB, 367.7 min, 5 matches: **progressive_carries 3, per 90 0.73**. Other: goals 0; non_penalty_goals 0; assists 0; shots 4; xg 0.151; npxg 0.151; key_passes 1; passes_attempted 121; passes_completed 103; progressive_passes 9; pressures 44; pressured_passes_attempted 12; pressured_passes_completed 9; shot_creating_actions 2; xt_added 0.108; pass_completion_pct 85.1; pressured_pass_completion_pct 75.0
- Timothy Castagne: Belgium, FB, 270.0 min, 3 matches: **progressive_carries 3, per 90 1.00**. Other: goals 0; non_penalty_goals 0; assists 0; shots 0; xg 0; npxg 0; key_passes 0; passes_attempted 201; passes_completed 176; progressive_passes 30; pressures 31; pressured_passes_attempted 29; pressured_passes_completed 19; shot_creating_actions 0; xt_added 0.147; pass_completion_pct 87.6; pressured_pass_completion_pct 65.5
- Nicolás Tagliafico: Argentina, FB, 373.1 min, 6 matches: **progressive_carries 4, per 90 0.96**. Other: goals 0; non_penalty_goals 0; assists 0; shots 3; xg 0.912; npxg 0.912; key_passes 2; passes_attempted 182; passes_completed 153; progressive_passes 9; pressures 56; pressured_passes_attempted 23; pressured_passes_completed 18; shot_creating_actions 5; xt_added 0.183; pass_completion_pct 84.1; pressured_pass_completion_pct 78.3
- Ederson Moraes: Brazil, GK, 90.0 min, 1 matches: **progressive_carries 0, per 90 0.00**. Other: goals 0; non_penalty_goals 0; assists 0; shots 0; xg 0; npxg 0; key_passes 0; passes_attempted 30; passes_completed 28; progressive_passes 0; pressures 0; pressured_passes_attempted 1; pressured_passes_completed 1; shot_creating_actions 0; xt_added 0.039; pass_completion_pct 93.3; pressured_pass_completion_pct 100.0
- Hugo Lloris: France, GK, 570.0 min, 6 matches: **progressive_carries 0, per 90 0.00**. Other: goals 0; non_penalty_goals 0; assists 0; shots 0; xg 0; npxg 0; key_passes 0; passes_attempted 182; passes_completed 111; progressive_passes 0; pressures 0; pressured_passes_attempted 11; pressured_passes_completed 2; shot_creating_actions 1; xt_added 0.155; pass_completion_pct 61.0; pressured_pass_completion_pct 18.2
- Kevin De Bruyne: Belgium, W, 270.0 min, 3 matches: **progressive_carries 16, per 90 5.33**. Other: goals 0; non_penalty_goals 0; assists 0; shots 7; xg 0.178; npxg 0.178; key_passes 8; passes_attempted 140; passes_completed 100; progressive_passes 31; pressures 25; pressured_passes_attempted 24; pressured_passes_completed 14; shot_creating_actions 10; xt_added 1.17; pass_completion_pct 71.4; pressured_pass_completion_pct 58.3

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A077

**Question:** How many passes did Hwang In-Beom complete while under pressure during the 2022 World Cup?

**Ground truth** (Passes completed under pressure for Hwang In-Beom, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Hwang In-Beom | South Korea | 21 | 334 | 4 |

**Naive answer:**

> Hwang In-Beom completed **21 passes** while under pressure during the 2022 World Cup.

**Reference stats** (true tournament totals):

- Hwang In-Beom: South Korea, DM, 334.4 min, 4 matches: **pressured_passes_completed 21, per 90 5.65**. Other: goals 0; non_penalty_goals 0; assists 0; shots 6; xg 0.198; npxg 0.198; key_passes 3; passes_attempted 247; passes_completed 199; progressive_passes 43; progressive_carries 6; pressures 51; pressured_passes_attempted 31; shot_creating_actions 5; xt_added 0.268; pass_completion_pct 80.6; pressured_pass_completion_pct 67.7

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A078

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

## A079

**Question:** Compare Johnston and Milos Veljkovic for progressive passes per 90.

**Ground truth** (Progressive passes (simplified) per 90 for Alistair Johnston and Milos Veljkovic, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Alistair Johnston | Canada | 8.0 | 270 | 3 |
| 2 | Milos Veljkovic | Serbia | 2.84 | 222 | 3 |

**Naive answer:**

> Alistair Johnston (Canada, FB) made 24 progressive passes in 270 minutes. Per 90 minutes, this is 8.00 progressive passes.
> 
> Milos Veljkovic (Serbia, CB) made 7 progressive passes in 221.8 minutes. Per 90 minutes, this is 2.89 progressive passes.
> 
> Johnston had a higher rate of progressive passes per 90 compared to Milos Veljkovic.

**Reference stats** (true tournament totals):

- Alistair Johnston: Canada, FB, 270.0 min, 3 matches: **progressive_passes 24, per 90 8.00**. Other: goals 0; non_penalty_goals 0; assists 0; shots 2; xg 0.672; npxg 0.672; key_passes 4; passes_attempted 187; passes_completed 156; progressive_carries 8; pressures 38; pressured_passes_attempted 21; pressured_passes_completed 21; shot_creating_actions 11; xt_added 0.471; pass_completion_pct 83.4; pressured_pass_completion_pct 100.0
- Milos Veljkovic: Serbia, CB, 221.8 min, 3 matches: **progressive_passes 7, per 90 2.84**. Other: goals 0; non_penalty_goals 0; assists 0; shots 0; xg 0; npxg 0; key_passes 0; passes_attempted 112; passes_completed 99; progressive_carries 2; pressures 24; pressured_passes_attempted 9; pressured_passes_completed 7; shot_creating_actions 1; xt_added 0.067; pass_completion_pct 88.4; pressured_pass_completion_pct 77.8

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A080

**Question:** How many shots did Frankowski take in total during the 2022 World Cup?

**Ground truth** (Shots for Przemysław Frankowski, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Przemysław Frankowski | Poland | 1 | 240 | 4 |

**Naive answer:**

> Przemysław Frankowski took 1 shot during the 2022 World Cup.

**Reference stats** (true tournament totals):

- Przemysław Frankowski: Poland, W, 240.1 min, 4 matches: **shots 1, per 90 0.37**. Other: goals 0; non_penalty_goals 0; assists 0; xg 0.044; npxg 0.044; key_passes 1; passes_attempted 73; passes_completed 51; progressive_passes 8; progressive_carries 4; pressures 39; pressured_passes_attempted 11; pressured_passes_completed 6; shot_creating_actions 3; xt_added 0.082; pass_completion_pct 69.9; pressured_pass_completion_pct 54.5

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A081

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

## A082

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

## A083

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

## A084

**Question:** Who was the Serbia CB with the most passes attempted under pressure at the 2022 World Cup?

**Ground truth** (The player with the most passes attempted under pressure, among centre-backs (CB), playing for Serbia, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Nikola Milenković | Serbia | 21 | 270 | 3 |

**Naive answer:**

> The Serbia CB with the most passes attempted under pressure at the 2022 World Cup was Nikola Milenković, with 21 pressured passes attempted.

**Reference stats** (true tournament totals):

- Nikola Milenković: Serbia, CB, 270.0 min, 3 matches: **pressured_passes_attempted 21, per 90 7.00**. Other: goals 0; non_penalty_goals 0; assists 0; shots 3; xg 0.123; npxg 0.123; key_passes 0; passes_attempted 157; passes_completed 136; progressive_passes 19; progressive_carries 4; pressures 28; pressured_passes_completed 16; shot_creating_actions 0; xt_added 0.175; pass_completion_pct 86.6; pressured_pass_completion_pct 76.2

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A085

**Question:** which 3 brazil forwards had the least key passes per 90 in the 2022 world cup?

**Ground truth** (The 3 players with the lowest key passes per 90, among forwards (ST, W), playing for Brazil, with at least 270 minutes (default threshold), World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Richarlison | Brazil | 1.39 | 324 | 4 |
| 2 | Raphinha | Brazil | 2.28 | 316 | 5 |
| 3 | Vinícius Júnior | Brazil | 2.39 | 301 | 4 |

**Naive answer:**

> The three Brazil forwards with the least key passes per 90 minutes in the 2022 World Cup are:
> 
> 1. **Gabriel Jesus** (ST) - 0.63 key passes per 90  
> 2. **Richarlison** (ST) - 0.63 key passes per 90  
> 3. **Alex Sandro** (FB) - 0.63 key passes per 90

**Reference stats** (true tournament totals):

- Richarlison: Brazil, ST, 324.3 min, 4 matches: **key_passes 5, per 90 1.39**. Other: goals 3; non_penalty_goals 3; assists 0; shots 8; xg 1.618; npxg 1.618; passes_attempted 54; passes_completed 39; progressive_passes 4; progressive_carries 9; pressures 59; pressured_passes_attempted 14; pressured_passes_completed 11; shot_creating_actions 8; xt_added 0.043; pass_completion_pct 72.2; pressured_pass_completion_pct 78.6
- Raphinha: Brazil, W, 316.4 min, 5 matches: **key_passes 8, per 90 2.28**. Other: goals 0; non_penalty_goals 0; assists 0; shots 8; xg 0.923; npxg 0.923; passes_attempted 150; passes_completed 115; progressive_passes 14; progressive_carries 26; pressures 51; pressured_passes_attempted 16; pressured_passes_completed 11; shot_creating_actions 20; xt_added 1.426; pass_completion_pct 76.7; pressured_pass_completion_pct 68.8
- Vinícius Júnior: Brazil, W, 300.7 min, 4 matches: **key_passes 8, per 90 2.39**. Other: goals 1; non_penalty_goals 1; assists 2; shots 9; xg 0.812; npxg 0.812; passes_attempted 91; passes_completed 70; progressive_passes 9; progressive_carries 29; pressures 37; pressured_passes_attempted 13; pressured_passes_completed 9; shot_creating_actions 14; xt_added 1.241; pass_completion_pct 76.9; pressured_pass_completion_pct 69.2
- Gabriel Jesus: Brazil, ST, 92.6 min, 3 matches: **key_passes 4, per 90 3.89**. Other: goals 0; non_penalty_goals 0; assists 0; shots 2; xg 0.324; npxg 0.324; passes_attempted 27; passes_completed 23; progressive_passes 7; progressive_carries 2; pressures 15; pressured_passes_attempted 6; pressured_passes_completed 4; shot_creating_actions 5; xt_added 0.086; pass_completion_pct 85.2; pressured_pass_completion_pct 66.7
- Alex Sandro: Brazil, FB, 190.4 min, 3 matches: **key_passes 1, per 90 0.47**. Other: goals 0; non_penalty_goals 0; assists 0; shots 1; xg 0.022; npxg 0.022; passes_attempted 169; passes_completed 150; progressive_passes 33; progressive_carries 8; pressures 21; pressured_passes_attempted 11; pressured_passes_completed 9; shot_creating_actions 7; xt_added 0.248; pass_completion_pct 88.8; pressured_pass_completion_pct 81.8

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A086

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

## A087

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

## A088

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

## A089

**Question:** How many shot-creating actions did Sofiane Boufal have?

**Ground truth** (Shot-creating actions for Sofiane Boufal, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Sofiane Boufal | Morocco | 15 | 477 | 7 |

**Naive answer:**

> Sofiane Boufal had 4 shot-creating actions.

**Reference stats** (true tournament totals):

- Sofiane Boufal: Morocco, W, 476.7 min, 7 matches: **shot_creating_actions 15, per 90 2.83**. Other: goals 0; non_penalty_goals 0; assists 0; shots 7; xg 0.316; npxg 0.316; key_passes 4; passes_attempted 134; passes_completed 107; progressive_passes 23; progressive_carries 33; pressures 93; pressured_passes_attempted 18; pressured_passes_completed 11; xt_added 0.985; pass_completion_pct 79.9; pressured_pass_completion_pct 61.1

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A090

**Question:** Which 5 Denmark players had the most progressive passes per 90?

**Ground truth** (The 5 players with the highest progressive passes (simplified) per 90, playing for Denmark, with at least 270 minutes (default threshold), World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Pierre-Emile Højbjerg | Denmark | 14.33 | 270 | 3 |
| 2 | Joachim Andersen | Denmark | 13.67 | 270 | 3 |
| 3 | Andreas Christensen | Denmark | 10.67 | 270 | 3 |
| 3 | Christian Eriksen | Denmark | 10.67 | 270 | 3 |
| 5 | Kasper Schmeichel | Denmark | 0.33 | 270 | 3 |

**Naive answer:**

> The 5 Denmark players with the most progressive passes per 90 are:
> 
> 1. **Pierre-Emile Højbjerg** - 43.00 progressive passes/90  
> 2. **Kasper Schmeichel** - 1.00 progressive passes/90  
> 3. **Andreas Christensen** - 32.00 progressive passes/90  
> 4. **Mikkel Damsgaard** - 20.00 progressive passes/90  
> 5. **Andreas Cornelius** - 3.00 progressive passes/90

**Reference stats** (true tournament totals):

- Pierre-Emile Højbjerg: Denmark, DM, 270.0 min, 3 matches: **progressive_passes 43, per 90 14.33**. Other: goals 0; non_penalty_goals 0; assists 0; shots 2; xg 0.024; npxg 0.024; key_passes 1; passes_attempted 224; passes_completed 200; progressive_carries 5; pressures 28; pressured_passes_attempted 19; pressured_passes_completed 17; shot_creating_actions 2; xt_added 0.256; pass_completion_pct 89.3; pressured_pass_completion_pct 89.5
- Joachim Andersen: Denmark, CB, 270.0 min, 3 matches: **progressive_passes 41, per 90 13.67**. Other: goals 0; non_penalty_goals 0; assists 0; shots 4; xg 0.145; npxg 0.145; key_passes 0; passes_attempted 245; passes_completed 199; progressive_carries 11; pressures 25; pressured_passes_attempted 14; pressured_passes_completed 7; shot_creating_actions 3; xt_added 0.391; pass_completion_pct 81.2; pressured_pass_completion_pct 50.0
- Andreas Christensen: Denmark, CB, 270.0 min, 3 matches: **progressive_passes 32, per 90 10.67**. Other: goals 1; non_penalty_goals 1; assists 0; shots 2; xg 0.525; npxg 0.525; key_passes 0; passes_attempted 250; passes_completed 236; progressive_carries 8; pressures 11; pressured_passes_attempted 17; pressured_passes_completed 13; shot_creating_actions 1; xt_added 0.233; pass_completion_pct 94.4; pressured_pass_completion_pct 76.5
- Christian Eriksen: Denmark, CM, 270.0 min, 3 matches: **progressive_passes 32, per 90 10.67**. Other: goals 0; non_penalty_goals 0; assists 0; shots 4; xg 0.154; npxg 0.154; key_passes 9; passes_attempted 231; passes_completed 193; progressive_carries 11; pressures 32; pressured_passes_attempted 21; pressured_passes_completed 17; shot_creating_actions 15; xt_added 0.372; pass_completion_pct 83.5; pressured_pass_completion_pct 81.0
- Kasper Schmeichel: Denmark, GK, 270.0 min, 3 matches: **progressive_passes 1, per 90 0.33**. Other: goals 0; non_penalty_goals 0; assists 0; shots 0; xg 0; npxg 0; key_passes 0; passes_attempted 87; passes_completed 72; progressive_carries 0; pressures 0; pressured_passes_attempted 6; pressured_passes_completed 4; shot_creating_actions 0; xt_added 0.131; pass_completion_pct 82.8; pressured_pass_completion_pct 66.7
- Mikkel Damsgaard: Denmark, W, 149.4 min, 3 matches: **progressive_passes 20, per 90 12.05**. Other: goals 0; non_penalty_goals 0; assists 0; shots 0; xg 0; npxg 0; key_passes 3; passes_attempted 71; passes_completed 57; progressive_carries 6; pressures 31; pressured_passes_attempted 7; pressured_passes_completed 5; shot_creating_actions 4; xt_added 0.443; pass_completion_pct 80.3; pressured_pass_completion_pct 71.4
- Andreas Cornelius: Denmark, ST, 91.2 min, 3 matches: **progressive_passes 1, per 90 0.99**. Other: goals 0; non_penalty_goals 0; assists 0; shots 5; xg 0.802; npxg 0.802; key_passes 3; passes_attempted 32; passes_completed 21; progressive_carries 1; pressures 18; pressured_passes_attempted 16; pressured_passes_completed 10; shot_creating_actions 6; xt_added -0.166; pass_completion_pct 65.6; pressured_pass_completion_pct 62.5

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A091

**Question:** Which striker had the most goals?

**Ground truth** (The player with the most goals, among strikers (ST), World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Lionel Messi | Argentina | 7 | 690 | 7 |

**Naive answer:**

> Lionel Messi (Argentina) had the most goals among strikers with 7 goals.

**Reference stats** (true tournament totals):

- Lionel Messi: Argentina, ST, 690.0 min, 7 matches: **goals 7, per 90 0.91**. Other: non_penalty_goals 3; assists 3; shots 32; xg 6.032; npxg 2.114; key_passes 19; passes_attempted 371; passes_completed 306; progressive_passes 79; progressive_carries 61; pressures 89; pressured_passes_attempted 75; pressured_passes_completed 65; shot_creating_actions 41; xt_added 1.759; pass_completion_pct 82.5; pressured_pass_completion_pct 86.7

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A092

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

## A093

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

## A094

**Question:** How many passes did Kimmich attempt under pressure in the 2022 World Cup?

**Ground truth** (Passes attempted under pressure for Joshua Kimmich, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Joshua Kimmich | Germany | 30 | 270 | 3 |

**Naive answer:**

> Joshua Kimmich attempted 35 passes under pressure in the 2022 World Cup.

**Reference stats** (true tournament totals):

- Joshua Kimmich: Germany, DM, 270.0 min, 3 matches: **pressured_passes_attempted 30, per 90 10.00**. Other: goals 0; non_penalty_goals 0; assists 0; shots 7; xg 0.335; npxg 0.335; key_passes 8; passes_attempted 271; passes_completed 229; progressive_passes 48; progressive_carries 8; pressures 35; pressured_passes_completed 25; shot_creating_actions 17; xt_added 1.091; pass_completion_pct 84.5; pressured_pass_completion_pct 83.3

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A095

**Question:** Which 10 players completed the highest number of passes under pressure during the 2022 World Cup?

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

> The 10 players who completed the highest number of passes under pressure during the 2022 World Cup are:
> 
> 1. **Christian Pulisic (United States, W)** – 20 completed pressured passes
> 2. **Youssef En-Nesyri (Morocco, ST)** – 19
> 3. **Harry Kane (England, ST)** – 12
> 4. **Hakim Ziyech (Morocco, W)** – 23
> 5. **Cody Gakpo (Netherlands, AM)** – 18
> 6. **Kylian Mbappé (France, W)** – 22
> 7. **Adrien Rabiot (France, DM)** – 26
> 8. **Jordan Henderson (England, CM)** – 13
> 9. **Achraf Hakimi (Morocco, FB)** – 36
> 10. **Sofyan Amrabat (Morocco, DM)** – 18

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
- Christian Pulisic: United States, W, 315.0 min, 4 matches: **pressured_passes_completed 20, per 90 5.71**. Other: goals 1; non_penalty_goals 1; assists 2; shots 9; xg 1.138; npxg 1.138; key_passes 9; passes_attempted 139; passes_completed 84; progressive_passes 21; progressive_carries 33; pressures 44; pressured_passes_attempted 27; shot_creating_actions 16; xt_added 0.679; pass_completion_pct 60.4; pressured_pass_completion_pct 74.1
- Youssef En-Nesyri: Morocco, ST, 543.8 min, 7 matches: **pressured_passes_completed 9, per 90 1.49**. Other: goals 2; non_penalty_goals 2; assists 0; shots 11; xg 1.046; npxg 1.046; key_passes 1; passes_attempted 76; passes_completed 48; progressive_passes 2; progressive_carries 2; pressures 113; pressured_passes_attempted 19; shot_creating_actions 3; xt_added 0.121; pass_completion_pct 63.2; pressured_pass_completion_pct 47.4
- Harry Kane: England, ST, 402.3 min, 5 matches: **pressured_passes_completed 12, per 90 2.68**. Other: goals 2; non_penalty_goals 1; assists 3; shots 12; xg 2.331; npxg 0.764; key_passes 5; passes_attempted 97; passes_completed 64; progressive_passes 21; progressive_carries 10; pressures 31; pressured_passes_attempted 25; shot_creating_actions 7; xt_added 0.618; pass_completion_pct 66.0; pressured_pass_completion_pct 48.0
- Hakim Ziyech: Morocco, W, 636.2 min, 7 matches: **pressured_passes_completed 23, per 90 3.25**. Other: goals 1; non_penalty_goals 1; assists 1; shots 10; xg 0.312; npxg 0.312; key_passes 7; passes_attempted 300; passes_completed 210; progressive_passes 40; progressive_carries 28; pressures 137; pressured_passes_attempted 31; shot_creating_actions 20; xt_added 0.541; pass_completion_pct 70.0; pressured_pass_completion_pct 74.2
- Cody Gakpo: Netherlands, AM, 453.7 min, 5 matches: **pressured_passes_completed 18, per 90 3.57**. Other: goals 3; non_penalty_goals 3; assists 0; shots 5; xg 0.562; npxg 0.562; key_passes 10; passes_attempted 154; passes_completed 98; progressive_passes 18; progressive_carries 17; pressures 52; pressured_passes_attempted 28; shot_creating_actions 16; xt_added 0.495; pass_completion_pct 63.6; pressured_pass_completion_pct 64.3
- Kylian Mbappé: France, W, 597.4 min, 7 matches: **pressured_passes_completed 22, per 90 3.31**. Other: goals 8; non_penalty_goals 6; assists 2; shots 31; xg 4.233; npxg 2.666; key_passes 11; passes_attempted 233; passes_completed 180; progressive_passes 31; progressive_carries 71; pressures 37; pressured_passes_attempted 26; shot_creating_actions 41; xt_added 1.899; pass_completion_pct 77.3; pressured_pass_completion_pct 84.6
- Adrien Rabiot: France, DM, 482.4 min, 6 matches: **pressured_passes_completed 26, per 90 4.85**. Other: goals 1; non_penalty_goals 1; assists 1; shots 9; xg 0.728; npxg 0.728; key_passes 2; passes_attempted 285; passes_completed 246; progressive_passes 39; progressive_carries 14; pressures 84; pressured_passes_attempted 37; shot_creating_actions 9; xt_added 0.226; pass_completion_pct 86.3; pressured_pass_completion_pct 70.3
- Jordan Henderson: England, CM, 271.7 min, 4 matches: **pressured_passes_completed 13, per 90 4.31**. Other: goals 1; non_penalty_goals 1; assists 0; shots 2; xg 0.149; npxg 0.149; key_passes 4; passes_attempted 166; passes_completed 141; progressive_passes 20; progressive_carries 6; pressures 35; pressured_passes_attempted 15; shot_creating_actions 8; xt_added 0.498; pass_completion_pct 84.9; pressured_pass_completion_pct 86.7
- Sofyan Amrabat: Morocco, DM, 660.0 min, 7 matches: **pressured_passes_completed 18, per 90 2.45**. Other: goals 0; non_penalty_goals 0; assists 0; shots 1; xg 0.021; npxg 0.021; key_passes 2; passes_attempted 323; passes_completed 274; progressive_passes 42; progressive_carries 17; pressures 123; pressured_passes_attempted 24; shot_creating_actions 6; xt_added 0.247; pass_completion_pct 84.8; pressured_pass_completion_pct 75.0

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A096

**Question:** How do Hassan Mohammed Al Tambakti and Timothy Castagne compare in terms of non-penalty xG?

**Ground truth** (Non-penalty xG for Hassan Mohammed Al Tambakti and Timothy Castagne, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Hassan Mohammed Al Tambakti | Saudi Arabia | 0.0 | 180 | 2 |
| 1 | Timothy Castagne | Belgium | 0.0 | 270 | 3 |

**Naive answer:**

> Hassan Mohammed Al Tambakti (Saudi Arabia, CB) has a non-penalty xG of 0.04, while Timothy Castagne (Belgium, FB) has a non-penalty xG of 0.0. Al Tambakti has a slightly higher non-penalty xG, but the difference is minimal.

**Reference stats** (true tournament totals):

- Hassan Mohammed Al Tambakti: Saudi Arabia, CB, 180.0 min, 2 matches: **npxg 0, per 90 0.00**. Other: goals 0; non_penalty_goals 0; assists 0; shots 0; xg 0; key_passes 0; passes_attempted 49; passes_completed 37; progressive_passes 4; progressive_carries 1; pressures 18; pressured_passes_attempted 6; pressured_passes_completed 2; shot_creating_actions 0; xt_added -0.075; pass_completion_pct 75.5; pressured_pass_completion_pct 33.3
- Timothy Castagne: Belgium, FB, 270.0 min, 3 matches: **npxg 0, per 90 0.00**. Other: goals 0; non_penalty_goals 0; assists 0; shots 0; xg 0; key_passes 0; passes_attempted 201; passes_completed 176; progressive_passes 30; progressive_carries 3; pressures 31; pressured_passes_attempted 29; pressured_passes_completed 19; shot_creating_actions 0; xt_added 0.147; pass_completion_pct 87.6; pressured_pass_completion_pct 65.5

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A097

**Question:** whos the 3 players with the least goals in the 2022 world cup?

**Ground truth** (The 3 players with the fewest goals, with at least 270 minutes (default threshold), World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Aaron Mooy | Australia | 0 | 360 | 4 |
| 1 | Abdelkarim Hassan | Qatar | 0 | 270 | 3 |
| 1 | Abdou Diallo | Senegal | 0 | 331 | 4 |

**Naive answer:**

> The three players with the least goals (0 goals) in the 2022 World Cup are:
> 
> 1. **Youri Tielemans** (Belgium) – 0 goals in 93.7 minutes
> 2. **Kamil Glik** (Ghana) – 0 goals in 97.9 minutes
> 3. **Christian Eriksen** (Denmark) – 0 goals in 270.0 minutes

**Reference stats** (true tournament totals):

- Aaron Mooy: Australia, DM, 360.0 min, 4 matches: **goals 0, per 90 0.00**. Other: non_penalty_goals 0; assists 0; shots 1; xg 0.039; npxg 0.039; key_passes 1; passes_attempted 219; passes_completed 171; progressive_passes 29; progressive_carries 6; pressures 44; pressured_passes_attempted 25; pressured_passes_completed 13; shot_creating_actions 4; xt_added 0.144; pass_completion_pct 78.1; pressured_pass_completion_pct 52.0
- Abdelkarim Hassan: Qatar, CB, 270.0 min, 3 matches: **goals 0, per 90 0.00**. Other: non_penalty_goals 0; assists 0; shots 6; xg 0.275; npxg 0.275; key_passes 1; passes_attempted 158; passes_completed 125; progressive_passes 19; progressive_carries 16; pressures 29; pressured_passes_attempted 21; pressured_passes_completed 17; shot_creating_actions 3; xt_added 0.337; pass_completion_pct 79.1; pressured_pass_completion_pct 81.0
- Abdou Diallo: Senegal, CB, 331.4 min, 4 matches: **goals 0, per 90 0.00**. Other: non_penalty_goals 0; assists 0; shots 1; xg 0.035; npxg 0.035; key_passes 1; passes_attempted 183; passes_completed 142; progressive_passes 24; progressive_carries 9; pressures 25; pressured_passes_attempted 16; pressured_passes_completed 9; shot_creating_actions 2; xt_added 0.321; pass_completion_pct 77.6; pressured_pass_completion_pct 56.2
- Youri Tielemans: Belgium, DM, 93.7 min, 3 matches: **goals 0, per 90 0.00**. Other: non_penalty_goals 0; assists 0; shots 0; xg 0; npxg 0; key_passes 1; passes_attempted 61; passes_completed 51; progressive_passes 5; progressive_carries 1; pressures 17; pressured_passes_attempted 8; pressured_passes_completed 7; shot_creating_actions 1; xt_added 0.017; pass_completion_pct 83.6; pressured_pass_completion_pct 87.5
- Kamil Glik: Poland, CB, 360.0 min, 4 matches: **goals 0, per 90 0.00**. Other: non_penalty_goals 0; assists 0; shots 3; xg 0.151; npxg 0.151; key_passes 0; passes_attempted 130; passes_completed 122; progressive_passes 6; progressive_carries 0; pressures 15; pressured_passes_attempted 5; pressured_passes_completed 3; shot_creating_actions 1; xt_added 0.07; pass_completion_pct 93.8; pressured_pass_completion_pct 60.0
- Christian Eriksen: Denmark, CM, 270.0 min, 3 matches: **goals 0, per 90 0.00**. Other: non_penalty_goals 0; assists 0; shots 4; xg 0.154; npxg 0.154; key_passes 9; passes_attempted 231; passes_completed 193; progressive_passes 32; progressive_carries 11; pressures 32; pressured_passes_attempted 21; pressured_passes_completed 17; shot_creating_actions 15; xt_added 0.372; pass_completion_pct 83.5; pressured_pass_completion_pct 81.0

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A098

**Question:** Which 5 full-backs had the fewest goals (minimum 270 minutes)?

**Ground truth** (The 5 players with the fewest goals, among full-backs (FB), with at least 270 minutes, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Achraf Hakimi | Morocco | 0 | 632 | 7 |
| 1 | Alistair Johnston | Canada | 0 | 270 | 3 |
| 1 | Antonee Robinson | United States | 0 | 360 | 4 |
| 1 | Aziz Behich | Australia | 0 | 360 | 4 |
| 1 | Bartosz Bereszyński | Poland | 0 | 342 | 4 |

**Naive answer:**

> The 5 full-backs with the fewest goals (minimum 270 minutes) are:
> - Jan Vertonghen (Belgium) - 0 goals
> - Thomas Meunier (Belgium) - 0 goals
> - Nathan Aké (Netherlands) - 0 goals
> - Youssouf Sabaly (Senegal) - 0 goals
> - Ben Davies (Wales) - 0 goals

**Reference stats** (true tournament totals):

- Achraf Hakimi: Morocco, FB, 631.6 min, 7 matches: **goals 0, per 90 0.00**. Other: non_penalty_goals 0; assists 1; shots 4; xg 0.136; npxg 0.136; key_passes 7; passes_attempted 380; passes_completed 314; progressive_passes 33; progressive_carries 16; pressures 104; pressured_passes_attempted 45; pressured_passes_completed 36; shot_creating_actions 12; xt_added 0.88; pass_completion_pct 82.6; pressured_pass_completion_pct 80.0
- Alistair Johnston: Canada, FB, 270.0 min, 3 matches: **goals 0, per 90 0.00**. Other: non_penalty_goals 0; assists 0; shots 2; xg 0.672; npxg 0.672; key_passes 4; passes_attempted 187; passes_completed 156; progressive_passes 24; progressive_carries 8; pressures 38; pressured_passes_attempted 21; pressured_passes_completed 21; shot_creating_actions 11; xt_added 0.471; pass_completion_pct 83.4; pressured_pass_completion_pct 100.0
- Antonee Robinson: United States, FB, 360.0 min, 4 matches: **goals 0, per 90 0.00**. Other: non_penalty_goals 0; assists 0; shots 0; xg 0; npxg 0; key_passes 3; passes_attempted 240; passes_completed 175; progressive_passes 24; progressive_carries 25; pressures 51; pressured_passes_attempted 15; pressured_passes_completed 13; shot_creating_actions 6; xt_added 0.732; pass_completion_pct 72.9; pressured_pass_completion_pct 86.7
- Aziz Behich: Australia, FB, 360.0 min, 4 matches: **goals 0, per 90 0.00**. Other: non_penalty_goals 0; assists 0; shots 2; xg 0.127; npxg 0.127; key_passes 0; passes_attempted 204; passes_completed 154; progressive_passes 9; progressive_carries 10; pressures 33; pressured_passes_attempted 16; pressured_passes_completed 11; shot_creating_actions 4; xt_added 0.237; pass_completion_pct 75.5; pressured_pass_completion_pct 68.8
- Bartosz Bereszyński: Poland, FB, 342.0 min, 4 matches: **goals 0, per 90 0.00**. Other: non_penalty_goals 0; assists 0; shots 0; xg 0; npxg 0; key_passes 0; passes_attempted 150; passes_completed 121; progressive_passes 11; progressive_carries 6; pressures 38; pressured_passes_attempted 23; pressured_passes_completed 19; shot_creating_actions 2; xt_added 0.065; pass_completion_pct 80.7; pressured_pass_completion_pct 82.6
- Jan Vertonghen: Belgium, CB, 270.0 min, 3 matches: **goals 0, per 90 0.00**. Other: non_penalty_goals 0; assists 0; shots 2; xg 0.108; npxg 0.108; key_passes 0; passes_attempted 264; passes_completed 237; progressive_passes 18; progressive_carries 2; pressures 15; pressured_passes_attempted 16; pressured_passes_completed 12; shot_creating_actions 1; xt_added 0.124; pass_completion_pct 89.8; pressured_pass_completion_pct 75.0
- Thomas Meunier: Belgium, FB, 212.3 min, 3 matches: **goals 0, per 90 0.00**. Other: non_penalty_goals 0; assists 0; shots 3; xg 0.119; npxg 0.119; key_passes 2; passes_attempted 142; passes_completed 109; progressive_passes 10; progressive_carries 8; pressures 24; pressured_passes_attempted 19; pressured_passes_completed 13; shot_creating_actions 7; xt_added 0.171; pass_completion_pct 76.8; pressured_pass_completion_pct 68.4
- Nathan Aké: Netherlands, CB, 480.0 min, 5 matches: **goals 0, per 90 0.00**. Other: non_penalty_goals 0; assists 0; shots 0; xg 0; npxg 0; key_passes 0; passes_attempted 352; passes_completed 319; progressive_passes 49; progressive_carries 20; pressures 49; pressured_passes_attempted 27; pressured_passes_completed 18; shot_creating_actions 2; xt_added 0.413; pass_completion_pct 90.6; pressured_pass_completion_pct 66.7
- Youssouf Sabaly: Senegal, FB, 360.0 min, 4 matches: **goals 0, per 90 0.00**. Other: non_penalty_goals 0; assists 0; shots 2; xg 0.018; npxg 0.018; key_passes 8; passes_attempted 222; passes_completed 192; progressive_passes 32; progressive_carries 21; pressures 47; pressured_passes_attempted 20; pressured_passes_completed 17; shot_creating_actions 12; xt_added 0.68; pass_completion_pct 86.5; pressured_pass_completion_pct 85.0
- Ben Davies: Wales, CB, 238.6 min, 3 matches: **goals 0, per 90 0.00**. Other: non_penalty_goals 0; assists 0; shots 3; xg 0.384; npxg 0.384; key_passes 0; passes_attempted 160; passes_completed 121; progressive_passes 14; progressive_carries 5; pressures 25; pressured_passes_attempted 21; pressured_passes_completed 10; shot_creating_actions 3; xt_added 0.2; pass_completion_pct 75.6; pressured_pass_completion_pct 47.6

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A099

**Question:** How do Aurélien Tchouaméni and Costa compare in terms of progressive passes during the 2022 World Cup?

**Ground truth** (Progressive passes (simplified) for Aurélien Tchouaméni and Diogo Costa, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Aurélien Tchouaméni | France | 66 | 622 | 7 |
| 2 | Diogo Costa | Portugal | 0 | 450 | 5 |

**Naive answer:**

> Aurélien Tchouaméni made 66 progressive passes in 621.8 minutes (0.11 per 90 minutes), while Costa is not listed in the provided data.

**Reference stats** (true tournament totals):

- Aurélien Tchouaméni: France, DM, 621.8 min, 7 matches: **progressive_passes 66, per 90 9.55**. Other: goals 1; non_penalty_goals 1; assists 0; shots 6; xg 0.399; npxg 0.399; key_passes 6; passes_attempted 470; passes_completed 431; progressive_carries 17; pressures 64; pressured_passes_attempted 51; pressured_passes_completed 42; shot_creating_actions 10; xt_added 0.758; pass_completion_pct 91.7; pressured_pass_completion_pct 82.4
- Diogo Costa: Portugal, GK, 450.0 min, 5 matches: **progressive_passes 0, per 90 0.00**. Other: goals 0; non_penalty_goals 0; assists 0; shots 0; xg 0; npxg 0; key_passes 1; passes_attempted 159; passes_completed 111; progressive_carries 0; pressures 1; pressured_passes_attempted 20; pressured_passes_completed 10; shot_creating_actions 1; xt_added 0.128; pass_completion_pct 69.8; pressured_pass_completion_pct 50.0

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---

## A100

**Question:** whcih 5 plyaers had the highes number of progrssive carries in the 2022 world cup?

**Ground truth** (The 5 players with the most progressive carries, World Cup 2022.):

| Rank | Player | Team | Value | Minutes | Matches |
|---|---|---|---|---|---|
| 1 | Kylian Mbappé | France | 71 | 597 | 7 |
| 2 | Lionel Messi | Argentina | 61 | 690 | 7 |
| 3 | Luka Modrić | Croatia | 42 | 654 | 7 |
| 4 | Ivan Perišić | Croatia | 39 | 670 | 7 |
| 5 | Mateo Kovačić | Croatia | 37 | 638 | 7 |

**Naive answer:**

> The 5 players with the highest number of progressive carries in the 2022 World Cup are:
> 
> 1. **Lionel Messi (Argentina, ST)** – 61
> 2. **Kylian Mbappé (France, W)** – 71
> 3. **Hakim Ziyech (Morocco, W)** – 28
> 4. **Ángel Di María (Argentina, W)** – 34
> 5. **Marcus Rashford (England, W)** – 8

**Reference stats** (true tournament totals):

- Kylian Mbappé: France, W, 597.4 min, 7 matches: **progressive_carries 71, per 90 10.70**. Other: goals 8; non_penalty_goals 6; assists 2; shots 31; xg 4.233; npxg 2.666; key_passes 11; passes_attempted 233; passes_completed 180; progressive_passes 31; pressures 37; pressured_passes_attempted 26; pressured_passes_completed 22; shot_creating_actions 41; xt_added 1.899; pass_completion_pct 77.3; pressured_pass_completion_pct 84.6
- Lionel Messi: Argentina, ST, 690.0 min, 7 matches: **progressive_carries 61, per 90 7.96**. Other: goals 7; non_penalty_goals 3; assists 3; shots 32; xg 6.032; npxg 2.114; key_passes 19; passes_attempted 371; passes_completed 306; progressive_passes 79; pressures 89; pressured_passes_attempted 75; pressured_passes_completed 65; shot_creating_actions 41; xt_added 1.759; pass_completion_pct 82.5; pressured_pass_completion_pct 86.7
- Luka Modrić: Croatia, CM, 654.4 min, 7 matches: **progressive_carries 42, per 90 5.78**. Other: goals 0; non_penalty_goals 0; assists 0; shots 6; xg 0.344; npxg 0.344; key_passes 6; passes_attempted 549; passes_completed 463; progressive_passes 107; pressures 115; pressured_passes_attempted 68; pressured_passes_completed 54; shot_creating_actions 19; xt_added 1.111; pass_completion_pct 84.3; pressured_pass_completion_pct 79.4
- Ivan Perišić: Croatia, W, 669.6 min, 7 matches: **progressive_carries 39, per 90 5.24**. Other: goals 1; non_penalty_goals 1; assists 3; shots 16; xg 0.756; npxg 0.756; key_passes 9; passes_attempted 304; passes_completed 214; progressive_passes 34; pressures 98; pressured_passes_attempted 51; pressured_passes_completed 35; shot_creating_actions 18; xt_added 0.994; pass_completion_pct 70.4; pressured_pass_completion_pct 68.6
- Mateo Kovačić: Croatia, CM, 637.8 min, 7 matches: **progressive_carries 37, per 90 5.22**. Other: goals 0; non_penalty_goals 0; assists 0; shots 3; xg 0.345; npxg 0.345; key_passes 9; passes_attempted 456; passes_completed 416; progressive_passes 71; pressures 136; pressured_passes_attempted 59; pressured_passes_completed 52; shot_creating_actions 16; xt_added 0.913; pass_completion_pct 91.2; pressured_pass_completion_pct 88.1
- Hakim Ziyech: Morocco, W, 636.2 min, 7 matches: **progressive_carries 28, per 90 3.96**. Other: goals 1; non_penalty_goals 1; assists 1; shots 10; xg 0.312; npxg 0.312; key_passes 7; passes_attempted 300; passes_completed 210; progressive_passes 40; pressures 137; pressured_passes_attempted 31; pressured_passes_completed 23; shot_creating_actions 20; xt_added 0.541; pass_completion_pct 70.0; pressured_pass_completion_pct 74.2
- Ángel Di María: Argentina, W, 289.9 min, 5 matches: **progressive_carries 34, per 90 10.56**. Other: goals 1; non_penalty_goals 1; assists 1; shots 7; xg 0.534; npxg 0.534; key_passes 11; passes_attempted 164; passes_completed 126; progressive_passes 24; pressures 34; pressured_passes_attempted 23; pressured_passes_completed 19; shot_creating_actions 20; xt_added 1.329; pass_completion_pct 76.8; pressured_pass_completion_pct 82.6
- Marcus Rashford: England, W, 138.1 min, 5 matches: **progressive_carries 8, per 90 5.21**. Other: goals 3; non_penalty_goals 3; assists 0; shots 11; xg 1.383; npxg 1.383; key_passes 0; passes_attempted 67; passes_completed 50; progressive_passes 4; pressures 17; pressured_passes_attempted 7; pressured_passes_completed 6; shot_creating_actions 4; xt_added 0.173; pass_completion_pct 74.6; pressured_pass_completion_pct 85.7

**Your verdict:** [ ] no error  [ ] has an error

If an error: [ ] wrong number  [ ] wrong player or team  [ ] wrong order

**Notes:** 

---
