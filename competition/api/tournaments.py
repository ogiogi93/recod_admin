import json

from competition.infrastructure.tournament import Tournament
from competition.api import authorized_session
from recod_admin import logging

TOORNAMENT_API_TOURNAMENT_URL = 'https://api.toornament.com/v1/tournaments'
TOORNAMENT_API_PARTICIPATE_URL = 'https://api.toornament.com/v1/tournaments/{}/participants'

logger = logging.getLogger(__name__)


class ApiTournamentEntity(object):
    def __init__(self, response):
        """
        :param dict response:
        """
        self._response = response

    def id(self):
        """
        An unique identifier for this tournament.
        :rtype int:
        """
        return self._response.get('id', '')

    def discipline(self):
        """
        This string is a unique identifier of a discipline.
        :rtype str:
        """
        return self._response.get('discipline', '')

    def name(self):
        """
        Name of a tournament (maximum 30 characeters).
        :rtype str:
        """
        return self._response.get('name', '')

    def full_name(self):
        """
        Complete name of this tournament (maximum 80 characters).
        :rtype str|None:
        """
        return self._response.get('full_name', None)

    def status(self):
        """
        Status of the tournament.
        Possible values: setup, running, completed
        :rtype str:
        """
        return self._response.get('status', '')

    def date_start(self):
        """
        Starting date of the tournament
        :rtype date|None:
        """
        return self._response.get('date_start', None)

    def date_end(self):
        """
        Ending date of the tournament
        :rtype date|None:
        """
        return self._response.get('date_end', None)

    def timezone(self):
        """
        Time zone of the tournament.
        :rtype str:
        """
        return self._response.get('timezone', None)

    def online(self):
        """
        Whether the tournament is played on internet or not.
        :rtype bool:
        """
        return self._response.get('online', True)

    def public(self):
        """
        Whether the tournament is public or private.
        :rtype bool:
        """
        return self._response.get('public', True)

    def location(self):
        """
        Location (city, address, place of interest) of the tournament.
        :rtype str|None:
        """
        return self._response.get('location', None)

    def country(self):
        """
        Country of the tournament. This value uses the ISO 3166-1 alpha-2 country code.
        :rtype str|None:
        """
        return self._response.get('country', None)

    def size(self):
        """
        Size of a tournament.
        :rtype int:
        """
        return int(self._response.get('size', 0))

    def participant_type(self):
        """
        Type of participants who plays in the tournament.
        Possible values: team, single
        :rtype str:
        """
        return self._response.get('participant_type', '')

    def match_type(self):
        """
        Type of matches played in the tournament.
        Possible values: duel, ffa
        :rtype str:
        """
        return self._response.get('match_type', '')

    def organization(self):
        """
        Tournament organizer: individual, group, association or company.
        :rtype str|None:
        """
        return self._response.get('organization', None)

    def website(self):
        """
        URL of website.
        :rtype str|None:
        """
        return self._response.get('website', None)

    def description(self):
        """
        User-defined description of the tournament (maximum 1,500 characters).
        :rtype str|None:
        """
        return self._response.get('description', None)

    def rules(self):
        """
        User-defined rules of the tournament (maximum 10,000 characters).
        :rtype str|None:
        """
        return self._response.get('rules', None)

    def prize(self):
        """
        User-defined description of the tournament prizes (maximum 1,500 characters).
        :rtype str|None:
        """
        return self._response.get('prize', None)

    def team_size_min(self):
        """
        The smallest possible team size.
        :rtype int:
        """
        return int(self._response.get('team_size_min', 0))

    def team_size_max(self):
        """
        The largest possible team size.
        :rtype int:
        """
        return int(self._response.get('team_size_max', 0))

    def match_format(self):
        """
        Define the default match format for every matches in the tournament.
        Possible values: none, one, home_away, bo3, bo5, bo7, bo9, bo11
        :rtype str|None:
        """
        return self._response.get('match_format', None)

    def platforms(self):
        """
        Define the list of platforms used for the tournament.
        Possible values: pc, playstation4, xbox_one, nintendo_switch, mobile, playstation3, playstation2, playstation1,
        ps_vita, psp, xbox360, xbox, wii_u, wii, gamecube, nintendo64, snes, nes, dreamcast, saturn, megadrive,
        master_system, 3ds, ds, game_boy, neo_geo, other_platform, not_video_game
        :rtype List[str]:
        """
        return list(self._response.get('platforms', []))


