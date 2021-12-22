import re
from itertools import combinations, product
from typing import Iterable, Any

raw = """on x=-31..17,y=-17..30,z=-43..8
on x=-6..44,y=-24..30,z=-8..39
on x=0..49,y=-19..25,z=-12..38
on x=-31..14,y=-46..5,z=-43..9
on x=-42..3,y=-28..23,z=-25..28
on x=-20..26,y=-13..35,z=-36..8
on x=-26..27,y=-27..25,z=-11..38
on x=-42..11,y=-14..40,z=-23..24
on x=-25..19,y=-31..15,z=-39..8
on x=-42..11,y=-36..17,z=-39..9
off x=8..22,y=-3..14,z=10..29
on x=-13..38,y=-13..32,z=2..48
off x=33..42,y=4..13,z=-30..-19
on x=-19..26,y=-46..5,z=-40..12
off x=-23..-12,y=-7..2,z=-45..-29
on x=-17..35,y=-48..4,z=-16..36
off x=-12..2,y=-9..5,z=-12..3
on x=-34..19,y=-11..33,z=-26..24
off x=24..34,y=25..37,z=0..15
on x=-19..26,y=-28..26,z=-43..9
on x=-83807..-77448,y=-20052..2919,z=-8512..1270
on x=261..16256,y=65313..89218,z=-28825..-17392
on x=21434..35058,y=20632..40485,z=-84146..-55709
on x=-48812..-29971,y=55216..62921,z=-28022..-15766
on x=-14177..-7019,y=-91302..-62058,z=-8174..14864
on x=-87932..-62316,y=-38001..-18727,z=11302..39445
on x=69701..87455,y=-42551..-10451,z=13336..36833
on x=-86409..-53996,y=-5254..13252,z=26280..42952
on x=-42814..-21164,y=-7698..2546,z=55051..73047
on x=25078..37622,y=-90285..-66595,z=-24071..-3060
on x=72118..87866,y=-12079..17875,z=-23528..7587
on x=41274..64840,y=-63475..-48661,z=-4425..19395
on x=-15708..-4678,y=-749..19989,z=-82391..-64453
on x=-71898..-36969,y=40640..46191,z=28902..49264
on x=-80801..-66576,y=26395..31167,z=-31512..-21568
on x=57523..76560,y=-33285..-13800,z=4254..29473
on x=-82863..-64700,y=29768..59691,z=-30341..-7257
on x=-32065..-29379,y=38932..53508,z=-76878..-61315
on x=-10..11173,y=463..24967,z=77705..82346
on x=-47643..-23025,y=-42923..-34119,z=-60420..-57438
on x=-63621..-57529,y=33066..53811,z=23273..49072
on x=-74975..-60385,y=-22950..10155,z=-53348..-35419
on x=-54611..-35147,y=62313..72179,z=2482..3966
on x=57715..75033,y=-64838..-39620,z=-1072..18608
on x=-52076..-50307,y=-61914..-46848,z=2878..22917
on x=18629..39073,y=49950..76827,z=-62037..-28762
on x=34981..62227,y=53577..76994,z=12832..19906
on x=-72481..-43672,y=-47886..-26014,z=19399..48223
on x=-8950..18603,y=13309..37971,z=-74484..-69436
on x=-16767..5528,y=16470..32643,z=58249..82004
on x=-12651..2322,y=-64352..-47538,z=-62218..-30467
on x=-13237..8368,y=13412..29497,z=-78707..-55825
on x=-70547..-51064,y=6615..34177,z=42557..65661
on x=53013..71650,y=-38792..-10775,z=13355..31530
on x=52535..81262,y=-40006..-8742,z=-51591..-34103
on x=-39175..-23449,y=-2507..11905,z=55543..76852
on x=-68613..-57649,y=-53324..-43784,z=-8169..24131
on x=12853..22883,y=-21702..7249,z=-86624..-74055
on x=-11924..-411,y=-61590..-26323,z=47210..75920
on x=-51437..-43336,y=20599..48347,z=42966..60967
on x=45961..70580,y=19314..30352,z=-69098..-36802
on x=-60548..-34212,y=28954..46429,z=-59117..-39859
on x=-62440..-53023,y=12554..29103,z=32563..61939
on x=-51210..-28161,y=-68322..-51093,z=-21278..6194
on x=42750..73271,y=14889..35221,z=-58744..-53543
on x=-55823..-39470,y=-59599..-42144,z=17019..42589
on x=-14626..1632,y=-75196..-45499,z=29813..52303
on x=595..15798,y=73516..83286,z=-31411..-649
on x=-53834..-23305,y=45868..77210,z=33357..43262
on x=-24495..-6726,y=-24062..8131,z=56914..78360
on x=31518..45518,y=-75363..-55006,z=-2265..32328
on x=57179..80090,y=-53436..-28434,z=-10507..9540
on x=19193..49089,y=-78839..-71457,z=-17995..13869
on x=-62402..-51981,y=15899..34762,z=42267..58576
on x=17944..47745,y=-63935..-40872,z=-59048..-54098
on x=49358..64243,y=-18839..-6213,z=43211..65808
on x=14483..30044,y=42994..52549,z=-76659..-50535
on x=58035..68100,y=31678..54302,z=3451..28759
on x=-77543..-46970,y=3229..19452,z=38608..55865
on x=25815..33030,y=-29894..-10792,z=-86864..-62425
on x=43157..63898,y=39033..71114,z=-17821..16384
on x=11415..35975,y=-11789..896,z=-80905..-55968
on x=-33140..74,y=1083..12500,z=-81991..-63882
on x=-66126..-33283,y=-65854..-39427,z=-45468..-32819
on x=4778..21861,y=-71042..-48871,z=-59417..-42793
on x=66654..98311,y=-14961..2381,z=-15527..21698
on x=-84564..-52129,y=19269..38044,z=-34897..-17597
on x=59012..82206,y=-8303..11953,z=8834..25699
on x=13574..46006,y=-83277..-58527,z=-23044..14824
on x=20382..38581,y=30744..51434,z=57888..62080
on x=60452..85307,y=32764..40622,z=-39762..-26058
on x=-78269..-58393,y=30582..39299,z=-30047..576
on x=-30355..-13803,y=-51780..-37571,z=-74008..-46299
on x=-5431..15605,y=53001..91889,z=16338..46040
on x=24783..34698,y=-17285..5932,z=-90031..-65175
on x=22358..42285,y=-80259..-68397,z=-44798..-13377
on x=-5296..6765,y=28079..58182,z=-70072..-55694
on x=20162..30602,y=55806..73597,z=27897..41445
on x=4271..31598,y=-72728..-35977,z=44519..65750
on x=12440..24271,y=-48277..-26561,z=-71145..-51252
on x=-3230..30303,y=59709..79501,z=10257..23939
on x=15863..29909,y=55157..84726,z=-45716..-34568
on x=-6007..6155,y=-3590..10865,z=71616..95535
on x=-33417..-10218,y=32825..45380,z=49512..67932
on x=-52225..-19339,y=29366..54193,z=50056..61916
on x=64277..67962,y=-43243..-11282,z=30508..35903
on x=-25177..-400,y=-7312..31058,z=-84444..-76940
on x=-32582..-31592,y=52567..73867,z=-29799..-644
on x=-84821..-54152,y=13669..28233,z=18162..40461
on x=-212..22532,y=-85995..-59972,z=-6638..19342
on x=12495..32263,y=-18338..7656,z=72462..78596
on x=-14608..7212,y=-42813..-23395,z=-77420..-66253
on x=48698..63913,y=-53779..-49939,z=22862..39950
on x=50278..66996,y=8527..23848,z=28235..47427
on x=57129..66794,y=-37690..-15365,z=-48526..-23737
on x=39681..56086,y=-25423..8630,z=54173..70201
on x=12258..19958,y=-18056..-1191,z=67738..79771
on x=8088..31780,y=59042..84353,z=-35793..-10401
on x=33774..60133,y=-65548..-55788,z=-28589..-14140
on x=-35368..-12283,y=60938..81793,z=8638..32729
on x=19323..33787,y=14954..31736,z=57324..83827
on x=-934..27284,y=40738..64401,z=-72346..-44994
on x=37375..56938,y=14496..26504,z=-56123..-45458
on x=24597..39787,y=-48993..-23146,z=-79980..-61163
on x=5654..31491,y=-75282..-55534,z=-55679..-38046
on x=-6909..9001,y=-61556..-41382,z=44118..70793
on x=17333..28049,y=-86638..-52349,z=-48249..-30637
on x=-54748..-36063,y=-53508..-34114,z=-70131..-49615
on x=-28293..-6652,y=-90647..-75184,z=-12684..-4912
on x=-45167..-15419,y=-28987..-21061,z=-81664..-51780
on x=-23584..1129,y=-76808..-57898,z=33500..49257
on x=20054..42613,y=-47298..-28108,z=-82063..-42355
on x=-53852..-50576,y=-58701..-26251,z=-50341..-23253
on x=16211..25395,y=-21523..2810,z=-76930..-73048
on x=-32350..-13979,y=15333..30593,z=63987..77503
on x=-8540..11739,y=-11533..13133,z=-83865..-74061
on x=-14483..-1886,y=-54080..-24422,z=68560..79157
on x=-3326..5748,y=-72142..-58513,z=26135..45825
on x=44814..49451,y=-57335..-50365,z=40302..43907
on x=4519..27632,y=-48455..-26946,z=56271..73794
on x=22085..40257,y=-68663..-56245,z=6126..33900
on x=62259..84567,y=-897..27249,z=25041..52288
on x=-13814..513,y=-50211..-37031,z=-75913..-52812
on x=29410..54807,y=-59381..-42873,z=-59848..-44729
on x=48369..55589,y=-47449..-32898,z=29920..58696
on x=-79974..-56928,y=33336..65377,z=1585..19083
on x=61530..76326,y=-44520..-38327,z=-10820..7865
on x=-519..20760,y=-84206..-61108,z=-35843..-26411
on x=-17069..7484,y=-90856..-64674,z=-24329..-1589
on x=-37063..-25376,y=49505..53507,z=-56710..-42167
on x=-4283..20066,y=-26785..-3166,z=65856..80455
on x=-48412..-15302,y=-20001..-2462,z=66578..77948
on x=-85185..-46109,y=12909..39448,z=19995..51409
on x=9077..10893,y=-45852..-25338,z=-76093..-58832
on x=4235..8723,y=-80698..-63392,z=10001..36085
on x=-80998..-68799,y=-15775..9125,z=8355..32754
on x=29736..45732,y=-68693..-46530,z=-65819..-28780
on x=-84121..-55327,y=33443..54629,z=-27874..1837
on x=63558..91048,y=14768..50851,z=-10949..5883
on x=-74257..-64318,y=17934..34398,z=-42665..-30288
on x=-35499..7,y=-68944..-57972,z=-51036..-27054
on x=-5826..14898,y=73968..86327,z=-1325..19771
on x=52265..75083,y=-43126..-37164,z=13180..33003
on x=-46654..-24382,y=29960..46509,z=-74247..-48459
on x=47920..68066,y=46517..57977,z=-39718..-25106
on x=67799..77261,y=-30142..2227,z=-47871..-33556
on x=32537..50313,y=-60037..-36772,z=-57616..-34052
on x=55131..80059,y=9933..30679,z=31041..39852
on x=-51790..-25717,y=69072..86821,z=5328..25157
on x=-9634..15278,y=-44873..-27097,z=52183..76657
on x=26064..42758,y=-65898..-39589,z=-60043..-38316
on x=-71038..-50707,y=25477..49544,z=-9651..13867
on x=51862..75445,y=-48493..-28730,z=-40041..-16410
on x=-12631..-1689,y=-2359..25910,z=71977..98447
on x=58553..94594,y=-18471..1345,z=-19004..-11715
on x=-76801..-60256,y=-29512..-9792,z=17888..53358
on x=-36213..-13560,y=-31746..-2878,z=67013..88654
on x=19685..41298,y=31326..45650,z=59044..70405
on x=-4773..12117,y=-74551..-58365,z=27808..58364
on x=-54161..-36263,y=-58729..-50436,z=35796..52763
on x=7068..33109,y=-28410..-18985,z=65097..79170
on x=543..21647,y=42265..65414,z=-76179..-44183
on x=-74831..-62130,y=25051..37135,z=-182..2511
on x=-55744..-48390,y=-55491..-38135,z=29126..58726
on x=17589..46473,y=-19752..-4935,z=68463..81314
on x=-8754..14914,y=68586..95547,z=-13195..25723
on x=-45570..-29917,y=61533..81728,z=-9102..11762
on x=-87207..-67050,y=-5358..6724,z=32549..40075
on x=44807..69788,y=-8679..21707,z=-72043..-48974
on x=67959..84337,y=30525..40997,z=-5550..18396
on x=-66642..-48144,y=36756..53651,z=-18915..2025
on x=-14430..-4207,y=-30597..-15319,z=-77714..-60129
on x=38233..57987,y=-38146..-17316,z=62073..80776
on x=-44193..-21291,y=63992..82999,z=13111..26839
on x=47767..81128,y=-17336..7363,z=35331..66767
on x=-10931..15773,y=-26584..-7643,z=60045..81152
on x=-21028..8981,y=3056..5995,z=-89837..-77762
on x=53372..83042,y=-38534..-30429,z=11424..44089
on x=-20367..-12598,y=-73831..-42838,z=37245..50968
on x=-93494..-69398,y=-20963..4662,z=-19387..-6312
on x=-38328..-7673,y=48091..72363,z=-45146..-27089
on x=41967..55226,y=-22379..-10396,z=-79439..-64136
on x=-28947..-12923,y=55354..77038,z=-10552..14300
on x=17750..40077,y=-72902..-52282,z=33711..54899
on x=-8384..19161,y=-78375..-70414,z=26928..39449
on x=21150..30449,y=46423..80290,z=-56110..-29699
on x=77183..86674,y=-6921..23292,z=-10970..15396
on x=-80017..-60226,y=-44559..-30295,z=-12256..12301
on x=14432..31999,y=62141..83030,z=-59990..-35638
on x=65838..69805,y=-53619..-37236,z=4018..36533
on x=-68396..-47047,y=-53102..-30228,z=9435..25148
on x=-26617..10833,y=1875..16926,z=-92009..-61186
on x=-38124..-3078,y=6187..36060,z=66201..88886
on x=-72143..-45931,y=-27814..-16383,z=38655..59573
on x=61446..71298,y=-5408..13016,z=38021..60585
on x=-3408..11974,y=55698..68864,z=37690..70781
on x=47034..72746,y=-55183..-33673,z=23446..40762
on x=-84421..-61649,y=-6840..5363,z=14932..43322
on x=28846..65493,y=-72426..-48346,z=-20535..-10722
on x=-78528..-59010,y=-22590..11550,z=-47404..-41508
off x=-74639..-48768,y=50612..58676,z=-37470..-23435
off x=43917..73832,y=2245..19604,z=-65699..-56425
on x=15344..22153,y=-79043..-61452,z=-32495..4414
off x=58763..90185,y=-25653..-9217,z=-25619..-6105
on x=-76822..-52893,y=42123..54159,z=-5873..23732
on x=-73837..-54010,y=-34332..-8871,z=15166..40844
on x=-68153..-37957,y=35664..48505,z=-54094..-31793
off x=-78798..-58209,y=-1962..22855,z=-30619..-17925
off x=30588..44097,y=-39741..-16114,z=52031..76732
off x=-21370..-3036,y=-92078..-63714,z=-23463..-9635
off x=-39616..-9573,y=-76126..-52989,z=-36329..-25733
off x=-78975..-60696,y=5492..16103,z=37680..45425
on x=-13273..4741,y=-57234..-22905,z=-84956..-60280
on x=12195..39003,y=-56490..-28038,z=46958..84048
on x=-65407..-38585,y=-67817..-42389,z=-12866..9632
off x=54548..66564,y=-61939..-42742,z=-22049..9590
on x=-56650..-35894,y=51789..62557,z=-8337..9488
off x=51851..60699,y=-58887..-26242,z=-46246..-36918
on x=-30216..3645,y=65431..87903,z=3102..28512
off x=-38385..-20582,y=-67082..-51436,z=-50559..-33537
off x=-37826..-24595,y=55536..90023,z=-27711..-15046
on x=-88016..-51046,y=17580..52942,z=16868..29419
off x=20737..24390,y=71411..81207,z=7623..42707
off x=-79899..-61924,y=14415..31841,z=-22454..-1564
off x=30389..53719,y=-7867..-4328,z=-71576..-52704
on x=-33559..-17170,y=28168..43819,z=-74041..-68536
on x=62447..80758,y=-52441..-20813,z=11444..34397
off x=6189..17502,y=-69036..-44498,z=37852..65122
on x=8710..43957,y=-60672..-36883,z=-73854..-47471
on x=-63831..-42541,y=-47630..-33073,z=-35136..-23775
off x=-54635..-47473,y=41469..47997,z=-37298..-19312
on x=19094..36724,y=59501..73156,z=-11554..2780
on x=-36499..-5010,y=31578..59809,z=50869..79415
on x=-34865..-25789,y=11805..33967,z=57305..89626
on x=-50240..-39620,y=-81921..-51481,z=10359..28340
on x=-77806..-70466,y=-30235..-10612,z=3085..22812
off x=551..19833,y=-76142..-57090,z=41520..54215
off x=-79120..-72537,y=-22772..-11937,z=-20754..-805
on x=-31334..-1081,y=-78350..-64599,z=24953..35506
on x=-51889..-20757,y=-74362..-51343,z=-34621..-15692
on x=-98265..-66145,y=-24839..1358,z=15084..24204
on x=38568..60507,y=26311..38854,z=41126..63130
on x=56296..82005,y=-4401..12363,z=32618..57099
on x=-46852..-16936,y=41968..79172,z=-55910..-41041
off x=13532..40243,y=59041..84883,z=-24915..-6012
off x=-70988..-55771,y=-27811..-11605,z=-48798..-30685
on x=-54732..-28612,y=50039..67869,z=30748..51720
on x=-83072..-60710,y=-36043..-10715,z=-13135..10245
on x=10728..36396,y=-31100..-18055,z=57919..84461
on x=2737..12084,y=-85649..-62210,z=-4469..20470
off x=-44779..-24754,y=53929..71783,z=-50551..-33795
off x=-82953..-57138,y=15163..42222,z=-32984..-15683
on x=-61323..-50856,y=-53357..-47904,z=-35587..-22281
on x=-74588..-57833,y=-8832..6132,z=-31991..-24666
off x=-27374..-15579,y=-59298..-34543,z=-69631..-48697
off x=-27254..-9222,y=71007..92442,z=-3642..5546
off x=28969..57928,y=57762..73100,z=12034..21785
on x=-30375..-12525,y=52858..65456,z=-54830..-33732
on x=60470..95369,y=-2198..23349,z=-29883..-8231
on x=-13378..-8866,y=49702..52549,z=-64388..-44609
off x=-32460..-18370,y=60059..68523,z=33081..53134
off x=43676..68601,y=44878..74155,z=17421..23197
on x=-45699..-37167,y=-25693..-8124,z=-81683..-65258
on x=-58139..-40120,y=-24376..2800,z=-65986..-47088
on x=-49747..-44146,y=46481..69677,z=-56278..-36813
on x=-16341..4614,y=60869..81852,z=26267..50883
off x=-13764..3695,y=-80186..-53825,z=-48931..-38545
off x=7407..32603,y=20253..45103,z=-67931..-66776
on x=14925..45347,y=31662..50222,z=53950..78292
on x=13191..26905,y=62052..92403,z=-31024..1155
on x=-83062..-54122,y=-1357..19888,z=27293..48527
off x=-93419..-68794,y=-31330..-7620,z=4925..33729
off x=-14318..-5495,y=57170..79754,z=27999..47808
off x=-74220..-50632,y=-46040..-26079,z=42743..49504
on x=19302..52277,y=-6661..31359,z=58677..87046
on x=57756..67065,y=-12060..1434,z=28209..50664
on x=-45256..-18994,y=64734..91459,z=-22776..147
on x=2323..22083,y=-89059..-63282,z=-49116..-32115
on x=27373..58488,y=48511..78089,z=-25094..-5863
on x=-46047..-19903,y=-34084..-17918,z=-86422..-56649
off x=27981..32209,y=7490..27523,z=58491..80769
off x=-39210..-18976,y=-22509..29,z=-79485..-60560
off x=-22207..3806,y=74571..91724,z=-11234..12761
off x=-97092..-68711,y=5374..12518,z=4923..11841
off x=-90882..-68060,y=-16889..-11552,z=-5102..10039
off x=-11213..6478,y=-85565..-72283,z=-4476..8128
off x=64470..75862,y=10465..21634,z=-40243..-14437
off x=-27023..-4099,y=-15964..10612,z=67148..78876
off x=27963..54332,y=49375..73688,z=-44834..-7022
off x=-85216..-67584,y=-10377..18116,z=-43000..-22112
on x=72263..90946,y=6704..33616,z=771..33494
off x=-3433..25282,y=-9347..12401,z=-81820..-70318
on x=21693..58088,y=43923..61620,z=27668..46963
on x=39275..64334,y=-69135..-35447,z=-47184..-34444
off x=-32867..-7283,y=33466..64518,z=-65055..-36273
on x=32636..60251,y=-3200..14231,z=45891..68060
off x=50431..66008,y=7268..32152,z=50280..52350
off x=-63589..-60337,y=50981..55766,z=-18627..-6279
off x=8350..13892,y=-11989..6902,z=63824..88445
off x=-18142..-1779,y=43113..61876,z=-65235..-42503
on x=28737..38695,y=-3968..10606,z=60307..85107
on x=-43061..-32064,y=-9548..3036,z=47770..85409
on x=-27198..1005,y=77204..96476,z=-22312..-3369
off x=-26927..-4332,y=-93413..-62648,z=-2165..15047
on x=882..15563,y=-80136..-53702,z=34131..58891
on x=-82201..-55429,y=-15919..-9449,z=-50253..-22652
off x=40616..66339,y=-57859..-47076,z=10603..36553
on x=18063..33341,y=69011..93465,z=-8627..-2040
off x=-68385..-60942,y=30536..50506,z=1797..9915
on x=-40928..-30471,y=-82701..-64341,z=-35902..-18193
off x=-77469..-57415,y=-24271..-6869,z=8167..25744
on x=24531..61482,y=-66994..-46687,z=22052..36424
off x=-28776..-3137,y=70836..93673,z=-12735..7999
off x=6064..16870,y=52387..90446,z=15339..41943
off x=68478..76396,y=-41052..-24834,z=-39798..-16372
off x=28793..45427,y=-66929..-48078,z=27086..47805
off x=-67582..-45224,y=16788..32165,z=-62442..-49126
off x=-84727..-64172,y=9719..33126,z=-50240..-36413
off x=2764..9857,y=68298..90509,z=6926..34758
on x=-59645..-42830,y=44942..60976,z=9930..34747
on x=-7043..20419,y=-95055..-75260,z=-10382..13178
off x=-4928..21508,y=-54356..-42031,z=63343..71761
off x=-4483..8807,y=-82132..-61856,z=31416..63277
on x=-72217..-55909,y=46952..67423,z=10714..31698
off x=22895..58198,y=47638..57414,z=25383..50967
off x=70546..91637,y=-48361..-21603,z=2899..10335
on x=7909..29028,y=-64056..-52017,z=35749..74647
off x=62260..98572,y=8097..20893,z=-8563..2624
off x=33752..54759,y=36452..63551,z=28533..51030
off x=63896..85471,y=28114..42147,z=-26803..-17284
off x=43558..70451,y=-17272..13603,z=38130..67484
on x=-19731..6034,y=-15193..12094,z=-81066..-60427
off x=49659..72102,y=2603..16710,z=53930..76446
off x=-5332..26219,y=-16112..16161,z=74016..87514
off x=-84911..-54855,y=35128..47433,z=-10860..9165
off x=17935..47626,y=12273..26771,z=-72306..-53894
off x=26346..27207,y=-60137..-44600,z=-72346..-36244
on x=-46145..-43523,y=-49645..-30008,z=38829..58204
off x=-86551..-64146,y=-12293..14180,z=-38097..-32731
off x=27238..64184,y=-14354..6709,z=-84864..-57867
off x=-77014..-45379,y=-65518..-37193,z=-21935..2444
on x=-12304..-8053,y=-32349..-1395,z=58655..80497
on x=60942..83152,y=-53023..-35167,z=-17188..13921
on x=30704..42290,y=53720..85918,z=-6435..11238
off x=-9341..12410,y=-9684..1176,z=65742..82506
off x=52580..71820,y=-14100..8167,z=-48182..-32699
off x=-42414..-26715,y=286..21760,z=51828..88130
off x=-24023..1914,y=-78725..-67305,z=-57408..-32261
off x=-1061..34327,y=-41010..-16073,z=66069..77692
off x=-27106..-11480,y=-129..22973,z=-90479..-56907
on x=28531..62573,y=46883..69383,z=-11048..22810
on x=71560..96555,y=-10327..5671,z=2846..39738
off x=15176..26978,y=-88043..-66452,z=-35176..-9815
off x=-21046..-2463,y=74147..88780,z=-22899..7921
off x=62521..73879,y=-6047..23513,z=25987..41982
off x=-3229..10686,y=26952..30191,z=-86491..-69080
on x=54889..65155,y=-8873..22280,z=46500..63262
on x=31457..39435,y=45593..77266,z=18802..43882
off x=-56671..-39916,y=-69216..-52639,z=-25565..-4992
on x=101..4685,y=-12296..8001,z=-83483..-79508
on x=-73290..-37527,y=44928..65483,z=-9413..-5646
on x=-35222..-23190,y=-73159..-49735,z=-57972..-42478
on x=13833..31933,y=19452..33559,z=72451..89356
on x=29205..56079,y=46677..62132,z=40103..54403
off x=-2638..11110,y=23932..40331,z=-87224..-51338
on x=35387..44166,y=-66558..-44113,z=49996..62991
off x=-15021..9148,y=-37367..-22659,z=-76451..-51588
off x=19600..42706,y=9725..35919,z=-88597..-50137
off x=-97042..-67514,y=-6597..3898,z=11572..33424
off x=-39628..-19723,y=58528..82562,z=-11091..6319
off x=-8834..-1223,y=-89647..-71163,z=11939..19850
on x=-65021..-39602,y=-71515..-46679,z=-23801..3437
off x=-83879..-62719,y=13926..28623,z=-8747..21702
off x=-8646..-3497,y=8971..26462,z=-98278..-61916
on x=-33221..-9104,y=-78841..-46220,z=-43878..-41648
off x=-43550..-17837,y=-9584..8219,z=-76098..-74685
off x=-82579..-61705,y=38202..56469,z=-1055..14298
on x=25689..37701,y=65232..69607,z=24367..42672
on x=-42458..-32066,y=-75719..-65472,z=-29193..-3801
off x=-22..14837,y=-29209..635,z=-90363..-72543
on x=-74413..-47264,y=-54522..-28588,z=5937..39559
on x=21089..26076,y=37702..51056,z=-67095..-55472
off x=31742..58033,y=4590..25947,z=-76500..-60789
on x=-35852..-9119,y=-76205..-45203,z=-47687..-35294
off x=23217..41029,y=-3234..15105,z=68782..74072
on x=52058..89126,y=-50422..-30857,z=-8709..10826
off x=-51490..-42068,y=11308..31021,z=-73967..-44035
on x=-90713..-53955,y=3847..17459,z=-42841..-13064
off x=69346..89076,y=16046..26148,z=-31148..2070
on x=-91236..-71702,y=-9654..12433,z=1477..13198
on x=1331..28078,y=-69702..-40355,z=-64692..-43979
off x=50574..70337,y=-15383..-6575,z=41848..64343
on x=24149..54714,y=-29135..-3260,z=-82604..-46272
on x=61674..92804,y=-37425..-18188,z=-10269..9583
on x=29278..46289,y=59081..63620,z=29317..53729
off x=22296..41176,y=66892..90309,z=-27453..7399
off x=53038..58101,y=-58443..-50874,z=-10298..19080
off x=30371..49011,y=-39391..-24388,z=-68271..-62633
on x=-72143..-61407,y=32665..57053,z=-32273..464
off x=-47814..-25131,y=46029..74913,z=36938..62900"""

