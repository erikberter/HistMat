
def add_exp(user, xp):
    print("Añadiendo xp")
    user.xp += xp
    print(user.xp)
    while user.xp > user.level*10:
        print("Sube")
        user.xp -= user.level*10
        user.level += 1
    print(user.level)
    user.save()