#!/usr/bin/env python
import numpy as np
from matplotlib import pyplot as plt
plt.style.use(['ggplot'])

ref_X_Y = np.array([[0,0],[1,1],[1,0],[0,1]])*50
ref_X_Y

P_t = np.random.rand(2)*50

def _dist(ref_X_Y,P_target):
    d = []
    for i in range(len(ref_X_Y)):
        d.append(np.linalg.norm(ref_X_Y[i]-P_target))
        #d.append(np.sum((ref_X_Y[i]-P_target)**2)**.5)
    return np.array(d)

P_t = np.random.rand(2)*50
R = _dist(ref_X_Y,P_t)


'''
plt.scatter(ref_X_Y.T[0],ref_X_Y.T[1],marker='^')
plt.scatter(P_t[0],P_t[1],marker='o')
#plt.scatter(P_approach[0],P_approach[1],marker='x')
for i in range(len(ref_X_Y)):
    circle = plt.Circle(ref_X_Y[i],R[i],color='b',fill=False)
    plt.gca().add_patch(circle)

plt.show()
'''

# convert polar to cartesian
def _p(ref_X_Y,theta,R):
    P = []
    for i in range(len(ref_X_Y)):
        y = R[i]*np.sin(theta[i])+ref_X_Y[i][1]
        x = R[i]*np.cos(theta[i])+ref_X_Y[i][0]
        P.append([x,y])
    return np.array(P)

def _cost(ref_X_Y,theta,R):
    
    P = _p(ref_X_Y,theta,R)
    
    cost = np.zeros(len(R))
    for i in range(len(P)):
        for j in range(len(P)):
            if i==j: continue
            cost[i]+=np.sum((P[i]-P[j])**2)

    return cost

def _gradient(ref_X_Y,theta,R):
    
    P = _p(ref_X_Y,theta,R)
    
    gradient = np.zeros(len(R))
    cost = 0
    
    for i in range(len(P)):
        for j in range(len(P)):
            if i==j: continue
            gradient[i]+=                 2*np.dot( (P[i]-P[j]) , R[i]*np.array([-np.sin(theta[i]),np.cos(theta[i])]))
            
        for i in range(len(gradient)):
            if np.abs(np.sum(gradient[i]))>10e9:return None
    return np.array(gradient)

def gradient_descent(ref_X_Y,R,learning_rate=0.0002,iterations=30):
    theta = np.random.rand(len(ref_X_Y))
    cost = _cost(ref_X_Y,theta,R)

    m = len(R)
    cost_history = []
    theta_history=[]
    gradient_history=[]
    
    for it in range(iterations):
        gradient = _gradient(ref_X_Y,theta,R)
        theta = theta -(1/m)*learning_rate*(gradient)
        
        plot(ref_X_Y,P_t,theta,R,np.max(2*R))
        
        theta_history.append(theta)
        cost_history.append(_cost(ref_X_Y,theta,R))
        gradient_history.append(gradient)
    return theta, np.array(cost_history).T, np.array(theta_history), np.array(gradient_history).T

def plot(ref_X_Y,P_t,theta,R,lim):
    plt.cla()
    P = _p(ref_X_Y,theta,R)
    plt.scatter(ref_X_Y.T[0],ref_X_Y.T[1],marker='^')
    plt.scatter(P_t[0],P_t[1],marker='o')
    plt.scatter(P.T[0],P.T[1],marker='x')
    for i in range(len(ref_X_Y)):
        circle = plt.Circle(ref_X_Y[i],R[i],color='b',fill=False)
        plt.gca().add_patch(circle)
    plt.pause(0.02)

lim = np.max(2*R)
plt.xlim(-lim,lim)
plt.ylim(-lim,lim)

theta, cost_history, theta_history, gradient_history = gradient_descent(ref_X_Y,R)

fig,ax = plt.subplots(figsize=(12,8))
ax.set_ylabel('Cost')
ax.set_xlabel('Iterations')
for i in range(len(R)):
    ax.plot(range(len(cost_history[i])),cost_history[i])
