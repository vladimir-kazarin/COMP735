import sys


class Vertex:
    def __init__(self, node_id):
        self.priority = node_id.split('.')[0]
        self.id = node_id
        self.adjacent = {}
        # Set distance to infinity for all nodes
        self.distance = sys.maxsize
        # Mark all nodes unvisited
        self.visited = False
        # Predecessor
        self.previous = None

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

    def set_distance(self, dist):
        self.distance = dist

    def get_distance(self):
        return self.distance

    def set_previous(self, prev):
        self.previous = prev

    def set_visited(self):
        self.visited = True

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])

class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node_id):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node_id)
        self.vert_dict[node_id] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def get_root(self):
        min = 0
        for k, v in self.vert_dict.items():
            priority = int(v.priority)
            if min == 0:
                min = v
                continue

            if int(min.priority) > int(v.priority):
                min = v
            elif int(min.priority) == int(v.priority):
                # compare mac address
                mac = v.id.split('.')
                min_mac = min.id.split('.')
                for octet in mac:
                    for min_octet in min_mac:
                        if int(min_octet) > int(octet):
                            min = v
        return min

    def add_edge(self, frm, to, cost=0):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

    def get_vertices(self):
        return self.vert_dict.keys()

    def set_previous(self, current):
        self.previous = current

    def get_previous(self, current):
        return self.previous


def shortest(v, path):
    ''' make shortest path from v.previous'''
    if v.previous:
        path.append(v.previous.get_id())
        shortest(v.previous, path)
    return


import heapq


def dijkstra(aGraph, start):
    print '''Dijkstra's shortest path'''
    # Set the distance for the start node to zero
    start.set_distance(0)

    # Put tuple pair into the priority queue
    unvisited_queue = [(v.get_distance(), v) for v in aGraph]
    heapq.heapify(unvisited_queue)

    while len(unvisited_queue):
        # Pops a vertex with the smallest distance
        uv = heapq.heappop(unvisited_queue)
        current = uv[1]
        current.set_visited()

        # for next in v.adjacent:
        for next in current.adjacent:
            # if visited, skip
            if next.visited:
                continue
            new_dist = current.get_distance() + current.get_weight(next)

            if new_dist < next.get_distance():
                next.set_distance(new_dist)
                next.set_previous(current)
                print 'updated : current = %s next = %s new_dist = %s' \
                        % (current.get_id(), next.get_id(), next.get_distance())
            else:
                print 'not updated : current = %s next = %s new_dist = %s' \
                        % (current.get_id(), next.get_id(), next.get_distance())

        # Rebuild heap
        # 1. Pop every item
        while len(unvisited_queue):
            heapq.heappop(unvisited_queue)
        # 2. Put all vertices not visited into the queue
        unvisited_queue = [(v.get_distance(), v) for v in aGraph if not v.visited]
        heapq.heapify(unvisited_queue)


if __name__ == '__main__':

    g = Graph()

    g.add_vertex('32768.0200.0000.1111')  # a
    g.add_vertex('28672.0200.0000.2222')  # b
    g.add_vertex('32768.0200.0000.3333')  # c
    g.add_vertex('36864.0200.0000.4444')  # d
    g.add_vertex('40960.0200.0000.5555')  # e
    g.add_vertex('32768.0200.0000.6666')  # f

    g.add_edge('32768.0200.0000.1111', '28672.0200.0000.2222', 7)
    g.add_edge('32768.0200.0000.1111', '32768.0200.0000.3333', 9)
    g.add_edge('32768.0200.0000.1111', '32768.0200.0000.6666', 14)
    g.add_edge('28672.0200.0000.2222', '32768.0200.0000.3333', 10)
    g.add_edge('28672.0200.0000.2222', '36864.0200.0000.4444', 15)
    g.add_edge('32768.0200.0000.3333', '36864.0200.0000.4444', 11)
    g.add_edge('32768.0200.0000.3333', '32768.0200.0000.6666', 2)
    g.add_edge('36864.0200.0000.4444', '40960.0200.0000.5555', 6)
    g.add_edge('40960.0200.0000.5555', '32768.0200.0000.6666', 9)

    print 'Graph data:'
    for v in g:
        for w in v.get_connections():
            vid = v.get_id()
            wid = w.get_id()
            print '( %s , %s, %3d)' % (vid, wid, v.get_weight(w))

    dijkstra(g, g.get_root())

    for t in ['36864.0200.0000.4444', '40960.0200.0000.5555', '32768.0200.0000.6666']:
        target = g.get_vertex(t)
        path = [t]
        shortest(target, path)
        print 'The shortest path for %s : %s' % (t, path[::-1])

