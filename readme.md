# Yahtzee

## Getting Started

Clone the repository

```bash
git clone https://github.com/yourusername/yahtzee.git
cd yahtzee
```
Use one of the scripts to run the game:

On Windows:

```bash
.\run.bat
```

On Linux:

```bash
./run.sh
```

## RTP

```python
combos = {
    "Pair": 1,
    "Full House": 2,
    "Yahtzee": 3,
    "Three Pairs": 4,
    "Other": 0.0
}
```

With the provided coefficients , the RTP is about 71.5%. To get RTP of about 95%, you can use the following coefficients:

```python
combos = {
    "Pair": 1.5,
    "Full House": 2.5,
    "Yahtzee": 3.8,
    "Three Pairs": 4.9,
    "Other": 0.0
}
```
I got these coefficients by manually adjusting the values until I got the desired RTP.

But this approach is definitely not the best. We can get desired RTP by 

1. Simulating the game to get observed probabilities

2. Calculating current RTP

3. Using a scaling factor to adjust all payouts

4. Recalculate to confirm the new RTP is ~95%

New coefficients:

```python
combos = {
    "Pair": 1.33,
    "Full House": 2.66,
    "Yahtzee": 3.99,
    "Three Pairs": 5.32,
    "Other": 0.0
}
```

To get current RTP by simply simulating the game, use the following code:

```bash
python3 app/rtp.py
```

To get the new coefficients, use the following code:

```bash
python3 app/adjust_rtp.py
```
