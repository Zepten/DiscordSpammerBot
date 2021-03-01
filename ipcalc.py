# IP-калькулятор
def calculate(ip, bitmask):
    T = 20 # Tab for displaying addresses

    # Returns a string of dot-separated list values
    def dot_sep(l):
        if l == 'N/A':
            return l
        else:
            return '.'.join(map(str, l))
    
    output = '```pas'

    # Print parsed and clamped parameters
    output += '\n'
    output += 'IP-адрес:'.ljust(T) + dot_sep(ip) + '\n'
    output += 'Номер маски:'.ljust(T) + str(bitmask) + '\n'

    # Netmask
    netmask = [0, 0, 0, 0]
    for i in range(bitmask >> 3):
        netmask[i] = 255
    if bitmask < 32:
        netmask[bitmask >> 3] = ~(255 >> bitmask % 8) + 256
    output += 'Маска:'.ljust(T) + dot_sep(netmask) + '\n'

    # Wildcard
    wildcard = [~i + 256 for i in netmask]
    output += 'Обратная маска:'.ljust(T) + dot_sep(wildcard) + '\n'

    # Network
    network = [ip[i] & netmask[i] for i in range(4)]
    output += 'Адрес сети:'.ljust(T) + dot_sep(network) + '\n'

    # Broadcast
    if bitmask < 32:
        broadcast = [ip[i] | wildcard[i] for i in range(4)]
    else:
        broadcast = 'N/A'
    output += 'Широковещательный:'.ljust(T) + dot_sep(broadcast) + '\n'

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

    output += 'Минимальный хост:'.ljust(T) + dot_sep(hostmin) + '\n'
    output += 'Максимальный хост:'.ljust(T) + dot_sep(hostmax) + '\n'

    if (hosts == 'N/A'):
        output += 'Хостов/сеть:'.ljust(T) + hosts + '\n'
    else:
        output += 'Хостов/сеть:'.ljust(T) + '{:,}'.format(hosts) + '\n'

    # Network class
    octet = bin(network[0])
    output += 'Класс:'.ljust(T)
    if octet.startswith('0b0'):
        output += 'A' + '\n'
    elif octet.startswith('0b10'):
        output += 'B' + '\n'
    elif octet.startswith('0b110'):
        output += 'C' + '\n'
    elif octet.startswith('0b1110'):
        output += 'D' + '\n'
    elif octet.startswith('0b1111'):
        output += 'E' + '\n'
    
    output += '```'
    return output
