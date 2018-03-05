import random


class Player:
    
    def __init__(self, name, hp, ap, traits):
        self.name = name
        self.hp = hp
        self.ap = ap
        self.traits = traits
        self.alive = True

    def round(self):
        if self.alive:
            if self.ap >= 1:
                self.ap -= 1
                return 1
            else:
                self.ap += 1
                return 0
        else:
            return 0

    def penalty(self, penalties):
        for t in penalties:
            if t == 'get':
                # (if trait, add trait)
                print '{0} is adding {1} to {2}'.format(self.name, penalties[t][0], penalties[t][1])
                if penalties[t][0] in self.traits:
                    self.add_trait(penalties[t][1])

            elif t in self.traits and self.alive:
                self.hp -= penalties[t]

    def clean_up(self):
        print '{0} hp: {1}, ap: {2}'.format(self.name, self.hp, self.ap)
        if self.hp <= 0:
            self.alive = False
            print self.name + ' is dead!'

    def add_trait(self, trait):
        self.traits.append(trait)



class Event:

    def __init__(self, *args):
        self.id = args[0]
        self.name = args[1]
        self.requirement = args[2]
        self.penalties = args[3]



if __name__ == "__main__":
    
    # create 5 characters
    doctor = Player('Doctor Ashley', 7, 4, ['extrovert', 'alcoholic', 'tired'])
    soldier = Player('Soldier Alex', 8, 5, ['introvert', 'depressed', 'aggressive', 'alcoholic'])
    grandpa = Player('Grandpa Bill', 9, 3, ['cold', 'introvert', 'aggressive', 'passive'])
    girl = Player('Little Girl Alison', 8, 3, ['depressed', 'introvert', 'cold'])
    engineer = Player('Engineer Taylor', 7, 4, ['extrovert', 'tired', 'passive'])
    characters = [doctor, soldier, grandpa, girl, engineer]

    # load events
    events = []
    with open('events.csv', 'r') as f:
        for ln in f.readlines():
            print 'reading' + ln[:2]
            e = Event(*(ln.split(',')))
            events.append(e)
        n = len(f.readlines())

    # each turn
    turn = 1
    while turn <= 12:
        r = random.randint(0, n)
        current_event = events[r]
        del events[r]
        print 'current event is ' + current_event.name
        
        total_point = 0
        for char in characters:
            total_point += char.round()
        print 'this round we spend: ' + str(total_point)

        if total_point >= current_event.requirement:
            pass
        else:
            p_list = current_event.penalties.split(' ')
            p_dict = {}
            for p in p_list:
                if '-' in p:
                    # minus
                    p0 = p.split('-')[0]
                    p1 = p.split('-')[1]
                    p_dict[p0] = int(p1)
                elif p.find('get') >= 0:
                    # get trait 
                    p_dict['get'] = (p.split('_get_')[0], p.split('_get_')[1])
                else:
                    # others
                    pass

            print p_dict 

        # penalty
        for char in characters:
            char.penalty(p_dict)
        
        # clean up
        for char in characters:
            char.clean_up()
        print '-------------round {0} end --------------\n'.format(turn)
        turn += 1
    
    surviver = filter(lambda x: x.hp > 0, characters)
    print 'survivers...' + ' '.join(surviver)

    
