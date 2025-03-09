import random
from typing import List
from core import Action, Strategy, PlayerInformation


class SimpleStrategy(Strategy):
    """ChatGPT's basic strategy"""

    def get_bet_size(self, info: PlayerInformation, bankroll: float) -> float:
        # Simple constant bet size - 5% of bankroll with minimum of 10
        return 1.0

    def get_action(
        self, info: PlayerInformation, possible_actions: List[Action], bankroll: float
    ) -> Action:
        """
        Determine the next action based on the basic strategy chart.
        Follows standard blackjack strategy for hard totals, soft totals, and pairs.
        """
        # If no actions are possible, return None
        if not possible_actions:
            return None

        # Get current hand and dealer upcard
        current_hand = info.current_game.player_hands[info.current_hand_index]
        dealer_upcard = info.current_game.dealer_hand.cards[0]

        # Convert dealer's card to numerical value (2-10, 11 for Ace)
        dealer_value = dealer_upcard.blackjack_value[0]
        if dealer_value == 1:  # Ace
            dealer_value = 11

        # Check if we have a pair
        has_pair = (
            len(current_hand.cards) == 2
            and current_hand.cards[0].value == current_hand.cards[1].value
        )

        # Check if we have a soft hand (contains an Ace counted as 11)
        is_soft = any(value for value in current_hand.possible_values if value <= 21)

        # Get the best hand value
        hand_value = current_hand.best_value

        # PAIR SPLITTING STRATEGY
        if has_pair and Action.SPLIT in possible_actions:
            value = current_hand.cards[0].value

            # Always split Aces and 8s
            if value == "A" or value == "8":
                return Action.SPLIT

            # Never split 10s, 5s, or 4s
            if value in ["10", "J", "Q", "K"] or value == "5" or value == "4":
                # Continue to hard/soft strategy
                pass

            # Split 9s against dealer 2-6, 8-9
            elif (
                value == "9"
                and dealer_value != 7
                and dealer_value != 10
                and dealer_value != 11
            ):
                return Action.SPLIT

            # Split 7s against dealer 2-7
            elif value == "7" and dealer_value <= 7:
                return Action.SPLIT

            # Split 6s against dealer 2-6
            elif value == "6" and dealer_value <= 6:
                return Action.SPLIT

            # Split 3s and 2s against dealer 2-7
            elif (value == "2" or value == "3") and dealer_value <= 7:
                return Action.SPLIT

        # SOFT TOTALS STRATEGY (hand with an Ace counted as 11)
        if is_soft:
            # Soft 20 (A,9): Always stand
            if hand_value >= 20:
                return Action.STAND

            # Soft 19 (A,8): Stand, except double against dealer 6
            elif hand_value == 19:
                if (
                    dealer_value == 6
                    and Action.DOUBLE in possible_actions
                    and len(current_hand.cards) == 2
                ):
                    return Action.DOUBLE
                else:
                    return Action.STAND

            # Soft 18 (A,7): Double against dealer 2-6, stand against 7-8, hit against 9-A
            elif hand_value == 18:
                if (
                    2 <= dealer_value <= 6
                    and Action.DOUBLE in possible_actions
                    and len(current_hand.cards) == 2
                ):
                    return Action.DOUBLE
                elif 7 <= dealer_value <= 8:
                    return Action.STAND
                else:
                    return (
                        Action.HIT if Action.HIT in possible_actions else Action.STAND
                    )

            # Soft 17 (A,6): Double against dealer 3-6, otherwise hit
            elif hand_value == 17:
                if (
                    3 <= dealer_value <= 6
                    and Action.DOUBLE in possible_actions
                    and len(current_hand.cards) == 2
                ):
                    return Action.DOUBLE
                else:
                    return (
                        Action.HIT if Action.HIT in possible_actions else Action.STAND
                    )

            # Soft 16 (A,5) and Soft 15 (A,4): Double against dealer 4-6, otherwise hit
            elif hand_value >= 15:
                if (
                    4 <= dealer_value <= 6
                    and Action.DOUBLE in possible_actions
                    and len(current_hand.cards) == 2
                ):
                    return Action.DOUBLE
                else:
                    return (
                        Action.HIT if Action.HIT in possible_actions else Action.STAND
                    )

            # Soft 14 (A,3) and Soft 13 (A,2): Double against dealer 5-6, otherwise hit
            else:
                if (
                    5 <= dealer_value <= 6
                    and Action.DOUBLE in possible_actions
                    and len(current_hand.cards) == 2
                ):
                    return Action.DOUBLE
                else:
                    return (
                        Action.HIT if Action.HIT in possible_actions else Action.STAND
                    )

        # HARD TOTALS STRATEGY
        else:
            # 17+: Always stand
            if hand_value >= 17:
                return Action.STAND

            # 16: Stand against dealer 2-6, otherwise hit
            elif hand_value == 16:
                if 2 <= dealer_value <= 6:
                    return Action.STAND
                else:
                    return (
                        Action.HIT if Action.HIT in possible_actions else Action.STAND
                    )

            # 15: Stand against dealer 2-6, otherwise hit
            elif hand_value == 15:
                if 2 <= dealer_value <= 6:
                    return Action.STAND
                else:
                    return (
                        Action.HIT if Action.HIT in possible_actions else Action.STAND
                    )

            # 14: Stand against dealer 2-6, otherwise hit
            elif hand_value == 14:
                if 2 <= dealer_value <= 6:
                    return Action.STAND
                else:
                    return (
                        Action.HIT if Action.HIT in possible_actions else Action.STAND
                    )

            # 13: Stand against dealer 2-6, otherwise hit
            elif hand_value == 13:
                if 2 <= dealer_value <= 6:
                    return Action.STAND
                else:
                    return (
                        Action.HIT if Action.HIT in possible_actions else Action.STAND
                    )

            # 12: Stand against dealer 4-6, otherwise hit
            elif hand_value == 12:
                if 4 <= dealer_value <= 6:
                    return Action.STAND
                else:
                    return (
                        Action.HIT if Action.HIT in possible_actions else Action.STAND
                    )

            # 11: Always double if possible, otherwise hit
            elif hand_value == 11:
                if Action.DOUBLE in possible_actions and len(current_hand.cards) == 2:
                    return Action.DOUBLE
                else:
                    return (
                        Action.HIT if Action.HIT in possible_actions else Action.STAND
                    )

            # 10: Double against dealer 2-9 if possible, otherwise hit
            elif hand_value == 10:
                if (
                    dealer_value <= 9
                    and Action.DOUBLE in possible_actions
                    and len(current_hand.cards) == 2
                ):
                    return Action.DOUBLE
                else:
                    return (
                        Action.HIT if Action.HIT in possible_actions else Action.STAND
                    )

            # 9: Double against dealer 3-6 if possible, otherwise hit
            elif hand_value == 9:
                if (
                    3 <= dealer_value <= 6
                    and Action.DOUBLE in possible_actions
                    and len(current_hand.cards) == 2
                ):
                    return Action.DOUBLE
                else:
                    return (
                        Action.HIT if Action.HIT in possible_actions else Action.STAND
                    )

            # 8 or less: Always hit
            else:
                return Action.HIT if Action.HIT in possible_actions else Action.STAND

        # Default action if nothing else applies
        if Action.HIT in possible_actions:
            return Action.HIT
        elif Action.STAND in possible_actions:
            return Action.STAND
        else:
            return possible_actions[0]  # Return first available action
