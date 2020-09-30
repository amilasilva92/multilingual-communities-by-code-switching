#!/usr/bin/env python

import sys
import json

postFullSentence=0.0
postOpposes=0.0
postQuestions=0.0
postSupports=0.0
postProvidesAdditionalInfo=0.0
relevance=0.0
language=0.0

score=0.0
count=0.0
total_posts=0
for line in sys.stdin:
    discussion_blob=json.loads(line)
    discussion=discussion_blob["discussion"]
    ground_truth=discussion_blob["ground_truth"]
    if "predicted_ground_truth" not in discussion_blob:
        predicted_ground_truth=ground_truth
    else:
        predicted_ground_truth=discussion_blob["predicted_ground_truth"]
    count+=1
    DpostFullSentence=0.0
    DpostOpposes=0.0
    DpostQuestions=0.0
    DpostSupports=0.0
    DpostProvidesAdditionalInfo=0.0
    Drelevance=0.0
    Dlanguage=0.0
    posts={}
    for post_truth in ground_truth:
        posts[post_truth["post_id"]]=post_truth
    for post_predicted_truth in predicted_ground_truth:
        if post_predicted_truth["post_id"] in posts:
            if post_predicted_truth["consensus"]["postFullSentence"]==posts[post_predicted_truth["post_id"]]["consensus"]["postFullSentence"]:
                DpostFullSentence+=1.0
            if post_predicted_truth["consensus"]["postOpposes"]==\
                posts[post_predicted_truth["post_id"]]["consensus"]["postOpposes"]:
                DpostOpposes+=1.0
            if post_predicted_truth["consensus"]["postQuestions"]==\
                posts[post_predicted_truth["post_id"]]["consensus"]["postQuestions"]:
                DpostQuestions+=1.0
            if post_predicted_truth["consensus"]["postSupports"]==\
                posts[post_predicted_truth["post_id"]]["consensus"]["postSupports"]:
                DpostSupports+=1.0
            if post_predicted_truth["consensus"]["postProvidesAdditionalInfo"]==\
                posts[post_predicted_truth["post_id"]]["consensus"]["postProvidesAdditionalInfo"]:
                DpostProvidesAdditionalInfo+=1.0
            Drelevance+=1.0/(1.0+abs(post_predicted_truth["consensus"]["relevance"]-posts[post_predicted_truth["post_id"]]["consensus"]["relevance"]))
            match=0.0
            for i in range(0, len(posts[post_predicted_truth["post_id"]]["consensus"]["tokens"])):
                if posts[post_predicted_truth["post_id"]]["consensus"]["tokens"][i]["lang"]==post_predicted_truth["consensus"]["tokens"][i]["lang"]:
                    match+=1.0
            Dlanguage+=match/len(posts[post_predicted_truth["post_id"]]["consensus"]["tokens"])
    total_posts+=len(posts)
    DpostFullSentence/=len(posts)
    DpostOpposes/=len(posts)
    DpostQuestions/=len(posts)
    DpostSupports/=len(posts)
    DpostProvidesAdditionalInfo/=len(posts)
    Drelevance/=len(posts)
    Dlanguage/=len(posts)
    postFullSentence+=DpostFullSentence
    postOpposes+=DpostOpposes
    postQuestions+=DpostQuestions
    postSupports+=DpostSupports
    postProvidesAdditionalInfo+=DpostProvidesAdditionalInfo
    relevance+=Drelevance
    language+=Dlanguage
final_score=(postFullSentence+postOpposes+postQuestions+postSupports+postProvidesAdditionalInfo+relevance+3*language)/9.0/count
final_score = relevance/count
final_score = language/count
print("scored %i discussions with a total of %i scored posts: %f"%(count, total_posts, final_score))
# print(final_score)
#return final_score
