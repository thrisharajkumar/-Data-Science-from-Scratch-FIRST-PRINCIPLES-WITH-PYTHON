# DataSciencester - Example to begin with data science 
# key connectors
# a list of users, each represented by a dict that contains for each user his or her id 
users = [
    { "id": 0, "name": "Hero" },
    { "id": 1, "name": "Dunn" },
    { "id": 2, "name": "Sue" },
    { "id": 3, "name": "Chi" },
    { "id": 4, "name": "Thor" },
    { "id": 5, "name": "Clive" },
    { "id": 6, "name": "Hicks" },
    { "id": 7, "name": "Devin" },
    { "id": 8, "name": "Kate" },
    { "id": 9, "name": "Klein" }
 ]

 friendships = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4),
 (4, 5), (5, 6), (5, 7), (6, 8), (7, 8), (8, 9)]

#Adding a List of friends to each user 
for user in users:
  user["friends"] = []

#Populate the lists using the friendships data:
for i, j in friendships:
  #this works because users[i] is user whose id is i 
  users[i]["friends"].append(users[j]) # add i as a friend of j 
  users[j]["friends"].append(users[i]) # add j as a friend of i 

# Once each user dict contains a list of friends, we can easily ask questions of our 
# graph, like “what’s the average number of connections?”

#  Total number of connections by summing up the lengths 
def number_of_friends(user):
  """how many friends does _user_ have?"""
  retuen len(user["friends"])

total_connections = sum(number_of_friends(user) for user in users) #24
from __future__ import division 
num_users = len(users)
avg_connections = total_connections / num_users #2.4

# creatina a list (useer_id , number_of_friends)
num_friends_by_id = [(user["id"], number_of_friends(user)) for user in users]

sorted(num_friends_by_id, key=lambda (user_id, num_friends): num_friends, reverse = True)
 # each pair is (user_id, num_friends)
 # [(1, 3), (2, 3), (3, 3), (5, 3), (8, 3),
 #  (0, 2), (4, 2), (6, 2), (7, 2), (9, 1)]

#This example is as a way of identifying people who are somehow central to the network. 
#network metric degree centrality 

def friends_of_friend_ids_bad(user):
  # "foaf" is short for friends of a friend
  return [foaf["id"]
          for friend in user["friends"]
          for foaf in friend["friends"]]
          
 print [friend["id"] for friend in users[0]["friends"]]  # [1, 2]
 print [friend["id"] for friend in users[1]["friends"]]  # [0, 2, 3]
 print [friend["id"] for friend in users[2]["friends"]]  # [0, 1, 3]

# count of mutual friends
from collections import Counter

def not_the_same(user, other_user):
  """two users are not the same if they have different ids"""
  return user["id"] != other_user["id"]

def not_friends(user, other_user):
  """other_user is not a friend if he's not in user["friends"];
    that is, if he's not_the_same as all the people in user["friends"]"""
  return all(not_the_same(friend, other_user)
             for friend in user["friends"])

 def friends_of_friend_ids(user):
   return Counter(foaf["id"]
                  for friend in user["friends"]    # for each of my friends
                  for foaf in friend["friends"]     # count *their* friends
                  if not_the_same(user, foaf)      # who aren't me
                  and not_friends(user, foaf))      # and aren't my friends
   print friends_of_friend_ids(users[3])              # Counter({0: 2, 5: 1})  

# pairs (user_id, interest)
 interests = [
 (0, "Hadoop"), (0, "Big Data"), (0, "HBase"), (0, "Java"),
 (0, "Spark"), (0, "Storm"), (0, "Cassandra"),
 (1, "NoSQL"), (1, "MongoDB"), (1, "Cassandra"), (1, "HBase"),
 (1, "Postgres"), (2, "Python"), (2, "scikit-learn"), (2, "scipy"),
 (2, "numpy"), (2, "statsmodels"), (2, "pandas"), (3, "R"), (3, "Python"),
 (3, "statistics"), (3, "regression"), (3, "probability"),
 (4, "machine learning"), (4, "regression"), (4, "decision trees"),
 (4, "libsvm"), (5, "Python"), (5, "R"), (5, "Java"), (5, "C++"),
 (5, "Haskell"), (5, "programming languages"), (6, "statistics"),
 (6, "probability"), (6, "mathematics"), (6, "theory"),
 (7, "machine learning"), (7, "scikit-learn"), (7, "Mahout"),
 (7, "neural networks"), (8, "neural networks"), (8, "deep learning"),
 (8, "Big Data"), (8, "artificial intelligence"), (9, "Hadoop"),
 (9, "Java"), (9, "MapReduce"), (9, "Big Data")
 ]

 def data_scientists_who_like(target_interest):
   return [user_id
           for user_id, user_interest in interests
           if user_interest == target_interest]

 from collections import defaultdict
 # keys are interests, values are lists of user_ids with that interest
 user_ids_by_interest = defaultdict(list)
