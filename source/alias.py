import utilities as ut
import dumper

class AliasManager(dumper.Dumper):
    def __init__(self, dumpfile):
        super().__init__(dumpfile)

        self.aliases = dict()

    def get_aliases(self, user):
        """
        get_aliases(user) -> List

        Get all the aliases for a certain user.
        """
        return [a for a in self.aliases if self.aliases[a] == user]

    def exists(self, alias):
        """
        Test if a certain alias exists.
        """

        return (alias in self.aliases)

    def add_alias(self, alias, user):
        """
        add_to_group(alias, user) -> None

        Add an alias for a user.
        """

        if alias in self.aliases:
            return "Alias @%s already exists." % alias
        else:
            self.aliases[alias] = ut.filter_nick(user)
            return "User @%s now has alias @%s." % (user, alias)

    def remove_alias(self, alias):
        """
        remove_alias(alias) -> None

        Remove an alias.
        """

        if ut.filter_nick(alias) in self.aliases:
            self.aliases.remove(ut.filter_nick(alias))
            return "Removed alias @%s." % alias
        else:
            return "The alias does not exist."

    def dump_aliases(self):
        self.dump(self.aliases)

    def recover_aliases(self):
        self.aliases = self.recover()
        if self.aliases is None:
            self.aliases = dict()
