from code import*

play=MagicTowerGame()
pygame.mixer.init()
pygame.mixer.music.load(r".\resources\music\no1.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play()
play.run()