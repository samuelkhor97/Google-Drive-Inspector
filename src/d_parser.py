"""
Prototype of parser class, ver1: take in an array of revisions data, provide functions extract data by file_id
"""
import time


class D_Parser:

    def __init__(self, files_revisions):
        self.file_revs = files_revisions

    def _get_revisions_by_id(self, file_id):
        # except KeyError on caller
        return self.file_revs[file_id]

    def get_file_name(self, file_id):
        # Tiong: I'm ashamed of myself for writing this piece of shit
        revs_list = self._get_revisions_by_id(file_id)
        for rev in revs_list:
            return rev['originalFilename']

    """
    Output: [ (userA, modifiedTime), (userA, modifiedTime), (userB, modifiedTime),  (userC, modifiedTime)... ]
    Can obtain the contribution percentage by calculating the frequency of each user over total revisions count.
    *Awaiting implementation* 
    """

    def list_revisions_user(self, file_id):
        try:
            userlist = []
            file_revs = self._get_revisions_by_id(file_id)
            for rev in file_revs:
                userlist.append(
                    (rev['lastModifyingUser']['displayName'], rev['modifiedTime']))
            return userlist
        except KeyError:
            return []

    def calculate_contribution(self):
        """
        Return number of contributions for each member of team drive 
        @:return all_users_contribution: (dict) {key:(string) user, value: (int) number_of_contributions}
        """
        all_users = []

        for file_id in self.file_revs:
            for user in self.list_revisions_user(file_id):
                all_users.append(user[0])

        all_users_contribution = {}
        for user in all_users:
            if user not in all_users_contribution:
                all_users_contribution[user] = 1
            else:
                all_users_contribution[user] += 1

        return all_users_contribution

    def calculate_contribution_percentage(self):
        """
        Return percentage of contributions for each member of team drive 
        @:return contribution_percentage: (dict) {key:(string) user, value: (int) contributions_percentage}
        """

        all_users_contribution = self.calculate_contribution()

        total_contributions_by_all = sum(all_users_contribution.values())

        contribution_percentage = {}
        for user in all_users_contribution:
            contribution_percentage[user] = round(all_users_contribution[
                user] / total_contributions_by_all * 100, 2)

        return contribution_percentage

    def _process_date(self, date):
        """
        Process RFC 3339-date-time to "YYYYweekWW" format
        @:return str(year) + "week" + str(week): (string) A string containing year and week 
        """

        # Getting the date yy-mm-dd
        date = date.split('T')[0]
        date = date.replace('-', ' ')
        date = time.strptime(date, '%Y %m %d')
        # Get year
        year = time.strftime('%Y', date)
        # Get week
        week = time.strftime('%W', date)

        return str(year) + "week" + str(week)

    def calculate_contribution_with_week(self):
        """
        Return number of contributions for each member of team drive at particular duration
        @:return all_users_contribution: (dict) {UserName1(String): 
        {whichWeek(String):numberOfVersionContributed(int),...}}
        """
        all_users = []

        for file_id in self.file_revs:
            all_users = all_users + self.list_revisions_user(file_id)

        for i in range(len(all_users)):
            # convert modifiedTime into "YYYYweekWW"
            all_users[i] = (all_users[i][0],
                            self._process_date(all_users[i][1]))

        # all_users: [(userA, YYYYweekWW), (userB, YYYYweekWW),...]
        # all_user_contribution = {UserName1(String):
        # {whichWeek(String):numberOfVersionContributed(int),...}}
        all_users_contribution = {}
        for user in all_users:
            # Add user in the all_users_contribution if not found in the dict
            if user[0] not in all_users_contribution:
                all_users_contribution[user[0]] = {}
                all_users_contribution[user[0]][user[1]] = 1
            else:
                # Add the week into the user contribution if not found
                if user[1] not in all_users_contribution[user[0]]:
                    all_users_contribution[user[0]][user[1]] = 1
                else:
                    # Increment user contribution count for corresponding week
                    all_users_contribution[user[0]][user[1]] += 1

        return all_users_contribution

    """
    A function to test the usability/whatev of list_revision_user function, DEV build only
    """

    def print_revisions_user(self, file_id):
        user_list = self.list_revisions_user(file_id)
        if user_list is []:
            print("[ERROR] file_id not found in given array")
            return
        try:
            print("[%s] FILENAME: %s " %
                  (file_id, self.get_file_name(file_id)))
        except KeyError:
            print("[%s] FILENAME unavailable, might be a gdoc" % file_id)
            pass
        for user in user_list:
            print("[%s] %s " % (file_id, user))
