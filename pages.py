from otree.api import (
    models, Currency as c, currency_range
)
from ._builtin import Page, WaitPage
from .models import Constants
from math import factorial
import datetime
import random
import time


class WelcomePage(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        return {
            'item_type': self.participant.vars['item_type'],
            'num_items': self.participant.vars['num_items'],
            'outcomes': self.participant.vars['outcomes'],
            'randout': self.participant.vars['randout'],
            'outcomep': self.participant.vars['outcome_pairs'],
        }


class QuestionPage(Page):
    form_model = 'player'
    form_fields = ['gender', 'major', 'langs']  #, 'attend_hs', 'hs_input']

    def is_displayed(self):
        return self.subsession.round_number == 1


class IntroStageTwo(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1


class SetUtilPage_Movie(Page):
    form_model = 'player'
    form_fields = ['m_outcome1', 'm_outcome2', 'm_outcome3', 'm_outcome4', 'm_outcome5', 'm_outcome6', 'm_outcome7', 'm_outcome8']

    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        outcomes = Constants.movie_types
        return {
            'outcomes': outcomes,
            'item_type': 'movies'
        }

    def before_next_page(self):
        movie_utilities = [self.player.m_outcome1, self.player.m_outcome2, self.player.m_outcome3, self.player.m_outcome4,
                           self.player.m_outcome5, self.player.m_outcome6, self.player.m_outcome7, self.player.m_outcome8]

        #Save all movie util values
        for i in range(len(movie_utilities)):
            self.participant.vars['movie_utils'][i] = movie_utilities[i]


class SetUtilPage_Pizza(Page):
    form_model = 'player'
    form_fields = ['p_outcome1', 'p_outcome2', 'p_outcome3', 'p_outcome4', 'p_outcome5', 'p_outcome6', 'p_outcome7', 'p_outcome8']

    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        outcomes = Constants.pizza_types
        return {
            'outcomes': outcomes,
            'item_type': 'pizza'
        }

    def before_next_page(self):
        pizza_utilities = [self.player.p_outcome1, self.player.p_outcome2, self.player.p_outcome3, self.player.p_outcome4,
                          self.player.p_outcome5, self.player.p_outcome6, self.player.p_outcome7, self.player.p_outcome8]

        #Save all pizza util values
        for i in range(len(pizza_utilities)):
            self.participant.vars['pizza_utils'][i] = pizza_utilities[i]

        #Get the util values for the subset of items being used in this interaction
        for i in range(self.participant.vars['num_items']):
            item = self.participant.vars['outcomes'][i]
            if self.participant.vars['item_type'] == "movies":
                index = Constants.movie_types.index(item)
                self.participant.vars['self_utils'][i] = self.participant.vars['movie_utils'][index]
            else:
                index = Constants.pizza_types.index(item)
                self.participant.vars['self_utils'][i] = self.participant.vars['pizza_utils'][index]

        #Payoff values for each item type
        self.participant.vars['movie_payoffs'] = [round(2*x + 2, 2) for x in self.participant.vars['movie_utils']]
        self.participant.vars['pizza_payoffs'] = [round(2*x + 2, 2) for x in self.participant.vars['pizza_utils']]

        #Pick a random outcome that does not have a util value = 0
        outcomes = self.participant.vars['outcomes']
        self_utils = self.participant.vars['self_utils']
        self.participant.vars['randout'] = random.choice([x for x in outcomes if self_utils[outcomes.index(x)] != 0])


class InstructionsPage0(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1


class InstructionsPage1(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1


class InstructionsPage2(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1


class InstructionsPage3(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1


class InstructionsPage4(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1


class InstructionsPage5(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1


class InstructionsPage6(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1


class InstructionsPage7(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        m_payoff_str = []
        p_payoff_str = []
        for i in range(len(self.participant.vars['movie_payoffs'])):
            #Put payoffs in standard money format ($##.##) for HTML page
            m_payoff_str.append("{:0.2f}".format(self.participant.vars['movie_payoffs'][i]))
            p_payoff_str.append("{:0.2f}".format(self.participant.vars['pizza_payoffs'][i]))
        return {
            'movie_types_payoffs': self.player.join_lists(Constants.movie_types, m_payoff_str),
            'pizza_types_payoffs': self.player.join_lists(Constants.pizza_types, p_payoff_str)
        }


class SetOppModelPage1(Page):
    form_model = 'player'
    form_fields = ['likert_scale']

    def is_displayed(self):
        return self.subsession.round_number % Constants.rounds_per_partner == 1 and self.subsession.round_number != Constants.num_rounds

    def vars_for_template(self):
        interact = (self.subsession.round_number // Constants.rounds_per_partner) + 1
        round_to_interact = {1: "First", 2: "Second", 3: "Third", 4: "Fourth", 5: "Fifth"}

        return {
            'interaction': round_to_interact[interact],
            'random_outcome': self.participant.vars['randout'],
            'item_type': self.participant.vars['item_type'],
            'num_items': len(self.participant.vars['outcomes']),
            'outcomes': self.participant.vars['outcomes'],
        }

    def before_next_page(self):
        self.participant.vars['likert_info'] = (self.participant.vars['randout'], self.player.likert_scale)


class SetOppModelPage2(Page):
    form_model = 'player'
    form_fields = ['actother']

    def vars_for_template(self):
        return {
            'opp_likert_answer': self.player.get_partner().participant.vars['likert_info'][1],
            'opp_likert_outcome': self.player.get_partner().participant.vars['likert_info'][0],
            'item_type': self.participant.vars['item_type'][:-1],
            'item_type_plural': self.participant.vars['item_type']
        }

    def is_displayed(self):
        return self.subsession.round_number % Constants.rounds_per_partner == 2

    def before_next_page(self):
        #Value of actother cannot be zero--otherwise all values in opp_model will get set to 0
        if self.player.actother == 0:
            self.player.actother = 0.001

        #From actother and randout, determine the rest of the opponent player model
        self.player.set_opp_model(self.player.in_round(self.round_number - 1).get_partner().participant.vars['randout'],
                                  self.player.actother, self.player.get_partner().participant.vars['self_utils'])
        self.player.set_tradeoff_constant()

        all_vals = list(self.participant.vars['self_utils'])
        if self.participant.vars['num_items'] == 5:
            all_vals.extend([self.player.opp_util_model_1, self.player.opp_util_model_2, self.player.opp_util_model_3,
                             self.player.opp_util_model_4, self.player.opp_util_model_5])
        else:
            all_vals.extend([self.player.opp_util_model_1, self.player.opp_util_model_2, self.player.opp_util_model_3,
                             self.player.opp_util_model_4, self.player.opp_util_model_5, self.player.opp_util_model_6,
                             self.player.opp_util_model_7, self.player.opp_util_model_8])

        #Find most extreme value to set limits of the comp_utility applet
        magnitudes = [abs(x) for x in all_vals]
        self.participant.vars['scale_max_value'] = max(max(magnitudes), 0.5)


class WaitingPageTimer(WaitPage):
    template_name = 'accom_dynam/WaitingPageTimer.html'

    def is_displayed(self):
        return self.subsession.round_number % Constants.rounds_per_partner == 2

    def after_all_players_arrive(self):
        #User has 10 minutes to complete as many pages as possible
        self.group.get_player_by_id(1).participant.vars['expiry'] = time.time() + 10 * 60
        self.group.get_player_by_id(2).participant.vars['expiry'] = time.time() + 10 * 60


class AccomDynamPage(Page):
    form_model = 'player'
    form_fields = ['opp_util_model_1', 'opp_util_model_2', 'opp_util_model_3', 'opp_util_model_4',
                   'opp_util_model_5', 'opp_util_model_6', 'opp_util_model_7', 'opp_util_model_8']

    timer_text = 'Time left to complete interaction with First Partner:'

    def get_timeout_seconds(self):
        return self.participant.vars['expiry'] - time.time()

    def is_displayed(self):
        return self.subsession.round_number % Constants.rounds_per_partner >= 3 and self.participant.vars['end_experiment'] == False

    def vars_for_template(self):
        for p in self.group.get_players():
            p.get_prev_opp_model()

        #Make sure that options_to_display is the same for players in the same group
        self.group.get_player_by_id(1).participant.vars['options_to_display'] = self.group.get_player_by_id(1).pick_pair(self.subsession.round_number)
        self.group.get_player_by_id(2).participant.vars['options_to_display'] = self.group.get_player_by_id(1).participant.vars['options_to_display']
        #Randomize order of option1 and option2
        rand_index = random.randint(0, 1)
        if rand_index == 0:
            option1, option2 = self.group.get_player_by_id(1).participant.vars['options_to_display']
        else:
            option2, option1 = self.group.get_player_by_id(1).participant.vars['options_to_display']

        self.player.best_option(option1, option2)
        self.player.get_partner().best_option(option1, option2)
        result = int(self.player.best_choice == self.player.get_partner().best_choice)   #0=disagreement, 1=agreement

        if result == 0:
            self.player.round_result = "Disagree"
            # self.participant.vars['disagree_count'] += 1
            # self.participant.vars['success_pairs'] = []
        else:
            self.player.round_result = "Agree"
            # self.participant.vars['success_pairs'].append(self.participant.vars['options_to_display'])

        if self.participant.vars['num_items'] == 5:
            opp_model = [self.player.opp_util_model_1, self.player.opp_util_model_2, self.player.opp_util_model_3, self.player.opp_util_model_4, self.player.opp_util_model_5]
        else:
            opp_model = [self.player.opp_util_model_1, self.player.opp_util_model_2, self.player.opp_util_model_3, self.player.opp_util_model_4,
                         self.player.opp_util_model_5, self.player.opp_util_model_6, self.player.opp_util_model_7, self.player.opp_util_model_8]
        payoff_sess = []
        for i in range(len(self.participant.vars['self_utils'])):
            payoff_sess.append("{:0.2f}".format(self.participant.vars['self_utils'][i]*2 + 2))

        return {
            'round_number': (self.subsession.round_number % Constants.rounds_per_partner) - 2,
            'num_items': self.participant.vars['num_items'],
            'self_utils': self.participant.vars['self_utils'],
            'opp_model': opp_model,
            'scale_max_value': self.participant.vars['scale_max_value'],
            'option1': option1,
            'option2': option2,
            'self_best_choice': self.player.best_choice,
            'opp_best_choice': self.player.get_partner().best_choice,
            'result': self.player.round_result,
            'table': self.player.join_lists(self.participant.vars['outcomes'], payoff_sess),
            'item_type': self.participant.vars['item_type'],
        }

    def before_next_page(self):
        self_last_round = self.player.in_round(self.subsession.round_number - 1)
        if self.timeout_happened:
            self.player.opp_util_model_1 = self_last_round.opp_util_model_1
            self.player.opp_util_model_2 = self_last_round.opp_util_model_2
            self.player.opp_util_model_3 = self_last_round.opp_util_model_3
            self.player.opp_util_model_4 = self_last_round.opp_util_model_4
            self.player.opp_util_model_5 = self_last_round.opp_util_model_5
            if self.participant.vars['num_items'] == 8:
                self.player.opp_util_model_6 = self_last_round.opp_util_model_6
                self.player.opp_util_model_7 = self_last_round.opp_util_model_7
                self.player.opp_util_model_8 = self_last_round.opp_util_model_8

            if self_last_round.opp_util_model_1 == 0:
                p = self.player.opp_util_model_2 / self_last_round.opp_util_model_2
            else:
                p = self.player.opp_util_model_1 / self_last_round.opp_util_model_1
            self.player.update_tradeoff_constant(p)
        else:
            if self_last_round.opp_util_model_1 == 0:
                p = self.player.opp_util_model_2 / self_last_round.opp_util_model_2
            else:
                p = self.player.opp_util_model_1 / self_last_round.opp_util_model_1
            self.player.update_tradeoff_constant(p)


class WaitingPage(WaitPage):
    template_name = 'accom_dynam/WaitingPage.html'

    def after_all_players_arrive(self):
        self.group.set_payoffs()

        if self.subsession.round_number % Constants.rounds_per_partner > 2:
            for p in self.group.get_players():
                if p.round_result == "Agree":
                    p.participant.vars['success_pairs'].append(p.participant.vars['options_to_display'])
                else:
                    p.participant.vars['disagree_count'] += 1
                    p.participant.vars['success_pairs'] = []

            if len(self.group.get_player_by_id(1).participant.vars['success_pairs']) == len(self.group.get_player_by_id(1).participant.vars['outcome_pairs']):
                for p in self.group.get_players():
                    p.participant.vars['end_experiment'] = True
                    p.participant.vars['reach_equilibrium'] = True
                    p.participant.vars['total_rounds'] = (self.subsession.round_number % Constants.rounds_per_partner) - 2
            elif self.group.get_player_by_id(1).participant.vars['expiry'] - time.time() < 2 or \
                    self.group.get_player_by_id(2).participant.vars['expiry'] - time.time() < 2:
                for p in self.group.get_players():
                    p.participant.vars['end_experiment'] = True
                    p.participant.vars['reach_equilibrium'] = False
                    p.participant.vars['total_rounds'] = (self.subsession.round_number % Constants.rounds_per_partner) - 2
            else:
                for p in self.group.get_players():
                    p.participant.vars['end_experiment'] = False

    def vars_for_template(self):
        return {
            'end_experiment': self.participant.vars['end_experiment'],
            'reach_equilibrium': self.participant.vars['reach_equilibrium'],
            'next_round': self.subsession.round_number - 1,
        }

    def is_displayed(self):
        return self.subsession.round_number % Constants.rounds_per_partner != 2 and self.participant.vars['end_experiment'] == False


class Results(Page):
    def is_displayed(self):
        return self.participant.vars['end_experiment'] and self.subsession.round_number % Constants.rounds_per_partner == 0

    def vars_for_template(self):
        vars_to_keep = dict()
        vars_to_keep['num_items'] = self.participant.vars['num_items']
        vars_to_keep['item_type'] = self.participant.vars['item_type']
        vars_to_keep['outcomes'] = self.participant.vars['outcomes']
        vars_to_keep['self_utils'] = self.participant.vars['self_utils']
        vars_to_keep['reach_equilibrium'] = self.participant.vars['reach_equilibrium']
        self.player.participant_vars_dump = str(vars_to_keep)

        total_rounds = self.participant.vars['total_rounds']
        try:
            paying_rounds = random.sample(range(1, total_rounds+1), 5)
        except ValueError:  #less than 5 rounds played in total
            paying_rounds = []
        player_in_paying_rounds = []

        x = (self.subsession.round_number // Constants.rounds_per_partner) - 1

        for round_num in paying_rounds:
            player = self.player.in_round(round_num + (Constants.rounds_per_partner*x) + 2)
            player_in_paying_rounds.append((round_num, player.round_result, player.best_choice, player.payoff))

        cumulative_payoff = sum([p[3] for p in player_in_paying_rounds])

        if self.participant.vars['reach_equilibrium']:
            eq_payoff = c(4)
        else:
            eq_payoff = c(0)

        total_payoff = cumulative_payoff + eq_payoff + c(7)

        payment_info = {
            'total_rounds': total_rounds,
            'paying_rounds': sorted(paying_rounds),
            'player_in_paying_rounds': sorted(player_in_paying_rounds),
            'cumulative_payoff': cumulative_payoff,
            'reach_eq_payoff': eq_payoff,
            'total_earned_payoff': cumulative_payoff + eq_payoff,
            'total_payoff': total_payoff,
            'rounded_total': c(self.player.round_to_quarter(total_payoff)),
            'reach_equilibrium': self.player.participant.vars['reach_equilibrium'],
            'num_rounds_agree': total_rounds - self.participant.vars['disagree_count'],
        }

        interact = (self.subsession.round_number // Constants.rounds_per_partner)
        self.participant.vars['payoff_history'][interact] = payment_info

        round_to_interact = {1: "First", 2: "Second", 3: "Third", 4: "Fourth", 5: "Fifth"}
        interaction = round_to_interact[interact]

        return {
            'interaction': interaction,
            'reach_equilibrium': self.player.participant.vars['reach_equilibrium'],
            'total_rounds': total_rounds,
            'num_rounds_agree': total_rounds - self.participant.vars['disagree_count']
        }

    # def app_after_this_page(self, upcoming_apps):
    #     return 'accom_dynam_two'


class WaitPageBetweenPartner(WaitPage):
    template_name = 'accom_dynam/WaitPageBetweenPartner.html'

    def is_displayed(self):
        return self.participant.vars['end_experiment'] and self.subsession.round_number % Constants.rounds_per_partner == 0

    def after_all_players_arrive(self):
        interaction = self.round_number // Constants.rounds_per_partner

        if interaction == 5:
            for g in self.subsession.get_groups():
                num_items = random.choice([5, 8])  # ***
                item_type = random.choice(["pizzas", "movies"])  # ***

                if item_type == "pizzas":
                    outcomes = random.sample(Constants.pizza_types, num_items)  # ***
                elif item_type == "movies":
                    outcomes = random.sample(Constants.movie_types, num_items)  # ***
                else:
                    outcomes = []

                outcome_pairs = [[x, y] for x in outcomes for y in outcomes if outcomes.index(x) < outcomes.index(y)]

                for p in g.get_players():
                    #Redefine variables for the new interaction
                    p.participant.vars['num_items'] = num_items
                    p.participant.vars['item_type'] = item_type
                    p.participant.vars['outcomes'] = outcomes
                    # p.participant.vars['randout'] = random.choice(outcomes)
                    p.participant.vars['outcome_pairs'] = outcome_pairs
                    # p.participant.vars['expiry'] = []

                    #Pull utility values from set_util
                    self_utils = []
                    for i in outcomes:
                        if item_type == 'pizzas':
                            index = Constants.pizza_types.index(i)
                            util = p.participant.vars['pizza_utils'][index]
                        else:
                            index = Constants.movie_types.index(i)
                            util = p.participant.vars['movie_utils'][index]
                        self_utils.append(util)
                    p.participant.vars['self_utils'] = self_utils

                    #Pick a random outcome that does not have a util value = 0
                    outcomes = self.participant.vars['outcomes']
                    self_utils = self.participant.vars['self_utils']
                    self.participant.vars['randout'] = random.choice([x for x in outcomes if self_utils[outcomes.index(x)] != 0])

                    #Reset other participant variables
                    p.participant.vars['likert_info'] = ('x', 'y')  # (outcome, likert_answer) #***
                    p.participant.vars['scale_max_value'] = 0.5
                    p.participant.vars['options_to_display'] = ('x', 'y')  # ***
                    p.participant.vars['success_pairs'] = []  # ***
                    p.participant.vars['disagree_count'] = 0  # ***
                    p.participant.vars['end_experiment'] = False  # ***
                    p.participant.vars['reach_equilibrium'] = False  # ***

    def vars_for_template(self):
        round_to_interact = {1: "First", 2: "Second", 3: "Third", 4: "Fourth", 5: "Fifth"}
        interaction = round_to_interact[self.round_number // Constants.rounds_per_partner]

        return {'interaction': interaction,
                'last_interact': interaction == "Fifth"}


class PersonalityTestPage(Page):
    form_model = 'player'
    form_fields = ['Q01', 'Q02', 'Q03', 'Q04', 'Q05', 'Q06', 'Q07', 'Q08', 'Q09', 'Q10', 'Q11', 'Q12', 'Q13', 'Q14',
                   'Q15', 'Q16', 'Q17', 'Q18', 'Q19', 'Q20', 'Q21', 'Q22', 'Q23', 'Q24', 'Q25', 'Q26', 'Q27', 'Q28',
                   'Q29', 'Q30', 'Q31', 'Q32', 'Q33', 'Q34', 'Q35', 'Q36', 'Q37', 'Q38', 'Q39', 'Q40', 'Q41']

    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds


class PaymentPage(Page):
    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    def vars_for_template(self):
        # Check if there is at least one valid interaction for payment
        valid_payment_interacts = [x for x in self.participant.vars['payoff_history'].keys() if self.participant.vars['payoff_history'][x]['paying_rounds'] != []]

        if valid_payment_interacts == []:
            #No interactions are eligible for payment
            valid_payment = False
            return {'date': datetime.datetime.today().strftime("%B %d, %Y"),
                    'valid_payment': valid_payment,
                    'total_earned_payoff': '$0.00',
                    'cumulative_payoff': '$0.00',
                    'reach_eq_payoff': '$0.00',
                    'total_payoff': '$7.00',
                    'rounded_total': '$7.00'}
        else:
            valid_payment = True

            #Pick a random interaction for payment
            payment_interact = random.choice(valid_payment_interacts)

            #Get payment information for the chosen interaction
            payment_info = self.participant.vars['payoff_history'][payment_interact]

            round_to_interact = {1: "First", 2: "Second", 3: "Third", 4: "Fourth", 5: "Fifth"}

            payment_info['date'] = datetime.datetime.today().strftime("%B %d, %Y")
            payment_info['interact_for_payment'] = round_to_interact[payment_interact]
            payment_info['valid_payment'] = valid_payment

            return payment_info



page_sequence = [
    # WelcomePage,
    # QuestionPage,
    # IntroStageTwo,
    # SetUtilPage_Movie,
    # SetUtilPage_Pizza,
    # InstructionsPage0,
    # InstructionsPage1,
    # InstructionsPage2,
    # InstructionsPage3,
    # InstructionsPage4,
    # InstructionsPage5,
    # InstructionsPage6,
    # InstructionsPage7,
    # SetOppModelPage1,
    # SetOppModelPage2,
    # WaitingPageTimer,
    # AccomDynamPage,
    # WaitingPage,
    # Results,
    # WaitPageBetweenPartner,
    PersonalityTestPage,
    PaymentPage
]
