import json
import random

class Anime:
    def __init__(self, title, studios, type, episode, popularity, score) -> None:
        self.title = title
        self.studios = studios
        self.type = type
        self.episode = episode
        self.popularity = popularity
        self.score = score
        
    def to_dict(self):
        return {
            'title': self.title,
            'studios': self.studios,
            'type': self.type,
            'episode': self.episode,
            'popularity': self.popularity,
            'score': self.score
        }

class Node:     
    def __init__(self, anime) -> None:
        self.anime = anime
        self.next = None
        self.prev = None

class CircularDoubleLinkedList:
    def __init__(self) -> None:
        self.head = None

    def anime_add(self, anime):
        new_node = Node(anime)
        if not self.head:
            self.head = new_node
            self.head.next = self.head
            self.head.prev = self.head  
        else:
            tail = self.head.prev
            tail.next = new_node
            new_node.prev = tail
            new_node.next = self.head
            self.head.prev = new_node

    def anime_delete(self, title):
        if not self.head:
            print("Daftar anime masih kosong.")
            return False
        current = self.head
        while True:
            if current.anime.title == title:
                current.prev.next = current.next
                current.next.prev = current.prev
                if current == self.head:
                    self.head = current.next
                return True
            current = current.next
            if current == self.head:
                break
            print(f'Anime "{title}" tidak ada di List Lee.')
        return False
    
    def linear_search(self, target_title):
        current = self.head
        while current:
            if current.anime.title.lower() == target_title.lower():
                return current.anime
            current = current.next
            if current == self.head:
                break
        return None
    
    def allanimes(self):
        all_animes = []
        current = self.head
        if not current:
            return all_animes
        while True:
            all_animes.append(current.anime) 
            current = current.next
            if current == self.head:
                break
        return all_animes

    def display_animes(self, animes=None):
        if not animes: 
            animes = self.allanimes()
        if not animes:
            print("Daftar anime masih kosong.")
            return
        for anime in animes:
            print(f"TITLE       : {anime.title}")
            print(f"STUDIOS     : {anime.studios}")
            print(f"TYPE        : {anime.type}")
            print(f"EPISODE     : {anime.episode}")
            print(f"POPULARITY  : {anime.popularity}")
            print(f"SCORE       : {anime.score}")
            print()

class Stack:
    def __init__(self):
        self.stack = []

    def push(self, anime):
        self.stack.append(anime)

    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        print("kosong Leee...")
        return None

    def peek(self):
        if not self.is_empty():
            return self.stack[-1]
        print("kosong Leee...")
        return None

    def is_empty(self):
        return len(self.stack) == 0

    def display_stack(self):
        if self.is_empty():
            print("kosong Leee...")
            return
        for anime in reversed(self.stack):
            print(anime.title)

class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, anime):
        self.queue.append(anime)

    def dequeue(self):
        if not self.is_empty():
            return self.queue.pop(0)
        print("kosong Leee...")
        return None

    def is_empty(self):
        return len(self.queue) == 0

    def display_queue(self):
        if self.is_empty():
            print("kosong Leee...")
            return
        for anime in self.queue:
            print(anime.title)

