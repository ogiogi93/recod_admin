import random


class GenerateTournament(object):
    """
    トーナメントを生成する
    """
    def __init__(self, teams):
        """
        指定されてチームでトーナメント表を生成する
        :param List[int] teams:
        """
        self.teams = teams
        self.team_num = len(teams)
        self.round_num = None

    def calculate_round_num(self, round_num=0):
        """
        ラウンド数(何回戦か)を返す
        :param int round_num:
        :rtype int:
        """
        if not self.round_num:
            team_num = self.team_num
            while team_num > 2:
                team_num /= 2
                round_num += 1
            self.round_num = round_num
        return self.round_num

    def single_illumination(self):
        """
        シングルイルミネーション形式でトーナメント表を生成する
        :rtype dict{round: List[int]}:
        """
        if not self.round_num:
            self.calculate_round_num()

        teams = self.teams
        round_matches = {}
        for r in range(self.round_num):
            if r == 0:
                # 初戦は参加チーム数からマッチ数を算出する
                round_match_num = int(len(teams) / 2)
            else:
                # 2会戦以降は前戦数からマッチ数を算出する　
                round_match_num = int(len(round_matches[r - 1]) / 2)
            matches = []
            for n in range(round_match_num):
                if not teams:
                    match = [None, None]
                elif len(teams) >= 2:
                    match = random.sample(teams, 2)
                elif len(teams) == 1 and r != 0:
                    # 参加チームが奇数で溢れた場合は次戦で登録
                    match = [teams[0], None]
                    teams = []
                matches.append(match)
                #  選択されたチームを除く
                teams = [t for t in teams if t not in match]
            round_matches[r] = matches
        return round_matches
