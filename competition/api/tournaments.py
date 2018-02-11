import requests
from datetime import date

from competition.api import authorized_session


class ApiTournamentEntity(object):
    def __init__(self, response):
        """
        :param int response:
        """
        self._response = response

    def id(self):
        """
        An unique identifier for this tournament.
        :rtype int: 
        """
        return self._response.__dict__.get('id', '')

    def discipline(self):
        """
        This string is a unique identifier of a discipline.
        :rtype str:
        """
        return self._response.__dict__.get('discipline', '')

    def name(self):
        """
        Name of a tournament (maximum 30 characeters).
        :rtype str:
        """
        return self._response.__dict__.get('name', '')

    def full_name(self):
        """
        Complete name of this tournament (maximum 80 characters).
        :rtype str|None:
        """
        return self._response.__dict__.get('full_name', None)

    def status(self):
        """
        Status of the tournament.
        Possible values: setup, running, completed
        :rtype str:
        """
        return self._response.__dict__.get('status', '')

    def date_start(self):
        """
        Starting date of the tournament
        :rtype date|None:
        """
        return self._response.__dict__.get('date_start', None)

    def date_end(self):
        """
        Ending date of the tournament
        :rtype date|None:
        """
        return self._response.__dict__.get('date_end', None)

    def timezone(self):
        """
        Time zone of the tournament.
        :rtype str:
        """
        return self._response.__dict__.get('timezone', None)

    def online(self):
        """
        Whether the tournament is played on internet or not.
        :rtype bool:
        """
        return self._response.__dict__.get('online', True)

    def public(self):
        """
        Whether the tournament is public or private.
        :rtype bool:
        """
        return self._response.__dict__.get('public', True)

    def location(self):
        """
        Location (city, address, place of interest) of the tournament.
        :rtype str|None:
        """
        return self._response.__dict__.get('location', None)

    def country(self):
        """
        Country of the tournament. This value uses the ISO 3166-1 alpha-2 country code.
        :rtype str|None:
        """
        return self._response.__dict__.get('country', None)

    def size(self):
        """
        Size of a tournament.
        :rtype int:
        """
        return int(self._response.__dict__.get('size', 0))

    def participant_type(self):
        """
        Type of participants who plays in the tournament.
        Possible values: team, single
        :rtype str:
        """
        return self._response.__dict__.get('participant_type', '')

    def match_type(self):
        """
        Type of matches played in the tournament.
        Possible values: duel, ffa
        :rtype str:
        """
        return self._response.__dict__.get('match_type', '')

    def organization(self):
        """
        Tournament organizer: individual, group, association or company.
        :rtype str|None:
        """
        return self._response.__dict__.get('organization', None)

    def website(self):
        """
        URL of website.
        :rtype str|None:
        """
        return self._response.__dict__.get('website', None)

    def description(self):
        """
        User-defined description of the tournament (maximum 1,500 characters).
        :rtype str|None:
        """
        return self._response.__dict__.get('description', None)

    def rules(self):
        """
        User-defined rules of the tournament (maximum 10,000 characters).
        :rtype str|None:
        """
        return self._response.__dict__.get('rules', None)

    def prize(self):
        """
        User-defined description of the tournament prizes (maximum 1,500 characters).
        :rtype str|None:
        """
        return self._response.__dict__.get('prize', None)

    def team_size_min(self):
        """
        The smallest possible team size.
        :rtype int:
        """
        return int(self._response.__dict__.get('team_size_min', 0))

    def team_size_max(self):
        """
        The largest possible team size.
        :rtype int:
        """
        return int(self._response.__dict__.get('team_size_max', 0))

    def match_format(self):
        """
        Define the default match format for every matches in the tournament.
        Possible values: none, one, home_away, bo3, bo5, bo7, bo9, bo11
        :rtype str|None:
        """
        return self._response.__dict__.get('match_format', None)

    def platforms(self):
        """
        Define the list of platforms used for the tournament.
        Possible values: pc, playstation4, xbox_one, nintendo_switch, mobile, playstation3, playstation2, playstation1,
        ps_vita, psp, xbox360, xbox, wii_u, wii, gamecube, nintendo64, snes, nes, dreamcast, saturn, megadrive,
        master_system, 3ds, ds, game_boy, neo_geo, other_platform, not_video_game
        :rtype List[str]:
        """
        return list(self._response.__dict__.get('platforms', []))
