import random
from unicodedata import digit

DIGITS = '0123456789'
def get_random_number(digits):
    number = ''
    for i in range(digits):
        number+= DIGITS[random.randint(0,len(DIGITS)-1)]
    return number

CHARS = 'abcdefghijklmnopqrstuvwxyz'
CHARS = CHARS.upper()

def get_random_char(digits):
    chars=""
    for i in range(digits):
        chars += CHARS[random.randint(0,len(CHARS)-1)]
    return chars

def get_random_alphanumeric(digits):
    chars=""
    an = CHARS + DIGITS
    for i in range(digits):
        chars += an[random.randint(0,len(an)-1)]
    return chars

def get_option(num_options):
    return random.randint(1,num_options)

#NUMERIC RANGE PROTOTYPE
def get_alabama():
    digits = random.randint(1,8)
    dl_num = get_random_number(digits)
    return dl_num

def get_alaska():
    digits = random.randint(1,7)
    dl_num = get_random_number(digits)
    return dl_num

def get_arizona():
    o = get_option(2)
    if o == 1:
        dl_num = get_random_char(1) + get_random_number(8)
    if o == 2:
        dl_num = get_random_number(9)
    return dl_num

def get_arkansas():
    digits = random.randint(4,9)
    dl_num = get_random_number(digits)
    return dl_num

#ALPHA+NUMERIC FIXED PROTOTYPE
def get_california():
    dl_num = get_random_char(1) + get_random_number(7)
    return dl_num

#NUMERIC FIXED PROTOTYPE
def get_connecticut():
    dl_num = get_random_number(9)
    return dl_num

def get_colorado():
    o = get_option(3)
    if o == 1:
        digits = random.randint(3,6)
        dl_num = get_random_char(1) + get_random_number(digits)
    if o == 2:
        dl_num = get_random_number(9)
    if o ==3:
        digits = random.randint(2,5)
        dl_num = get_random_char(2) + get_random_number(digits)
    return dl_num

def get_delaware():
    digits = random.randint(1,7)
    dl_num = get_random_number(digits)
    return dl_num

def get_dc():
    o = get_option(2)
    if o == 1:
        dl_num = get_random_number(7)
    if o == 2:
        dl_num = get_random_number(9)
    return dl_num

def get_florida():
    dl_num = get_random_char(1) + get_random_number(12)
    return dl_num

def get_georgia():
    digits = random.randint(7,9)
    dl_num = get_random_number(digits)
    return dl_num

def get_hawaii():
    o = get_option(2)
    if o == 1:
        dl_num = get_random_char(1) + get_random_number(8)
    if o == 2:
        dl_num = get_random_number(9)
    return dl_num

def get_idaho():
    o = get_option(2)
    if o == 1:
        dl_num = get_random_char(2) + get_random_number(6) + get_random_char(1)
    if o == 2:
        dl_num = get_random_number(9)
    return dl_num

def get_illinois():
    digits = random.randint(11,12)
    dl_num = get_random_char(1) + get_random_number(digits)
    return dl_num

def get_indiana():
    o = get_option(2)
    if o == 1:
        dl_num = get_random_char(1) + get_random_number(9)
    if o == 2:
        digits = random.randint(9,10)
        dl_num = get_random_number(digits)
    return dl_num

def get_iowa():
    o = get_option(2)
    if o == 1:
        dl_num = get_random_number(3) + get_random_char(2) + get_random_number(4)
    if o == 2:
        dl_num = get_random_number(9)
    return dl_num

def get_kansas():
    o = get_option(3)
    if o == 1:
        dl_num = get_random_char(1) + get_random_number(1) + get_random_char(1) + get_random_number(1) +get_random_char(1)
    if o == 2:
        dl_num = get_random_number(9)
    if o ==3:
        dl_num = get_random_char(1) + get_random_number(8)
    return dl_num

def get_kentucky():
    o = get_option(3)
    if o == 1:
        dl_num = get_random_char(1) + get_random_number(9)
    if o == 2:
        dl_num = get_random_number(9)
    if o ==3:
        dl_num = get_random_char(1) + get_random_number(8)
    return dl_num

def get_louisiana():
    digits = random.randint(1,9)
    dl_num = get_random_number(digits)
    return dl_num
    
def get_maine():
    o = get_option(3)
    if o == 1:
        dl_num = get_random_number(7)
    if o == 2:
        dl_num = get_random_number(7) + get_random_char(1)
    if o ==3:
        dl_num = get_random_number(8)
    return dl_num

def get_maryland():
    dl_num = get_random_char(1) + get_random_number(12)
    return dl_num

def get_massachusetts():
    o = get_option(2)
    if o == 1:
        dl_num = get_random_number(9)
    if o == 2:
        dl_num = get_random_char(1) + get_random_number(8)
    return dl_num

def get_michigan():
    o = get_option(2)
    if o == 1:
        dl_num = get_random_char(1) + get_random_number(10)
    if o == 2:
        dl_num = get_random_char(1) + get_random_number(12)
    return dl_num

def get_minnesota():
    dl_num = get_random_char(1) + get_random_number(12)
    return dl_num

