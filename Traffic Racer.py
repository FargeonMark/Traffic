import pygame
import random
import mysql.connector
import datetime

score_added = False
def AddMYSQL(score):
    # Create a connection to the MySQL server
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='85697456',
        database='TrafficRacer'
    )
    
    # Create a cursor object
    cursor = connection.cursor()

    try:
        # Create the 'TrafficRacer' database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS TrafficRacer")

        # Switch to the 'TrafficRacer' database
        cursor.execute("USE TrafficRacer")

        # Create the 'Score' table if it doesn't exist
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS Score (Score VARCHAR(500),\
            TimeOfPlay Varchar(30), DateOfPlay Varchar(30))")

        # Getting current date and time
        current_datetime = datetime.datetime.now()
        time = current_datetime.strftime("%H:%M:%S")
        date = current_datetime.strftime("%d/%m/%Y")

        # Inserting data into the 'Score' table
        cursor.execute("INSERT INTO Score (Score, TimeOfPlay, DateOfPlay) VALUES (%s, %s, %s)", (score, time, date))
        
        # Commit the changes
        connection.commit()
    
    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()


# Initialize Pygame 
icon = pygame.image.load('Images/icon.png')
pygame.init()
pygame.display.set_caption("Traffic Racer")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
gameActive = True
Rectangles = []

# Set up the screen
xaxis = 800
yaxis = 700
screen = pygame.display.set_mode((xaxis, yaxis))

# Load images
RoadSurface = pygame.image.load('Images/road2.png').convert_alpha()
roadRect = RoadSurface.get_rect(center=(400, 350))

RoadSide = pygame.image.load('Images/road_side.jpg').convert()

car = pygame.image.load('Images/car.png').convert_alpha()
carRect = car.get_rect(center=(310, 500))

# Making Rectangels for end screen
font = pygame.font.Font(None, 100)
game_over_text = font.render("Game Over", True, (255, 0, 0))
game_over_rect = game_over_text.get_rect(center=(xaxis // 2, yaxis // 2 - 50))


# Truck
truck = pygame.image.load('Images/truck.png').convert_alpha()
truckRect = truck.get_rect()

# Timer for obstacle spawning
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 500)

# Function to handle obstacle movement
def obstacleMovement(ObstacleList):
    if ObstacleList:
        for i in ObstacleList:
            i.y += 15
            screen.blit(truck, i)
        return ObstacleList
    else:
        return []

# Function to handle collisions
def collisions(player, obstacles):
    for obstacles_rect in obstacles:
        if player.colliderect(obstacles_rect):
            return False  # Collision detected
    return True  # No collisions

# Spacing between trucks
truck_spacing = 375  # Adjust this value as needed

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        # Keyboard movements
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                carRect.centerx -= 183
            elif event.key == pygame.K_d:
                carRect.centerx += 183
        if event.type == obstacle_timer and gameActive:
            random_x = random.choice([310, 493])
            # Calculate random_y for the second truck, taking into account truck height, car height, and spacing
            if Rectangles:
                random_y = Rectangles[-1].y - truck_spacing
            else:
                random_y = random.randint(-truckRect.height - carRect.height, -truckRect.height)

            Rectangles.append(truck.get_rect(center=(random_x, random_y)))

    if gameActive:
        screen.blit(RoadSide, (0, 0))
        screen.blit(RoadSurface, roadRect)
        screen.blit(car, carRect)

        Rectangles = obstacleMovement(Rectangles)

        ticks = int(pygame.time.get_ticks() / 1000)
        score = pygame.font.Font(None, 50).render(f'Score: {ticks}', False, (138, 28, 28))
        scoreRect = score.get_rect(center=(100, 50))
        screen.blit(score, scoreRect)

        pygame.display.update()
        clock.tick(60)  # Reduce the frame rate to 60 FPS for smoother gameplay

        # Collisions
        gameActive = collisions(carRect, Rectangles)
        finalScore = ticks
        
    else:
        if not score_added:
            AddMYSQL(finalScore)
            score_added = True 
        # Display "Game Over" message
        screen.blit(game_over_text, game_over_rect)

        # Display final score
        final_score_text = font.render(f'Final Score: {finalScore}', True, (255, 0, 0))
        final_score_rect = final_score_text.get_rect(center=(xaxis // 2, yaxis // 2 + 50))
        screen.blit(final_score_text, final_score_rect)

        pygame.display.update()
        pygame.time.delay(3000)  # Display "Game Over" for 3 seconds
        pygame.quit()
        quit()
