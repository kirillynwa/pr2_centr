import vk_api
import networkx as nx
import matplotlib.pyplot as plt
import time
start_time = time.time()

access_token = 'vk1.a.AEAygR6PdYUaDeLqDAhUjcj6pucYbJQB9QJaQhBP78CNT6J9QjbAeAL9p7DVccsYEqUqKXdhRLsvzgxtVeWNIFYBqIc-G7VK4yuCyvEiuG7ovBVKGbiSzJvF2fBo1cT3M--HZfZaEosNa4auvgrNdHNlleKswN2gI8TH7kd0YtdbZBavTcGiGymAIEBJi3ciT-ZhJdMMyplpSsPYZuI1mw'

try:
    vk_session = vk_api.VkApi(token=access_token)
except Exception as error:
    print(error)

vk = vk_session.get_api()

G = nx.Graph()
users = vk.friends.search(id=412981588)
users_id = []
for u in users['items']:
    users_id.append(u['id'])

for u in users_id:
    G.add_edge(412981588, u)

dict = vk.friends.getMutual(source_uid=412981588, target_uids=users_id)
for key in dict:
    for ids in key['common_friends']:
        G.add_edge(ids, key['id'])

print("--- %s seconds ---" % (time.time() - start_time))


color_map = []
for node in G:
    if node == 412981588:
        color_map.append('blue')
    else:
        color_map.append('red')

nx.draw_spring(G, with_labels=False, node_color=color_map, node_size=100)
plt.savefig('result.png')
plt.show()


with open("result.txt", "a") as file:
    nodes = sorted(list(nx.betweenness_centrality(G).items()), key=lambda i: i[1], reverse=True)
    print('Центральность по посредничеству {id:', nodes[0][0], ', частота выбора:', nodes[0][1], '}', file=file)

    nodes = sorted(list(nx.closeness_centrality(G).items()), key=lambda i: i[1], reverse=True)
    print('Центральность по близости {id:', nodes[0][0], ', значение:', nodes[0][1], '}', file=file)

    nodes = sorted(list(nx.eigenvector_centrality(G).items()), key=lambda i: i[1], reverse=True)
    print('Центральность по собственному значению {id:', nodes[0][0], ', значение:', nodes[0][1], '}', file=file)


