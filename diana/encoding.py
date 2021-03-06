import struct

ENCODERS = {}

def struct_encoder_for(char):
	format_expr = "<{}".format(char)
	def st_encode(fmt, data):
		if not data:
			raise ValueError("Not enough data")
		return (struct.pack(format_expr, data[0]) +
				encode(fmt[1:], data[1:]))
	return st_encode

for base_format in 'bBiIf':
	ENCODERS[base_format] = struct_encoder_for(base_format)
ENCODERS['s'] = struct_encoder_for('h')
ENCODERS['S'] = struct_encoder_for('H')

def encode_unicode_string(fmt, data):
	subject = data[0]
	block = subject.encode('utf-16le')
	output = struct.pack('<I', 1 + len(block)//2) + block + b'\x00\x00'
	return output + encode(fmt[1:], data[1:])
ENCODERS['u'] = encode_unicode_string

def encode_array(fmt, data):
	array_elements = data[0]
	stack_depth = 0
	for index, element in enumerate(fmt):
		if element == '[':
			stack_depth += 1
		elif element == ']':
			stack_depth -= 1
		if stack_depth == 0:
			end_index = index
			break
	else:
		raise ValueError('Bad format; unbalanced brackets')
	remainder_fmt = fmt[(end_index+1):]
	remaining_data = data[1:]
	remainder = encode(fmt[(end_index+1):], data[1:])
	this_fmt = fmt[1:end_index]
	return b''.join(encode(this_fmt, x) for x in array_elements) + remainder
ENCODERS['['] = encode_array

def encode_star(fmt, data):
	if len(data) != 1:
		raise ValueError('Need single bytestring for *')
	return data[0]
ENCODERS['*'] = encode_star

def encode(fmt, data):
	if not fmt:
		if data:
			raise ValueError('Too much data')
		return b''
	return ENCODERS[fmt[0]](fmt, data)

DECODERS = {}
def struct_decoder_for(char):
	format_expr = "<{}".format(char)
	expected_size = struct.calcsize(format_expr)
	def st_decode(fmt, data, handle_trail):
		if len(data) < expected_size:
			raise ValueError("Truncated data")
		decoded, = struct.unpack(format_expr, data[:expected_size])
		rest = decode(fmt[1:], data[expected_size:], handle_trail)
		return (decoded,) + rest
	return st_decode

for base_format in 'bBiIf':
	DECODERS[base_format] = struct_decoder_for(base_format)
DECODERS['s'] = struct_decoder_for('h')
DECODERS['S'] = struct_decoder_for('H')

def decode_unicode_string(fmt, data, handle_trail):
	if len(data) < 4:
		raise ValueError('Truncated data')
	#print("\t",":".join("{:02x}".format(c) for c in data[:4]))
	str_len_padded, = struct.unpack('<I', data[:4])
	#print("\t str_len_padded: ",str_len_padded)
	#print("\t str_len_padded 2: ",2147483648-str_len_padded)
	#print("\t str_len_padded 2: ",str_len_padded)

	#print("data:")
	#for dc in chunks(data,8):
	#	print(" ".join("{:02x}".format(c) for c in dc))
	if str_len_padded == 0:
		raise ValueError('Zero-length string (no null trailer?)')
	data = data[4:]
	#print('\t',"Len(data) =",len(data))
	#if (str_len_padded == 
	if len(data) < (str_len_padded * 2):
		#print("\t","Nyaaa~")
		raise ValueError('Truncated data')
	str_len = str_len_padded - 1
	str_data = data[:(str_len * 2)].decode('utf-16le')
	data = data[(str_len*2):]
	if data[0] != 0 or data[1] != 0:
		raise ValueError('null trailer missing')
	return (str_data,) + decode(fmt[1:], data[2:], handle_trail)
DECODERS['u'] = decode_unicode_string

#def decode_unicode_string_bad(fmt, data, handle_trail):
#	if len(data) < 4:
#		raise ValueError('Truncated data')
#	data = data[4:] # kill length, it's a bad string
#	str_data=""
#	while True:
#		str_data = str_data + data[:1].decode('utf-16le')
#		print(str_data)
#		data = data[1:]
#		if data[0] == 0 and data[1] == 0: # null terminator found
#			break # break
#	# return string and tell to decode remaining bytes as remaining fmt
#	return (total_str_data,) + decode(fmt[1:], data[2:], handle_trail)
#DECODERS['U'] = decode_unicode_string_bad
	
def decode_array(fmt, data, handle_trail):
	stack_depth = 0
	for index, element in enumerate(fmt):
		if element == '[':
			stack_depth += 1
		elif element == ']':
			stack_depth -= 1
		if stack_depth == 0:
			end_index = index
			break
	else:
		raise ValueError('Bad format; unbalanced brackets')
	remainder_fmt = fmt[(end_index+1):]
	this_fmt = fmt[1:end_index]
	matches = []
	try:
		def internal_handle_trail(trail):
			nonlocal data
			data = trail
			return ()
		while True:
			inner_decode = decode(this_fmt, data, handle_trail=internal_handle_trail)
			matches.append(inner_decode)
	except ValueError:
		pass
	return (matches,) + decode(remainder_fmt, data, handle_trail)
DECODERS['['] = decode_array

def decode_star(fmt, data, handle_trail):
	return (data,) + handle_trail(b'')
DECODERS['*'] = decode_star

def handle_trail_error(trailer):
	if not trailer:
		return ()
	raise ValueError('Trailing bytes')

def chunks(l, n): # i use this for debug xd
	"""Yield successive n-sized chunks from l."""
	for i in range(0, len(l), n):
		yield l[i:i + n]
def decode(fmt, data, handle_trail=handle_trail_error):
	#print(DECODERS.keys())
	#print("fmt:\n\t"," ".join("{:02x}".format(ord(c)) for c in fmt)," || ",fmt)
	#print("data:")
	#for dc in chunks(data,8):
	#	print(" ".join("{:02x}".format(c) for c in dc))
	if fmt == '':
		return handle_trail(data)
	return DECODERS[fmt[0]](fmt, data, handle_trail)

