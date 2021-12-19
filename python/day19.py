import re
from collections import deque
from pprint import pprint

raw = """--- scanner 0 ---
-254,619,-733
-486,-729,544
807,441,685
-611,-859,516
-280,628,-633
-654,-760,550
782,-651,265
-779,702,594
792,439,689
858,-686,356
857,734,-711
405,-383,-473
-814,-443,-779
-5,56,-110
833,420,502
512,-465,-442
-790,-313,-826
-742,834,501
879,681,-656
115,-50,16
-305,681,-634
806,695,-591
-751,896,637
506,-384,-370
-672,-407,-828
812,-724,242

--- scanner 1 ---
-385,-707,644
547,569,-466
-537,541,-637
-496,708,-577
539,780,875
-673,-647,-522
467,-678,445
452,-748,373
-522,577,-514
801,-707,-465
561,634,-393
504,818,809
-381,492,301
803,-711,-480
-603,-570,-512
-486,561,299
87,57,48
-415,-710,785
-509,-691,660
-638,-720,-452
384,744,768
-64,-19,-42
508,689,-415
-400,745,313
454,-741,583
822,-524,-439

--- scanner 2 ---
362,-684,-471
-654,-602,-819
-883,736,292
673,614,-903
576,-259,509
320,927,301
517,898,234
-183,158,-129
414,801,255
-927,818,457
682,710,-820
-733,-696,-707
-813,709,453
-635,544,-442
780,-284,577
-905,-283,537
-132,26,16
-18,11,-157
639,-256,636
-940,-251,580
371,-532,-552
-864,-282,641
-567,690,-435
665,551,-745
-743,-709,-809
379,-534,-558
-687,634,-391

--- scanner 3 ---
387,-333,-811
794,382,-470
-350,-484,733
-526,655,459
494,-302,-729
714,453,692
-504,684,-465
-672,690,-434
-629,656,-335
764,405,-543
-808,-686,-881
-632,687,490
840,496,-508
-832,-639,-751
-436,-501,702
595,390,657
594,-765,459
488,-230,-810
561,-740,480
632,562,616
-690,-688,-787
98,26,-130
-609,690,617
4,162,47
486,-757,537
-458,-625,736

--- scanner 4 ---
726,719,-563
445,-551,451
3,11,32
765,689,513
640,-943,-584
830,751,617
83,-88,-92
-760,507,688
-388,331,-324
-684,466,745
879,770,489
-456,254,-360
447,-433,357
-328,-495,-804
639,-918,-637
709,741,-731
494,-409,487
-494,-547,-759
742,652,-774
-618,486,579
-535,-545,-828
-778,-708,376
-371,254,-342
540,-969,-575
-794,-660,444
-596,-720,404

--- scanner 5 ---
-450,529,-435
-343,449,-368
-411,-365,-818
-821,-676,432
-682,868,691
-743,892,544
798,-426,478
-803,915,709
471,-589,-721
-418,-394,-827
-712,-538,380
310,902,-680
550,706,500
755,-477,564
-462,436,-346
-473,-328,-822
366,745,-703
727,-384,456
599,631,543
305,741,-681
534,-692,-692
-737,-650,448
56,50,-63
-92,-33,36
593,-523,-749
634,807,576

--- scanner 6 ---
571,-840,417
-355,312,-834
-575,-725,-402
-636,-578,-378
-559,-778,741
706,-577,-639
554,-818,585
-630,373,296
657,-534,-564
-523,-819,815
640,844,564
473,669,-525
-494,382,358
412,647,-529
-343,401,-741
538,-751,374
-587,345,490
-724,-812,788
24,-96,43
740,870,573
741,-610,-463
641,819,511
417,646,-368
-696,-743,-355
143,19,-129
-236,334,-821

--- scanner 7 ---
692,674,-596
-796,518,391
524,705,-602
89,-168,58
-734,414,456
-697,-873,479
-815,390,342
-765,-432,-582
-764,-662,495
-412,591,-487
-302,557,-519
399,-757,-646
-786,-830,512
-363,755,-539
-5,-11,-24
873,-736,582
898,-683,581
567,804,-568
-758,-459,-783
-724,-506,-618
427,-951,-689
924,-674,681
364,388,727
506,352,776
388,258,774
436,-889,-553

--- scanner 8 ---
-483,-819,348
-357,-772,407
329,662,-347
471,601,-345
684,671,830
-459,729,-734
674,-494,738
633,-425,740
-403,424,565
-881,-672,-682
840,-449,790
-754,-790,-686
-384,465,537
1,-2,109
-728,-720,-588
580,-516,-549
853,653,801
33,-143,-25
551,-452,-463
777,653,839
501,587,-360
-443,510,-695
-494,-834,463
-443,598,575
-392,594,-746
541,-569,-453

--- scanner 9 ---
-269,713,626
-549,315,-507
712,346,-755
166,48,87
810,-793,-445
551,-630,856
441,487,574
-420,-393,-717
830,-728,-450
-399,-519,417
790,338,-647
-393,-578,-656
-319,-596,413
-517,454,-393
769,363,-680
-257,696,585
-338,-508,453
481,435,650
451,481,620
105,-105,-33
-599,349,-486
543,-680,625
-268,832,714
586,-678,698
732,-734,-311
-401,-640,-743

--- scanner 10 ---
-562,-785,664
67,-3,-4
-559,849,300
-740,824,-844
732,789,-674
795,-407,-542
-500,888,301
865,-668,798
584,553,281
1,121,-155
-374,-391,-514
-712,788,-857
713,763,-427
734,-371,-553
864,-580,679
-355,781,303
534,532,315
616,439,420
-813,751,-938
-536,-804,774
876,-539,662
740,702,-612
814,-367,-630
-425,-268,-633
-350,-269,-596
-561,-811,509

--- scanner 11 ---
174,-15,-94
-287,-483,418
-365,528,547
-292,-538,352
802,434,-674
112,-89,93
-411,301,-721
-422,469,716
804,-713,-593
-679,-515,-505
-393,406,613
-296,-476,389
810,334,686
794,-790,-523
771,-987,759
956,226,694
875,-940,763
864,-863,-558
-746,-408,-425
834,238,702
679,398,-659
739,565,-700
727,-885,760
-768,-527,-412
-434,245,-878
-433,240,-717

--- scanner 12 ---
309,-697,759
-124,90,-29
-454,627,471
589,-753,-296
747,598,928
650,-758,-524
-445,491,409
-384,766,-721
-417,534,603
653,546,-289
-846,-553,-646
-524,-353,418
35,-44,112
671,425,-242
-892,-564,-799
-860,-602,-586
-473,778,-628
411,-729,785
724,-792,-411
-491,-406,555
706,562,854
440,-677,729
506,485,-265
740,397,901
-539,-436,521
-406,885,-708

--- scanner 13 ---
883,-434,-802
-633,721,-335
598,-683,406
-311,576,666
480,-659,504
-490,-681,527
628,534,777
-346,653,537
-410,-734,-635
789,-491,-825
644,482,-707
729,-438,-795
-643,771,-432
571,484,-664
147,-65,-35
613,469,672
-550,-666,679
-487,-655,-542
16,0,114
-693,687,-281
510,-745,363
-437,-673,550
-345,563,745
688,514,655
-514,-739,-636
413,532,-699

--- scanner 14 ---
815,593,506
490,-765,493
-739,-898,-828
-752,-920,-709
-497,600,625
-830,-412,621
-571,652,-523
-641,642,-446
387,-780,410
572,-887,-477
835,684,-382
-677,-458,610
440,-850,-570
-659,-831,-721
-378,640,611
-400,630,566
-606,712,-373
854,725,-569
40,-82,145
524,-813,463
855,598,636
833,699,-386
378,-859,-434
804,517,564
-617,-444,659

--- scanner 15 ---
658,-585,-536
-278,682,382
56,-5,-82
516,-608,-461
803,504,406
520,-578,-410
885,773,-453
-628,-753,582
977,821,-570
-484,720,-679
-341,707,-731
539,-446,699
-370,-382,-725
573,-398,729
-781,-799,571
777,402,438
-372,-602,-801
-425,-546,-750
-568,-767,533
-506,743,377
824,826,-596
-393,817,343
-418,802,-717
747,533,458
436,-431,782

--- scanner 16 ---
-382,323,350
-476,300,407
-656,-563,666
669,-448,602
721,-545,-853
-413,-524,-727
-449,-463,-738
-536,330,354
667,-363,710
454,705,-518
90,-24,-73
788,503,815
-852,426,-616
-75,-113,19
-741,-503,817
-621,418,-566
449,685,-453
703,-488,765
719,559,774
-756,-586,627
-409,-444,-650
660,-518,-668
582,442,799
747,-526,-606
315,607,-512
-694,461,-568

--- scanner 17 ---
-515,-462,857
790,-685,519
-354,578,-320
763,-735,-688
393,408,537
530,464,475
764,-587,589
-826,-825,-379
14,84,113
119,-22,1
391,369,-721
-686,-795,-430
708,-747,-794
-804,791,860
-536,566,-348
-597,741,884
-544,-548,793
-505,-452,740
-805,-706,-362
917,-681,637
519,349,490
427,548,-773
715,-700,-630
-638,739,815
-338,626,-388
497,415,-704

--- scanner 18 ---
535,-556,-635
775,624,-831
-636,-911,432
-699,504,767
330,-620,548
-638,-771,580
-660,-416,-820
-708,476,515
-56,-43,3
780,625,-670
451,-632,-736
-665,-664,436
614,665,660
-576,-573,-797
287,-534,497
-634,484,689
-479,325,-441
719,647,-674
492,693,594
-170,45,131
358,-512,455
-627,-398,-835
551,636,763
-572,334,-423
-403,363,-441
486,-599,-560

--- scanner 19 ---
-530,724,-458
-536,382,731
695,276,943
686,-872,419
296,-611,-759
-419,392,721
-121,3,25
474,562,-439
-416,-861,432
457,-610,-764
-483,478,692
620,289,771
-583,-438,-535
453,-588,-703
634,274,801
57,-138,154
-392,-811,639
-461,-809,598
-569,673,-578
515,502,-606
-645,-387,-436
704,-901,588
500,625,-570
686,-910,495
-583,746,-513
-636,-413,-536

--- scanner 20 ---
-639,-437,561
-616,-385,619
-752,797,-468
-382,-845,-641
-590,493,529
849,672,763
889,758,-497
908,717,-469
-547,-391,632
416,-476,634
-610,387,699
73,45,37
-476,-830,-543
387,-347,649
833,453,802
849,584,-507
900,588,814
635,-597,-452
442,-387,630
-672,795,-359
-528,434,601
755,-571,-361
-425,-700,-531
-709,827,-340
730,-508,-471

--- scanner 21 ---
597,566,-444
-555,-442,330
611,596,-459
-411,643,589
-581,-562,421
-371,-755,-661
-492,-467,440
97,23,-142
527,779,731
-331,-810,-680
76,163,1
-645,724,-648
545,872,740
-663,652,561
600,-348,476
545,948,702
688,-348,-794
-585,717,581
469,-364,-833
-531,628,-575
604,-297,-845
536,424,-446
-567,639,-628
774,-308,466
-460,-781,-665
733,-289,438

--- scanner 22 ---
685,365,-686
-525,-603,382
596,395,-727
-564,-723,433
-531,586,724
520,-751,604
383,-547,-346
-658,580,-678
625,626,817
-556,-512,-908
700,798,830
-478,547,628
-578,-658,360
-83,-86,-24
505,-715,481
-401,-548,-801
18,41,-100
-592,552,-864
-414,576,714
639,656,832
469,-731,-332
364,-800,-334
-549,594,-802
479,-584,544
-521,-474,-842
584,296,-593

--- scanner 23 ---
773,789,374
715,-317,-357
-441,586,-402
-553,-452,574
-556,-579,597
739,-263,-352
-473,620,-292
822,825,516
437,659,-786
39,130,34
502,763,-724
-804,-597,-372
-522,373,577
-550,503,702
759,-698,748
388,787,-805
722,-264,-384
820,919,398
153,-18,117
-493,422,-353
-806,-357,-339
-812,-382,-410
-521,-421,680
618,-695,856
-556,472,534
635,-664,770

--- scanner 24 ---
668,-697,471
-743,805,518
-640,783,504
362,-783,-510
-72,-14,21
826,465,271
-545,-591,754
-653,-531,-578
-710,-680,726
-643,-638,822
808,498,286
592,-613,370
-574,-643,-484
625,-648,546
-842,233,-656
772,314,-917
384,-800,-678
849,382,-881
-862,384,-702
651,414,309
55,-151,-57
-713,742,390
451,-816,-467
849,297,-899
-819,368,-743
-564,-541,-471

--- scanner 25 ---
-706,-813,685
98,0,61
-475,-742,-701
-814,-959,693
735,-469,-555
-802,-837,701
607,-658,701
-800,430,-718
-571,419,715
-606,-805,-675
459,730,-489
552,721,-471
679,551,719
-512,362,546
688,579,467
-795,431,-879
383,692,-489
-642,-682,-660
692,-638,623
765,-454,-541
703,-585,587
614,571,641
-739,408,-722
907,-456,-480
161,-133,-93
-634,390,612

--- scanner 26 ---
-659,-489,657
-732,-491,614
-823,652,-554
-574,431,745
750,892,572
-705,676,-456
-110,0,-129
-615,-521,-705
462,708,-601
427,756,-543
-420,427,752
277,-435,468
416,-441,370
337,-833,-852
-890,-539,649
681,851,516
367,-693,-801
544,876,633
411,-376,390
-675,-541,-827
-690,-476,-722
-514,484,775
456,-812,-869
415,701,-437
-793,738,-413
-7,141,-31

--- scanner 27 ---
572,353,841
-339,-700,406
12,57,81
907,705,-751
644,325,809
-794,-701,-378
593,-488,-622
-447,735,-487
-524,785,476
414,-403,408
-322,754,-393
-463,751,-363
72,-91,-45
676,311,789
452,-550,334
-232,-736,561
780,839,-721
-662,722,489
509,-439,-648
-806,-448,-359
749,747,-694
454,-453,349
-734,792,474
-298,-774,526
-808,-517,-464
446,-477,-709

--- scanner 28 ---
-491,-629,-453
-583,-640,672
-489,-551,-496
-783,756,-453
852,-485,-746
646,679,642
742,626,681
745,-567,-777
378,579,-563
369,-493,360
-890,601,-417
-824,636,-379
451,593,-628
-784,608,689
-658,-623,717
80,-140,-1
-643,-518,652
-660,499,675
-7,-5,137
732,743,671
400,632,-508
-846,565,647
751,-486,-849
399,-544,500
488,-476,381
-563,-649,-521

--- scanner 29 ---
-630,722,-554
-97,-7,20
693,686,710
803,652,678
-815,-593,-528
742,850,658
381,-411,579
-537,644,689
-423,753,685
778,-506,-680
-527,713,-484
-410,-316,562
-486,-347,501
347,-364,414
676,-480,-712
-467,671,850
-714,683,-420
-445,-348,605
-695,-645,-591
652,632,-439
-870,-681,-520
647,-536,-660
710,521,-439
720,561,-493
340,-337,615

--- scanner 30 ---
-629,628,-636
124,-147,157
850,-817,756
-27,-79,-34
-679,-520,-392
-287,-441,830
-685,-381,-490
594,491,674
-427,-471,779
-581,786,-671
484,580,-741
-744,-515,-412
387,-717,-432
536,504,-781
569,417,772
-644,586,700
395,-825,-510
-599,511,683
819,-924,838
530,550,-771
922,-823,837
-631,555,-679
-579,571,805
526,419,694
412,-750,-453
-308,-560,847

--- scanner 31 ---
654,704,-644
-939,552,-557
284,-417,580
477,-370,-775
-515,-482,-510
553,812,632
-808,572,-587
-881,739,510
-99,60,-31
-568,-339,-449
386,-393,522
366,748,662
447,-393,-880
-813,793,581
371,-463,733
469,678,671
-837,520,-531
534,641,-696
-813,-550,817
-773,-417,727
-771,-428,683
709,712,-732
438,-303,-910
-871,793,470
-520,-456,-357

--- scanner 32 ---
573,-915,546
-489,-355,592
-598,414,-575
537,-773,497
530,-664,-742
-565,705,734
513,304,852
572,757,-394
158,24,149
-673,-777,-442
-604,756,614
-718,-829,-276
-651,510,-536
-742,-779,-483
96,-91,-28
-498,-381,692
443,-891,499
490,-604,-544
521,787,-254
-551,778,669
514,405,955
462,-616,-726
504,668,-275
-715,424,-565
595,411,883
-551,-406,691

--- scanner 33 ---
-640,600,-495
725,-844,644
691,-904,-428
-634,-912,440
-617,542,-443
128,-7,27
-826,-468,-849
2,-123,-33
-779,-454,-655
773,-848,-474
415,527,-534
-591,632,435
624,-825,690
832,359,395
848,398,614
-829,-418,-712
630,-846,839
441,531,-445
386,512,-405
-548,529,-449
735,-945,-603
899,347,530
-529,560,376
-685,-841,398
-730,-860,525
-611,462,329

--- scanner 34 ---
-760,-822,-576
533,-563,-395
-901,-792,-662
436,478,-707
774,701,598
710,615,627
596,-877,622
616,-551,-415
-771,428,-680
-445,457,888
-858,-704,-600
657,711,588
-85,-24,28
554,482,-834
-462,338,909
506,576,-681
639,-815,580
-609,-614,597
530,-691,594
-513,368,769
-592,-689,552
521,-581,-371
-487,-674,617
-713,463,-632
-877,416,-625

--- scanner 35 ---
898,-575,633
876,-630,580
-261,-552,686
811,770,875
-723,582,480
-8,-34,145
-704,431,-619
-235,-652,695
-459,-329,-246
-458,-324,-407
769,706,-601
-286,-553,633
-436,-385,-403
839,779,-566
162,109,80
-760,675,612
-793,443,-712
-771,324,-699
714,-649,-424
779,629,-531
826,766,873
654,-482,-465
-732,718,418
777,-518,-450
825,-510,619
852,583,894

--- scanner 36 ---
-379,-490,-640
-406,-497,-841
711,273,-570
-84,-168,35
-816,457,696
-803,467,594
443,-440,284
-609,-491,437
602,387,-566
437,565,329
-709,546,706
610,-953,-577
527,513,278
629,317,-405
-820,-558,421
808,-892,-597
467,-521,398
-453,-531,-676
-358,260,-693
583,633,322
644,-843,-545
571,-459,333
36,-94,-126
-390,295,-650
-389,336,-754
-777,-469,454

--- scanner 37 ---
-593,283,-862
694,490,-417
-688,611,438
-540,-467,-841
-16,22,74
689,-709,613
699,559,889
554,-446,-443
-741,-474,-814
796,480,-404
640,-752,538
-625,628,598
-713,-543,329
-592,-561,376
151,-117,-27
537,-468,-611
521,-535,-400
746,461,821
-653,-708,352
-550,318,-830
-654,359,-831
-576,-508,-767
724,-676,437
-498,591,466
806,569,-511
657,626,793"""


