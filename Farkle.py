import numpy as np
from collections import Counter

class FarkleRoll(object):
    def __init__(self):
        # Current score
        self.score = 0
        self.n_dice = 6
        self.taken = 0
        self.roll = Counter()
        # Counters for each combo
        self.six_of_kind = 0
        self.two_triplets = 0
        self.five_of_kind = 0
        self.straight_flush = 0
        self.three_pairs = 0
        self.four_of_kind_paired = 0
        self.four_of_kind = 0
        self.three_of_kind = 0
        self.single_hundred = 0
        self.single_fifty = 0

    def play(self):
        rolling = True
        i=0
        while rolling:
            self.taken=0
            assert self.n_dice > 0, "No dice available"
            self.roll_dice(self.n_dice)
            #print(self.roll)
            self.parse_roll(self.n_dice)
            #print(self.score, self.taken)
            #i+=1
            if self.taken==0:
                rolling=False
                return self.score
            elif self.taken==self.n_dice:
                self.n_dice = 6
            elif self.taken >= 0:
                self.n_dice -= self.taken
                assert self.n_dice >=0, "Can't have {} dice".format(self.n_dice)
        
    def roll_dice(self, n, forced=None):
        """Rolls dice. Generates n_dice number of random integers
        between 1 and 6."""
        if forced==None:
            roll_arr = np.random.randint(1, 7, size=n)
        else:
            roll_arr = forced
        self.roll = Counter(roll_arr)
        
    def parse_roll(self, n_initial):
        """Given a roll of the dice, find max score."""
        n_initial = sum(self.roll.values())
        if sum(self.roll.values())==6:
            self.is_six_of_kind()
        if sum(self.roll.values())==6:
            self.is_two_triplets()
        if sum(self.roll.values())>=5:
            self.is_five_of_kind()
        if sum(self.roll.values())==6:
            self.is_straight_flush()
        if sum(self.roll.values())==6:
            self.is_three_pairs()
        if sum(self.roll.values())>=4:
            self.is_four_of_kind()
        if sum(self.roll.values())>=3:
            self.is_three_of_kind()
        # Always check for ones and fives:
        self.is_100()
        self.is_50()
        
            
    def is_six_of_kind(self):
        """Checks if there's six of a kind. If so, increment
        score by 3000 and remove all dice from table"""
        if max(self.roll.values())==6:
            self.score += 3000
            self.roll.clear()
            self.taken += 6
            self.six_of_kind += 1
    
    def is_two_triplets(self):
        """Checks if there's two triplets in roll. If so,
        increment score by 2500 and remove all dice from table."""
        if (len(self.roll.items())==2)&(list(self.roll.values())==[3,3]):
            self.score += 2500
            self.roll.clear()
            self.taken += 6
            self.two_triplets += 1
            
    def is_five_of_kind(self):
        """Checks if there's five of a kind in roll. If so,
        increment score by 2000 and remove five dice from roll."""
        if max(self.roll.values())==5:
            self.score += 2000
            _ = self.roll.pop(self.roll.most_common(1)[0][0])
            self.taken += 5
            
    def is_straight_flush(self):
        """Checks if there's 1-6 straight. If so,
        increment score by 1500 and remove all dice rom table."""
        if len(self.roll.items())==6:
            self.score += 1500
            self.roll.clear()
            self.taken += 6
            self.straight_flush += 1
            
    def is_three_pairs(self):
        """Checks if there's three pairs. If so, increment
        score by 1500 and remove all dice from table."""
        if (len(self.roll.items())==3)&(list(self.roll.values())==[2,2]):
            self.score += 1500
            self.roll.clear()
            self.taken += 6
            
    def is_four_of_kind(self):
        """Checks if there's four of a kind and if remaining
        dice form a pair."""
        if max(self.roll.values())==4:
            if (sum(self.roll.values())==6)&(min(self.roll.values())==2):
                self.score += 1500
                self.roll.clear()
                self.taken += 6
                self.four_of_kind_paired += 1
            else:
                self.score += 1000
                _ = self.roll.pop(self.roll.most_common(1)[0][0])
                self.taken += 4
                self.four_of_kind += 1
    
    def is_three_of_kind(self):
        """Checks if there's a three of kind. If so, increment
        score by 100 * dice_value and remove three dice."""
        if max(self.roll.values())==3:
            dice_val = self.roll.most_common(1)[0][0]
            _ = self.roll.pop(dice_val)
            self.score += 100*dice_val
            self.taken += 3
            self.three_of_kind += 1
        
    def is_100(self):
        """Checks if there's any 100's in the roll. Take all of them.
        Note that at this point in the decision tree, there is at most two 1s."""
        if self.roll[1]>0:
            to_take = min(2, self.roll[1])
            self.score += to_take*100
            self.roll[1] -= to_take
            self.taken += to_take
            self.single_hundred += to_take
    
    def is_50(self):
        """Checks if there's any 50's in the roll. Only take one."""
        if self.roll[5]>0:
            if self.roll[5]==sum(self.roll.values()):
                # Take all the fives if it means using up dice
                self.score += 50*self.roll[5]
                self.taken += self.roll[5]
                self.single_fifty += self.roll[5]
                _ = self.roll.pop(5)
                
            elif self.taken==0:
                # Only take one five otherwise
                self.score += 50
                self.roll[5] -= 1
                self.taken += 1
                self.single_fifty += 1