for user_id, interest in interests:
  user_ids_by_interest[interest].append(user_id)

 # keys are user_ids, values are lists of interests for that user_id
 interests_by_user_id = defaultdict(list)
for user_id, interest in interests:
 interests_by_user_id[user_id].append(interest)

def most_common_interests_with(user):
 return Counter(interested_user_id
      for interest in interests_by_user_id[user["id"]]
      for interested_user_id in user_ids_by_interest[interest]
      if interested_user_id != user["id"])

# anonymous data set containing each user’s 
# salary (in dollars) and tenure as a data scientist (in years)

salaries_and_tenures = [(83000, 8.7), (88000, 8.1),
 (48000, 0.7), (76000, 6),
 (69000, 6.5), (76000, 7.5),
 (60000, 2.5), (83000, 10),
 (48000, 1.9), (63000, 4.2)]

# keys are years, values are lists of the salaries for each tenure
 salary_by_tenure = defaultdict(list)

for salary, tenure in salaries_and_tenures:
 salary_by_tenure[tenure].append(salary)

 # keys are years, each value is average salary for that tenure
 average_salary_by_tenure = {
   tenure : sum(salaries) / len(salaries)
   for tenure, salaries in salary_by_tenure.items()
 }

def tenure_bucket(tenure):
 if tenure < 2:
   return "less than two"
 elif tenure < 5:
   return "between two and five"
 else:
   return "more than five"

 # keys are tenure buckets, values are lists of salaries for that bucket
 salary_by_tenure_bucket = defaultdict(list)
 for salary, tenure in salaries_and_tenures:
   bucket = tenure_bucket(tenure)
   salary_by_tenure_bucket[bucket].append(salary)

#average salary for each group

# keys are tenure buckets, values are average salary for that bucket
 average_salary_by_bucket = {
   tenure_bucket : sum(salaries) / len(salaries)
   for tenure_bucket, salaries in salary_by_tenure_bucket.iteritems()
 }
 
def predict_paid_or_unpaid(years_experience):
 if years_experience < 3.0:
   return "paid"
 elif years_experience < 8.5:
   return "unpaid"
 else:
   return "paid"

interests = [
 (0, "Hadoop"), (0, "Big Data"), (0, "HBase"), (0, "Java"),
 (0, "Spark"), (0, "Storm"), (0, "Cassandra"),
  (1, "NoSQL"), (1, "MongoDB"), (1, "Cassandra"), (1, "HBase"),
 (1, "Postgres"), (2, "Python"), (2, "scikit-learn"), (2, "scipy"),
 (2, "numpy"), (2, "statsmodels"), (2, "pandas"), (3, "R"), (3, "Python"),
 (3, "statistics"), (3, "regression"), (3, "probability"),
 (4, "machine learning"), (4, "regression"), (4, "decision trees"),
 (4, "libsvm"), (5, "Python"), (5, "R"), (5, "Java"), (5, "C++"),
 (5, "Haskell"), (5, "programming languages"), (6, "statistics"),
 (6, "probability"), (6, "mathematics"), (6, "theory"),
 (7, "machine learning"), (7, "scikit-learn"), (7, "Mahout"),
 (7, "neural networks"), (8, "neural networks"), (8, "deep learning"),
 (8, "Big Data"), (8, "artificial intelligence"), (9, "Hadoop"),
 (9, "Java"), (9, "MapReduce"), (9, "Big Data")
 ]
""" 1. Lowercase each interest (since different users may or may not capitalize their
 interests).
 2. Split it into words.
 3. Count the results"""

words_and_counts = Counter(word
 for user, interest in interests
 for word in interest.lower().split())

 for word, count in words_and_counts.most_common():
   if count > 1:
     print word, count
