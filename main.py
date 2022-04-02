from constants import *
from game.directing.director import Director
from game.directing.scene_manager import SceneManager
from game.services.video_service import VideoService

def main():
    director = Director(VideoService)
    director.start_game()

if __name__ == "__main__":
    main()