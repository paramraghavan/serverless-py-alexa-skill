from alexa_skills.LuckyNumberSkill import LuckNumberSkill


def lucky_number(event, context):
    # instantiate LuckNumberSkill
    lucky_number_skill = LuckNumberSkill()
    response = lucky_number_skill.handle(event, context)

    return response