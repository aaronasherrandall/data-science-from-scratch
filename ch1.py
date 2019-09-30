## Below is a list of users, each represented by a dict
## the dict contains the user's id (nunber) and a name
## [] is a list; standard array
## {} is a dict; associative array
## () is a tuple
users = [
    { "id":0, "name": "Hero" },
    { "id":1, "name": "Dunn" },
    { "id":2, "name": "Sue" },
    { "id":3, "name": "Chi" },
    { "id":4, "name": "Thor" },
    { "id":5, "name": "Clive" },
    { "id":6, "name": "Hicks" },
    { "id":7, "name": "Devin" },
    { "id":8, "name": "Kate" },
    { "id":9, "name": "Klein" }, 
]

## (0, 1) tuple shows that id0 (Hero) and id1 (Dunn) 
## are friends

friendsip_pairs = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3),
(3, 4), (4, 5), (5, 6), (5, 7), (6, 8), (7, 8), (8, 9)]

## create a dict where the keys are user ids and
## the values are lists of friends

## Initialize the dict with an empty list for each
## user id:
friendships = {user["id"]: [] for user in users}
# loop over the friendship pairs to populate list
for i, j in friendsip_pairs:
    friendships[i].append(j) # add j as a friend of user i
    friendships[j].append(i) # add i as a friend to user j

# find the total number of connections by summing the 
# lengths of all of the friends lists

def number_of_friends(user):
    """How many friends hoes _user_ have?"""
    user_id = user["id"]
    friend_ids = friendships[user_id]
    return len(friend_ids)

total_connections = sum(number_of_friends(user) for user in users)

# then, we divide by the number of users

num_users = len(users)
# 10
avg_connections = total_connections / num_users
# 2.4

# most connected people == people w/ largest # of friends
# sort from most friends to least friends

# Create a list (user_id, number_of_friends)
num_friends_by_id = [(user["id"],
number_of_friends(user))
for user in users]

num_friends_by_id.sort(
# sort the list
    key=lambda id_and_friends:
id_and_friends[1], # by num_friends
    reverse=True)
# largest to smallest

# print(num_friends_by_id)
# this computes the network metric degree centrality
 
# "Data Scientist You May Know" suggestor

def foaf_ids_bad(user):
    return [foaf_id
     for friend_id in friendships[user["id"]]
     for foaf_id in friendships[friend_id]]

# Produce a count of mutual friends
# And exclude people already known to the user:

from collections import Counter

def friends_of_friends(user):
    user_id = user["id"]
    return Counter(
        foaf_id
        for friend_id in friendships[user_id]
        # for each of my friends
        for foaf_id in friendships[friend_id]
        # find their friends
        if foaf_id != user_id # who aren't me
        and foaf_id not in friendships[user_id] 
        # and aren't my friends
    )

print(friends_of_friends(users[3]))
# Counter({0: 2, 5: 1})

# This correctly tells user (id n) that she has
# mutual friends with user or users (id n)
# print(friends_of_friends(users[4]))
# Counter({1: 1, 2: 1, 6: 1, 7: 1})

# users might also enjoy meeting users with similar interests
# "substantitive expertise"
# list of pairs: (user_id, interest):

interests = [ (0, "Hadoop"), (0, "Big Data"), (0, "HBase"), (0, "Java"), (0, "Spark"), (0, "Storm"), (0, "Cassandra"), 
(1, "NoSQL"), (1, "MongoDB"), (1, "Cassandra"), (1, "HBase"), (1, "Postgres"), 
(2, "Python"), (2, "scikit-learn"), (2, "scipy"), (2, "numpy"), (2, "statsmodels"), (2, "pandas"), 
(3, "R"), (3, "Python"), (3, "statistics"), (3, "regression"), (3, "probability"), 
(4, "machine learning"), (4, "regression"), (4, "decision trees"), (4, "libsvm"), 
(5, "Python"), (5, "R"), (5, "Java"), (5, "C + +"), (5, "Haskell"), (5, "programming languages"), 
(6, "statistics"), (6, "probability"), (6, "mathematics"), (6, "theory"), 
(7, "machine learning"), (7, "scikit-learn"), (7, "Mahout"), (7, "neural networks"), 
(8, "neural networks"), (8, "deep learning"), (8, "Big Data"), (8, "artificial intelligence"), 
(9, "Hadoop"), (9, "Java"), (9, "MapReduce"), (9, "Big Data") ]

# Hero (id 0) has no friends in common wth Klein (id 9)
# but they share interests in Java and Big Data

