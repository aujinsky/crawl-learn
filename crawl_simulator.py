import torch
import torch.distributions.constraints as constraints
import pyro
import numpy
from copy import deepcopy
import torch.nn as nn
import torch.nn.functional as F
class World():
    def __init__(self):
        # los is 15*15. 17*17 for just evading error
        self.size = 11
        self.mid = 6
        size = self.size
        mid = self.mid
        self.los = torch.LongTensor((size + 2),(size + 2)).fill_(-1)
        self.player = Player()
        self.los[mid][mid] = 0 # player
        self.mob_count = dice_nm(2,8) + 6
        self.mob_dict = dict()
        self.total_score = 0
        for mob_no in range(1, self.mob_count+1):
            mob_x = dice_nm(1, size) - mid
            mob_y = dice_nm(1, size) - mid
            while(self.los[mob_x + mid][mob_y + mid] != -1):
                mob_x = int(dice_nm(1, size) - mid)
                mob_y = int(dice_nm(1, size) - mid)
            self.los[mob_x + mid][mob_y + mid] = mob_no
            self.mob_dict[mob_no] = Mob(mob_no, mob_x, mob_y)
            self.total_score = self.total_score + self.mob_dict[mob_no].score
        self.print_mob_dict()
        self.print_world()
    def world_tensor():
        self.world_tensor = torch.ones((5, 11, 11))
        for j in range(self.size):
            for k in range(self.size):
                self.world_tensor[0] = self.los[j][k].curhp
                self.world_tensor[1] = self.los[j][k].dmg
                self.world_tensor[2] = self.los[j][k].abfreq
                self.world_tensor[3] = self.los[j][k].abdmg
                self.world_tensor[4] = self.los[j][k].score
        return self.tensor
    def end(self):
        if((not self.mob_dict) or self.player.curhp < 0):
            return True
        else:
            return False
    def print_world(self):
        print(self.los)
        print(self.player.curhp)
    def print_mob_dict(self):
        mob_dict_v ="mob dict: "
        for mob_no in self.mob_dict:
            mob_dict_v = mob_dict_v + " " + str(mob_no)+" "+str(self.mob_dict[mob_no].curhp)
        print(mob_dict_v)
    def head_towards(self, mob_no):
        mob = self.mob_dict[mob_no]
        inx = mob.posx
        iny = mob.posy
        fix = self.player.posx
        fiy = self.player.posy
        vecx = numpy.sign(fix - inx)
        vecy = numpy.sign(fiy - iny)
        if(self.change_pos(mob_no, inx+vecx, iny+vecy)):
            return True
        elif(self.change_pos(mob_no, int(inx+numpy.ceil((vecy+vecx)/2)), int(iny+numpy.ceil((vecy-vecx)/2)))):
            return True
        elif(self.change_pos(mob_no, int(inx+numpy.ceil((vecx-vecy)/2)), int(iny+numpy.ceil((vecx+vecy)/2)))):
            return True
        else:
            return False    # did nothing
    def change_pos(self, mob_no, newx, newy):
        mid = self.mid
        if(newx<=-mid or newy<=-mid):
            return False
        if(newx>=mid or newy>=mid):
            return False
        if(mob_no == 0):
            oldx = self.player.posx
            oldy = self.player.posy
        else:
            oldx = self.mob_dict[mob_no].posx
            oldy = self.mob_dict[mob_no].posy
        if(self.is_free(newx, newy)):    # if new pos is empty, change pos
            self.los[newx + mid][newy + mid] = self.los[oldx+ mid][oldy + mid]
            if(mob_no == 0):
                self.player.posx = newx
                self.player.posy = newy
            else:    # not player
                self.mob_dict[mob_no].posx = newx
                self.mob_dict[mob_no].posy = newy
            self.los[oldx + mid][oldy + mid] = -1
            return True
        else:   # if new pos is not empty, do nothing
            return False
    def is_free(self, posx, posy):
        mid = self.mid
        if(self.los[posx + mid][posy + mid] == -1):
            return True
        else:
            return False
    def attackable(self, mob_no):
        mob = self.mob_dict[mob_no]
        if (-1 <= self.player.posx - mob.posx and self.player.posx - mob.posx <= 1) and (-1 <= self.player.posy - mob.posy and self.player.posy - mob.posy <= 1):
            return True
        return False
