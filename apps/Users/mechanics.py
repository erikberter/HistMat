
level_name_relation = ['Principiante','Novato','Aprendiz','Jugador','Experto','Dios','Stalin']

def add_exp(user, xp):
    user.xp += xp
    print(user.xp)
    while user.xp > user.level*10:
        user.xp -= user.level*10
        user.level += 1
        if user.level % 10 == 0 and user.level < 65:
            user.kind_of_user = level_name_relation[user.level // 10]

    user.save()