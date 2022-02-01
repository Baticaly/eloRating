import csv

PLAYERS = 'players.csv'
GAMES = 'games.csv'
RESULT = 'result.csv'

def scoreUpdate(player1, player2):
    k = 32
    player1expectedScore = 1 / ( 1 + 10**( (player2 - player1) / 400 ) )
    player1update = player1 + ( k*( 1 - player1expectedScore ) )
    player2expectedScore = 1 / ( 1 + 10**( (player1 - player2) / 400 ) )
    player2update = player2 + ( k*( 0 - player2expectedScore ) )
    return round(player1update), round(player2update)

def drawScoreUpdate(player1, player2):
    k = 32
    player1expectedScore = 1 / ( .5 + 10**( (player2 - player1) / 400 ) )
    player1update = player1 + ( k*( 1 - player1expectedScore ) )
    player2expectedScore = 1 / ( .5 + 10**( (player1 - player2) / 400 ) )
    player2update = player2 + ( k*( 0 - player2expectedScore ) )
    return round(player1update), round(player2update)

def getElo(player, playerList):
    for i in range(len(playerList)):
        if playerList[i][0] == player:
            return int(playerList[i][1])

def sortbyElo(playerList):
    def getElo(playerListItem):
        return int(playerListItem[1])

    playerList.sort(key= getElo, reverse=True)
    return playerList

def updateElo(player, elo, playerList):
    playerIndex = len(playerList) + 1
    for i in range(len(playerList)):
        if playerList[i][0] == player:
            playerIndex = i

    playerList.pop(playerIndex)
    playerList.append([player, elo])
    playerList = sortbyElo(playerList)
    return playerList

def saveCSV(playerList, path):
    try:
        with open(path, 'w', newline='') as result:
            writer = csv.writer(result, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            for player in playerList:
                writer.writerow(player)
    except OSError as e:
        print(e)

def Main():

    # playerList Formating
    playerList = []
    try:
        with open(PLAYERS, newline='') as players:
            for p in csv.reader(players, delimiter=','):
                if p[0] != 'PLAYER':
                    playerList.append(p)

    except OSError as e:
        print(e)

    # gameList Formating
    gameList = []
    try:
        with open(GAMES, newline='') as games:
            for g in csv.reader(games, delimiter=','):
                if g[0] != 'PLAYER 1':
                    gameList.append(g)

    except OSError as e:
        print(e)

    # Analyze all games
    for g in gameList:
        player1, player2, result = g

        # Search for player elo
        elo1 = getElo(player1, playerList)
        elo2 = getElo(player2, playerList)

        # Create a player listing with a default value of 1500 if not exists
        if isinstance(elo1, int) != True:
            print(f'\nNew player: {player1}')
            playerList.append([player1, '1500'])
            elo1 = 1500
        elif isinstance(elo2, int) != True:
            print(f'\nNew player: {player2}')
            playerList.append([player2, '1500'])
            elo2 = 1500

        # Player 1 won
        if result[0] == '1':
            print(f'\n{player1}({elo1}) won against {player2}({elo2})')
            elo1, elo2 = scoreUpdate(elo1, elo2)
            print(f'Update: {player1}({elo1}), {player2}({elo2})')
            playerList = updateElo(player1, elo1, playerList)
            playerList = updateElo(player2, elo2, playerList)

        # Player 2 won
        elif result[2] == '1':
            print(f'\n{player2}({elo2}) won against {player1}({elo1})')
            elo2, elo1 = scoreUpdate(elo2, elo1)
            print(f'Update: {player2}({elo2}), {player1}({elo1})')
            playerList = updateElo(player1, elo1, playerList)
            playerList = updateElo(player2, elo2, playerList)

        # Draw
        else:
            print(f'\nDraw between {player1}({elo1}), {player2}({elo2})')
            elo1, elo2 = drawScoreUpdate(elo1, elo2)
            print(f'Update: {player2}({elo2}), {player1}({elo1})')
            playerList = updateElo(player1, elo1, playerList)
            playerList = updateElo(player2, elo2, playerList)

    # Save final scores as .csv
    saveCSV(playerList, RESULT)

    print('\n')
    for player in playerList:
        print(f'{player[0]} - {player[1]}')

if __name__ == '__main__':
    Main()