def get_mississippi():
    dl_num = get_random_number(9)
    return dl_num

def get_missouri():
    o = get_option(6)
    if o == 1:
        dl_num = get_random_number(3) + get_random_char(1) + get_random_number(6)
    if o == 2:
        dl_num = get_random_char(1) + get_random_number(6) + 'R'
    if o == 3:
        digits = random.randint(5,9)
        dl_num =get_random_char(1) + get_random_number(digits)
    if o == 4:
        dl_num = get_random_number(8) + get_random_char(2)
    if o == 5:
        dl_num = get_random_number(9) + get_random_char(1)
    if o == 6:
        dl_num = get_random_number(9)
    return dl_num

def get_montana():
    o = get_option(3)
    if o == 1:
        dl_num = get_random_char(1) + get_random_number(8)
    if o == 2:
        dl_num = get_random_number(9)
    if o ==3:
        digits = random.randint(13,14)
        dl_num = get_random_number(digits)
    return dl_num

def get_nebraska():
    digits = random.randint(6,8)
    dl_num = get_random_char(1) + get_random_number(digits)
    return dl_num

def get_nevada():
    o = get_option(3)
    if o == 1:
        dl_num = 'X' + get_random_number(8)
    if o == 2:
        dl_num = get_random_number(12)
    if o ==3:
        digits = random.randint(9,10)
        dl_num = get_random_number(digits)
    return dl_num

def get_new_hampshire():
    dl_num = get_random_number(2) + get_random_char(3) + get_random_number(5)
    return dl_num

def get_new_jersey():
    dl_num = get_random_char(1) + get_random_number(14)
    return dl_num

def get_new_mexico():
    digits = random.randint(8,9)
    dl_num = get_random_number(digits)
    return dl_num

def get_new_york():
    o = get_option(5)
    if o == 1:
        dl_num = get_random_char(1) + get_random_number(7)
    if o == 2:
        dl_num = get_random_char(1) + get_random_number(18)
    if o == 3:
        digits = random.randint(8,9)
        dl_num = get_random_number(digits)
    if o == 4:
        dl_num = get_random_number(16)
    if o == 5:
        dl_num = get_random_char(8)
    return dl_num

def get_north_carolina():
    digits = random.randint(1,12)
    dl_num = get_random_number(digits)
    return dl_num

def get_north_dakota():
    o = get_option(2)
    if o == 1:
        dl_num = get_random_char(3) + get_random_number(6)
    if o == 2:
        dl_num = get_random_number(9)
    return dl_num

def get_ohio():
    o = get_option(3)
    if o == 1:
        digits = random.randint(4,8)
        dl_num = get_random_char(1) + get_random_number(digits)
    if o == 2:
        digits = random.randint(3,7)
        dl_num = get_random_char(2) + get_random_number(digits)
    if o ==3:
        dl_num = get_random_number(8)
    return dl_num

def get_oklahoma():
    o = get_option(2)
    if o == 1:
        dl_num = get_random_char(1) + get_random_number(9)
    if o == 2:
        dl_num = get_random_number(9)
    return dl_num

def get_oregon():
    digits = random.randint(1,9)
    dl_num = get_random_number(digits)
    return dl_num
    
def get_pennsylvania():
    dl_num = get_random_number(8)
    return dl_num

def get_rhode_island():
    o = get_option(2)
    if o == 1:
        dl_num = get_random_char(1) + get_random_number(6)
    if o == 2:
        dl_num = get_random_number(7)
    return dl_num

def get_south_carolina():
    digits = random.randint(5,11)
    dl_num = get_random_number(digits)
    return dl_num

def get_south_dakota():
    o = get_option(2)
    if o == 1:
        digits = random.randint(6,10)
        dl_num = get_random_number(digits)
    if o == 2:
        dl_num = get_random_number(12)
    return dl_num

def get_tennessee():
    digits = random.randint(7,9)
    dl_num = get_random_number(digits)
    return dl_num

def get_texas():
    digits = random.randint(7,8)
    dl_num = get_random_number(digits)
    return dl_num

def get_utah():
    digits = random.randint(4,10)
    dl_num = get_random_number(digits)
    return dl_num

def get_vermont():
    o = get_option(2)
    if o == 1:
        dl_num = get_random_number(8)
    if o == 2:
        dl_num = get_random_number(7) + 'A'
    return dl_num

def get_virginia():
    o = get_option(2)
    if o == 1:
        digits = random.randint(8,11)
        dl_num = get_random_char(1) + get_random_number(digits)
    if o == 2:
        dl_num = get_random_number(9)
    return dl_num

def get_washington():
    chars= random.randint(1,7)
    digits = 12 - chars
    dl_num = get_random_char(chars) + get_random_alphanumeric(digits)
    return dl_num

def get_west_virginia():
    o = get_option(2)
    if o == 1:
        digits = random.randint(5,6)
        chars = random.randint(1,2)
        dl_num = get_random_char(chars) + get_random_number(digits)
    if o == 2:
        dl_num = get_random_number(7)
    return dl_num

