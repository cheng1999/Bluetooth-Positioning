#!/usr/bin/env python
import numpy as np
from matplotlib import pyplot as plt
plt.style.use(['ggplot'])

GATEWAYS = np.array([[0,0],[1,1],[1,0],[0,1]])*50

beacon = np.random.rand(2)*50

# computing the distance betwen beacon and GATEWAYS
def _dist(GATEWAYS,P_target):
    d = []
    for i in range(len(GATEWAYS)):
        d.append(np.linalg.norm(GATEWAYS[i]-P_target))
        #d.append(np.sum((GATEWAYS[i]-beaconarget)**2)**.5)
    return np.array(d)

beacon = np.random.rand(2)*50
R = _dist(GATEWAYS,beacon)


# convert polar to cartesian coordinate
def _p(GATEWAYS,theta,R):
    P = []
    for i in range(len(GATEWAYS)):
        y = R[i]*np.sin(theta[i])+GATEWAYS[i][1]
        x = R[i]*np.cos(theta[i])+GATEWAYS[i][0]
        P.append([x,y])
    return np.array(P)

# cost function
def _cost(GATEWAYS,theta,R):
    
    P = _p(GATEWAYS,theta,R)
    
    cost = np.zeros(len(R))
    for i in range(len(P)):
        for j in range(len(P)):
            if i==j: continue
            cost[i]+=np.sum((P[i]-P[j])**2)

    return cost

# computing the gradient of cost function
def _gradient(GATEWAYS,theta,R):
    
    P = _p(GATEWAYS,theta,R)
    
    gradient = np.zeros(len(R))
    cost = 0
    
    for i in range(len(P)):
        for j in range(len(P)):
            if i==j: continue
            gradient[i]+=2*np.dot( (P[i]-P[j]) , R[i]*np.array([-np.sin(theta[i]),np.cos(theta[i])]))
            
        for i in range(len(gradient)):
            if np.abs(np.sum(gradient[i]))>10e9:return None
    return np.array(gradient)

# gradient descent algorithm
def gradient_descent(GATEWAYS,R,learning_rate=0.0002,iterations=30):
    theta = np.random.rand(len(GATEWAYS))
    cost = _cost(GATEWAYS,theta,R)

    m = len(R)
    cost_history = []
    theta_history=[]
    gradient_history=[]
    
    for it in range(iterations):
        gradient = _gradient(GATEWAYS,theta,R)
        theta = theta -(1/m)*learning_rate*(gradient)
        
        plot(GATEWAYS,beacon,theta,R,np.max(2*R))
        
        theta_history.append(theta)
        cost_history.append(_cost(GATEWAYS,theta,R))
        gradient_history.append(gradient)
    return theta, np.array(cost_history).T, np.array(theta_history), np.array(gradient_history).T

# plot to animate the numerical progress
def plot(GATEWAYS,beacon,theta,R,lim):
    plt.cla()
    P = _p(GATEWAYS,theta,R)
    plt.scatter(GATEWAYS.T[0],GATEWAYS.T[1],marker='^')
    plt.scatter(beacon[0],beacon[1],marker='o')
    plt.scatter(P.T[0],P.T[1],marker='x')
    for i in range(len(GATEWAYS)):
        circle = plt.Circle(GATEWAYS[i],R[i],color='b',fill=False)
        plt.gca().add_patch(circle)
    plt.pause(0.02)

lim = np.max(2*R)
plt.xlim(-lim,lim)
plt.ylim(-lim,lim)

theta, cost_history, theta_history, gradient_history = gradient_descent(GATEWAYS,R)

fig,ax = plt.subplots(figsize=(12,8))
ax.set_ylabel('Cost')
ax.set_xlabel('Iterations')
for i in range(len(R)):
    ax.plot(range(len(cost_history[i])),cost_history[i])
