def trade_value(player, rd_weight=0.5):
    return player.glicko_rating - rd_weight * player.glicko_rd

def team_value(players):
    return sum(trade_value(p) for p in players)

def evaluate_trade(team1_players, team2_players):
    team1_val = team_value(team1_players)
    team2_val = team_value(team2_players)

    diff = team1_val - team2_val
    if abs(diff) < 25:
        verdict = "Fair"
    elif abs(diff) > 75:
        verdict = "Slight Edge"
    else:
        verdict = "Unbalanced"
    return{
        "team1_value": team1_val,
        "team2_value": team2_val,
        "difference": diff,
        "verdict": verdict,
    }