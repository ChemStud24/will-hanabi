from hanabi_learning_environment.pyhanabi import color_char_to_idx, HanabiMoveType
# from pyhanabi import color_char_to_idx, HanabiMove
import random

def is_discardable(color,rank,state):
	return rank <= state.fireworks()[color_char_to_idx(color)]

def discard_legal(state):
	for move in state.legal_moves():
		if move.type() == HanabiMoveType.DISCARD:
			return True
	return False

def double_dummy_action(state):
	cur_hand = (card.to_dict() for card in state.player_hands()[state.cur_player()])

	# if I have a playable card, play it
	for idx,card in enumerate(cur_hand):
		if state.card_playable_on_fireworks(color_char_to_idx(card['color']),card['rank']):
			return HanabiMove.get_play_move(idx)

	# if you have a playable card, I will give a random clue if allowed
	if state.information_tokens() > 0:
		all_hands = state.player_hands()
		for pid,hand in enumerate(all_hands):
			if pid != state.cur_player():
				hand = (card.to_dict() for card in hand)
				for idx,card in enumerate(hand):
					if state.card_playable_on_fireworks(color_char_to_idx(card['color']),card['rank']):
						# give the first clue
						for move in state.legal_moves():
							if move.type() == HanabiMoveType.REVEAL_COLOR or move.type() == HanabiMoveType.REVEAL_RANK:
								return move

	if discard_legal(state):

		# if I have a discardable card, I will discard it
		for idx,card in enumerate(cur_hand):
			if is_discardable(card['color'],card['rank'],state):
				return HanabiMove.get_discard_move(idx)

		# if I have duplicates, I will discard one
		# else, I will discard the highest card in my hand
		dups = []
		highest = -1
		high_idx = -1
		for idx,card in enumerate(cur_hand):
			if card in dups:
				return HanabiMove.get_discard_move(idx)
			else:
				dups.append(card)
				if card['rank'] > highest:
					highest = card['rank']
					high_idx = idx
		return HanabiMove.get_discard_move(high_idx)

	# an edge case where none of the above is true
	return random.choice(state.legal_moves())