example = """--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14"""

raw = example


def print_stuff(things):
    xs = [x for x, y in things]
    ys = [-y for x, y in things]
    min_x = min(xs)
    max_x = max(xs)
    min_y = min(ys)
    max_y = max(ys)
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            print(things.get((x, -y), "."), end="")
        print("")


def init():
    input = raw.split("\n\n")
    scanners = dict()
    for text in input:
        lines = text.splitlines()
        scanner = int(re.findall("\d+", lines.pop(0))[0])
        scanners[scanner] = d = dict()
        # d[(0, 0, 0)] = "S"
        for line in lines:
            x, y, z = list(map(int, line.split(",")))
            d[(x, y, z)] = "B"

    return scanners


def match_scanners(scanner0, scanner1):
    # loop: try matching every beacon on scanner1 to every beacon in scanner0
    for (x0, y0, z0) in scanner0:
        for (x1, y1, z1) in scanner1:
            # will need to shift the x,y of all scanner2 to achieve this.
            dx = x0 - x1
            dy = y0 - y1
            dz = z0 - z1
            shifted1 = {(x + dx, y + dy, z + dz): value for (x, y, z), value in scanner1.items()}

            # if, after the shift, 3 beacons overlap, it's a match
            hits = set(shifted1).intersection(scanner0)
            if len(hits) > 11:
                return (dx, dy, dz), shifted1
    return False, None