raw_part2 = """on x=-5..47,y=-31..22,z=-19..33
on x=-44..5,y=-27..21,z=-14..35
on x=-49..-1,y=-11..42,z=-10..38
on x=-20..34,y=-40..6,z=-44..1
off x=26..39,y=40..50,z=-2..11
on x=-41..5,y=-41..6,z=-36..8
off x=-43..-33,y=-45..-28,z=7..25
on x=-33..15,y=-32..19,z=-34..11
off x=35..47,y=-46..-34,z=-11..5
on x=-14..36,y=-6..44,z=-16..29
on x=-57795..-6158,y=29564..72030,z=20435..90618
on x=36731..105352,y=-21140..28532,z=16094..90401
on x=30999..107136,y=-53464..15513,z=8553..71215
on x=13528..83982,y=-99403..-27377,z=-24141..23996
on x=-72682..-12347,y=18159..111354,z=7391..80950
on x=-1060..80757,y=-65301..-20884,z=-103788..-16709
on x=-83015..-9461,y=-72160..-8347,z=-81239..-26856
on x=-52752..22273,y=-49450..9096,z=54442..119054
on x=-29982..40483,y=-108474..-28371,z=-24328..38471
on x=-4958..62750,y=40422..118853,z=-7672..65583
on x=55694..108686,y=-43367..46958,z=-26781..48729
on x=-98497..-18186,y=-63569..3412,z=1232..88485
on x=-726..56291,y=-62629..13224,z=18033..85226
on x=-110886..-34664,y=-81338..-8658,z=8914..63723
on x=-55829..24974,y=-16897..54165,z=-121762..-28058
on x=-65152..-11147,y=22489..91432,z=-58782..1780
on x=-120100..-32970,y=-46592..27473,z=-11695..61039
on x=-18631..37533,y=-124565..-50804,z=-35667..28308
on x=-57817..18248,y=49321..117703,z=5745..55881
on x=14781..98692,y=-1341..70827,z=15753..70151
on x=-34419..55919,y=-19626..40991,z=39015..114138
on x=-60785..11593,y=-56135..2999,z=-95368..-26915
on x=-32178..58085,y=17647..101866,z=-91405..-8878
on x=-53655..12091,y=50097..105568,z=-75335..-4862
on x=-111166..-40997,y=-71714..2688,z=5609..50954
on x=-16602..70118,y=-98693..-44401,z=5197..76897
on x=16383..101554,y=4615..83635,z=-44907..18747
off x=-95822..-15171,y=-19987..48940,z=10804..104439
on x=-89813..-14614,y=16069..88491,z=-3297..45228
on x=41075..99376,y=-20427..49978,z=-52012..13762
on x=-21330..50085,y=-17944..62733,z=-112280..-30197
on x=-16478..35915,y=36008..118594,z=-7885..47086
off x=-98156..-27851,y=-49952..43171,z=-99005..-8456
off x=2032..69770,y=-71013..4824,z=7471..94418
on x=43670..120875,y=-42068..12382,z=-24787..38892
off x=37514..111226,y=-45862..25743,z=-16714..54663
off x=25699..97951,y=-30668..59918,z=-15349..69697
off x=-44271..17935,y=-9516..60759,z=49131..112598
on x=-61695..-5813,y=40978..94975,z=8655..80240
off x=-101086..-9439,y=-7088..67543,z=33935..83858
off x=18020..114017,y=-48931..32606,z=21474..89843
off x=-77139..10506,y=-89994..-18797,z=-80..59318
off x=8476..79288,y=-75520..11602,z=-96624..-24783
on x=-47488..-1262,y=24338..100707,z=16292..72967
off x=-84341..13987,y=2429..92914,z=-90671..-1318
off x=-37810..49457,y=-71013..-7894,z=-105357..-13188
off x=-27365..46395,y=31009..98017,z=15428..76570
off x=-70369..-16548,y=22648..78696,z=-1892..86821
on x=-53470..21291,y=-120233..-33476,z=-44150..38147
off x=-93533..-4276,y=-16170..68771,z=-104985..-24507"""

