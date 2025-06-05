e = 3
N = 140435453730354645791411355194663476189925572822633969369789174462118371271596760636019139860253031574578527741964265651042308868891445943157297334529542262978581980510561588647737777257782808189452048059686839526183098369088517967034275028064545393619471943508597642789736561111876518966375338087811587061841
C_final = 49352042282005059128581014505726171900605591297613623345867441621895112187636996726631442703018174634451487011943207283077132380966236199654225908444639768747819586037837300977718224328851698492514071424157020166404634418443047079321427635477610768472595631700807761956649004094995037741924081602353532946351

original_ciphertext = (C_final + N) // (2**164)

def integer_cube_root(n):
    if n == 0:
        return 0
    low, high = 0, n
    while low <= high:
        mid = (low + high) // 2
        cube = mid ** 3
        if cube == n:
            return mid
        elif cube < n:
            low = mid + 1
        else:
            high = mid - 1
    return high

m = integer_cube_root(original_ciphertext)
if m**3 != original_ciphertext:
    for offset in range(-5, 6):
        test_m = m + offset
        if test_m**3 == original_ciphertext:
            m = test_m
            break

def int_to_bytes(n):
    byte_length = (n.bit_length() + 7) // 8
    return n.to_bytes(byte_length, 'big')

try:
    flag_bytes = int_to_bytes(m)
    flag = flag_bytes.decode('ascii')
    print(f"\n FLAG: {flag}")
except Exception as e:
    print(f"Error decoding flag: {e}")


