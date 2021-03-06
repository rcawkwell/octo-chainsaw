#! /usr/bin/env python

import math 
import random, itertools
from collections import namedtuple 
import sys

HEARTS = 'Heart' 
DIAMONDS = 'Diamond' 
CLUBS = 'Club' 
SPADES = 'Spade' 
ACE = 1
JACK = 11
QUEEN = 12 
KING = 13
EMPTY = 'Empty'

SUITLIST = [HEARTS, DIAMONDS, SPADES, CLUBS]
RANKLIST = [ACE, 2, 3, 4, 5, 6, 7, 8, 9, 10, JACK, QUEEN, KING]

class Card:
	'''
	Each card has a corresponding rank and suit 
	Cards are only comparble if they are the same suit 
	Only one deck of cards so no need for equal
	''' 
	def __init__(self, rank, suit): 
		self.rank = rank
		self.suit = suit
		self.idt = self.makeID()
	def sameSuit(self, other): 
		if self.suit == other.suit: 
			return True
		return False
	def makeID(self): 
		idt = self.rank 
		if self.suit == HEARTS: 
			return idt 
		elif self.suit == DIAMONDS:
			idt += 13
			return idt
		elif self.suit == SPADES:
			idt += 26
			return idt
		else:
			idt += 39
			return idt
	#overload lesss than and greater than operators
	def __lt__(self, other): 
		if self.sameSuit(other): 
			if self.rank < other.rank: 
			    return True  
			else: 
			    return False
		return False
	def __gt__(self, other):
		if self.sameSuit(other): 
			if self.rank > other.rank: 
				return True 
			else: 
				return False
		return False
	def __repr__(self): 
		return "%d of %s" %(self.rank, self.suit)

class Stack(list): 
	'''
	The stack represents one of the four piles that the player works on 
	Only one card can be removed from the stack at a time 
	'''
	def __init__(self): 
		super(Stack, self).__init__()
	def add(self, card): 
		self.append(card)
	def isEmpty(self): 
		return not self 
	def clear(self): 
		self[:] = []
	def peak (self): 
		if self.isEmpty():
			return EMPTY
		else:		
			answer = self[len(self)-1]
			return answer
	def remove(self): 
		self.pop()

class SetUp: 
	def __init__(self): 
		self.deck = Stack()
		self.createDeck()
		self.pile1 = Stack()
		self.pile2 = Stack()
		self.pile3 = Stack()
		self.pile4 = Stack()
		self.deal()
		self.top1 = self.pile1.peak()
		self.top2 = self.pile2.peak()
		self.top3 = self.pile3.peak()
		self.top4 = self.pile4.peak()
	def shuffle(self): 
		random.shuffle(self.deck)	

	def createDeck(self): 
		for rank, suit in itertools.product(RANKLIST, SUITLIST):
			self.deck.append(Card(rank, suit))
		self.shuffle()

	def canDeal(self): 
		return not self.deck.isEmpty()
			
	def deal(self): 
		'''
		If the deck is empty, checkt to see if won 
		Else add a new card to each of the four piles 
		'''
		if self.canDeal():  
			self.pile1.add(self.deck.pop())
			self.top1 = self.pile1.peak()
			self.pile2.add(self.deck.pop())
			self.top2 = self.pile2.peak()
			self.pile3.add(self.deck.pop())
			self.top3 = self.pile3.peak()
			self.pile4.add(self.deck.pop())
			self.top4 = self.pile4.peak() 
	def gameOver(self): 
		''' 
		if the four piles each only have one card 
		then you have won the game
		'''
		self.pile1.pop(); 
		self.pile2.pop(); 
		self.pile3.pop(); 
		self.pile4.pop(); 
		if self.pile1.isEmpty() and self.pile2.isEmpty() and self.pile3.isEmpty() and self.pile4.isEmpty(): 
			print 'Yay, you won' 
		print 'Sorry, you lost'
	def printTop(self):
                l = [self.pile1, self.pile2, self.pile3, self.pile4]
                return l
	def turn(self):
		remove = raw_input("Enter move (a card, pile to pile, nothing): ")
		while remove:
			prmv = remove.split(" ")
			if (prmv[1] == 'of'):
				rmvID = self.wordToID(prmv)
				if (self.isRemovable(rmvID, prmv[2])):
					self.removeCard(rmvID)
  			else: 
				pFrom = int(prmv[0])
				pTo = int(prmv[2])
				self.movePile(self.intToPile(pFrom), self.intToPile(pTo))
				self.updateTop(pFrom) 
				self.updateTop(pTo)
			self.printTop()
			remove = raw_input("Enter card to remove: ")

	def wordToID(self, s): 
		rmvID = int(s[0]) 
		if s[2] == DIAMONDS: 
			rmvID += 13
		if s[2] == SPADES: 
			rmvID += 13
		if s[2] == CLUBS: 
			rmvID += 13
		return rmvID

	def intToPile(self, num): 
		if num == 1: 
			return self.pile1 
		elif num == 2: 
			return self.pile2
		elif num == 3:	
			return self.pile3 
		elif num == 4: 
			return self.pile4

	def updateTop(self, num): 
		if num == 1: 
			self.top1 = self.pile1.peak()
		elif num == 2: 
			self.top2 = self.pile2.peak()
		elif num == 3:	
			self.top3 = self.pile3.peak()
		elif num == 4: 
			self.top4 = self.pile4.peak()
	def isRemovable(self, rmv, rmvsuit):
		'''
		print self.pile1.peak() 
		p1words = (self.pile1.peak()).split(" ")
		p2words = (self.pile2.peak()).split(" ")
		p3words = (self.pile3.peak()).split(" ")
		p4words = (self.pile4.peak()).split(" ")
		if p1words[2] == rmvsuit:
			pile1ID = self.wordToID(p1words)
			if pile1ID < rmv :
				return False
		if p2words[2] == rmvsuit:
			pile2ID = self.wordToID(p2words)
			if pile2ID < rmv : 
				return False
		if p3words[2] == rmvsuit: 
			pile3ID = self.wordToID(p3words)
			if pile3ID < rmv: 
				return False
		if p4words[2] == rmvsuit: 		
			pile4ID = self.wordToID(p4words)
			if pile4ID < rmv: 
				return False
		'''
		return True
		
	def removeCard(self, rmv): 
		if rmv == self.top1.idt: 
			self.pile1.remove() 
			self.top1 = self.pile1.peak()  
		elif rmv == self.top2.idt: 
			self.pile2.remove()
			self.top2 = self.pile2.peak()
		elif rmv == self.top3.idt: 
			self.pile3.remove()
			self.top3 = self.pile3.peak()
		elif rmv == self.top4.idt:
			self.pile4.remove()
			self.top4 = self.pile4.peak()

	def movePile(self,a,b): 
		if not b.isEmpty() or a.isEmpty():
			print 'cannot move' 
		moving = a.peak()
		b.add(moving) 
		a.remove()
	def play(self): 
		while not self.deck.isEmpty():
			self.printTop()
			self.turn()		
			self.deal()
		self.gameOver()

#Main function 
def main():  
	g = SetUp()
        g.printTop()
	#g.play()
if __name__ == '__main__': 
	main()
