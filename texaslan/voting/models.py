from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
import json

from texaslan.users.models import User

CANDIDATE_POSITIONS = (
    ("P", "President"),
    ("A", "VP of Administration"),
    ("T", "Treasurer"),
    ("S", "VP of Service"),
    ("N", "VP of New Member Services"),
    ("O", "VP of Social Affairs"),
    ("J", "VP of Standards"),
    ("R", "Risk Management"),
    ("B", "Standards Board"),
)

POSITION_NUMS = {
    "P": 1,
    "A": 1,
    "T": 1,
    "S": 1,
    "N": 1,
    "O": 1,
    "J": 1,
    "R": 1,
    "B": 2,
}


class Candidate(models.Model):
    position = models.CharField(max_length=1, choices=CANDIDATE_POSITIONS, default="P")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="candidate_user",
                             verbose_name=_("Candidate"))
    description = models.TextField(_("Description"), help_text="Describe why you should be in this role")
    has_won = models.BooleanField(_("Has won"), default=False)

    def get_position_str(self):
        for (short, actual) in CANDIDATE_POSITIONS:
            if short == self.position:
                return actual
        return "N/A"

    def __str__(self):
        return self.get_position_str() + "- " + self.user.full_name


class VoteStatus(models.Model):
    class Meta:
        verbose_name_plural = 'Vote statuses'

    voter = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="vote_status",
                              verbose_name=_("Voter"))
    has_voted = models.BooleanField(_("Has Voted"), default=True)

    def __str__(self):
        return self.voter.full_name


class VoteBallot(models.Model):
    position = models.CharField(max_length=1, choices=CANDIDATE_POSITIONS, default="P")
    candidates_json = models.TextField(_("Candidates json"))

    def __str__(self):
        return str(self.id)


class VoteService:
    @staticmethod
    def run_election():
        success = True
        print("Starting Election")

        for (position_id, position_str) in CANDIDATE_POSITIONS:
            print("Starting " + position_str)
            positions_won = len(Candidate.objects.filter(position=position_id, has_won=True))
            while positions_won < POSITION_NUMS[position_id]:
                winning_candidate = VoteService.get_winner_for_position(position_id)

                # if winner found, make them win, remove ballots for position,
                #       remove all other candidate positions for winner
                if winning_candidate != None:
                    positions_won += 1
                    winning_candidate.has_won = True
                    winning_candidate.save()
                    if positions_won == POSITION_NUMS[position_id]:
                        VoteBallot.objects.filter(position=position_id).delete()
                    print("delete these candidates: " + str([cand.user.username for cand in
                                                             Candidate.objects.filter(
                                                                 user__pk=winning_candidate.user.pk,
                                                                 has_won=False)]))
                    Candidate.objects.filter(user__pk=winning_candidate.user.pk, has_won=False).delete()
                else:
                    success = False
                    break

            if not success:
                break

        return success

    @staticmethod
    def get_winner_for_position(position_id):
        candidates = set(Candidate.objects.filter(position=position_id, has_won=False))
        ballots = set(VoteBallot.objects.filter(position=position_id))
        winner_candidate = None

        while winner_candidate == None and len(candidates) > 0:
            print("Looking for winner...")
            candidates_results = {candidate.id: 0 for candidate in candidates}

            # Find Voters First Choice out of candidates
            for ballot in ballots:
                ballot_candidates = json.loads(ballot.candidates_json)
                for candidate_id in ballot_candidates:
                    if candidate_id in candidates_results:
                        candidates_results[candidate_id] += 1
                        break
            print("results: " + str(candidates_results))

            # Find the majority winner
            num_actives = len(User.objects.filter(groups__name='Active'))
            needed_amt_votes = (num_actives // 2) + 1
            print(needed_amt_votes)

            for candidate_id in candidates_results:
                print("checking for majority..." + str(candidate_id) + " " + str(
                    candidates_results[candidate_id] >= needed_amt_votes))
                if candidates_results[candidate_id] >= needed_amt_votes:
                    majority_candidate = Candidate.objects.get(pk=candidate_id)
                    if majority_candidate in candidates:
                        print("Winner found here! " + str(candidate_id))
                        winner_candidate = majority_candidate
                        break

            if winner_candidate != None:
                # Found winner, return
                print("Winner returned here! " + str(winner_candidate))
                return winner_candidate
            else:
                # Remove min vote candidates to continue (smallest or tied with smallest)
                min_vote_candidate_id_list = []
                print("num_actives " + str(num_actives))
                min_vote_count = num_actives
                for candidate_id in candidates_results:
                    if candidates_results[candidate_id] == min_vote_count:
                        min_vote_candidate_id_list.append(candidate_id)
                    elif candidates_results[candidate_id] < min_vote_count:
                        min_vote_count = candidates_results[candidate_id]
                        min_vote_candidate_id_list.clear()
                        min_vote_candidate_id_list.append(candidate_id)

                print("min_vote_candidates " + str(min_vote_count) + str(min_vote_candidate_id_list))
                min_candidates = set(Candidate.objects.filter(pk__in=min_vote_candidate_id_list))
                for min_cand in min_candidates:
                    candidates.remove(min_cand)

        return winner_candidate

    @staticmethod
    def get_position_str(position):
        for (short, actual) in CANDIDATE_POSITIONS:
            if short == position:
                return actual
        return "N/A"
