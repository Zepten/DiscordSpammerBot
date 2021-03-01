# IP-калькулятор
def calculate(ip, bitmask):
    T1 = 20 # Tab for displaying base-10 addresses
    T2 = 17 # Tab for displaying base-2 addresses

    clamp_byte = lambda b: max(0, min(b, 255)) # Returns a clamped number value between 0 and 255
    clamp_mask = lambda m: max(0, min(m, 32))  # Returns a clamped number value between 0 and 32
    to_bin = lambda x: '{:08b}'.format(x)      # Returns a string of formatted binary value
    # Returns a string of dot-separated list values
    def dot_sep(l):
        if l == 'N/A':
            return l
        else:
            return '.'.join(map(str, l))

    # Returns a string of dot-separated binary list values
    def bin_dot_sep(l):
        if l == 'N/A':
            return l
        else:
            return '.'.join(map(to_bin, l))
    
    output = '```pas'

    # IP parsing
    try:
        ip = list(map(int, ip.split('.')))
    except:
        output = 'Я думаю, это точно не IP-адрес...'
        return output

    if len(ip) > 4:
        output = 'В IP-адресе должно быть **4** октета.\n*На самом деле надо ввести хотя бы один...*```'
        return output
    else:
        while len(ip) < 4:
            ip.append(0)

    ip = [clamp_byte(i) for i in ip]

    # Bitmask parsing
    try:
        bitmask = clamp_mask(int(bitmask))
    except:
        output = '```Маску введи нормально пж.\nЕсли что, это должно быть число от 0 до 32.```'
        return output

    # Print parsed and clamped parameters
    output += '\n'
    output += 'IP-адрес:'.ljust(T1) + dot_sep(ip).ljust(T2) + bin_dot_sep(ip) + '\n'
    output += 'Номер маски:'.ljust(T1) + str(bitmask) + '\n'

    # Netmask
    netmask = [0, 0, 0, 0]
    for i in range(bitmask >> 3):
        netmask[i] = 255
    if bitmask < 32:
        netmask[bitmask >> 3] = ~(255 >> bitmask % 8) + 256
    output += 'Маска:'.ljust(T1) + dot_sep(netmask).ljust(T2) + bin_dot_sep(netmask) + '\n'

    # Wildcard
    wildcard = [~i + 256 for i in netmask]
    output += 'Обратная маска:'.ljust(T1) + dot_sep(wildcard).ljust(T2) + bin_dot_sep(wildcard) + '\n'

    # Network
    network = [ip[i] & netmask[i] for i in range(4)]
    output += 'Адрес сети:'.ljust(T1) + dot_sep(network).ljust(T2) + bin_dot_sep(network) + '\n'

    # Broadcast
    if bitmask < 32:
        broadcast = [ip[i] | wildcard[i] for i in range(4)]
    else:
        broadcast = 'N/A'
    output += 'Широковещательный:'.ljust(T1) + dot_sep(broadcast).ljust(T2) + bin_dot_sep(broadcast) + '\n'

    # Hosts
    hosts = 2 ** (32 - bitmask) - 2

    if hosts > 0:
        # HostMin
        hostmin = network
        hostmin[3] += 1

        # HostMax
        hostmax = broadcast
        hostmax[3] -= 1
    else:
        hostmin = 'N/A'
        hostmax = 'N/A'
        hosts = 'N/A'

    output += 'Мин. хост:'.ljust(T1) + dot_sep(hostmin).ljust(T2) + bin_dot_sep(hostmin) + '\n'
    output += 'Макс. хост:'.ljust(T1) + dot_sep(hostmax).ljust(T2) + bin_dot_sep(hostmax) + '\n'

    if (hosts == 'N/A'):
        output += 'Хостов/сеть:'.ljust(T1) + hosts.ljust(T2) + '\n'
    else:
        output += 'Хостов/сеть:'.ljust(T1) + '{:,}'.format(hosts).ljust(T2) + '\n'

    # Network class
    octet = to_bin(network[0])
    output += 'Класс:'.ljust(T1)
    if octet.startswith('0'):
        output += 'A' + '\n'
    elif octet.startswith('10'):
        output += 'B' + '\n'
    elif octet.startswith('110'):
        output += 'C' + '\n'
    elif octet.startswith('1110'):
        output += 'D' + '\n'
    elif octet.startswith('1111'):
        output += 'E - Экспериментальное адресное пространство' + '\n'
    
    output += '```'
    return output
