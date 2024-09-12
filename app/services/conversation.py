import redis
import json
import os

redis_client = redis.Redis(host=os.getenv('REDIS_HOST'), port=int(os.getenv('REDIS_PORT')), db=int(os.getenv('REDIS_DB')))

REDIS_HISTORY_KEY = "conversation_history"

def save_conversation(query, answer, documents, is_followup):
    if not is_followup:
        redis_client.delete(REDIS_HISTORY_KEY)

    conversation_data = {
        "query": query,
        "answer": answer,
        "documents": documents
    }

    conversation_json = json.dumps(conversation_data)

    redis_client.rpush(REDIS_HISTORY_KEY, conversation_json)

def get_conversation():
    conversation_json_list = redis_client.lrange(REDIS_HISTORY_KEY, 0, -1)

    conversation_history = [json.loads(convo) for convo in conversation_json_list]

    return conversation_history
