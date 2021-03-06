"""
@author: Samuel, Tiong
@since: 25/8/2018
@modified: 28/9/2018

"""

import time


class D_Parser:

    def __init__(self, files_revisions):
        """
        @:files_revisions: (dict) A dict containing files' id and
        their corresponding list of Revision resources
        """
        self.file_revs = files_revisions

    def _get_revisions_by_id(self, file_id):
        # except KeyError on caller
        return self.file_revs[file_id]

    def list_revisions_user(self, file_id):
        """
        Return the files' modifying users and modifiedTime in list of tuple
        @:return userlist: (list) [ (userA, modifiedTime), (userA, modifiedTime), (userB, modifiedTime)... ]

        """
        try:
            userlist = []
            file_revs = self._get_revisions_by_id(file_id)
            for rev in file_revs:
                userlist.append(
                    (rev['lastModifyingUser']['displayName'], rev['modifiedTime']))
            return userlist
        except KeyError:
            return []

    def calculate_total_contribution(self):
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

    def calculate_total_contribution_percentage(self):
        """
        Return percentage of contributions for each member of team drive
        @:return contribution_percentage: (dict) {key:(string) user, value: (int) contributions_percentage}
        """

        all_users_contribution = self.calculate_total_contribution()

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

    def calculate_contribution_with_week(self, file_id=None):
        """
        Return users_list and number of contributions for each member of team drive at particular duration
        @:file_id: (String) The file ID
        @:return all_users_contribution: (tuple) (users_list(set),
                    {whichWeek1(String):
                        {UserName1(String):numberOfVersionContributed(int),
                        UserName2(String):numberOfVersionContributed(int)...}}
        """
        all_users = []
        if file_id == None:
            for file_id in self.file_revs:
                all_users = all_users + self.list_revisions_user(file_id)
        else:
            all_users = self.list_revisions_user(file_id)

        for i in range(len(all_users)):
            # convert modifiedTime into "YYYYweekWW"
            all_users[i] = (all_users[i][0],
                            self._process_date(all_users[i][1]))

        # all_users: [(userA, YYYYweekWW), (userB, YYYYweekWW),...]
        # all_user_contribution = {whichWeek1(String):
        # {UserName1(String):numberOfVersionContributed(int),...}}
        all_users_contribution = {}
        # Keep track of users in every week
        users_list = set()
        for user in all_users:
            # Add whichWeek into the all_users_contribution if not found in the
            # dict
            if user[1] not in all_users_contribution:
                all_users_contribution[user[1]] = {}
                all_users_contribution[user[1]][user[0]] = 1
            else:
                # Add the userName into the user week contribution if not found
                if user[0] not in all_users_contribution[user[1]]:
                    all_users_contribution[user[1]][user[0]] = 1
                else:
                    # Increment user contribution count for corresponding week
                    all_users_contribution[user[1]][user[0]] += 1

            users_list.add(user[0])

        # Add in user with zero contribution into each week
        for week in all_users_contribution:
            if not all(user in all_users_contribution[week] for user in users_list):
                # Perform set operation to find ) contribution users
                missing_user = users_list - all_users_contribution[week].keys()
                for i in missing_user:
                    all_users_contribution[week][i] = 0

        # Sort userName in each week in all_users_contribution
        for week in all_users_contribution:
            temp = {}
            for key in sorted(all_users_contribution[week]):
                temp[key] = all_users_contribution[week][key]
            all_users_contribution[week] = temp

        # Convert users_list from set into list
        users_list = list(users_list)
        # Sort the userName
        users_list.sort()

        return (users_list, all_users_contribution)

    def calculate_file_contribution(self, file_id):
        """
        Return number of contributions for each member for the file specified by file_id
        @:return all_users_contribution: (dict) {key:(string) user, value: (int) number_of_contributions}
        """
        all_users = []

        for file_revision in self.file_revs[file_id]:

            all_users.append(file_revision['lastModifyingUser']['displayName'])

        all_users_contribution = {}
        for user in all_users:
            if user not in all_users_contribution:
                all_users_contribution[user] = 1
            else:
                all_users_contribution[user] += 1

        return all_users_contribution

    def calculate_file_contribution_percentage(self, file_id):
        """
        Return percentage of contributions for each member for the file
        @:return contribution_percentage: (dict) {key:(string) user, value: (int) contributions_percentage}
        """

        file_contribution = self.calculate_file_contribution(file_id)

        total_file_contributions_by_all = sum(file_contribution.values())

        contribution_percentage = {}
        for user in file_contribution:
            contribution_percentage[user] = round(file_contribution[
                user] / total_file_contributions_by_all * 100, 2)

        return contribution_percentage

    def calculate_total_contribution_within_timeframe(self, time1, time2):
        """
        Return number of contributions for each member for the drive within timeframe
        @:time1: (string) Lower bound for the time frame (included)
        @:time2: (string) Upper bound for the time frame (included)
        @:return all_users_contribution: (dict) {key:(string) user, value: (int) number_of_contributions}
        """

        # [ (userA, modifiedTime), (userA, modifiedTime), (userB, modifiedTime),... ]
        all_users = []

        for file_id in self.file_revs:
            for user in self.list_revisions_user(file_id):
                # Check if the modifiedTime is withink timeframe, if yes,
                # append into all_users list
                if (time1 <= user[1] <= time2):
                    all_users.append(user[0])

        all_users_contribution = {}
        for user in all_users:
            if user not in all_users_contribution:
                all_users_contribution[user] = 1
            else:
                all_users_contribution[user] += 1

        return all_users_contribution

    def calculate_total_contribution_within_timeframe_percentage(self, time1, time2):
        """
        Return percentage of contributions for each member for the drive within timeframe
        @:return contribution_percentage: (dict) {key:(string) user, value: (int) contributions_percentage}
        """

        contribution_within_timeframe = self.calculate_total_contribution_within_timeframe(
            time1, time2)

        total_contributions_by_all = sum(
            contribution_within_timeframe.values())

        contribution_percentage = {}
        for user in contribution_within_timeframe:
            contribution_percentage[user] = round(contribution_within_timeframe[
                user] / total_contributions_by_all * 100, 2)

        return contribution_percentage
