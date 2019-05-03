from flask import jsonify
from dao.post import PostDAO
from dictionaryMapping import *
from dao.hashtag import HashtagDAO
from ttp import ttp


class PostHandler:

    def getAllPost(self):
        dao = PostDAO()
        result = dao.getAllPosts()
        if not result:
            return jsonify(Error="Not found"), 404
        mapped_result = []
        for r in result:
            mapped_result.append(mapPostToDict(r))
        return jsonify(mapped_result)

    def getPostByGroupId(self, gID):
        dao = PostDAO()
        result = dao.getPostsByGroupID(gID)
        if not result:
            return jsonify(Error="Not found"), 404
        mapped_result = []
        for r in result:
            mapped_result.append(mapPostToDict(r))
        return jsonify(mapped_result)

    def getPostByGroupIdDETAILED(self,gID):
        dao = PostDAO()
        result = dao.getPostsByGroupID(gID)
        mapped_result = []
        for r in result:
            mapped_result.append(mapPostToDictDETAILED(r, self.getRepliesByPostIDDETAILED(r[0])))
        return jsonify(mapped_result)

    def getNumberOfLikesForGivenPost(self, pID):
        dao = PostDAO()
        result = dao.getNumberOfReactionsForGivenPost(pID, "like")
        if not result:
            return jsonify(Error="Not found"), 404
        mapped_result = mapReacCountToDict(result)
        return jsonify(mapped_result)

    def getNumberOfDislikesForGivenPost(self, pID):
        dao = PostDAO()
        result = dao.getNumberOfReactionsForGivenPost(pID, "dislike")
        if not result:
            return jsonify(Error="Not found"), 404
        mapped_result = mapReacCountToDict(result)
        return jsonify(mapped_result)

    def getListOfUsersWhoLikedPost(self, pID):
        dao = PostDAO()
        result = dao.getListOfUsersWhoReactedPost(pID, "like")
        if not result:
            return jsonify(Error="Not found"), 404
        mapped_result = []
        for r in result:
            mapped_result.append(mapToReactDict(r))
        return jsonify(mapped_result)

    def getListOfUsersWhoDislikedPost(self, pID):
        dao = PostDAO()
        result = dao.getListOfUsersWhoReactedPost(pID, "dislike")
        if not result:
            return jsonify(Error="Not found"), 404
        mapped_result = []
        for r in result:
            mapped_result.append(mapToReactDict(r))
        return jsonify(mapped_result)

    def getNumberOfPostsPerDay(self):
        dao = PostDAO()
        result = dao.getNumberOfPostsPerDay()
        if not result:
            return jsonify(Error="Not found"), 404
        mapped_result = []
        for r in result:
            mapped_result.append(mapInteractionPerDayToDict(r))
        return jsonify(mapped_result)

    def getNumberOfRepliesPerDay(self):
        dao = PostDAO()
        result = dao.getNumberOfRepliesPerDay()
        if not result:
            return jsonify(Error="Not found"), 404
        mapped_result = []
        for r in result:
            mapped_result.append(mapInteractionPerDayToDict(r))
        return jsonify(mapped_result)

    def getNumberOfLikesPerDay(self):
        dao = PostDAO()
        result = dao.getNumberOfLikesPerDay()
        if not result:
            return jsonify(Error="Not found"), 404
        mapped_result = []
        for r in result:
            mapped_result.append(mapInteractionPerDayToDict(r))
        return jsonify(mapped_result)

    def getNumberOfDislikesPerDay(self):
        dao = PostDAO()
        result = dao.getNumberOfDislikesPerDay()
        if not result:
            return jsonify(Error="Not found"), 404
        mapped_result = []
        for r in result:
            mapped_result.append(mapInteractionPerDayToDict(r))
        return jsonify(mapped_result)

    def getNumberOfRepliesForGivenPost(self, pID):
        dao = PostDAO()
        result = dao.getNumberOfRepliesForGivenPost(pID)
        if not result:
            return jsonify(Error="Not found"), 404
        mapped_result = []
        for r in result:
            mapped_result.append(mapReplyCountToDict(r))
        return jsonify(mapped_result)

    def getNumberOfPostsPerDayByUser(self, uID):
        dao = PostDAO()
        result = dao.getNumberOfPostsPerDayByUser(uID)
        if not result:
            return jsonify(Error="Not found"), 404
        mapped_result = []
        for r in result:
            mapped_result.append(mapInteractionPerDayToDict(r))
        return jsonify(mapped_result)

    def getRepliesByPostID(self, pID):
        dao = PostDAO()
        result = dao.getRepliesByPostID(pID)
        if not result:
            return jsonify(Error="Not found"), 404
        mapped_result = []
        for r in result:
            mapped_result.append(mapReplyToDict(r))
        return jsonify(mapped_result)

    def getRepliesByPostIDDETAILED(self, pID):
        dao = PostDAO()
        result = dao.getRepliesByPostID(pID)
        mapped_result = []
        for r in result:
            mapped_result.append(mapReplyToDict(r))
        return mapped_result

    def addPost(self, gID, json):
        dao = PostDAO()
        hdao = HashtagDAO()
        p = ttp.Parser()

        if len(json) != 3:
            return jsonify(Error="Malformed post request"), 400
        else:
            chat_group_id = gID
            user_id = json['user_id']
            message = json['message']
            media = json['media']

            if chat_group_id and user_id and message and media:
                post_id = dao.addPost(media, message, chat_group_id, user_id)

                hashtags = p.parse(message).tags

                noDupHashtags = []
                for tag in hashtags:
                    if tag.lower() not in noDupHashtags:
                        noDupHashtags.append(tag.lower())

                for hashtag in noDupHashtags:
                    hdao.insertHashtag(hashtag, post_id)

                return jsonify(post_id), 201
            else:
                return jsonify(Error="Unexpected attributes in post request"), 400

    def likeaPost(self, json):
        if json is None:
            return jsonify(Error="Malformed post request"), 400
        else:
            user_id = json['user_id']
            post_id = json['post_id']
            dao = PostDAO()
            result = dao.reactToPost(user_id,post_id)
            return jsonify(result)

    def dislikeaPost(self, json):
        if json is None:
            return jsonify(Error="Malformed post request"), 400
        else:
            user_id = json['user_id']
            post_id = json['post_id']
            dao = PostDAO()
            result = dao.dislikeaPost(user_id,post_id)
            return jsonify(result)

    def replyToPostID(self, post_id, json):
        if json is None:
            return jsonify(Error="Malformed post request"), 400
        else:
            reply_message = json['reply_message']
            user_id = json['user_id']

            dao = PostDAO()
            result = dao.replyToPostID(reply_message, post_id, user_id)
            return jsonify(result)

