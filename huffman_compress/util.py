# The functions in this file are to be implemented by students.
'''
	Assignment 2
	Alan(Xutong) Zhao	1430631
	Yue Ma 				1434071
	LBL EB1
	Acknowledgement:	I received help from Junfeng Wen during office hour
						on March 4th, Friday. He explained the structure of 
						Huffman tree.

'''

import bitio
import huffman


'''
	Read a description of a Huffman tree from the given bit reader,
	and construct and return the tree. When this function returns, the
	bit reader should be ready to read the next bit immediately
	following the tree description.

	Huffman trees are stored in the following format:
		* TreeLeafEndMessage is represented by the two bits 00.
		* TreeLeaf is represented by the two bits 01, followed by 8 bits
			for the symbol at that leaf.
		* TreeBranch is represented by the single bit 1, followed by a
			description of the left subtree and then the right subtree.

	Args:
		bitreader: An instance of bitio.BitReader to read the tree from.

	Returns:
		A Huffman tree constructed according to the given description.
'''
def read_tree (bitreader):
	# bit == 1, TreeBranch
	if bitreader.readbit() == 1:
		tree = huffman.TreeBranch(read_tree(bitreader), read_tree(bitreader))
		return tree
	# bit == 0, could be either TreeLeaf(value) or TreeLeafEndMessage()
	else:
		# bit == 1, 01 - TreeLeaf(value)
		if bitreader.readbit() == 1:
			# read 8 bits for the symbol at this leaf
			value = bitreader.readbits(8)
			leaf = huffman.TreeLeaf(value)
			return leaf
		# bit == 0, 00 - TreeLeafEndMessage()
		else:
			endMsg = huffman.TreeLeafEndMessage()
			return endMsg


'''
	First, read a Huffman tree from the 'compressed' stream using your
	read_tree function. Then use that tree to decode the rest of the
	stream and write the resulting symbols to the 'uncompressed'
	stream.

	Args:
		compressed: A file stream from which compressed input is read.
		uncompressed: A writable file stream to which the uncompressed
			output is written.
'''
def decompress (compressed, uncompressed):
	bitreader = bitio.BitReader(compressed)
	bitwriter = bitio.BitWriter(uncompressed)
	tree = read_tree(bitreader)
	# Repeatedly read coded bits from the file, decode them using tree
	while True:
		decoded = huffman.decode(tree, bitreader)
		# As soon as you decode the end-of-message symbol, you should stop reading.
		if decoded is None:
			break
		# write the decoded byte to the uncompressed output
		bitwriter.writebits(decoded, 8)
	#bitwriter.flush()


'''
	Write the specified Huffman tree to the given bit writer.  The
	tree is written in the format described above for the read_tree
	function.

	DO NOT flush the bit writer after writing the tree.

	Args:
		tree: A Huffman tree.
		bitwriter: An instance of bitio.BitWriter to write the tree to.
'''
def write_tree (tree, bitwriter):
	# TreeBranch, bit = 1
	if isinstance(tree, huffman.TreeBranch):
		bitwriter.writebit(1)
		write_tree(tree.left, bitwriter)
		write_tree(tree.right, bitwriter)
	# TreeLeaf(value), bits = 01 + <ascii code for value>
	elif isinstance(tree, huffman.TreeLeaf):
		bitwriter.writebit(0)
		bitwriter.writebit(1)
		bitwriter.writebits(tree.value, 8)
	# TreeLeafEndMessage(), bits = 00
	elif isinstance(tree, huffman.TreeLeafEndMessage):
		bitwriter.writebit(0)
		bitwriter.writebit(0)

'''
	First write the given tree to the stream 'compressed' using the
	write_tree function. Then use the same tree to encode the data
	from the input stream 'uncompressed' and write it to 'compressed'.
	If there are any partially-written bytes remaining at the end,
	write 0 bits to form a complete byte.

	Args:
		tree: A Huffman tree.
		uncompressed: A file stream from which you can read the input.
		compressed: A file stream that will receive the tree description
			and the coded input data.
'''
def compress (tree, uncompressed, compressed):
	# write the given tree to the stream 'compressed' using the write_tree function
	bitwriter = bitio.BitWriter(compressed)
	write_tree(tree, bitwriter)

	# for reading bytes from the uncompressed input file
	bitreader = bitio.BitReader(uncompressed)
	
	# The function huffman.make_encoding_table takes tree and produces a dictionary 
	# mapping bytes to bit sequences; constructing this dictionary once before you 
	# start coding the message
	encodingTable = huffman.make_encoding_table(tree)
	
	# # for terminating the program
	# reachEnd = False
	
	# Read each byte from the uncompressed input file
	while True:
		try:
			inputByte = bitreader.readbits(8)
			# encode it using tree
			encoded = encodingTable[inputByte]
			for i in encoded:
				if i == True:
					bitwriter.writebit(1)
				else:
					bitwriter.writebit(0)
		except EOFError:
			encoded = encodingTable[None]
			for i in encoded:
				if i == True:
					bitwriter.writebit(1)
				else:
					bitwriter.writebit(0)
			break
	bitwriter.flush()

# if __name__ == '__main__':
	
# 	with open('index.html.huf', 'rb') as compressed:
# 		bitreader = bitio.BitReader(compressed)
# 		tree = read_tree(bitreader)
# 		while True:
# 			decoded = huffman.decode(tree, bitreader)
# 			if decoded is None:
# 				break
# 			print(chr(decoded), end = '')
	
	
# 	with open('wwwroot/huffman.bmp.huf','rb') as compressed:
# 		with open('wwwroot/index.html', 'wb') as uncompressed:
# 			decompress(compressed, uncompressed)

	
# 	with open('wwwroot/index.html', 'rb') as uncompressed:
# 		freqs = huffman.make_freq_table(uncompressed)
# 		tree = huffman.make_tree(freqs)
# 		encodingTable = huffman.make_encoding_table(tree)
# 		print(str(encodingTable))
				
		