import re

_colors = {
    "aliceblue": 0xf0f8ffff,
    "antiquewhite": 0xfaebd7ff,
    "antiquewhite1": 0xffefdbff,
    "antiquewhite2": 0xeedfccff,
    "antiquewhite3": 0xcdc0b0ff,
    "antiquewhite4": 0x8b8378ff,
    "aquamarine": 0x7fffd4ff,
    "aquamarine1": 0x7fffd4ff,
    "aquamarine2": 0x76eec6ff,
    "aquamarine3": 0x66cdaaff,
    "aquamarine4": 0x458b74ff,
    "azure": 0xf0ffffff,
    "azure1": 0xf0ffffff,
    "azure2": 0xe0eeeeff,
    "azure3": 0xc1cdcdff,
    "azure4": 0x838b8bff,
    "beige": 0xf5f5dcff,
    "bisque": 0xffe4c4ff,
    "bisque1": 0xffe4c4ff,
    "bisque2": 0xeed5b7ff,
    "bisque3": 0xcdb79eff,
    "bisque4": 0x8b7d6bff,
    "black": 0x000000ff,
    "blanchedalmond": 0xffebcdff,
    "blue": 0x0000ffff,
    "blue1": 0x0000ffff,
    "blue2": 0x0000eeff,
    "blue3": 0x0000cdff,
    "blue4": 0x00008bff,
    "blueviolet": 0x8a2be2ff,
    "brown": 0xa52a2aff,
    "brown1": 0xff4040ff,
    "brown2": 0xee3b3bff,
    "brown3": 0xcd3333ff,
    "brown4": 0x8b2323ff,
    "burlywood": 0xdeb887ff,
    "burlywood1": 0xffd39bff,
    "burlywood2": 0xeec591ff,
    "burlywood3": 0xcdaa7dff,
    "burlywood4": 0x8b7355ff,
    "cadetblue": 0x5f9ea0ff,
    "cadetblue1": 0x98f5ffff,
    "cadetblue2": 0x8ee5eeff,
    "cadetblue3": 0x7ac5cdff,
    "cadetblue4": 0x53868bff,
    "chartreuse": 0x7fff00ff,
    "chartreuse1": 0x7fff00ff,
    "chartreuse2": 0x76ee00ff,
    "chartreuse3": 0x66cd00ff,
    "chartreuse4": 0x458b00ff,
    "chocolate": 0xd2691eff,
    "chocolate1": 0xff7f24ff,
    "chocolate2": 0xee7621ff,
    "chocolate3": 0xcd661dff,
    "chocolate4": 0x8b4513ff,
    "coral": 0xff7f50ff,
    "coral1": 0xff7256ff,
    "coral2": 0xee6a50ff,
    "coral3": 0xcd5b45ff,
    "coral4": 0x8b3e2fff,
    "cornflowerblue": 0x6495edff,
    "cornsilk": 0xfff8dcff,
    "cornsilk1": 0xfff8dcff,
    "cornsilk2": 0xeee8cdff,
    "cornsilk3": 0xcdc8b1ff,
    "cornsilk4": 0x8b8878ff,
    "cyan": 0x00ffffff,
    "cyan1": 0x00ffffff,
    "cyan2": 0x00eeeeff,
    "cyan3": 0x00cdcdff,
    "cyan4": 0x008b8bff,
    "darkblue": 0x00008bff,
    "darkcyan": 0x008b8bff,
    "darkgoldenrod": 0xb8860bff,
    "darkgoldenrod1": 0xffb90fff,
    "darkgoldenrod2": 0xeead0eff,
    "darkgoldenrod3": 0xcd950cff,
    "darkgoldenrod4": 0x8b6508ff,
    "darkgray": 0xa9a9a9ff,
    "darkgreen": 0x006400ff,
    "darkkhaki": 0xbdb76bff,
    "darkmagenta": 0x8b008bff,
    "darkolivegreen": 0x556b2fff,
    "darkolivegreen1": 0xcaff70ff,
    "darkolivegreen2": 0xbcee68ff,
    "darkolivegreen3": 0xa2cd5aff,
    "darkolivegreen4": 0x6e8b3dff,
    "darkorange": 0xff8c00ff,
    "darkorange1": 0xff7f00ff,
    "darkorange2": 0xee7600ff,
    "darkorange3": 0xcd6600ff,
    "darkorange4": 0x8b4500ff,
    "darkorchid": 0x9932ccff,
    "darkorchid1": 0xbf3effff,
    "darkorchid2": 0xb23aeeff,
    "darkorchid3": 0x9a32cdff,
    "darkorchid4": 0x68228bff,
    "darkred": 0x8b0000ff,
    "darksalmon": 0xe9967aff,
    "darkseagreen": 0x8fbc8fff,
    "darkseagreen1": 0xc1ffc1ff,
    "darkseagreen2": 0xb4eeb4ff,
    "darkseagreen3": 0x9bcd9bff,
    "darkseagreen4": 0x698b69ff,
    "darkslateblue": 0x483d8bff,
    "darkslategray": 0x2f4f4fff,
    "darkslategray1": 0x97ffffff,
    "darkslategray2": 0x8deeeeff,
    "darkslategray3": 0x79cdcdff,
    "darkslategray4": 0x528b8bff,
    "darkturquoise": 0x00ced1ff,
    "darkviolet": 0x9400d3ff,
    "deeppink": 0xff1493ff,
    "deeppink1": 0xff1493ff,
    "deeppink2": 0xee1289ff,
    "deeppink3": 0xcd1076ff,
    "deeppink4": 0x8b0a50ff,
    "deepskyblue": 0x00bfffff,
    "deepskyblue1": 0x00bfffff,
    "deepskyblue2": 0x00b2eeff,
    "deepskyblue3": 0x009acdff,
    "deepskyblue4": 0x00688bff,
    "dimgray": 0x696969ff,
    "dodgerblue": 0x1e90ffff,
    "dodgerblue1": 0x1e90ffff,
    "dodgerblue2": 0x1c86eeff,
    "dodgerblue3": 0x1874cdff,
    "dodgerblue4": 0x104e8bff,
    "firebrick": 0xb22222ff,
    "firebrick1": 0xff3030ff,
    "firebrick2": 0xee2c2cff,
    "firebrick3": 0xcd2626ff,
    "firebrick4": 0x8b1a1aff,
    "floralwhite": 0xfffaf0ff,
    "forestgreen": 0x228b22ff,
    "gainsboro": 0xdcdcdcff,
    "ghostwhite": 0xf8f8ffff,
    "gold": 0xffd700ff,
    "gold1": 0xffd700ff,
    "gold2": 0xeec900ff,
    "gold3": 0xcdad00ff,
    "gold4": 0x8b7500ff,
    "goldenrod": 0xdaa520ff,
    "goldenrod1": 0xffc125ff,
    "goldenrod2": 0xeeb422ff,
    "goldenrod3": 0xcd9b1dff,
    "goldenrod4": 0x8b6914ff,
    "gray": 0xbebebeff,
    "gray0": 0x000000ff,
    "gray1": 0x030303ff,
    "gray2": 0x050505ff,
    "gray3": 0x080808ff,
    "gray4": 0x0a0a0aff,
    "gray5": 0x0d0d0dff,
    "gray6": 0x0f0f0fff,
    "gray7": 0x121212ff,
    "gray8": 0x141414ff,
    "gray9": 0x171717ff,
    "gray10": 0x1a1a1aff,
    "gray11": 0x1c1c1cff,
    "gray12": 0x1f1f1fff,
    "gray13": 0x212121ff,
    "gray14": 0x242424ff,
    "gray15": 0x262626ff,
    "gray16": 0x292929ff,
    "gray17": 0x2b2b2bff,
    "gray18": 0x2e2e2eff,
    "gray19": 0x303030ff,
    "gray20": 0x333333ff,
    "gray21": 0x363636ff,
    "gray22": 0x383838ff,
    "gray23": 0x3b3b3bff,
    "gray24": 0x3d3d3dff,
    "gray25": 0x404040ff,
    "gray26": 0x424242ff,
    "gray27": 0x454545ff,
    "gray28": 0x474747ff,
    "gray29": 0x4a4a4aff,
    "gray30": 0x4d4d4dff,
    "gray31": 0x4f4f4fff,
    "gray32": 0x525252ff,
    "gray33": 0x545454ff,
    "gray34": 0x575757ff,
    "gray35": 0x595959ff,
    "gray36": 0x5c5c5cff,
    "gray37": 0x5e5e5eff,
    "gray38": 0x616161ff,
    "gray39": 0x636363ff,
    "gray40": 0x666666ff,
    "gray41": 0x696969ff,
    "gray42": 0x6b6b6bff,
    "gray43": 0x6e6e6eff,
    "gray44": 0x707070ff,
    "gray45": 0x737373ff,
    "gray46": 0x757575ff,
    "gray47": 0x787878ff,
    "gray48": 0x7a7a7aff,
    "gray49": 0x7d7d7dff,
    "gray50": 0x7f7f7fff,
    "gray51": 0x828282ff,
    "gray52": 0x858585ff,
    "gray53": 0x878787ff,
    "gray54": 0x8a8a8aff,
    "gray55": 0x8c8c8cff,
    "gray56": 0x8f8f8fff,
    "gray57": 0x919191ff,
    "gray58": 0x949494ff,
    "gray59": 0x969696ff,
    "gray60": 0x999999ff,
    "gray61": 0x9c9c9cff,
    "gray62": 0x9e9e9eff,
    "gray63": 0xa1a1a1ff,
    "gray64": 0xa3a3a3ff,
    "gray65": 0xa6a6a6ff,
    "gray66": 0xa8a8a8ff,
    "gray67": 0xabababff,
    "gray68": 0xadadadff,
    "gray69": 0xb0b0b0ff,
    "gray70": 0xb3b3b3ff,
    "gray71": 0xb5b5b5ff,
    "gray72": 0xb8b8b8ff,
    "gray73": 0xbababaff,
    "gray74": 0xbdbdbdff,
    "gray75": 0xbfbfbfff,
    "gray76": 0xc2c2c2ff,
    "gray77": 0xc4c4c4ff,
    "gray78": 0xc7c7c7ff,
    "gray79": 0xc9c9c9ff,
    "gray80": 0xccccccff,
    "gray81": 0xcfcfcfff,
    "gray82": 0xd1d1d1ff,
    "gray83": 0xd4d4d4ff,
    "gray84": 0xd6d6d6ff,
    "gray85": 0xd9d9d9ff,
    "gray86": 0xdbdbdbff,
    "gray87": 0xdededeff,
    "gray88": 0xe0e0e0ff,
    "gray89": 0xe3e3e3ff,
    "gray90": 0xe5e5e5ff,
    "gray91": 0xe8e8e8ff,
    "gray92": 0xebebebff,
    "gray93": 0xedededff,
    "gray94": 0xf0f0f0ff,
    "gray95": 0xf2f2f2ff,
    "gray96": 0xf5f5f5ff,
    "gray97": 0xf7f7f7ff,
    "gray98": 0xfafafaff,
    "gray99": 0xfcfcfcff,
    "gray100": 0xffffffff,
    "green": 0x00ff00ff,
    "green1": 0x00ff00ff,
    "green2": 0x00ee00ff,
    "green3": 0x00cd00ff,
    "green4": 0x008b00ff,
    "greenyellow": 0xadff2fff,
    "honeydew": 0xf0fff0ff,
    "honeydew1": 0xf0fff0ff,
    "honeydew2": 0xe0eee0ff,
    "honeydew3": 0xc1cdc1ff,
    "honeydew4": 0x838b83ff,
    "hotpink": 0xff69b4ff,
    "hotpink1": 0xff6eb4ff,
    "hotpink2": 0xee6aa7ff,
    "hotpink3": 0xcd6090ff,
    "hotpink4": 0x8b3a62ff,
    "indianred": 0xcd5c5cff,
    "indianred1": 0xff6a6aff,
    "indianred2": 0xee6363ff,
    "indianred3": 0xcd5555ff,
    "indianred4": 0x8b3a3aff,
    "ivory": 0xfffff0ff,
    "ivory1": 0xfffff0ff,
    "ivory2": 0xeeeee0ff,
    "ivory3": 0xcdcdc1ff,
    "ivory4": 0x8b8b83ff,
    "khaki": 0xf0e68cff,
    "khaki1": 0xfff68fff,
    "khaki2": 0xeee685ff,
    "khaki3": 0xcdc673ff,
    "khaki4": 0x8b864eff,
    "lavender": 0xe6e6faff,
    "lavenderblush": 0xfff0f5ff,
    "lavenderblush1": 0xfff0f5ff,
    "lavenderblush2": 0xeee0e5ff,
    "lavenderblush3": 0xcdc1c5ff,
    "lavenderblush4": 0x8b8386ff,
    "lawngreen": 0x7cfc00ff,
    "lemonchiffon": 0xfffacdff,
    "lemonchiffon1": 0xfffacdff,
    "lemonchiffon2": 0xeee9bfff,
    "lemonchiffon3": 0xcdc9a5ff,
    "lemonchiffon4": 0x8b8970ff,
    "lightblue": 0xadd8e6ff,
    "lightblue1": 0xbfefffff,
    "lightblue2": 0xb2dfeeff,
    "lightblue3": 0x9ac0cdff,
    "lightblue4": 0x68838bff,
    "lightcoral": 0xf08080ff,
    "lightcyan": 0xe0ffffff,
    "lightcyan1": 0xe0ffffff,
    "lightcyan2": 0xd1eeeeff,
    "lightcyan3": 0xb4cdcdff,
    "lightcyan4": 0x7a8b8bff,
    "lightgoldenrod": 0xeedd82ff,
    "lightgoldenrod1": 0xffec8bff,
    "lightgoldenrod2": 0xeedc82ff,
    "lightgoldenrod3": 0xcdbe70ff,
    "lightgoldenrod4": 0x8b814cff,
    "lightgoldenrodyellow": 0xfafad2ff,
    "lightgray": 0xd3d3d3ff,
    "lightgreen": 0x90ee90ff,
    "lightpink": 0xffb6c1ff,
    "lightpink1": 0xffaeb9ff,
    "lightpink2": 0xeea2adff,
    "lightpink3": 0xcd8c95ff,
    "lightpink4": 0x8b5f65ff,
    "lightsalmon": 0xffa07aff,
    "lightsalmon1": 0xffa07aff,
    "lightsalmon2": 0xee9572ff,
    "lightsalmon3": 0xcd8162ff,
    "lightsalmon4": 0x8b5742ff,
    "lightseagreen": 0x20b2aaff,
    "lightskyblue": 0x87cefaff,
    "lightskyblue1": 0xb0e2ffff,
    "lightskyblue2": 0xa4d3eeff,
    "lightskyblue3": 0x8db6cdff,
    "lightskyblue4": 0x607b8bff,
    "lightslateblue": 0x8470ffff,
    "lightslategray": 0x778899ff,
    "lightsteelblue": 0xb0c4deff,
    "lightsteelblue1": 0xcae1ffff,
    "lightsteelblue2": 0xbcd2eeff,
    "lightsteelblue3": 0xa2b5cdff,
    "lightsteelblue4": 0x6e7b8bff,
    "lightyellow": 0xffffe0ff,
    "lightyellow1": 0xffffe0ff,
    "lightyellow2": 0xeeeed1ff,
    "lightyellow3": 0xcdcdb4ff,
    "lightyellow4": 0x8b8b7aff,
    "limegreen": 0x32cd32ff,
    "linen": 0xfaf0e6ff,
    "magenta": 0xff00ffff,
    "magenta1": 0xff00ffff,
    "magenta2": 0xee00eeff,
    "magenta3": 0xcd00cdff,
    "magenta4": 0x8b008bff,
    "maroon": 0xb03060ff,
    "maroon1": 0xff34b3ff,
    "maroon2": 0xee30a7ff,
    "maroon3": 0xcd2990ff,
    "maroon4": 0x8b1c62ff,
    "mediumaquamarine": 0x66cdaaff,
    "mediumblue": 0x0000cdff,
    "mediumorchid": 0xba55d3ff,
    "mediumorchid1": 0xe066ffff,
    "mediumorchid2": 0xd15feeff,
    "mediumorchid3": 0xb452cdff,
    "mediumorchid4": 0x7a378bff,
    "mediumpurple": 0x9370dbff,
    "mediumpurple1": 0xab82ffff,
    "mediumpurple2": 0x9f79eeff,
    "mediumpurple3": 0x8968cdff,
    "mediumpurple4": 0x5d478bff,
    "mediumseagreen": 0x3cb371ff,
    "mediumslateblue": 0x7b68eeff,
    "mediumspringgreen": 0x00fa9aff,
    "mediumturquoise": 0x48d1ccff,
    "mediumvioletred": 0xc71585ff,
    "midnightblue": 0x191970ff,
    "mintcream": 0xf5fffaff,
    "mistyrose": 0xffe4e1ff,
    "mistyrose1": 0xffe4e1ff,
    "mistyrose2": 0xeed5d2ff,
    "mistyrose3": 0xcdb7b5ff,
    "mistyrose4": 0x8b7d7bff,
    "moccasin": 0xffe4b5ff,
    "navahowhite": 0xffdeadff,
    "navahowhite1": 0xffdeadff,
    "navahowhite2": 0xeecfa1ff,
    "navahowhite3": 0xcdb38bff,
    "navahowhite4": 0x8b795eff,
    "navajowhite": 0xffdeadff,
    "navajowhite1": 0xffdeadff,
    "navajowhite2": 0xeecfa1ff,
    "navajowhite3": 0xcdb38bff,
    "navajowhite4": 0x8b795eff,
    "navy": 0x000080ff,
    "navyblue": 0x000080ff,
    "oldlace": 0xfdf5e6ff,
    "olivedrab": 0x6b8e23ff,
    "olivedrab1": 0xc0ff3eff,
    "olivedrab2": 0xb3ee3aff,
    "olivedrab3": 0x9acd32ff,
    "olivedrab4": 0x698b22ff,
    "orange": 0xffa500ff,
    "orange1": 0xffa500ff,
    "orange2": 0xee9a00ff,
    "orange3": 0xcd8500ff,
    "orange4": 0x8b5a00ff,
    "orangered": 0xff4500ff,
    "orangered1": 0xff4500ff,
    "orangered2": 0xee4000ff,
    "orangered3": 0xcd3700ff,
    "orangered4": 0x8b2500ff,
    "orchid": 0xda70d6ff,
    "orchid1": 0xff83faff,
    "orchid2": 0xee7ae9ff,
    "orchid3": 0xcd69c9ff,
    "orchid4": 0x8b4789ff,
    "palegoldenrod": 0xeee8aaff,
    "palegreen": 0x98fb98ff,
    "palegreen1": 0x9aff9aff,
    "palegreen2": 0x90ee90ff,
    "palegreen3": 0x7ccd7cff,
    "palegreen4": 0x548b54ff,
    "paleturquoise": 0xafeeeeff,
    "paleturquoise1": 0xbbffffff,
    "paleturquoise2": 0xaeeeeeff,
    "paleturquoise3": 0x96cdcdff,
    "paleturquoise4": 0x668b8bff,
    "palevioletred": 0xdb7093ff,
    "palevioletred1": 0xff82abff,
    "palevioletred2": 0xee799fff,
    "palevioletred3": 0xcd6889ff,
    "palevioletred4": 0x8b475dff,
    "papayawhip": 0xffefd5ff,
    "peachpuff": 0xffdab9ff,
    "peachpuff1": 0xffdab9ff,
    "peachpuff2": 0xeecbadff,
    "peachpuff3": 0xcdaf95ff,
    "peachpuff4": 0x8b7765ff,
    "peru": 0xcd853fff,
    "pink": 0xffc0cbff,
    "pink1": 0xffb5c5ff,
    "pink2": 0xeea9b8ff,
    "pink3": 0xcd919eff,
    "pink4": 0x8b636cff,
    "plum": 0xdda0ddff,
    "plum1": 0xffbbffff,
    "plum2": 0xeeaeeeff,
    "plum3": 0xcd96cdff,
    "plum4": 0x8b668bff,
    "powderblue": 0xb0e0e6ff,
    "purple": 0xa020f0ff,
    "purple1": 0x9b30ffff,
    "purple2": 0x912ceeff,
    "purple3": 0x7d26cdff,
    "purple4": 0x551a8bff,
    "red": 0xff0000ff,
    "red1": 0xff0000ff,
    "red2": 0xee0000ff,
    "red3": 0xcd0000ff,
    "red4": 0x8b0000ff,
    "rosybrown": 0xbc8f8fff,
    "rosybrown1": 0xffc1c1ff,
    "rosybrown2": 0xeeb4b4ff,
    "rosybrown3": 0xcd9b9bff,
    "rosybrown4": 0x8b6969ff,
    "royalblue": 0x4169e1ff,
    "royalblue1": 0x4876ffff,
    "royalblue2": 0x436eeeff,
    "royalblue3": 0x3a5fcdff,
    "royalblue4": 0x27408bff,
    "saddlebrown": 0x8b4513ff,
    "salmon": 0xfa8072ff,
    "salmon1": 0xff8c69ff,
    "salmon2": 0xee8262ff,
    "salmon3": 0xcd7054ff,
    "salmon4": 0x8b4c39ff,
    "sandybrown": 0xf4a460ff,
    "seagreen": 0x2e8b57ff,
    "seagreen1": 0x54ff9fff,
    "seagreen2": 0x4eee94ff,
    "seagreen3": 0x43cd80ff,
    "seagreen4": 0x2e8b57ff,
    "seashell": 0xfff5eeff,
    "seashell1": 0xfff5eeff,
    "seashell2": 0xeee5deff,
    "seashell3": 0xcdc5bfff,
    "seashell4": 0x8b8682ff,
    "sienna": 0xa0522dff,
    "sienna1": 0xff8247ff,
    "sienna2": 0xee7942ff,
    "sienna3": 0xcd6839ff,
    "sienna4": 0x8b4726ff,
    "skyblue": 0x87ceebff,
    "skyblue1": 0x87ceffff,
    "skyblue2": 0x7ec0eeff,
    "skyblue3": 0x6ca6cdff,
    "skyblue4": 0x4a708bff,
    "slateblue": 0x6a5acdff,
    "slateblue1": 0x836fffff,
    "slateblue2": 0x7a67eeff,
    "slateblue3": 0x6959cdff,
    "slateblue4": 0x473c8bff,
    "slategray": 0x708090ff,
    "slategray1": 0xc6e2ffff,
    "slategray2": 0xb9d3eeff,
    "slategray3": 0x9fb6cdff,
    "slategray4": 0x6c7b8bff,
    "snow": 0xfffafaff,
    "snow1": 0xfffafaff,
    "snow2": 0xeee9e9ff,
    "snow3": 0xcdc9c9ff,
    "snow4": 0x8b8989ff,
    "springgreen": 0x00ff7fff,
    "springgreen1": 0x00ff7fff,
    "springgreen2": 0x00ee76ff,
    "springgreen3": 0x00cd66ff,
    "springgreen4": 0x008b45ff,
    "steelblue": 0x4682b4ff,
    "steelblue1": 0x63b8ffff,
    "steelblue2": 0x5caceeff,
    "steelblue3": 0x4f94cdff,
    "steelblue4": 0x36648bff,
    "tan": 0xd2b48cff,
    "tan1": 0xffa54fff,
    "tan2": 0xee9a49ff,
    "tan3": 0xcd853fff,
    "tan4": 0x8b5a2bff,
    "thistle": 0xd8bfd8ff,
    "thistle1": 0xffe1ffff,
    "thistle2": 0xeed2eeff,
    "thistle3": 0xcdb5cdff,
    "thistle4": 0x8b7b8bff,
    "tomato": 0xff6347ff,
    "tomato1": 0xff6347ff,
    "tomato2": 0xee5c42ff,
    "tomato3": 0xcd4f39ff,
    "tomato4": 0x8b3626ff,
    "turquoise": 0x40e0d0ff,
    "turquoise1": 0x00f5ffff,
    "turquoise2": 0x00e5eeff,
    "turquoise3": 0x00c5cdff,
    "turquoise4": 0x00868bff,
    "violet": 0xee82eeff,
    "violetred": 0xd02090ff,
    "violetred1": 0xff3e96ff,
    "violetred2": 0xee3a8cff,
    "violetred3": 0xcd3278ff,
    "violetred4": 0x8b2252ff,
    "wheat": 0xf5deb3ff,
    "wheat1": 0xffe7baff,
    "wheat2": 0xeed8aeff,
    "wheat3": 0xcdba96ff,
    "wheat4": 0x8b7e66ff,
    "white": 0xffffffff,
    "whitesmoke": 0xf5f5f5ff,
    "yellow": 0xffff00ff,
    "yellow1": 0xffff00ff,
    "yellow2": 0xeeee00ff,
    "yellow3": 0xcdcd00ff,
    "yellow4": 0x8b8b00ff,
    "yellowgreen": 0x9acd32ff,
}