# build a function that finds users with certain interests

def data_scientists_who_like(target_interest):
    """Find the ids of all users who like the target interest"""
    return [user_id
            for user_id, user_interest in interests
            if user_interest == target_interest]

# data_scientists_who_like("Java")
# [0, 5, 9]

# if we have a lot of users and interests
# we are better off building an index from interests to users

from collections import defaultdict

# keys are interests, values are lists of user_ids
# from interests to users
user_ids_by_interest = defaultdict(list)

for user_id, interest in interests:
    user_ids_by_interest[interest].append(user_id)

# user_ids_by_interest["Java"]
# [0, 5, 9]

# another from users to interests
# keys are user_ids, values are lists of interests for
# that user_id
interests_by_user_id = defaultdict(list)

for user_id, interest in interests:
    interests_by_user_id[user_id].append(interest)

# interests_by_user_id[2]
# ['Python', 'scikit-learn', 'scipy', 'numpy', 'statsmodels', 'pandas']

# Now, find who has the most interests in common with a given user
# iterate over the user's interest
# for each interest, iterated over the other users with that interest
# keep count of how many times we see each user

def most_common_interests_with(user_id):
    return Counter(
        interested_user_id
        for interest in interests_by_user_id[user_id]
        for interested_user_id in user_ids_by_interest[interest]
        if interested_user_id != user_id
    )

# most_common_interests_with(0)
# Counter({9: 3, 8: 1, 1: 2, 5: 1})

## Salaries and Experience

# dataset containing each user's salary (in dollars)
# and tenure (in years)

salaries_and_tenures = [( 83000, 8.7), (88000, 8.1), 
                        (48000, 0.7), (76000, 6), 
                        (69000, 6.5), (76000, 7.5),
                        (60000, 2.5), (83000, 10), 
                        (48000, 1.9), (63000, 4.2)]

# insert plotted graph

# look at average salary for each tenure
# keys are years, values are lists of the salaries for each tenure

salary_by_tenure = defaultdict(list)

for salary, tenure in salaries_and_tenures:
    salary_by_tenure[tenure].append(salary)
# salary_by_tenure[8.7]
# [83000]

# keys are years, each value is average salary for that tenure
average_salary_by_tenure = {
    tenure: sum(salaries) / len(salaries) 
    for tenure, salaries in salary_by_tenure.items() 
}

# average_salary_by_tenure
# {8.7: 83000.0,
# 8.1: 88000.0,
# 0.7: 48000.0,
# 6: 76000.0,
# 6.5: 69000.0,
# 7.5: 76000.0,
# 2.5: 60000.0,
# 10: 83000.0,
# 1.9: 48000.0,
# 4.2: 63000.0}

# Not useful, none of the users have the same tenure
# we are just reporting the individual users' salaries

# we need to "bucket" the tenures

def tenure_bucket(tenure):
    if tenure < 2:
        return "less than two"
    elif tenure < 5:
        return "between two and five"
    else:
        return "more than five"

# group together salaries corresponding to each bucket

# keys are tenure bukcets, values are lists of salaries for
# that bucket

salary_by_tenure_bucket = defaultdict(list)

for salary, tenure in salaries_and_tenures: 
    bucket = tenure_bucket(tenure)
    salary_by_tenure_bucket[bucket].append(salary)

# salary_by_tenure[8.7]
# [83000]

# compute the average salary for each group

# keys are tenure buckets, values are average salary
# for that bucket

average_salary_by_bucket = {
    tenure_bucket: sum(salaries) / len(salaries)
    for tenure_bucket, salaries in salary_by_tenure_bucket.items() 
}

# average_salary_by_bucket
# {'more than five': 79166.66666666667,
# 'less than two': 48000.0,
# 'between two and five': 61500.0}


# 0.7 paid 
# 1.9 unpaid 
# 2.5 paid 
# 4.2 unpaid 
# 6.0 unpaid 
# 6.5 unpaid 
# 7.5 unpaid 
# 8.1 unpaid 
# 8.7 paid 
# 10.0 paid

def predict_paid_or_unpaid(years_experience):
    if years_experience < 3.0:
        return "paid"
    elif years_experience < 8.5:
        return "unpaid"
    else:
        return "paid"

# find most popular interests amoung users
# 1. lowercase each interest (user input may vary)
# 2. split it into words
# 3. cound the results

words_and_counts = Counter(word 
    for user, interest in interests
    for word in interest.lower().split())

for word, count in words_and_counts.most_common():
        if count > 1:
            print(word, count)