example = """on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682"""

example = """on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682"""


# raw = example


def init(raw_string):
    instructions = []
    for line in raw_string.splitlines():
        onoff, range_strings = line.split(" ")
        range_strings = range_strings.split(",")
        ranges = []
        for string in range_strings:
            start, stop = list(map(int, re.findall("[-\d]+", string)))
            ranges.append(Range(start, stop + 1))
        shape = Shape(*ranges)
        instructions.append([onoff, shape])
    return instructions


def galaxy_brain(instructions):
    reactor = set()
    for onoff, new_shape in instructions:
        overlappers = {shape for shape in reactor if shape.overlaps(new_shape)}
        reactor = reactor.difference(overlappers)
        for shape in overlappers:
            shattered_shape = shape.difference(new_shape)
            reactor = reactor.union(shattered_shape)

        if onoff == "on":
            reactor.add(new_shape)

    return sum(shape.count() for shape in reactor)


def part1():
    instructions = [
        (onoff, shape)
        for onoff, shape in init(raw)
        if all(axis.overlaps(Range(-50, 50)) for axis in shape.axes)
    ]
    return galaxy_brain(instructions)


class RangeError(Exception):
    pass


class ShapeError(Exception):
    pass


class Range(tuple):
    def __new__(cls, start, stop):
        return super().__new__(cls, [start, stop])

    def __init__(self, start, stop):
        if stop < start:
            raise RangeError(f"stop must > start! {stop=}, {start=}")

    def __repr__(self) -> str:
        return f"Range({self.start}..{self.stop})"

    def __contains__(self, o: object) -> bool:
        return o in range(self.start, self.stop)

    def contains(self, o: "Range"):
        return (self.start < o.start < self.stop, self.start < o.stop < self.stop)

    def get_overlaps(self, o: "Range") -> list:
        if not any(self.contains(o)) and not any(o.contains(self)):
            return []
        return [max(self.start, o.start), min(self.stop, o.stop)]

    def overlaps(self, o: "Range") -> bool:
        return bool(self.get_overlaps(o))

    def split(self, *breakpoints):
        current = self
        new = []
        for bp in breakpoints:
            if bp in (self.start, self.stop):
                continue
            if bp not in self:
                raise RangeError(f"breakpoint {bp} not in {self}")
            new_range = Range(current.start, bp)
            if new_range.start != new_range.stop:
                new.append(new_range)
            current = Range(bp, self.stop)
        new.append(current)
        return new

    @property
    def start(self):
        return self[0]

    @property
    def stop(self):
        return self[1]