class Player():
    def __init__(self):
        self.maxhp = 250
        self.curhp = self.maxhp
        self.dmg = dice_nm(10,20)
        self.repos_count = numpy.random.randint(low = 1, high = 6)
        self.range_count = numpy.random.randint(low = 1, high = 5)
        self.heal_count = numpy.random.randint(low = 3, high = 10)
        self.posx = 0
        self.posy = 0

class Mob():
    def __init__(self, mob_no, posx, posy):
        self.mob_no = int(mob_no)
        self.maxhp =  max(0, numpy.random.normal(75, 75)) + dice_nm(1, 75)
        self.curhp = self.maxhp
        self.dmg = dice_nm(3, 20)
        self.hasab = numpy.random.binomial(1, 0.5)
        self.abfreq = self.hasab * numpy.random.uniform(0, 0.2)
        self.abdmg = self.hasab * dice_nm(3, 10)
        self.score = self.calc_mob_score()
        self.posx = posx
        self.posy = posy
        self.mob_info = [self.mob_no, self.maxhp, self.curhp, self.dmg, self.abfreq, self.abdmg, self.score]
    def is_alive(self):
        if self.curhp > 0:
            return true
        else:
            return false
    def calc_mob_score(self):
        return numpy.sqrt(self.maxhp*(self.dmg+self.abfreq*self.abdmg)) 

class Simulate():
    def __init__(self):
        # make initial player settings
        # make mob templates
        self.original_world = World()
        self.score_dp = 0
        self.score_pl = 0
    def total_score(self):
        if(self.original_world.player.curhp < 0):
            self.score_dp = -self.original_world.total_score
        return [self.score_dp, self.score_pl]
    def model_next_move(self, player_move):
        # called when player selected its next play
        # model next turn
        # first execute selected player move

        self.world = self.original_world
        self.player = self.world.player
        mid = self.world.mid
        if(player_move[0][0] == True):
            new_posx = self.player.posx + player_move[0][1]
            new_posy = self.player.posy + player_move[0][2]
            mob_no = int(self.world.los[new_posx + mid][new_posy + mid])
            if(mob_no == -1):
                # print("@"+str(mob_no))
                self.world.change_pos(0, new_posx, new_posy)
            else:
                # print("#"+str(mob_no))
                mob = self.world.mob_dict[mob_no]
                player_dmg = pyro.sample("pl_{}_dmg".format(mob_no), pyro.distributions.Uniform(1, self.player.dmg))
                mob.curhp = mob.curhp - player_dmg
                # print(mob.curhp)
                if(mob.curhp < 0):
                    if(self.player.curhp > 0):
                        self.score_dp = self.score_dp + mob.score
                        self.score_pl = self.score_dp + mob.score
                    self.world.los[mob.posx + mid][mob.posy + mid] = -1
                    del(self.world.mob_dict[mob_no])
        elif(player_move[1][0] == True and self.player.heal > 0):
            self.player.heal_count = self.player.heal_count - 1
            player_heal = pyro.sample("pl_heal", pyro.distributions.Normal(200, 75))
            self.player.curhp = self.player.curhp + player_heal * 3
        elif(player_move[2][0] == True):
            if(self.world.changepos(self.player.posx, self.player.posy, player_move[2][1], player_move[2][2])):
                self.player.posx = player_move[2][1]
                self.player.posy = player_move[2][2]

        # then do the rest
        # for mob_no in pyro.plate("data_loop", len(self.world.mob_dict)):
        for mob_no in self.world.mob_dict:
            mob = self.world.mob_dict[mob_no]
            m_mv = pyro.sample("m_{}_mv".format(str(mob_no)), pyro.distributions.Uniform(0, 1))
            if m_mv < mob.abfreq:
                m_abdmg = pyro.sample("m_{}_ab_dmg".format(str(mob_no)), pyro.distributions.Uniform(1, mob.abdmg))
                self.player.curhp = self.player.curhp - m_abdmg
            else:
                # melee or move
                if(self.world.attackable(mob_no)):
                    m_dmg = pyro.sample("m_{}_dmg".format(str(mob_no)), pyro.distributions.Uniform(1, mob.dmg))
                    self.player.curhp = self.player.curhp - m_dmg
                else:
                    self.world.head_towards(mob_no)
