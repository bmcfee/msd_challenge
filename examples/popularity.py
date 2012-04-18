#!/usr/bin/env python
'''
CREATED:2012-04-18 16:18:27 by Brian McFee <bmcfee@cs.ucsd.edu>

Example recommendation script, following the instructions in our "Getting Started" guide.

This script performs recommendation by raw popularity of items.

'''


# Step 1: load the triplets and compute song counts

with open('kaggle_visible_evaluation_triplets.txt', 'r') as f:
    song_to_count = dict() 
    for line in f:
        _, song, _ = line.strip().split('\t') 
        if song in song_to_count: 
            song_to_count[song] += 1 
        else: 
            song_to_count[song] = 1 
            pass
        pass
    pass


# Step 2: sort by popularity

songs_ordered = sorted( song_to_count.keys(), 
                        key=lambda s: song_to_count[s],
                        reverse=True)


# Step 3: load the user histories

with open('kaggle_visible_evaluation_triplets.txt', 'r') as f:
    user_to_songs = dict() 
    for line in f:
        user, song, _ = line.strip().split('\t') 
        if user in user_to_songs: 
            user_to_songs[user].add(song) 
        else: 
            user_to_songs[user] = set([song])
            pass
        pass
    pass


# Step 4: load the user ordering

with open('kaggle_users.txt', 'r') as f:
    canonical_users = map(lambda line: line.strip(), f.readlines()) 
    pass


# Step 5: load the song ordering

with open('kaggle_songs.txt', 'r') as f:
    song_to_index = dict(map(lambda line: line.strip().split(' '), f.readlines())) 
    pass


# Step 6: generate the prediction file
with open('submission_getting_started.txt', 'w') as f:
    for user in canonical_users:
        songs_to_recommend  = [] 

        for song in songs_ordered: 
            if len(songs_to_recommend) >= 500: 
                break 
            if not song in user_to_songs[user]: 
                songs_to_recommend.append(song) 
                pass
        
        # Transform song IDs to song indexes 
        indices = map(lambda s: song_to_index[s], songs_to_recommend) 
        
        # Write line for that user 
        f.write(' '.join(indices) + '\n') 
        pass
    pass

# And we're done!
