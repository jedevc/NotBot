import utilities as ut
import dumper

class GroupManager(dumper.Dumper):
    def __init__(self, dumpfile):
        super().__init__(dumpfile)

        self.groups = dict()

    def get_groups(self):
        """
        get_groups() -> List

        Get a list of all the groups.
        """

        return [g for g in self.groups]

    def get_users(self, group):
        """
        get_users(g) -> List

        Get all the users who are in a certain group.
        """

        if group in self.groups:
            return self.groups[group]
        else:
            return []

    def get_filtered_users(self, group):
        """
        get_filtered_users(group) -> List

        Get the filtered list of users in a certain group.
        """

        return [ut.filter_nick(u) for u in self.get_users(group)]

    def add_to_group(self, user, group):
        """
        add_to_group(user, group) -> None

        Add a user to a group.
        """

        if group not in self.groups:
            self.groups[group] = []

        filtered_group = [ut.filter_nick(u) for u in self.groups[group]]
        if ut.filter_nick(user) in filtered_group:
            #Already in group
            return "%s is already in group %s." % ("@" + user, "*" + group)
        else:
            #Add that person to the group
            self.groups[group].append(user)
            return "Added %s to group %s." % ("@" + user, "*" + group)

    def remove_from_group(self, user, group):
        """
        remove_from_group(user, group) -> None

        Remove a user from the group.
        """

        if group not in self.groups:
            self.groups[group] = []

        filtered_group = [ut.filter_nick(u) for u in self.groups[group]]
        if ut.filter_nick(user) not in filtered_group:
            #Person is not in group
            return "%s is not in group %s." % ("@" + user, "*" + group)
        else:
            #Remove from group
            self.groups[group].pop(filtered_group.index(ut.filter_nick(user)))
            if len(self.groups[group]) == 0:
                self.groups.pop(group)

            return "%s has been removed from group %s." % ("@" + user, "*" + group)

    def dump_groups(self):
        self.dump(self.groups)

    def recover_groups(self):
        self.groups = self.recover()
        if self.groups is None:
            self.groups = dict()
