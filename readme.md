# Yahtzee

## Getting Started

Clone the repository

```bash
git clone https://github.com/NeGat1FF/Yahtzee
cd Yahtzee
```

Create a virtual environment and run the game

On Windows:

```bash
python -m venv .venv
.\.venv\Scripts\activate.bat

.\run.bat
```

On Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate

chmod +x run.sh
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

With the provided coefficients , the RTP is about 57.1%. To get RTP of about 95%, you can use the following coefficients:

```python
combos = {
    "Pair": 1.9,
    "Full House": 2.9,
    "Yahtzee": 3.9,
    "Three Pairs": 4.6,
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
    "Pair": 1.66,
    "Full House": 3.33,
    "Yahtzee": 4.99,
    "Three Pairs": 6.66,
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
