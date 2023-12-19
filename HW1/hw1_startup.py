########################################################
#
# CMPSC 441: Homework 1
#
########################################################


########################################################
# 0. Your name and email address
########################################################

student_name = 'Ilaaksh Mishra'
student_email = 'ijm5304@psu.edu'


########################################################
### 1. Sequences
########################################################

def list_add(l1, l2):
    combined_list = l1 + l2
    unique_elements = set(combined_list)
    result_list = list(unique_elements)
    return result_list

def dict_extend(dict1, dict2):
    result_dict = {}
    for key in dict1.keys() | dict2.keys():
        value1 = dict1.get(key, None)
        value2 = dict2.get(key, None)
        if value1 is not None and value2 is not None:
            result_dict[key] = [value1, value2]
        elif value1 is not None:
            result_dict[key] = [value1]
        elif value2 is not None:
            result_dict[key] = [value2]
    return result_dict


def dict_invert(dct):
    inv_dct = dict()

    for key, value in dct.items():
        inv_dct.setdefault(value, list()).append(key)
    return inv_dct

########################################################
### 2. List Comprehension
########################################################

def list_product(l1, l2):
    result = []
    if l1 and l2:
        for x in l1:
            for y in l2:
                result.append([x, y])
    return result


def list_flatten(list_of_seqs):
    flattened_list = []
    for seqs in list_of_seqs:
        for item in seqs:
            flattened_list.append(item)
    return flattened_list

def dict_to_table(dct):
    result = []

    keys = list(dct.keys())
    values = list(dct.values())

    result.append(tuple(keys))

    for i in range(len(values[0])):
        row = [values[j][i] for j in range(len(keys))]
        result.append(tuple(row))

    return result

def nlargest(dct, n):
    sorted_items = sorted(dct.items(), key=lambda item: item[1], reverse=True)
    result = {}
    for i in range(min(n, len(sorted_items))):
        key, value = sorted_items[i]
        result[key] = value
    return result

def unique_values(list_of_dicts):
    unique_vals = []
    for dct in list_of_dicts:
        for value in dct.values():
            if value not in unique_vals:
                unique_vals.append(value)
    return unique_vals



#########################################################
# 3. Generators
########################################################

def prefixes(seq):
    input_length= len(seq)+1
    for i in range(0, input_length):
        yield seq[:i]

def suffixes(seq):
    length = len(seq)
    for i in range(length, -1, -1):
        yield seq[i:]



########################################################
# 4. Other algorithms
########################################################

def encode(input_string):
    if not input_string:
        return ""

    encoded = []
    count = 1
    prev_char = input_string[0]

    for char in input_string[1:]:
        if char == prev_char:
            count += 1
        else:
            encoded.append(str(count) + prev_char)
            count = 1
            prev_char = char

    encoded.append(str(count) + prev_char)

    return "".join(encoded)

def decode(encoded_string):
    decoded = []
    count = ""

    for char in encoded_string:
        if char.isdigit():
            count += char
        else:
            decoded.append(char * int(count))
            count = ""
    return "".join(decoded)

def camel_case(var_name):
    words = var_name.split('_')
    if len(words) == 1 and words[0] == '':
        return ""
    return words[0].lower() + ''.join(w.capitalize() for w in words[1:])

########################################################
### 5. Fraction class
########################################################

class Fraction:
    def __init__(self, numerator, denominator):
        if denominator == 0:
            raise ZeroDivisionError(f"{numerator}/{denominator}")
        self.numerator = numerator
        self.denominator = denominator

    def get_fraction(self):
        return (self.numerator, self.denominator)

    def __neg__(self):
        return Fraction(-self.numerator, self.denominator)

    def __add__(self, other):
        common_denominator = self.denominator * other.denominator
        new_numerator = (self.numerator * other.denominator) + (other.numerator * self.denominator)
        return Fraction(new_numerator, common_denominator)

    def __sub__(self, other):
        common_denominator = self.denominator * other.denominator
        new_numerator = (self.numerator * other.denominator) - (other.numerator * self.denominator)
        return Fraction(new_numerator, common_denominator)

    def __mul__(self, other):
        new_numerator = self.numerator * other.numerator
        new_denominator = self.denominator * other.denominator
        return Fraction(new_numerator, new_denominator)

    def __truediv__(self, other):
        if other.numerator == 0:
            raise ZeroDivisionError("Division by zero")
        new_numerator = self.numerator * other.denominator
        new_denominator = self.denominator * other.numerator
        return Fraction(new_numerator, new_denominator)

    def __eq__(self, other):
        return (self.numerator * other.denominator) == (other.numerator * self.denominator)

    def __lt__(self, other):
        return (self.numerator * other.denominator) < (other.numerator * self.denominator)

    def __call__(self):
        return self.numerator / self.denominator

    def simplify(self):
        num = self.numerator
        den = self.denominator
        while den != 0:
            num, den = den, num % den
        common_factor = num
        self.numerator //= common_factor
        self.denominator //= common_factor

    def __str__(self):
        return f"{self.numerator}/{self.denominator}"