#        self.world.print_mob_dict()
#        self.world.print_world()
        if(self.player.curhp > 0):
            is_alive = 1
        else:
            is_alive = 0
        return pyro.sample("alive", pyro.distributions.Normal(is_alive, 1/4), obs = 0)
    def greedy_heal_algo(self, num_turn):
        # doesn't fled
        # doesn't uses reposition
        # just move towards the nearest mob and attack mob which deals strongest damage
        # but if chance to die in next turn gets over a certain threshold, heal
        #pyro.infer.Importance(model_next_move, 
        #pyro.condition(model_next_move, data={"alive": 1})(player_move)
        for i in range(num_turn):
            min_dist = 1000
            for mob_no in self.world.mob_dict:
                vecx = self.world.mob_dict[mob_no].posx - self.world.player.posx
                vecy = self.world.mob_dict[mob_no].posy - self.world.player.posy
                dist = max(numpy.abs(vecx), numpy.abs(vecy))
                if(dist < min_dist):
                    min_dist = dist
                    next_x = numpy.sign(vecx)
                    next_y = numpy.sign(vecy)
                    next_dmg = self.world.mob_dict[mob_no].dmg
                elif(dist == min_dist):
                    if(self.world.mob_dict[mob_no].dmg > next_dmg):
                        next_x = numpy.sign(vecx)
                        next_y = numpy.sign(vecy)
                        next_dmg = self.world.mob_dict[mob_no].dmg
            self.model_next_move([[True, next_x, next_y],[False],[False]])
        return
    def model_next_move_1(self):
        next_move = [[1, 1], [1, 0], [1, -1], [0, 1], [0, -1], [-1, 1], [-1, 0], [-1, -1]]
        next_move_seed = pyro.sample("pl_mv", pyro.distributions.Categorical(torch.tensor([1/8,1/8,1/8,1/8,1/8,1/8,1/8,1/8])))
        player_move = [[True]+next_move[next_move_seed],[False],[False]]
        self.world = deepcopy(self.original_world)
        self.player = self.world.player
        mid = self.world.mid
        if(player_move[0][0] == True):
            new_posx = self.player.posx + player_move[0][1]
            new_posy = self.player.posy + player_move[0][2]
            mob_no = int(self.world.los[new_posx + mid][new_posy + mid])
            if(mob_no == -1):
                # print("@"+str(mob_no))
                self.world.change_pos(0, new_posx, new_posy)
            else:
                # print("#"+str(mob_no))
                mob = self.world.mob_dict[mob_no]
                player_dmg = pyro.sample("pl_{}_dmg".format(mob_no), pyro.distributions.Uniform(1, self.player.dmg))
                mob.curhp = mob.curhp - player_dmg
                # print(mob.curhp)
                if(mob.curhp < 0):
                    self.world.los[mob.posx + mid][mob.posy + mid] = -1
                    del(self.world.mob_dict[mob_no])
        elif(player_move[1][0] == True and self.player.heal > 0):
            self.player.heal_count = self.player.heal_count - 1
            player_heal = pyro.sample("pl_heal", pyro.distributions.Normal(200, 75))
            self.player.curhp = self.player.curhp + player_heal * 3
        elif(player_move[2][0] == True):
            if(self.world.changepos(self.player.posx, self.player.posy, player_move[2][1], player_move[2][2])):
                self.player.posx = player_move[2][1]
                self.player.posy = player_move[2][2]

        # then do the rest
        # for mob_no in pyro.plate("data_loop", len(self.world.mob_dict)):
        for mob_no in self.world.mob_dict:
            mob = self.world.mob_dict[mob_no]
            m_mv = pyro.sample("m_{}_mv".format(str(mob_no)), pyro.distributions.Uniform(0, 1))
            if m_mv < mob.abfreq:
                m_abdmg = pyro.sample("m_{}_ab_dmg".format(str(mob_no)), pyro.distributions.Uniform(1, mob.abdmg))
                self.player.curhp = self.player.curhp - m_abdmg
            else:
                # melee or move
                if(self.world.attackable(mob_no)):
                    m_dmg = pyro.sample("m_{}_dmg".format(str(mob_no)), pyro.distributions.Uniform(1, mob.dmg))
                    self.player.curhp = self.player.curhp - m_dmg
                else:
                    self.world.head_towards(mob_no)
