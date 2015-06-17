import utilities as ut

class GroupManager:
    def __init__(self, dumpfile):
        self.groups = dict()

        self.filename = dumpfile

    def get_groups(self):
        return [g for g in self.groups]

    def get_users(self, group):
        if group in self.groups:
            return self.groups[group]
        else:
            return []

    def add_to_group(self, user, group):
        """
        add_to_group(user, group) -> None

        Add a user to a group.
        """

        if group not in self.groups:
            self.groups[group] = []

        if ut.filter_nick(user) in self.groups[group]:
            #Already in group
            return "%s is already in group %s." % ("@" + user, "*" + group)
        else:
            #Add that person to the group
            self.groups[group].append(ut.filter_nick(user))
            return "Added %s to group %s." % ("@" + user, "*" + group)

    def remove_from_group(self, user, group):
        """
        remove_from_group(user, group) -> None

        Remove a user from the group.
        """

        if group not in self.groups or ut.filter_nick(user) not in self.groups[group]:
            #Person is not in group
            return "%s is not in group %s." % ("@" + user, "*" + group)
        else:
            #Remove from group
            self.groups[group].remove(ut.filter_nick(user))
            if len(self.groups[group]) == 0:
                self.groups.pop(group)

            return "%s has been removed from group %s." % ("@" + user, "*" + group)

    def dump_groups(self):
        """
        dump_groups() -> None

        Dump all the groups that exist in a file to be read in later.
        """

        with open(self.filename, 'w') as f:
            for group in self.groups:
                f.write(str((group, self.groups[group])) + "\n")

    def recover_groups(self):
        """
        recover_notifications() -> None

        Recover all the groups that you previously dumped in a file
        """

        groups = []
        try:
            with open(self.filename) as f:
                groups = f.read().split('\n')
        except FileNotFoundError:
            return

        for g in groups:
            if len(g) != 0:
                group, people = eval(g)

                for p in people:
                    self.add_to_group(p, group)
