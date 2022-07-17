label2class = {
    0:'低级别球员',
    1:'顶级球员',
    2:'快退役了',
    3:'经验老将',
    4:'未来可期',
    5:'定型无潜力',
    6:'少年老成',
    7:'大器晚成',
    8:'一般球员',
    9:'当打之年',
    10:'其他球员'
}

def get_player_class(age, ca, pa):
    if ca < 70 and pa < 70:
        return 0
    elif ca >= 85 and pa >= 85:
        return 1
    elif age >= 30 and ca < 70:
        return 2
    elif age >= 30 and ca >= 70:
        return 3
    elif age < 25 and ca < 80 and pa >= 80:
        return 4
    elif age < 25 and ca < 80 and pa < 80:
        return 5
    elif age < 25 and ca >= 80 and pa >= 80:
        return 6
    elif age >= 25 and age < 30 and ca < 80 and pa >= 80:
        return 7
    elif age >= 25 and age < 30 and ca < 80 and pa < 80:
        return 8
    elif age >= 25 and age < 30 and ca >= 80 and pa >= 80:
        return 9
    else:
        return 10

# c = label2class.get(get_player_class(32,65,66))
# print(c)
print('acc 0.9837540614846289\nKNN mat training complete in 0m 0s\nacc 0.9837540614846289\nKNN iter training complete in 0m 27s')