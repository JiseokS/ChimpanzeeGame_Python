import psycopg2

conn = psycopg2.connect(
    database="your_database",
    user="your_user",
    password="your_password",
    host="your_host",
    port="your_port"
)
cur = conn.cursor()


def save_score(name, score):
    cur.execute("INSERT INTO scores (name, score) VALUES (%s, %s)", (name, score))
    conn.commit()

def get_leaderboard():
    cur.execute("SELECT name, score FROM scores ORDER BY score DESC")
    leaderboard = cur.fetchall()
    return leaderboard


def game_over():
    global running, name, curr_level
    
    
    save_score(name, curr_level)

    
    leaderboard = get_leaderboard()

    
    print("Leaderboard:")
    for rank, (player_name, player_score) in enumerate(leaderboard, start=1):
        print(f"{rank}. {player_name}: {player_score}")

    running = False  


# Close database connection
cur.close()
conn.close()
pygame.quit