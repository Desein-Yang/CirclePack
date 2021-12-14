import matplotlib
import math
import click
import numpy as np
import matplotlib.pyplot as plt

# Framework Simuated Annealing
# initialize solution
# while end
#   mutate solution
#   caculate fitness and delta_t
#   update solution(if better: accept else:  accept prob = exp(-T/T))
#   annealing (decrease t)
# return solution 

# @click.command()
# @click.option('--L', default=10, help='Number of greetings.')
# @click.option('--W', default=10, help='The person to greet.')
def main(L,W,radius,max_iters=100,min_t=0,ini_t=100,alpha=0.9):
    iters = 0
    now_t = ini_t

    def is_placed(x,y,r):
        if min(L-x,W-y,x,y) > r:
            return True
        else:
            return False  
            
    def fitness(solu):
        f = 0
        for i,(x,y,r) in enumerate(solu):
            if is_placed(x,y,r): # 如果放进去
                f += math.pi*r*r
        return f/(L*W)
        # 只计算变动就快一点
   
    def remove(i,solu):
        x,y,r = solu[i]
        if is_placed(x,y,r):
            solu[i] = (-1*max_r,-1*max_r,radius[i])
            return True
        else:
            return False

    def add(i,solu):
        solu[i] = (np.random.rand(0,1)*L,np.random.rand(0,1)*W,radius[i])
        solu = adjust_overlap(i,solu)
        x,y,r = solu[i]
        if not is_placed(x,y,r):
            remove(i,solu)
            return False
        else:
            return True

    def mutate(solu):
        is_mutated = False
        while(is_mutated):
            # 在里面的抽出一个
            is_placeds = [int(is_placed(x,y,r)) for x,y,r in solu]
            non_placeds = [int(not is_placed(x,y,r)) for x,y,r in solu] 
            choosed = np.random.choice(solu,prob=is_placeds/len(solu))
            replaced = np.random.choice(solu,prob=non_placeds/len(solu))
            remove(choosed,solu)
            is_mutated = add(replaced,solu)
        return solu

    def adjust_overlap(i,solu):
        # 重叠了就往哪个方向移动/删除
        # 太宽松了就往反方向移动/删除
        # 相切
        x,y,r = solu[i]
        for j,(x2,y2,r2) in enumerate(solu):
            if i!=j:
                dist = math.sqrt((x-x2)*(x-x2)+(y-y2)*(y-y2))
                delta_x = (r+r2-dist)/dist*(x-x2)
                delta_y = (r+r2-dist)/dist*(y-y2)
                if dist < r+r2:
                    x,y = x+delta_x,y+delta_y
                else:
                    x,y = x-delta_x,y-delta_y
        solu[i] = x,y,r
        return solu

    def ini(radius):
        n = len(radius)
        max_r = max(radius)
        solu = [(np.random.rand(0,1)*L,np.random.rand(0,1)*W, radius[i]) for i in range(n)] # 空解
        fit = fitness(solu)
        return solu, fit

   
    def draw(solu):
        fig,ax = plt.subplots(figsize=(10,10))
        for (x,y,r) in solu:
            if is_placed(x,y,r):
                ax.add_artist(plt.Circle((x, y), r, alpha=0.1))
        plt.xlim((0,L))
        plt.ylim((0,W))
        plt.title('Solution')
        plt.show()

    solu, old_fit = ini(radius)

    while(now_t > min_t and iters < max_iters): # 终止条件
        new_solu = mutate(solu)# 扰动产生新解
        new_fit = fitness(new_solu)
        delta_t = new_fit-old_fit 
        print(solu)
        if delta_t > 0:
            solu = new_solu
            old_fit = new_fit
        else: # Metropolis 准则
            prob = np.random.rand(0,1)
            if prob > math.exp(-delta_t/now_t):
                solu = new_solu
                old_fit = new_fit
        now_t = alpha * now_t # 指数下降
        print("now temperatuer:",now_t)
        print("fitness:",new_fit)
        iters += 1
        if iters % 100 == 0:
            draw(solu)

    return solu, old_fit
    
if __name__ == "__main__":
    L=10 
    W=10
    radius=[1,1,1]
    main(L,W,radius)
