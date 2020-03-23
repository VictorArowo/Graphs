import random


class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)


class User:
    def __init__(self, name):
        self.name = name


class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
            return False
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
            return False
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)
            return True

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}

        # Add users
        for i in range(num_users):
            self.add_user(f"user_{i}")

        # O(N^2)

        # Create friendships
        # friendships = []
        # for user in self.users:
        #     for friend in range(user + 1, self.last_id + 1):
        #         friendships.append((user, friend))

        # random.shuffle(friendships)

        # for i in range(num_users * avg_friendships // 2):
        #     self.add_friendship(friendships[i][0], friendships[i][1])

        # O(N)
        friendship_count = num_users * avg_friendships

        while friendship_count != 0:
            user = random.randint(1, num_users)
            friend = random.randint(1, num_users)

            if self.add_friendship(user, friend):
                friendship_count -= 2

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        queue = Queue()
        queue.enqueue([user_id])
        visited = {}

        while queue.size() > 0:
            path = queue.dequeue()

            current_friend = path[-1]

            if current_friend not in visited:
                visited[current_friend] = path
                for friend in self.friendships[current_friend]:
                    copy = path.copy()
                    copy.append(friend)
                    queue.enqueue(copy)

        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2)
    print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    print(connections)