class Shape(tuple):
    def __new__(cls, *axes: Range):
        return super().__new__(cls, axes)

    def __init__(self, *axes: Range):
        if len(axes) < 2:
            raise ShapeError("You need to specify at least 2 axes")
        self.axes = axes

    def __repr__(self) -> str:
        return (
            "Shape("
            + ", ".join(
                f"{axisname}={axis.start}..{axis.stop}" for axisname, axis in zip("xyz", self.axes)
            )
            + ")"
        )

    def shatter(self, shape):
        overlaps = self.get_overlaps(shape)
        new_me = self.split(*overlaps)
        new_other = shape.split(*overlaps)
        return new_me, new_other

    def union(self, shape):
        my_pieces, other_pieces = self.shatter(shape)
        return set(my_pieces).union(set(other_pieces))

    def difference(self, shape):
        my_pieces, other_pieces = self.shatter(shape)
        return set(my_pieces).difference(set(other_pieces))

    def split(self, x_breaks, y_breaks=None, z_breaks=None):
        y_breaks = y_breaks or []
        z_breaks = z_breaks or []
        breakpoints = [x_breaks, y_breaks, z_breaks]
        new_axes = [axis.split(*breaks) for axis, breaks in zip(self.axes, breakpoints)]
        return {Shape(*axes) for axes in product(*new_axes)}

    def count(self):
        prod = 1
        for axis in self.axes:
            length = abs(axis.stop - axis.start)
            prod *= length
        return prod

    def get_overlaps(self, shape):
        return [mine.get_overlaps(other) for mine, other in zip(self.axes, shape.axes)]

    def overlaps(self, shape):
        return all(map(bool, self.get_overlaps(shape)))


def part2():
    instructions = init(raw)
    return galaxy_brain(instructions)


if __name__ == "__main__":
    p1 = part1()
    print(f"{p1=}")
    assert p1 == 533863
    p2 = part2()
    print(f"{p2=}")
    assert p2 == 1261885414840992
