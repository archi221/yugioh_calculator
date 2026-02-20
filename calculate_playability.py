from enum import Enum
import numpy as np
file = "Default_Deck.txt"

class Step(Enum):
    SPELLS = 1
    PLAYABAL_HANDS = 2
    GAMBA_EFFECTS = 3

def read_decklist(file):
    ignored_names = ["Monster", "Spell", "Trap"]
    reading_step = Step.SPELLS

    deck = []
    id_to_cards = []
    card_groups = {}
    playabal_hands = []
    gamba = {}
    id = 0
    with open(file) as f:
        for line in f:
            
            if line.strip() in ignored_names:
                continue
            if not line.strip():
                continue

            if line.lower().strip("\n") == ":playabal hands":
                reading_step = Step.PLAYABAL_HANDS
                continue
            if line.lower().strip("\n") == ":gamble effects":
                reading_step = Step.GAMBA_EFFECTS
                continue

            if reading_step == Step.SPELLS:

                line_list = line.split(" ", maxsplit=1)
                try:
                    amount = int(line_list[0])
                    card_name_and_group = line_list[1].split(";")
                except ValueError:
                    amount = 0
                    card_name_and_group = line.split(";")
                except IndexError as e:
                    print(f"Error while reading amount: {e}")
                    continue
                card_name = card_name_and_group[0].strip()
                group_list = card_name_and_group[1:]
                id_to_cards.insert(id, card_name)

                assert id_to_cards[id] == card_name, f"Karte: {card_name} wurde nicht korrekt an ID: {id} eingefügt"
                
                for i in range(amount):
                    deck.append(id)
                for group in group_list:
                    card_groups.setdefault(group.strip(), []).append(id)

                id += 1

            elif reading_step == Step.PLAYABAL_HANDS:
                group_names = set(card_groups.keys())
                playbal_combo = [item.strip() for item in line.split(";")]

                combinations = [[]]
                for item in playbal_combo:
                    
                    if item in group_names:
                        
                        combinations = [combo + [card] 
                                    for combo in combinations 
                                    for card in card_groups[item]]
                    else:
                        ID = id_to_cards.index(item) #Todo es sollte kartenname zu ids gemapt werden
                        combinations = [combo + [ID] for combo in combinations]
                
                playabal_hands.extend(combinations)

            elif reading_step == Step.GAMBA_EFFECTS:

                line_list = line.split(";")
                assert len(line_list) == 3 , "nicht genug angaben für gamba effekt"
                gamba[id_to_cards.index(line_list[0].strip())] = (int(line_list[1]), int(line_list[2]))
    #Todo check for unique playabal hands
    return deck, id_to_cards, playabal_hands, gamba

def IsHandPlayabal(deck, playabal_hands, gamba):
    playabal_gamba = False
    playabal = False
    drawn_cards_set = set(deck[:5])
    gamba_cards = gamba.keys()
    #print(f"Drawn Cards: {drawn_cards_set}")
    #print(f"playabal hands: {playabal_hands}")
    #print(f"issin: {np.isin(playabal_hands, drawn_cards_set)}")
    for combo in playabal_hands:
        if all(card in drawn_cards_set for card in combo):
            playabal = True
    if playabal:
        return playabal, playabal
    for card in gamba_cards:
        if card in drawn_cards_set:
            look_amount, draws_amount = gamba[card]
            looks = deck[6:6 + look_amount]
            for gamba_card in looks:
                drawn_cards_set.add(gamba_card)
                for combo in playabal_hands:
                    if all(_card in drawn_cards_set for _card in combo):
                        playabal_gamba = True
                        return playabal, playabal_gamba
    return playabal, playabal_gamba


def TestDeckConsistency(file):
    deck, id_to_cards, playabal_hands, gamba = read_decklist(file)
    print(f"""
Calculating Probability for {len(deck)} Card Deck

Unique Playabal_hands: {len(playabal_hands)}
""")
    testing_hands = 2_000_000
    counter = 0
    gamba_counter = 0
    deck = np.array(deck)

    for i in range(testing_hands):
        np.random.shuffle(deck)
        normal_playability , gamba_playability = IsHandPlayabal(deck, playabal_hands, gamba)
        if normal_playability:
            counter += 1
        if gamba_playability:
            gamba_counter += 1
    print(f"Playabal: {counter / testing_hands * 100}% of times")
    print(f"Playabal with gambling: {gamba_counter / testing_hands * 100}% of times")

def main():
    TestDeckConsistency(file)
    print("Hello World!")

if __name__ == "__main__":
    main()