def upsert_api_tournament(t, api_tournament_id=None):
    """
    Toornament APIにトーナメントを登録・更新する
    DB用にapi_tournament_idを返す
    :param Tournament t:
    :param int api_tournament_id:
    :rtype int:
    """
    oauth = authorized_session()
    try:
        body = json.dumps({
            'discipline': t.game.discipline.api_discipline_id,
            'name': t.name,
            'size': t.size,
            'participant_type': t.participant_type,
            'full_name': t.full_name,
            'organization': t.organization,
            'website': t.website,
            'date_start': str(t.date_start),
            'date_end': str(t.date_end),
            'time_zone': 'JP',
            'online': t.online,
            'public': t.public,
            'location': t.location,
            'country': t.country,
            'description': t.description,
            'rules': t.rules,
            'prize': t.prize,
            'check_in': True,
            'participant_nationality': True,
            'match_format': t.match_format.name,
            'platforms': [t.game.platform.name]
        })
        if api_tournament_id:
            # api_tournament_idが指定されている場合は更新する
            entity = ApiTournamentEntity(
                response=oauth.patch(url=TOORNAMENT_API_TOURNAMENT_URL + '/{}'.format(api_tournament_id),
                                     data=body).json())
        else:
            entity = ApiTournamentEntity(
                response=oauth.post(url=TOORNAMENT_API_TOURNAMENT_URL, data=body).json())
        logger.info('[upsert_api_tournament] succeeded.'
                    'Tournament ID:{} is created or updated.'.format(entity.id()))
        return entity.id()
    except Exception as e:
        logger.error('[upsert_api_tournament] failed.'
                     ' error_type: {}, error: {}'.format(type(e), e))
    finally:
        oauth.close()


def delete_api_tournament(api_tournament_id):
    """
    Toornament API上のトーナメントを削除する
    :param int api_tournament_id:
    :rtype None:
    """
    oauth = authorized_session()
    try:
        oauth.delete(url=TOORNAMENT_API_TOURNAMENT_URL + '/{}'.format(api_tournament_id))
        logger.info('[delete_api_tournament] succeeded.'
                    'Tournament ID:{} is deleted.'.format(api_tournament_id))
    except Exception as e:
        logger.error('[delete_api_participate] failed.'
                     ' error_type: {}, error: {}'.format(type(e), e))
    finally:
        oauth.close()


class ApiParticipateEntity(object):
    def __init__(self, response):
        self._response = response

    def id(self):
        """
        Unique identifier for this participant.
        :rtype int:
        """
        return int(self._response.get('id', 0))

    def name(self):
        """
        Participant name (maximum 40 characters).
        :rtype str:
        """
        return self._response.get('name', '')

    def lineup(self):
        """
        :rtype List[Dict[str]]:
        """
        return list(self._response.get('lineup', []))


def upsert_api_participate(t, api_tournament_id, api_participate_id=None):
    """
    Toornament API上でトーナメント参加登録または更新する
    DB用にapi_participate_idを返す
    :param Team t:
    :param int api_tournament_id:
    :param int api_participate_id:
    :rtype int:
    """
    oauth = authorized_session()
    try:
        body = json.dumps({
            'name': t.name
        })
        if api_participate_id:
            # api_tournament_idが指定されている場合は更新する
            url = TOORNAMENT_API_PARTICIPATE_URL.format(api_tournament_id) + '/{}'.format(api_participate_id)
            entity = ApiParticipateEntity(
                response=oauth.patch(url=url, data=body).json())
        else:
            url = TOORNAMENT_API_PARTICIPATE_URL.format(api_tournament_id)
            entity = ApiTournamentEntity(
                response=oauth.post(url=url, data=body).json())
        logger.info('[upsert_api_participate] succeeded.'
                    'Participate ID:{} is created or updated.'.format(entity.id()))
        return entity.id()
    except Exception as e:
        logger.error('[upsert_api_participate] failed.'
                     ' error_type: {}, error: {}'.format(type(e), e))
    finally:
        oauth.close()


def refusal_api_participate(api_tournament_id, api_participate_id):
    """
    Toornament API上のトーナメント登録情報を削除する
    :param int api_tournament_id:
    :param int api_participate_id:
    :return None:
    """
    oauth = authorized_session()
    try:
        oauth.delete(url=TOORNAMENT_API_PARTICIPATE_URL.format(api_tournament_id) + '/{}'.format(api_participate_id))
        logger.info('[refusal_api_participate] succeeded.'
                    'Participate ID:{} refusal Tournament ID: {}.'.format(api_participate_id, api_tournament_id))
    except Exception as e:
        logger.error('[refusal_api_participate] failed.'
                     ' error_type: {}, error: {}'.format(type(e), e))
    finally:
        oauth.close()
