def contribution_streaks(days, today):
    """Retorna as sequências atual e máxima para dias em ordem cronológica.

    Um dia de hoje sem contribuição ainda não encerra a sequência de ontem.
    """
    best = run = streak_before_today = 0
    for day in days:
        if day["date"] == today:
            streak_before_today = run
        run = run + 1 if day["contributionCount"] else 0
        best = max(best, run)

    if days and days[-1]["date"] == today and not days[-1]["contributionCount"]:
        return streak_before_today, best
    return run, best
