import pygame

def main():
    width = 1980
    height = 1080
    title = "Divitaris Game"

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(title)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((100, 100, 100)) 
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()