# Finding The Source Of Rumor in Large Scale Social Network

Various algorithms have been proposed in recent years to estimate rumour source in a social network, but very few have been implemented in real world.Previous work have mainly done by considering the whole network structures where they thrive to reduce the time complexity and increase the accuracy. We find out source of rumor by considering the modular structure of the social network and thereby reducing the search space. We have successfully proposed a nested model in order to showcase its effectiveness in tackling rumor spread in large social networks like Twitter. The nested model uses the modularity of the network to find out the most likely module where the source belong and then finds the source in that most likely module. We model the spreading of rumor in social network by using the popular Susceptible-infected (SI) model and then construct maximum likelihood estimator as proposed in Shah and Zaman original paper, originally used to estimate the source of computer virus in a network. This estimator is based upon a novel combinatorial quantity termed as rumor centrality. We evaluate our algorithm using a large data set from Twitter, Higgs-retweet-network and simulations shows that the estimator either finds out the source exactly or within few hops from the actual source ________ of the time, when the diameter of the networks varies between 8 and 13 hops. And finally, we statistically compare the accuracy of the algorithm for different size and type of social networks.

## Prerequisites
1. Libraries that needs to be installed
   _ Python2.7
   _ ndlib
   _ pandas
   _ networkx module
