#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>

#define INPUT_SIZE 36

// XOR Mask Generator Function (Sequential Updates)
uint8_t generate_mask(uint32_t *state) {
    uint32_t eax = *state;  
    uint32_t rdi, rdi_2, ecx = 0xC74F08C9;

    eax = eax * 0x14A + 0x64;
    rdi = ((uint64_t)eax * ecx) >> 32;
    rdi_2 = ((eax - rdi) >> 1) + rdi;
    rdi_2 >>= 11;
    eax -= rdi_2 * 0x8FF;

    *state = eax;  

    return (uint8_t)(eax & 0xFF);  // Return lowest byte 
}

int validate_and_print(const uint8_t *input) {
    const uint8_t stored_key[INPUT_SIZE] = {
        0xdd, 0x9a, 0xde, 0x4e, 0x69, 0xe1, 0xe9, 0x2c,
        0xd2, 0x4e, 0xec, 0xe7, 0x18, 0x26, 0x6a, 0x56,
        0x79, 0xd8, 0xa3, 0x55, 0x72, 0xbc, 0x76, 0xc4,
        0x0c, 0x0f, 0x9b, 0xbe, 0xc6, 0x81, 0xe2, 0x41,
        0x47, 0xa0, 0xf4, 0x26
    };

    uint32_t mask_state = 1;  // Reset state for each validation
    int valid = 0;

    for (int i = 0; i < INPUT_SIZE; i++) {
        uint8_t mask = generate_mask(&mask_state);

        if ((input[i] ^ mask) != stored_key[i]) {
            printf("%d %s\n", valid, input);
            return valid;  
        }

        valid += 1;
    }

    printf("Correct input!: %s\n", input);
    return valid;
}
int main() {

    uint8_t input[INPUT_SIZE] = {
        '-', '-', '-', '-', '-', '-', '-', '-', '-',
        '-', '-', '-', '-', '-', '-', '-', '-', '-',
        '-', '-', '-', '-', '-', '-', '-', '-', '-',
        '-', '-', '-', '-', '-', '-', '-', '-', '-'
    };

    for (int i = 0; i < INPUT_SIZE; i++) {
        uint8_t original = input[i];  // Save original value

        for (int character = 33; character < 127; character++) {
            input[i] = character;
            int result = validate_and_print(input);
            if (result > i) {
                break;
            }
        }

        // Reset input[i] if no valid character was found
        if (validate_and_print(input) <= i) {
            input[i] = original;
        }
        //Comment this out if you don't want the animation
        usleep(50000); 
    }

    return 0;
}