class myanimelist:
    def __init__(self) -> None:
        self.linked_list = CircularDoubleLinkedList()
        self.recently_watched = Stack()
        self.watchlist = Queue()

    def anime_add(self, anime):
        self.linked_list.anime_add(anime)                  

    def anime_delete(self, anime_title):
        return self.linked_list.anime_delete(anime_title)

    def add_to_watchlist(self, anime):
        self.watchlist.enqueue(anime)

    def remove_from_watchlist(self, title):
        new_queue = Queue()
        found = False
        removed_anime = None 
        while not self.watchlist.is_empty():
            current = self.watchlist.dequeue()
            if current.title == title:
                found = True
                removed_anime = current
            else:
                new_queue.enqueue(current)
        self.watchlist = new_queue
        if found and removed_anime:
            self.recently_watched.push(removed_anime)
        return found

    def display_watchlist(self):
        print("Watchlist:")
        self.watchlist.display_queue() 

    def display_recently_watched(self):
        print("Recently Watched:")
        self.recently_watched.display_stack() 

    def load_from_json(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            self.linked_list = CircularDoubleLinkedList()
            for entry in data:
                self.anime_add(Anime(**entry))
            print("Data anime berhasil dimuat.")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error saat membaca file: {e}")

    def save_to_json(self, file_path):
        data = [anime.to_dict() for anime in self.linked_list.allanimes()]
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
        print("Data anime berhasil disimpan")

    def save_recently_watched_to_json(self, file_path):
        data = [anime.to_dict() for anime in self.recently_watched.stack]
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
        print("Recently Watched berhasil disimpan")

    def load_recently_watched_from_json(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file: 
                data = json.load(file)
            self.recently_watched = Stack()
            for entry in reversed(data):
                self.recently_watched.push(Anime(**entry))
            print("Recently Watched berhasil dimuat.")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error saat memuat Recently Watched: {e}")

    def _quick_sort(self, animes, attribute, low, high):
        while low < high:
            pi = self._partition(animes, attribute, low, high)
            if pi - low < high - pi:
                self._quick_sort(animes, attribute, low, pi - 1)
                low = pi + 1
            else:
                self._quick_sort(animes, attribute, pi + 1, high)
                high = pi - 1

    def _partition(self, animes, attribute, low, high):
        pivot_index = low + (high - low) // 2
        pivot = getattr(animes[pivot_index], attribute)
        
        animes[pivot_index], animes[high] = animes[high], animes[pivot_index]
        
        store_index = low
        for i in range(low, high):
            if getattr(animes[i], attribute) < pivot:
                animes[i], animes[store_index] = animes[store_index], animes[i]
                store_index += 1
        
        animes[store_index], animes[high] = animes[high], animes[store_index]
        return store_index

    def search_anime_by_studios_quick_sort(self, studios):
        animes = self.linked_list.allanimes()
        self._quick_sort(animes, 'studios', 0, len(animes) - 1)
        return [anime for anime in animes if anime.studios.lower() == studios.lower()]

    def search_anime_by_score_quick_sort(self, score):
        animes = self.linked_list.allanimes()
        self._quick_sort(animes, 'score', 0, len(animes) - 1)
        return [anime for anime in animes if anime.score == score]

    def search_anime_by_episode_quick_sort(self, episode):
        animes = self.linked_list.allanimes()
        self._quick_sort(animes, 'episode', 0, len(animes) - 1)
        return [anime for anime in animes if anime.episode == episode]

    def search_anime_by_type_quick_sort(self, type):
        animes = self.linked_list.allanimes()
        self._quick_sort(animes, 'type', 0, len(animes) - 1)
        return [anime for anime in animes if anime.type == type]

def main_menu():
    file_path = r"D:\Project Coding\Python\MLA\New folder\fix_anime_data_v3.json"
    recently_watched_path = r"D:\Project Coding\Python\MLA\New folder\riwayat.json"
    my_anime_list = myanimelist()
    my_anime_list.load_from_json(file_path)
    my_anime_list.load_recently_watched_from_json(recently_watched_path)

    while True:
        print("\n<==========II MYANIMELIST MENU II=========>")
        print("1. Tambah Anime")
        print("2. Hapus Anime")
        print("3. Tampilkan Semua Anime")
        print("4. Tambah ke Watchlist")
        print("5. Tampilkan Watchlist")
        print("6. Hapus Anime dari Watchlist")
        print("7. Tampilkan Recently Watched")
        print("8. Sort by Studios")
        print("9. Sort by Episode")
        print("10. Sort by Score")
        print("11. Sort by Type")
        print("12. Keluar")

        choice = input("Silahkan pilih ya Mina-san! : ")

        if choice == '1':
            title = input("Masukkan judul anime: ")
            studios = input("Masukkan nama studio: ")
            type = input("Masukkan type anime : ")
            episode = int(input("Masukkan jumlah episode: "))
            popularity = int(input("Masukkan jumlah popularitas: "))
            score = float(input("Masukkan rating: "))
            anime = Anime(title, studios, type, episode, popularity, score)   
            my_anime_list.anime_add(anime)
            my_anime_list.save_to_json(file_path)
            print(f"Anime '{title}' berhasil ditambahkan.")

        elif choice == '2':
            title = input("Masukkan judul anime yang ingin dihapus: ")
            if my_anime_list.anime_delete(title):
                my_anime_list.save_to_json(file_path)
                print(f"Anime '{title}' berhasil dihapus.")
            else:
                print(f"Anime '{title}' tidak ditemukan.")

        elif choice == '3':
            print("Daftar Semua Anime:")
            my_anime_list.linked_list.display_animes()

        elif choice == '4':
            title = input("Masukkan judul anime untuk ditambahkan ke Watchlist: ")
            anime = my_anime_list.linked_list.linear_search(title)
            if anime:
                my_anime_list.add_to_watchlist(anime)
                print(f"Anime '{title}' berhasil ditambahkan ke Watchlist.")
            else:
                print(f"Anime '{title}' tidak ditemukan.")

        elif choice == '5':
            my_anime_list.display_watchlist()
 
        elif choice == '6':
            anime = my_anime_list.watchlist.dequeue()
            if anime:
                my_anime_list.recently_watched.push(anime)
                my_anime_list.save_recently_watched_to_json(recently_watched_path)
                print(f"Anime '{anime.title}' berhasil dihapus dari Watchlist.")
            else:
                print("Watchlist kosong Lee..")

        elif choice == '7':
            my_anime_list.load_recently_watched_from_json(recently_watched_path)
            my_anime_list.display_recently_watched() 

        elif choice == '8':
            studio_name = input("Masukkan nama studio : ")
            result = my_anime_list.search_anime_by_studios_quick_sort(studio_name)
            if result:
                print(f"Daftar Anime yang diproduksi oleh studio '{studio_name}':")
                my_anime_list.linked_list.display_animes(result)
            else:
                print(f"Tidak ada anime yang diproduksi oleh studio '{studio_name}'.")

        elif choice == '9':
            episode_count = int(input("Masukkan jumlah episode : "))
            result = my_anime_list.search_anime_by_episode_quick_sort(episode_count)
            if result:
                print(f"Daftar Anime dengan jumlah episode '{episode_count}':")
                my_anime_list.linked_list.display_animes(result)
            else:
                print(f"Tidak ada anime dengan jumlah episode '{episode_count}'.")

        elif choice == '10':
            score = float(input("Masukkan score : "))
            result = my_anime_list.search_anime_by_score_quick_sort(score)
            if result:
                print(f"Daftar Anime dengan rating '{score}':")
                my_anime_list.linked_list.display_animes(result)
            else:
                print(f"Tidak ada anime dengan rating '{score}'.")

        elif choice == '11':
            type_name = input("Masukkan Type Anime (TY/TV Special/OVA/ONA/Movie) : ")
            result = my_anime_list.search_anime_by_type_quick_sort(type_name)
            if result:
                print(f"Daftar Anime dengan Type '{type_name}':")
                my_anime_list.linked_list.display_animes(result)
            else:
                print(f"Tidak ada anime dengan Type '{type_name}'.")

        elif choice == '12':
            print("OTSU!! HAVE A NICE DAY!!")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

main_menu()