def get_wisconsin():
    dl_num = get_random_char(1) + get_random_number(13)
    return dl_num

def get_wyoming():
    digits = random.randint(9,10)
    dl_num = get_random_number(digits)
    return dl_num

def pars_arg(arg: str):
    dl_num = "Error - invalid argument"
    arg = arg.upper()
    if arg == "AL" or arg == "ALABAMA":
        dl_num = get_alabama()
    if arg == "AK" or arg == "ALASKA":
        dl_num = get_alaska()
    if arg == "AZ" or arg == "ARIZONA":
        dl_num = get_arizona()
    if arg == "AR" or arg == "ARKANSAS":
        dl_num = get_arkansas()
    if arg == "CA" or arg == "CALIFORNIA":
        dl_num = get_california()
    if arg == "CO" or arg == "COLORADO":
        dl_num = get_colorado()
    if arg == "CT" or arg == "CONNECTICUT":
        dl_num = get_connecticut()
    if arg == "DE" or arg == "DELAWARE":
        dl_num = get_delaware()
    if arg == "DC" or arg == "D.C." or arg == "DISTRICT OF COLUMBIA":
        dl_num = get_dc()
    if arg == "FL" or arg == "FLORIDA":
        dl_num = get_florida()
    if arg == "GA" or arg == "GEORGIA":
        dl_num = get_georgia()
    if arg == "HI" or arg == "HAWAII":
        dl_num = get_hawaii()
    if arg == "ID" or arg == "IDAHO":
        dl_num = get_idaho()
    if arg == "IL" or arg == "ILLINOIS":
        dl_num = get_illinois()
    if arg == "IN" or arg == "INDIANA":
        dl_num = get_indiana()
    if arg == "IA" or arg == "IOWA":
        dl_num = get_iowa()
    if arg == "KS" or arg == "KANSAS":
        dl_num = get_kansas()
    if arg == "KY" or arg == "KENTUCKY":
        dl_num = get_kentucky()
    if arg == "LA" or arg == "LOUISIANA":
        dl_num = get_louisiana()
    if arg == "ME" or arg == "MAINE":
        dl_num = get_maine()
    if arg == "MD" or arg == "MARYLAND":
        dl_num = get_maryland()
    if arg == "MA" or arg == "MASSACHUSETTS":
        dl_num = get_massachusetts()
    if arg == "MI" or arg == "MICHIGAN":
        dl_num = get_michigan()
    if arg == "MN" or arg == "MINNESOTA":
        dl_num = get_minnesota()
    if arg == "MS" or arg == "MISSISSIPPI":
        dl_num = get_mississippi()
    if arg == "MO" or arg == "MISSOURI":
        dl_num = get_missouri()
    if arg == "MT" or arg == "MONTANA":
        dl_num = get_montana()
    if arg == "NE" or arg == "NEBRASKA":
        dl_num = get_nebraska()
    if arg == "NV" or arg == "NEVADA":
        dl_num = get_nevada()
    if arg == "NH" or arg == "NEW HAMPSHIRE":
        dl_num = get_new_hampshire()
    if arg == "NJ" or arg == "NEW JERSEY":
        dl_num = get_new_jersey()
    if arg == "NM" or arg == "NEW MEXICO":
        dl_num = get_new_mexico()
    if arg == "NY" or arg == "NEW YORK":
        dl_num = get_new_york()
    if arg == "NC" or arg == "NORTH CAROLINA":
        dl_num = get_north_carolina()
    if arg == "ND" or arg == "NORTH DAKOTA":
        dl_num = get_north_dakota()
    if arg == "OH" or arg == "OHIO":
        dl_num = get_ohio()
    if arg == "OK" or arg == "OKLAHOMA":
        dl_num = get_oklahoma()
    if arg == "OR" or arg == "OREGON":
        dl_num = get_oregon()
    if arg == "PA" or arg == "PENNSYLVANIA":
        dl_num = get_pennsylvania()
    if arg == "RI" or arg == "RHODE ISLAND":
        dl_num = get_rhode_island()
    if arg == "SC" or arg == "SOUTH CAROLINA":
        dl_num = get_south_carolina()
    if arg == "SD" or arg == "SOUTH DAKOTA":
        dl_num = get_south_dakota()
    if arg == "TN" or arg == "TENNESSEE":
        dl_num = get_tennessee()
    if arg == "TX" or arg == "TEXAS":
        dl_num = get_texas()
    if arg == "UT" or arg == "UTAH":
        dl_num = get_utah()
    if arg == "VT" or arg == "VERMONT":
        dl_num = get_vermont()
    if arg == "VI" or arg == "VIRGINIA":
        dl_num = get_virginia()
    if arg == "WA" or arg == "WASHINGTON":
        dl_num = get_washington()
    if arg == "WV" or arg == "WEST VIRGINIA":
        dl_num = get_west_virginia()
    if arg == "WI" or arg == "WISCONSIN":
        dl_num = get_wisconsin()
    if arg == "WY" or arg == "WYOMING":
        dl_num = get_wyoming()
    return dl_num