class Color:
    __RE_HTML_COLOR = re.compile('^#([0-9a-fA-F]{2})?[0-9a-fA-F]{6}')
    
    def __init__(self, rgba):
        self.__value = rgba
    
    @property
    def alpha(self):
        return self.__value & 0xff
    
    @property
    def r(self):
        return self.__value >> 24
    
    @property
    def g(self):
        return (self.__value >> 16) & 0xff
    
    @property
    def b(self):
        return (self.__value >> 8) & 0xff
    
    @property
    def rgb(self):
        return self.__value & 0xffffff
    
    @property
    def argb(self):
        return ((self.__value & 0xff) << 24) + self.__value >> 8
    
    @property
    def rgba(self):
        return self.__value
    
    def invert(self):
        return Color(self.__value & 0xff + (0xffffff00 - self.__value & 0xffffff00))
    
    def __str__(self):
        return "#{0:08x}".format(self.__value)
    
    def __repr__(self):
        return "<Color {0}>".format(self)
    
    @staticmethod
    def get_color(color):
        if color in _colors: # named color
            return Color(_colors[color])
        if isinstance(color, tuple): # (r, g, b)
            return Color((color[0] << 24) + (color[1] << 16) + (color[1] << 8) + 0xff)
        if isinstance(color, str) and Color.__RE_HTML_COLOR.match(color): # html rgb/argb
            val = int(color[1:], 16)
            if len(color) == 6:
                val = (val << 8) + 0xff
            return Color(val)
        if isinstance(color, int): # rgba
            return Color(color)
        raise ValueError("color")