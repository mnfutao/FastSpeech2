""" from https://github.com/keithito/tacotron """

"""
Defines the set of symbols used in text input to the model.

The default is a set of ASCII characters that works well for English or text that has been run through Unidecode. For other data, you can modify _characters. See TRAINING_DATA.md for details. """

from text import cmudict, pinyin

_pad = "_"
_punctuation = "!'(),.:;? "
_special = "-"
_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
_silences = ["@sp", "@spn", "@sil"]

# Prepend "@" to ARPAbet symbols to ensure uniqueness (some are the same as uppercase letters):
_arpabet = ["@" + s for s in cmudict.valid_symbols]
_pinyin = ["@" + s for s in pinyin.valid_symbols]

# Export all symbols:
symbols = (
    [_pad]
    + list(_special)
    + list(_punctuation)
    + list(_letters)
    + _arpabet
    + _pinyin
    + _silences
)

symbols = ['@PAD', '@END', '@A_0', '@A_1', '@A_2', '@A_3', '@A_4', '@AI_0', '@AI_1', '@AI_2', '@AI_3', '@AI_4', '@AN_0', '@AN_1', '@AN_2', '@AN_3', '@AN_4', '@ANG_0', '@ANG_1', '@ANG_2', '@ANG_3', '@ANG_4', '@AO_0', '@AO_1', '@AO_2', '@AO_3', '@AO_4', '@B', '@C', '@CH', '@D', '@E_0', '@E_1', '@E_2', '@E_3', '@E_4', '@EI_0', '@EI_1', '@EI_2', '@EI_3', '@EI_4', '@EN_0', '@EN_1', '@EN_2', '@EN_3', '@EN_4', '@ENG_0', '@ENG_1', '@ENG_2', '@ENG_3', '@ENG_4', '@ER_0', '@ER_1', '@ER_2', '@ER_3', '@ER_4', '@F', '@G', '@H', '@I_0', '@I_1', '@I_2', '@I_3', '@I_4', '@IA_0', '@IA_1', '@IA_2', '@IA_3', '@IA_4', '@IAN_0', '@IAN_1', '@IAN_2', '@IAN_3', '@IAN_4', '@IANG_0', '@IANG_1', '@IANG_2', '@IANG_3', '@IANG_4', '@IAO_0', '@IAO_1', '@IAO_2', '@IAO_3', '@IAO_4', '@IE_0', '@IE_1', '@IE_2', '@IE_3', '@IE_4', '@II_0', '@II_1', '@II_2', '@II_3', '@II_4', '@III_0', '@III_1', '@III_2', '@III_3', '@III_4', '@IN_0', '@IN_1', '@IN_2', '@IN_3', '@IN_4', '@ING_0', '@ING_1', '@ING_2', '@ING_3', '@ING_4', '@IO_0', '@IO_1', '@IO_2', '@IO_3', '@IO_4', '@IONG_0', '@IONG_1', '@IONG_2', '@IONG_3', '@IONG_4', '@IOU_0', '@IOU_1', '@IOU_2', '@IOU_3', '@IOU_4', '@J', '@K', '@L', '@M', '@N', '@O_0', '@O_1', '@O_2', '@O_3', '@O_4', '@ONG_0', '@ONG_1', '@ONG_2', '@ONG_3', '@ONG_4', '@OU_0', '@OU_1', '@OU_2', '@OU_3', '@OU_4', '@P', '@Q', '@R', '@S', '@SH', '@T', '@U_0', '@U_1', '@U_2', '@U_3', '@U_4', '@UA_0', '@UA_1', '@UA_2', '@UA_3', '@UA_4', '@UAI_0', '@UAI_1', '@UAI_2', '@UAI_3', '@UAI_4', '@UAN_0', '@UAN_1', '@UAN_2', '@UAN_3', '@UAN_4', '@UANG_0', '@UANG_1', '@UANG_2', '@UANG_3', '@UANG_4', '@UEI_0', '@UEI_1', '@UEI_2', '@UEI_3', '@UEI_4', '@UEN_0', '@UEN_1', '@UEN_2', '@UEN_3', '@UEN_4', '@UENG_0', '@UENG_1', '@UENG_2', '@UENG_3', '@UENG_4', '@UO_0', '@UO_1', '@UO_2', '@UO_3', '@UO_4', '@V_0', '@V_1', '@V_2', '@V_3', '@V_4', '@VAN_0', '@VAN_1', '@VAN_2', '@VAN_3', '@VAN_4', '@VE_0', '@VE_1', '@VE_2', '@VE_3', '@VE_4', '@VN_0', '@VN_1', '@VN_2', '@VN_3', '@VN_4', '@X', '@Z', '@ZH', '@SIL', '@SP', '@,', '@.', '@?', '@!']
