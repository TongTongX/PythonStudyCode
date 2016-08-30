'''
	Alan(Xutong) Zhao	1430631
	Yue Ma 				1434071
	Section: EB1
	Assignment 1 Part 2

	Part2 running procedure:
	- Go into the client_soln_part2_base directory and make upload. Select the port by 
	arduino-port-select command if no port is detected.
	- Go back to the ZhaoMaAssign1Part2 directory and run the server by python3 server.py

	Acknowledgement: - I used graph.py and minheap.py that our profs developed in class.
					- I essentially used the read_city_graph() that I wrote for a previous
					weekly exercise.
					- I applied the same idea of Dijkstra to construct least_cost_path() 
					function, as well as the idea of handshake process, which my partner
					and I wrote for a CMPUT 274 assignment, to construct the communication
					portion of this program. 
					- I used some parts of the textserial.py to construct my setup portion
					and route finding process. (e.g. line = ser.readline())
					- I used built-in funcitons found at arduino.cc/en/Reference/HomePage.
					- I worked on some functions with Yu Zhu.

	MinHeap Note: Nodes are key-value pairs, stored in an array. The first element of 
			the pair is the key, the second is the value. However, in order to decide 
			the position of a node on the tree, the KEY is compared with other keys.
			I initially set the node in ((prev, curr), dist) format where (prev, curr) 
			is the key and dist is the value, but it is the value of prev that determines
			the relative position. For instance, ((2,3),0) is below ((1,3),1), i.e. the 
			min is ((1,3),1). Therefore, I changed the format to ((dist, prev, curr), None)
			where (dist, prev, curr) is the key with no value paired with it. 
	
	Error note: occasionally this error below occurs:

			  File "~/ZhaoMaAssign1Part2/minheap.py", line 31, in pop_min
    			r = self._array[0]
			IndexError: list index out of range
			
			Don't worry just ignore this error message and re-run the code. It is not the
			program's problem. 
'''

from graph import Graph
from minheap import MinHeap
from math import sqrt
import sys
import serial
import textserial
import time
import glob

'''
	Create a dictionary to store coordinates of all vertices
	Format: {vertex:[latitude, longitude]}
	Set it global so that it can be accessed in any function.
'''
coordinates = {}

'''
	Construct a graph corresponding to a city, each vertex represents
	a location, and each each edge represents a street.
	Argument: name of a file
	Return: a grpah (an instance of Graph() class)
'''
def read_city_graph(filename):
	#Format of a line of the file:
	#0 - V, 1 - vertex ID, 2 - vertex latitude, 3 - vertex longitude
	#0 - E, 1 - start ID, 2 - dest ID, 3 - edge name 
	global coordinates
	graph = Graph()
	with open(filename) as file:
		for line in file:
			line = line.strip().split(',', maxsplit = 3)
			if line[0] == 'V':
				graph.add_vertex(int(line[1]))
				lat = int(float(line[2])*100000)
				lon = int(float(line[3])*100000)
				coordinates[int(line[1])] = [lat,lon]
				#graph.add_coordinate(int(line[1]), lat, lon)
			elif line[0] == 'E':
				graph.add_edge(int(line[1]), int(line[2]))
				#graph.add_edgeName(int(line[1]), int(line[2]), line[3])
	return graph

'''
	Computes and returns the straight-line distance between the two
	vertices u and v.
	Args: u, v: The ids for two vertices that are the start and
				end of a valid edge in the graph.
	Returns: numeric value: the distance between the two vertices.
'''
def cost_distance(u,v):
	global coordinates
	uLat = coordinates[u][0]
	uLon = coordinates[u][1]
	vLat = coordinates[v][0]
	vLon = coordinates[v][1]
	distance = int(sqrt((uLat-vLat)**2 + (uLon-vLon)**2))

	return distance

