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
                gamba[line_list[0]] = (line_list[1], line_list[2])

    return deck, id_to_cards, playabal_hands, gamba

def IsHandPlayabal(deck, playabal_hands, gamba):
    print("Hello World!")

def TestDeckConsistency(file):
    deck, id_to_cards, playabal_hands, gamba = read_decklist(file)
    print(f"""
Calculating Probability for {len(deck)} Card Deck

Unique Cards: {', '.join(id_to_cards)}

Unique Playabal_hands: {len(playabal_hands)}
""")
    counter = 0
    for i in range(1,000,000):
        if IsHandPlayabal(deck, playabal_hands, gamba):
            counter += 1
    print(counter / 1,000,000 * 100)
def main():
    TestDeckConsistency(file)
    print("Hello World!")

if __name__ == "__main__":
    main()