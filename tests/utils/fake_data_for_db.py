users_data = [
    {
        "user_id": 123,
        "user_name": "Слава"
    },
    {
        "user_id": 12,
        "user_name": "Differ"
    }
]

attempts_data = [
    {
        "attempt_id": "0738c864-9ebd-4ec4-a70a-b7203373223b",
        "user_id": 12,
        "result": 0.2
    },
    {
        "attempt_id": "1fff68de-8942-4ea6-b3cf-d2ce4d6b5934",
        "user_id": 123,
        "result": 0.6
    },
    {
        "attempt_id": "5010d717-475f-413f-aa66-f0d325d3e5ef",
        "user_id": 123,
        "result": 0.8
    },
    {
        "attempt_id": "52c38208-13db-45e4-9346-a2acb06c68bb",
        "user_id": 12,
        "result": 0.9
    },
    {
        "attempt_id": "690ec65c-fc14-4517-8f5d-7df2cc54a4a4",
        "user_id": 123,
        "result": 0.8
    }
]

statuses_data = [
    {
        "user_id": 123,
        "theme": "src/bot/utils/data_4.json",
        "questions": 10
    },
    {
        "user_id": 12,
        "theme": "src/bot/utils/data_3.json",
        "questions": 20
    }
]


async def dp_filler(db): # TODO: сделать это чрез миграции
    """
    Fill the database fake data
    """
    for i in users_data:
        await db.user.new(user_id=i["user_id"], user_name=i["user_name"])

    for i in statuses_data:
        await db.test.new(user_id=i["user_id"], theme=i["theme"], questions=i["questions"])

    for i in attempts_data:
        await db.attempt.new(attempt_id=i["attempt_id"], user_id=i["user_id"], result=i["result"])