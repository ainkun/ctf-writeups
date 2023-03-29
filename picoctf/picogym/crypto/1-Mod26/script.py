import string

enc = "cvpbPGS{arkg_gvzr_V'yy_gel_2_ebhaqf_bs_ebg13_jdJBFOXJ}"

flag = ''

lower_alpha = string.ascii_lowercase
upper_alpha=string.ascii_uppercase

for chara in enc:
    if chara in lower_alpha:
        rot = (lower_alpha.index(chara)+13)%26
        flag = flag + lower_alpha[rot]
    elif chara in upper_alpha:
        rot = (upper_alpha.index(chara)+13)%26
        flag = flag + upper_alpha[rot]
    else:
        flag = flag+chara

print(flag)