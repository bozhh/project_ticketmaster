def individual_description(event) -> dict:
    return {
        "id": str(event["_id"]),
        "event_id": event["event_id"],
        "description": event["description"]
    }    

def individual_review(event) -> dict:
    return {
        "id": str(event["_id"]),
        "event_id": event["event_id"],
        "review": event["review"],
        "text": event["text"],
        "user": event["user"],
        "user_id": event["user_id"]
    }

def list_descriptions(events) -> list:
    return [individual_description(event) for event in events]

def list_reviews(events) -> list:
    return [individual_review(event) for event in events]