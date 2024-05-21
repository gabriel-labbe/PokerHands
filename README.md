# PokerHands
Data analysis project for my poker hands (cash game only, no tournament). Currently at 30k hands.

## Features
1. Parses PokerStars hand history files. See db/hand_parser.py
2. Creates database, tables, and stocks the poker hands after parsing. See db/scripts
3. Extracts new information from the basic data. See graphs.ipynb "New Columns" section.
4. Filters data to keep only specific situations. Ex: only hands where I 3bet preflop.
5. Creates graph/heatmap for better understanding of the data. See below.


## Examples
### Winnings Graph

![](/images/WinningsGraphEx.PNG)

As we can see from the graph, cash games is not a good format for me and it needs to be worked on :).

### Heatmap
![](/images/HeatmapEx.PNG)

We can see from the heatmap that I'm losing money with some unexpected hand combos, for example suited broadways and strong offsuit Ace combos.  I should try to identify the mistakes I make with these hands by splitting my sample by position and/or by number of preflop raises.

### Hand Count
![](/images/HandCountEx.PNG)

From the hand count matrix, we can see that even with 30k hands, my sample still becomes small for individual combos (Around 100 for suited combos and 300 for offsuit combos). Variance has therefore still a big influence on my winnings and I should be careful not to draw conclusions from the results only.