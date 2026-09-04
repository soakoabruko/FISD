#!/usr/bin/env python3

class Playlist:
    def __init__(self, title: str) -> None:
        self.title = title
        # Из ТЗ непонятно, какую структуру данных надо или можно использовать:
        # список или любую другую структуру данных Python.
        # Я использую словарь, потому что он позволяет удалять песню
        # из плейлиста за O(1) в среднем.
        self._songs: dict[str, int] = {}

    def add_song(self, title: str, duration_sec: int) -> None:
        self._songs[title] = duration_sec

    def remove_song(self, title: str) -> None:
        if self._songs.get(title) is not None:
            del self._songs[title]

    def get_total_duration_sec(self) -> int:
        if self._songs:
            return sum(self._songs.values())

    def __len__(self) -> int:
        return len(self._songs)

    def print_playlist(self) -> None:
        if self._songs:
            print(self.title)

            for song in self._songs.items():
                print(f"{song[0]} {song[1] // 60}:{song[1] % 60}")
        else:
            print(f"Плейлист «{self.title}» пуст")


def main() -> None:
    playlist = Playlist("Gorillaz")

    playlist.add_song("Feel Good Inc.", 255)
    playlist.add_song("Rhinestone Eyes", 200)

    print(playlist.get_total_duration_sec())
    print(len(playlist))

    playlist.print_playlist()

    playlist.remove_song("Feel Good Inc.")
    playlist.remove_song("19-2000")
    playlist.remove_song("RhineStone Eyes")


if __name__ == "__main__":
    main()