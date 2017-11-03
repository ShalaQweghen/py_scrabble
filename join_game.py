import socket, sys, re, threading

def find_own_ip():
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

  try:
    s.connect(('10.255.255.255', 1))
    ip = s.getsockname()[0]
  except:
    ip = '127.0.0.1'
  finally:
    s.close()

  return ip

def check_ip(ip, server):
  s = socket.socket()

  try:
    val = s.connect_ex((ip, 12345))
  except socket.error:
    s.close()

  if val:
    s.close()

  # connect_ex returns 0 if socket connects
  if val == 0:
    server.append(s)

def find_server():
  own_ip = find_own_ip()
  # ip address except for the last number
  base = re.match('(\d+\.\d+\.\d+\.)', own_ip).groups()[0]
  # Use threads to make it faster
  threads = []
  # serv is an array in order to modify it in another method
  serv = []

  # Check all the possible ips in range
  for i in range(0, 256):
    ip = base + str(i)
    threads.append(threading.Thread(target=check_ip, args=(ip, serv)))
    threads[i].start()

  # Join threads to wait all to finish before returning
  for i in range(0, 256):
    threads[i].join()

  if serv:
    return serv[0]
  else:
    return None

def join_game(option):
  p = '(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])'
  ip_p = p + '\.' + p + '\.' + p + '\.' + p
  port = 12345

  if opt == 'auto':
    print('\nScanning LAN for a hosted game... Please wait...')

    server = find_server()

    if not server:
      print('\nNo hosted games were found!')

      sys.exit()

  elif re.fullmatch(ip_p, opt):
    server = socket.socket()
    server.connect((opt, port))
  else:
    print('Usage: python3 join_game.py <ip_address>\n       python3 join_game.py auto')

    sys.exit()

  print('\nConnected to the game on {}:{}... Waiting for the opponent(s)...'.format(server.getsockname()[0], port))

  s_input = server.makefile('r')
  s_output = server.makefile('w')

  line = s_input.readline()

  while line:
    print(line, end="")

    if line.strip().endswith(':'):
      answer = input()
      s_output.write(answer + '\n')
      s_output.flush()

    line = s_input.readline()

  server.close()

try:
  opt = sys.argv[1]
except IndexError:
  print('Usage: python3 join_game.py <ip_address>\n       python3 join_game.py auto')
else:
  join_game(opt)