#        self.world.print_mob_dict()
#        self.world.print_world()
        if(self.player.curhp > 0):
            is_alive = 1
        else:
            is_alive = 0
        pyro.sample("alive", pyro.distributions.Normal(is_alive, 1/4), obs = 0)

        return next_move_seed
        
def dice_nm(n, m):
    return numpy.sum(numpy.random.randint(1, m, size = n))
def model_imp(num_iter, simulate):
    conditioned_alive = pyro.condition(simulate.model_next_move_1, data={"alive": 1})
    imp = pyro.infer.Importance(conditioned_alive, num_samples = num_iter).run()
    marginal_mv = pyro.infer.EmpiricalMarginal(imp, sites=["pl_mv"])

    return marginal_mv()

#    posterior = pyro.infer.SVI(conditioned_alive, simulate.guide_imp, pyro.optim.Adam({"lr": .05}), loss = pyro.infer.Trace_ELBO())
#    for i in range(num_iter):
#        posterior.step()
#        print(pro.param("a1").item())
def run_imp(simulate):
    simulate_imp = deepcopy(simulate)
    next_move = [[1, 1], [1, 0], [1, -1], [0, 1], [0, -1], [-1, 1], [-1, 0], [-1, -1]]
    turn = 0
    while (not simulate_imp.original_world.end()) and turn < 100:
        turn = turn + 1
        next_move_seed = model_imp(1000, simulate_imp).int()
        player_move = [[True]+next_move[next_move_seed],[False],[False]]
        simulate_imp.model_next_move(player_move)
    if(simulate_imp.player.curhp <0):
        score_dp = -simulate_imp.world.total_score
    else:
        score_dp = simulate_imp.score_dp
    score_pl = simulate_imp.score_pl
    simulate_imp.original_world.print_world()
    return score_pl

def run_imp_search(simulate):
    simulate_sea = deepcopy(simulate)
    search_depth = 5
    search_iter = 100
    turn = 0
    while (not simulate_sea.original_world.end()) and turn < 100:
        turn = turn + 1
        total_mv = [0] * 8
        total_score_dp = [0.0] * 8
        total_score_pl = [0.0] * 8
        expect_score = -100000
        for i in range(search_iter):
            simulate_search = deepcopy(simulate_sea)
            former_dp = simulate_search.score_dp
            former_pl = simulate_search.score_pl
            fmv = -2
            for j in range(search_depth):
                next_move_seed = model_imp(25, simulate_search)
                next_move = [[1, 1], [1, 0], [1, -1], [0, 1], [0, -1], [-1, 1], [-1, 0], [-1, -1]]
                mv = [[True]+next_move[next_move_seed],[False],[False]]
                simulate_search.model_next_move(mv)
                if(j == 0):
                    total_mv[next_move_seed] = total_mv[next_move_seed] + 1
                    fseed = next_move_seed
            if(simulate_search.player.curhp < 0):
                total_score_dp[fseed] = total_score_dp[fseed] + (-simulate_search.world.total_score - former_dp)
            else:
                total_score_dp[fseed] = total_score_dp[fseed] + (simulate_search.score_dp - former_dp)
            total_score_pl[fseed] = total_score_pl[fseed] + (simulate_search.score_pl - former_pl)
        for mv in range(8):
            if(total_mv[mv] != 0):
                total_score_pl[mv] = total_score_pl[mv]/total_mv[mv]
                if(expect_score < total_score_pl[mv]):
                    next_move_seed = mv
                    expect_score = total_score_pl[mv]
        next_move = [[1, 1], [1, 0], [1, -1], [0, 1], [0, -1], [-1, 1], [-1, 0], [-1, -1]]
        player_move = [[True]+next_move[next_move_seed],[False],[False]]
        simulate_sea.model_next_move(player_move)
    simulate_sea.original_world.print_world()
    return simulate_sea.score_pl

for i in range(10):
    simulate = Simulate()
    imp_score_pl = run_imp(simulate)
    imp_search_score_pl = run_imp_search(simulate)
    print(imp_score_pl, imp_search_score_pl)