'''
	Find and return the least cost path in graph from start vertex to dest vertex.
	Efficiency: If E is the number of edges, the run-time is O( E log(E) ).
				O(E) because each edge is traversed
				O(log(E)) due to use of MinHeap, instead of runners which takes O(E) 
					to extract the min value.
	Args:
		graph (Graph): The digraph defining the edges between the vertices.
		start: The vertex where the path starts. It is assumed that start is a vertex of graph.
		dest:  The vertex where the path ends. It is assumed that start is a vertex of graph.
		cost:  A function, taking the two vertices of an edge as parameters and returning the 
				cost of the edge. For its interface, see the definition of cost_distance.
	Returns:
		list: A potentially empty list (if no path can be found) of
		the vertices in the graph. If there was a path, the first
		vertex is always start, the last is always dest in the list.
		Any two consecutive vertices correspond to some
		edge in graph.
'''
def least_cost_path(graph, start, dest, cost):
	reached = {}
	# For faster implementation, use MinHeap to substitute runners
	tree = MinHeap()
	tree.add((0, start, start), None)
	while tree and dest not in reached:
		#print("tree: " + str(tree._array))
		(dist, prev, curr) = tree.pop_min()[0]
		if curr in reached:
			continue
		reached[curr] = prev
		for succ in graph.neighbours(curr):
			tree.add((dist + cost(curr, succ), curr, succ), None)
	if dest not in reached:
		return []
	#print("reached: ", reached)
	path = []
	v = dest
	while True:
		path.append(v)
		if path[-1] == start:
			break
		v = reached[v]
	path = path[::-1]
	#print("path: ", path)
	return path

'''
	wait for client's Acknowledgement in order to continue
'''
def waitingForACK():
	ACK = ser.readline().rstrip('\n')
	if ACK=='A':
		return True

'''
	Find the closest vertices in the roadmap of Edmonton to the start and end points
	Args: latitude and longitude of a point 
	Returns: the closest vertex to the point 
'''
def closestVert(lat,lon):
	global coordinates
	#near_position = []
	shortDist = 557865779647725222
	closestV = None
	for v,[a,b] in coordinates.items():
		dis = sqrt((lat-a)**2 +(lon-b)**2)
		if dis < shortDist:	
			shortDist = dis
			#near_position = [a,b]
			closestV = v	
	return closestV

'''
	communication between server and client
'''
def communication():
	global coordinates

	# wait for path request from the client
	# change the request line to ['R', int(xLat), int(xLon), int(yLat), int(yLon)]
	# for further calculations
	while True: 
		line = ser.readline().rstrip('\r\n')
		request = line.split()
		if len(request) == 5 and request[0] == 'R':
			print(line)
			for i in range(1,5):
				request[i] = int(request[i])
			break
		else: 
			communication()
	
	# find the shortest path between two points entered
	startVert = closestVert(request[1], request[2])
	endVert = closestVert(request[3], request[4])
	shortestPath = least_cost_path(edmonton, startVert, endVert, cost_distance)

	# sent the shortest path to client
	timeout = time.time() + 1;
	while True:
		print('N', len(shortestPath))
		print('N', len(shortestPath), file=ser)
		line = ser.readline().rstrip('\r\n')
		
		
		if time.time() > timeout or line == 'TIMEOUT':
			print('TIMEOUT. Restart the communication attempt.')
			communication()
		elif len(shortestPath) <= 0:
			# print('No path found. Restart the communication attempt.')
			print('E\n')
			print('E\n', file=ser)
			communication()		
		else: 
			break

	# wait for acknowledgement from client
	while True:
		line = ser.readline().rstrip('\r\n')
		if line == 'A':
			print(line)
			break

	# send waypoints
	for v in shortestPath: 
		wayPoint = ['W', coordinates[v][0], coordinates[v][1]]
		wayPointStr = ' '.join(str(i) for i in wayPoint)
		print(wayPointStr)
		print(wayPointStr, file=ser)
			
		# wait for the next acknowledgement from client
		timeout = time.time() + 1
		while True:
			if time.time() > timeout or line == 'TIMEOUT': 
				print('TIMEOUT. Restart the communication attempt.')
				communication() 
			if line == 'A':
				print(line)
				break

	# send the final ‘E’ character
	print('E\n')
	print('E\n', file=ser)

	# Restart the communication attempt
	communication()


'''
	process route finding requests here
'''
if __name__ == "__main__":
	edmonton = read_city_graph("edmonton-roads-2.0.1.txt")
	#print("Done importing Edmonton map to a graph.")
	
	try:
		# if one has an echo program:
		baud = 9600
		port = textserial.get_port()
		if port == None:
			print("No suitable port found, exiting")
			#return
		#print("Attempting to use an 'echo' program on",port)

		with textserial.TextSerial(port,baud,newline='\n') as ser:
			while True:
				communication()

	except serial.SerialException as exc:
		print("Failure. \n",exc)
	except OSError as exc: # error on Linux
		if exc.errno!=2:
			raise
		print("Failure. \n",exc)

	


