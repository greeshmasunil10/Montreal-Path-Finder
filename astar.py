class vertex():

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.pos = position
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.pos == other.pos


def calc(map, start, end):
    startnode = vertex(None, start)
    startnode.g = startnode.h = startnode.f = 0
    destination = vertex(None, end)
    destination.g = destination.h = destination.f = 0
    open_list = []
    closed_list = []
    open_list.append(startnode)
    while len(open_list) > 0:
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
        open_list.pop(current_index)
        closed_list.append(current_node)
        if current_node == destination:
            path = []
            current = current_node
            while current is not None:
                path.append(current.pos)
                current = current.parent
            return path[::-1] # Return reversed path
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares
            node_position = (current_node.pos[0] + new_position[0], current_node.pos[1] + new_position[1])
            if node_position[0] > (len(map) - 1) or node_position[0] < 0 or node_position[1] > (len(map[len(map)-1]) -1) or node_position[1] < 0:
                continue
            if map[node_position[0]][node_position[1]] != 0:
                continue
            new_node = vertex(current_node, node_position)
            children.append(new_node)
        for kid in children:
            for closed_child in closed_list:
                if kid == closed_child:
                    continue
            kid.g = current_node.g + 1
            kid.h = ((kid.pos[0] - destination.pos[0]) ** 2) + ((kid.pos[1] - destination.pos[1]) ** 2)
            kid.f = kid.g + kid.h
            for open_node in open_list:
                if kid == open_node and kid.g > open_node.g:
                    continue

            open_list.append(kid)


def main(maze,size,start,end):

    path = calc(maze, start, end)
    return path


if __name__ == '__main__':
    main()