def rotate_scanner(scanner, x=0, y=1, z=2, flip_x=False, flip_y=False, flip_z=False):
    rotated = {
        (
            coords[x] * (-1 if flip_x else 1),
            coords[y] * (-1 if flip_y else 1),
            coords[z] * (-1 if flip_z else 1),
        ): value
        for coords, value in scanner.items()
    }
    return rotated


def get_orientations():
    orientations = []
    xs = (0, 1, 2)
    for x in xs:
        ys = set(xs).difference({x})
        for y in ys:
            for z in set(ys).difference({y}):
                for flip_x in (True, False):
                    for flip_y in (True, False):
                        for flip_z in (True, False):
                            orientations.append((x, y, z, flip_x, flip_y, flip_z))
    return orientations


def smart_stuff(scanner0, scanner1):
    for (x, y, z, flip_x, flip_y, flip_z) in get_orientations():
        rotated1 = rotate_scanner(scanner1, x, y, z, flip_x, flip_y, flip_z)
        dxdydz, shifted1 = match_scanners(scanner0, rotated1)
        if dxdydz:
            return dxdydz, shifted1
    return False, False


if __name__ == "__main__":
    scanners = init()
    master = {**scanners.pop(0)}
    scanners = deque([(key, value) for key, value in scanners.items()])
    while scanners:
        key, scanner = scanners.popleft()
        print(f"comparing scanner {key}")
        dxdydz, shifted = smart_stuff(master, scanner)
        if dxdydz:
            print(f"dxdydz={','.join(map(str, dxdydz))}")
            master.update(shifted)
        else:
            print(f"no match for scanner {key} yet")
            scanners.append((key, scanner))

    print(len(master))
