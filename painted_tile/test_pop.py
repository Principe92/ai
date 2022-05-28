from pop import PlanningGraph


def main(arg):
    planning_graph = PlanningGraph(arg)
    plan = planning_graph.create(20)

    print(plan)


if __name__ == "__main__":
    arg = 'Blue(t03),Red(t07),At(t08),Blue(t09),Red(t14),Red(t17),Blue(t18),Red(t23),Blue(t24),Adj(t00,t05),Adj(t00,t01),Adj(t01,t06),Adj(t01,t00),Adj(t01,t02),Adj(t02,t07),Adj(t02,t01),Adj(t02,t03),Adj(t03,t08),Adj(t03,t02),Adj(t03,t04),Adj(t04,t09),Adj(t04,t03),Adj(t05,t00),Adj(t05,t10),Adj(t05,t06),Adj(t06,t01),Adj(t06,t11),Adj(t06,t05),Adj(t06,t07),Adj(t07,t02),Adj(t07,t12),Adj(t07,t06),Adj(t07,t08),Adj(t08,t03),Adj(t08,t13),Adj(t08,t07),Adj(t08,t09),Adj(t09,t04),Adj(t09,t14),Adj(t09,t08),Adj(t10,t05),Adj(t10,t15),Adj(t10,t11),Adj(t11,t06),Adj(t11,t16),Adj(t11,t10),Adj(t11,t12),Adj(t12,t07),Adj(t12,t17),Adj(t12,t11),Adj(t12,t13),Adj(t13,t08),Adj(t13,t18),Adj(t13,t12),Adj(t13,t14),Adj(t14,t09),Adj(t14,t19),Adj(t14,t13),Adj(t15,t10),Adj(t15,t20),Adj(t15,t16),Adj(t16,t11),Adj(t16,t21),Adj(t16,t15),Adj(t16,t17),Adj(t17,t12),Adj(t17,t22),Adj(t17,t16),Adj(t17,t18),Adj(t18,t13),Adj(t18,t23),Adj(t18,t17),Adj(t18,t19),Adj(t19,t14),Adj(t19,t24),Adj(t19,t18),Adj(t20,t15),Adj(t20,t21),Adj(t21,t16),Adj(t21,t20),Adj(t21,t22),Adj(t22,t17),Adj(t22,t21),Adj(t22,t23),Adj(t23,t18),Adj(t23,t22),Adj(t23,t24),Adj(t24,t19),Adj(t24,t23)'
    # arg = 'Blue(t01),Blue(t05),At(t06),Red(t07),Red(t11),Blue(t12),Red(t16),Adj(t00,t05),Adj(t00,t01),Adj(t01,t06),Adj(t01,t00),Adj(t01,t02),Adj(t02,t07),Adj(t02,t01),Adj(t02,t03),Adj(t03,t08),Adj(t03,t02),Adj(t03,t04),Adj(t04,t09),Adj(t04,t03),Adj(t05,t00),Adj(t05,t10),Adj(t05,t06),Adj(t06,t01),Adj(t06,t11),Adj(t06,t05),Adj(t06,t07),Adj(t07,t02),Adj(t07,t12),Adj(t07,t06),Adj(t07,t08),Adj(t08,t03),Adj(t08,t13),Adj(t08,t07),Adj(t08,t09),Adj(t09,t04),Adj(t09,t14),Adj(t09,t08),Adj(t10,t05),Adj(t10,t15),Adj(t10,t11),Adj(t11,t06),Adj(t11,t16),Adj(t11,t10),Adj(t11,t12),Adj(t12,t07),Adj(t12,t17),Adj(t12,t11),Adj(t12,t13),Adj(t13,t08),Adj(t13,t18),Adj(t13,t12),Adj(t13,t14),Adj(t14,t09),Adj(t14,t19),Adj(t14,t13),Adj(t15,t10),Adj(t15,t20),Adj(t15,t16),Adj(t16,t11),Adj(t16,t21),Adj(t16,t15),Adj(t16,t17),Adj(t17,t12),Adj(t17,t22),Adj(t17,t16),Adj(t17,t18),Adj(t18,t13),Adj(t18,t23),Adj(t18,t17),Adj(t18,t19),Adj(t19,t14),Adj(t19,t24),Adj(t19,t18),Adj(t20,t15),Adj(t20,t21),Adj(t21,t16),Adj(t21,t20),Adj(t21,t22),Adj(t22,t17),Adj(t22,t21),Adj(t22,t23),Adj(t23,t18),Adj(t23,t22),Adj(t23,t24),Adj(t24,t19),Adj(t24,t23)'
    # arg = 'Blue(t01),Blue(t05),At(t06),Red(t07),Red(t11),Blue(t12),Red(t16),Adj(t00,t05),Adj(t00,t01),Adj(t01,t06),Adj(t01,t00),Adj(t01,t02),Adj(t02,t07),Adj(t02,t01),Adj(t02,t03),Adj(t03,t08),Adj(t03,t02),Adj(t03,t04),Adj(t04,t09),Adj(t04,t03),Adj(t05,t00),Adj(t05,t10),Adj(t05,t06),Adj(t06,t01),Adj(t06,t11),Adj(t06,t05),Adj(t06,t07),Adj(t07,t02),Adj(t07,t12),Adj(t07,t06),Adj(t07,t08),Adj(t08,t03),Adj(t08,t13),Adj(t08,t07),Adj(t08,t09),Adj(t09,t04),Adj(t09,t14),Adj(t09,t08),Adj(t10,t05),Adj(t10,t15),Adj(t10,t11),Adj(t11,t06),Adj(t11,t16),Adj(t11,t10),Adj(t11,t12),Adj(t12,t07),Adj(t12,t17),Adj(t12,t11),Adj(t12,t13),Adj(t13,t08),Adj(t13,t18),Adj(t13,t12),Adj(t13,t14),Adj(t14,t09),Adj(t14,t19),Adj(t14,t13),Adj(t15,t10),Adj(t15,t20),Adj(t15,t16),Adj(t16,t11),Adj(t16,t21),Adj(t16,t15),Adj(t16,t17),Adj(t17,t12),Adj(t17,t22),Adj(t17,t16),Adj(t17,t18),Adj(t18,t13),Adj(t18,t23),Adj(t18,t17),Adj(t18,t19),Adj(t19,t14),Adj(t19,t24),Adj(t19,t18),Adj(t20,t15),Adj(t20,t21),Adj(t21,t16),Adj(t21,t20),Adj(t21,t22),Adj(t22,t17),Adj(t22,t21),Adj(t22,t23),Adj(t23,t18),Adj(t23,t22),Adj(t23,t24),Adj(t24,t19),Adj(t24,t23)'
    # arg = 'Blue(t01),Blue(t05),At(t06),Red(t07),Red(t11),Blue(t12),Red(t15),Red(t16),Red(t21),Adj(t00,t05),Adj(t00,t01),Adj(t01,t06),Adj(t01,t00),Adj(t01,t02),Adj(t02,t07),Adj(t02,t01),Adj(t02,t03),Adj(t03,t08),Adj(t03,t02),Adj(t03,t04),Adj(t04,t09),Adj(t04,t03),Adj(t05,t00),Adj(t05,t10),Adj(t05,t06),Adj(t06,t01),Adj(t06,t11),Adj(t06,t05),Adj(t06,t07),Adj(t07,t02),Adj(t07,t12),Adj(t07,t06),Adj(t07,t08),Adj(t08,t03),Adj(t08,t13),Adj(t08,t07),Adj(t08,t09),Adj(t09,t04),Adj(t09,t14),Adj(t09,t08),Adj(t10,t05),Adj(t10,t15),Adj(t10,t11),Adj(t11,t06),Adj(t11,t16),Adj(t11,t10),Adj(t11,t12),Adj(t12,t07),Adj(t12,t17),Adj(t12,t11),Adj(t12,t13),Adj(t13,t08),Adj(t13,t18),Adj(t13,t12),Adj(t13,t14),Adj(t14,t09),Adj(t14,t19),Adj(t14,t13),Adj(t15,t10),Adj(t15,t20),Adj(t15,t16),Adj(t16,t11),Adj(t16,t21),Adj(t16,t15),Adj(t16,t17),Adj(t17,t12),Adj(t17,t22),Adj(t17,t16),Adj(t17,t18),Adj(t18,t13),Adj(t18,t23),Adj(t18,t17),Adj(t18,t19),Adj(t19,t14),Adj(t19,t24),Adj(t19,t18),Adj(t20,t15),Adj(t20,t21),Adj(t21,t16),Adj(t21,t20),Adj(t21,t22),Adj(t22,t17),Adj(t22,t21),Adj(t22,t23),Adj(t23,t18),Adj(t23,t22),Adj(t23,t24),Adj(t24,t19),Adj(t24,t23)'
    # arg = 'Blue(t06),At(t13),Blue(t16),Red(t18),Adj(t00,t05),Adj(t00,t01),Adj(t01,t06),Adj(t01,t00),Adj(t01,t02),Adj(t02,t07),Adj(t02,t01),Adj(t02,t03),Adj(t03,t08),Adj(t03,t02),Adj(t03,t04),Adj(t04,t09),Adj(t04,t03),Adj(t05,t00),Adj(t05,t10),Adj(t05,t06),Adj(t06,t01),Adj(t06,t11),Adj(t06,t05),Adj(t06,t07),Adj(t07,t02),Adj(t07,t12),Adj(t07,t06),Adj(t07,t08),Adj(t08,t03),Adj(t08,t13),Adj(t08,t07),Adj(t08,t09),Adj(t09,t04),Adj(t09,t14),Adj(t09,t08),Adj(t10,t05),Adj(t10,t15),Adj(t10,t11),Adj(t11,t06),Adj(t11,t16),Adj(t11,t10),Adj(t11,t12),Adj(t12,t07),Adj(t12,t17),Adj(t12,t11),Adj(t12,t13),Adj(t13,t08),Adj(t13,t18),Adj(t13,t12),Adj(t13,t14),Adj(t14,t09),Adj(t14,t19),Adj(t14,t13),Adj(t15,t10),Adj(t15,t20),Adj(t15,t16),Adj(t16,t11),Adj(t16,t21),Adj(t16,t15),Adj(t16,t17),Adj(t17,t12),Adj(t17,t22),Adj(t17,t16),Adj(t17,t18),Adj(t18,t13),Adj(t18,t23),Adj(t18,t17),Adj(t18,t19),Adj(t19,t14),Adj(t19,t24),Adj(t19,t18),Adj(t20,t15),Adj(t20,t21),Adj(t21,t16),Adj(t21,t20),Adj(t21,t22),Adj(t22,t17),Adj(t22,t21),Adj(t22,t23),Adj(t23,t18),Adj(t23,t22),Adj(t23,t24),Adj(t24,t19),Adj(t24,t23)'
    # arg = 'Blue(t05),At(t06),Red(t12),Blue(t13),Red(t16),Red(t18),Blue(t19),Red(t22),Red(t24),Adj(t00,t05),Adj(t00,t01),Adj(t01,t06),Adj(t01,t00),Adj(t01,t02),Adj(t02,t07),Adj(t02,t01),Adj(t02,t03),Adj(t03,t08),Adj(t03,t02),Adj(t03,t04),Adj(t04,t09),Adj(t04,t03),Adj(t05,t00),Adj(t05,t10),Adj(t05,t06),Adj(t06,t01),Adj(t06,t11),Adj(t06,t05),Adj(t06,t07),Adj(t07,t02),Adj(t07,t12),Adj(t07,t06),Adj(t07,t08),Adj(t08,t03),Adj(t08,t13),Adj(t08,t07),Adj(t08,t09),Adj(t09,t04),Adj(t09,t14),Adj(t09,t08),Adj(t10,t05),Adj(t10,t15),Adj(t10,t11),Adj(t11,t06),Adj(t11,t16),Adj(t11,t10),Adj(t11,t12),Adj(t12,t07),Adj(t12,t17),Adj(t12,t11),Adj(t12,t13),Adj(t13,t08),Adj(t13,t18),Adj(t13,t12),Adj(t13,t14),Adj(t14,t09),Adj(t14,t19),Adj(t14,t13),Adj(t15,t10),Adj(t15,t20),Adj(t15,t16),Adj(t16,t11),Adj(t16,t21),Adj(t16,t15),Adj(t16,t17),Adj(t17,t12),Adj(t17,t22),Adj(t17,t16),Adj(t17,t18),Adj(t18,t13),Adj(t18,t23),Adj(t18,t17),Adj(t18,t19),Adj(t19,t14),Adj(t19,t24),Adj(t19,t18),Adj(t20,t15),Adj(t20,t21),Adj(t21,t16),Adj(t21,t20),Adj(t21,t22),Adj(t22,t17),Adj(t22,t21),Adj(t22,t23),Adj(t23,t18),Adj(t23,t22),Adj(t23,t24),Adj(t24,t19),Adj(t24,t23)'
    # arg ='Red(t00),Blue(t01),Blue(t06),At(t11),Adj(t00,t05),Adj(t00,t01),Adj(t01,t06),Adj(t01,t00),Adj(t01,t02),Adj(t02,t07),Adj(t02,t01),Adj(t02,t03),Adj(t03,t08),Adj(t03,t02),Adj(t03,t04),Adj(t04,t09),Adj(t04,t03),Adj(t05,t00),Adj(t05,t10),Adj(t05,t06),Adj(t06,t01),Adj(t06,t11),Adj(t06,t05),Adj(t06,t07),Adj(t07,t02),Adj(t07,t12),Adj(t07,t06),Adj(t07,t08),Adj(t08,t03),Adj(t08,t13),Adj(t08,t07),Adj(t08,t09),Adj(t09,t04),Adj(t09,t14),Adj(t09,t08),Adj(t10,t05),Adj(t10,t15),Adj(t10,t11),Adj(t11,t06),Adj(t11,t16),Adj(t11,t10),Adj(t11,t12),Adj(t12,t07),Adj(t12,t17),Adj(t12,t11),Adj(t12,t13),Adj(t13,t08),Adj(t13,t18),Adj(t13,t12),Adj(t13,t14),Adj(t14,t09),Adj(t14,t19),Adj(t14,t13),Adj(t15,t10),Adj(t15,t20),Adj(t15,t16),Adj(t16,t11),Adj(t16,t21),Adj(t16,t15),Adj(t16,t17),Adj(t17,t12),Adj(t17,t22),Adj(t17,t16),Adj(t17,t18),Adj(t18,t13),Adj(t18,t23),Adj(t18,t17),Adj(t18,t19),Adj(t19,t14),Adj(t19,t24),Adj(t19,t18),Adj(t20,t15),Adj(t20,t21),Adj(t21,t16),Adj(t21,t20),Adj(t21,t22),Adj(t22,t17),Adj(t22,t21),Adj(t22,t23),Adj(t23,t18),Adj(t23,t22),Adj(t23,t24),Adj(t24,t19),Adj(t24,t23)'
    # arg = 'Red(t04),Red(t07),Blue(t11),At(t12),Adj(t00,t05),Adj(t00,t01),Adj(t01,t06),Adj(t01,t00),Adj(t01,t02),Adj(t02,t07),Adj(t02,t01),Adj(t02,t03),Adj(t03,t08),Adj(t03,t02),Adj(t03,t04),Adj(t04,t09),Adj(t04,t03),Adj(t05,t00),Adj(t05,t10),Adj(t05,t06),Adj(t06,t01),Adj(t06,t11),Adj(t06,t05),Adj(t06,t07),Adj(t07,t02),Adj(t07,t12),Adj(t07,t06),Adj(t07,t08),Adj(t08,t03),Adj(t08,t13),Adj(t08,t07),Adj(t08,t09),Adj(t09,t04),Adj(t09,t14),Adj(t09,t08),Adj(t10,t05),Adj(t10,t15),Adj(t10,t11),Adj(t11,t06),Adj(t11,t16),Adj(t11,t10),Adj(t11,t12),Adj(t12,t07),Adj(t12,t17),Adj(t12,t11),Adj(t12,t13),Adj(t13,t08),Adj(t13,t18),Adj(t13,t12),Adj(t13,t14),Adj(t14,t09),Adj(t14,t19),Adj(t14,t13),Adj(t15,t10),Adj(t15,t20),Adj(t15,t16),Adj(t16,t11),Adj(t16,t21),Adj(t16,t15),Adj(t16,t17),Adj(t17,t12),Adj(t17,t22),Adj(t17,t16),Adj(t17,t18),Adj(t18,t13),Adj(t18,t23),Adj(t18,t17),Adj(t18,t19),Adj(t19,t14),Adj(t19,t24),Adj(t19,t18),Adj(t20,t15),Adj(t20,t21),Adj(t21,t16),Adj(t21,t20),Adj(t21,t22),Adj(t22,t17),Adj(t22,t21),Adj(t22,t23),Adj(t23,t18),Adj(t23,t22),Adj(t23,t24),Adj(t24,t19),Adj(t24,t23)'
    # arg = 'Blue(t02),At(t03),Blue(t04),Blue(t17),Adj(t00,t05),Adj(t00,t01),Adj(t01,t06),Adj(t01,t00),Adj(t01,t02),Adj(t02,t07),Adj(t02,t01),Adj(t02,t03),Adj(t03,t08),Adj(t03,t02),Adj(t03,t04),Adj(t04,t09),Adj(t04,t03),Adj(t05,t00),Adj(t05,t10),Adj(t05,t06),Adj(t06,t01),Adj(t06,t11),Adj(t06,t05),Adj(t06,t07),Adj(t07,t02),Adj(t07,t12),Adj(t07,t06),Adj(t07,t08),Adj(t08,t03),Adj(t08,t13),Adj(t08,t07),Adj(t08,t09),Adj(t09,t04),Adj(t09,t14),Adj(t09,t08),Adj(t10,t05),Adj(t10,t15),Adj(t10,t11),Adj(t11,t06),Adj(t11,t16),Adj(t11,t10),Adj(t11,t12),Adj(t12,t07),Adj(t12,t17),Adj(t12,t11),Adj(t12,t13),Adj(t13,t08),Adj(t13,t18),Adj(t13,t12),Adj(t13,t14),Adj(t14,t09),Adj(t14,t19),Adj(t14,t13),Adj(t15,t10),Adj(t15,t20),Adj(t15,t16),Adj(t16,t11),Adj(t16,t21),Adj(t16,t15),Adj(t16,t17),Adj(t17,t12),Adj(t17,t22),Adj(t17,t16),Adj(t17,t18),Adj(t18,t13),Adj(t18,t23),Adj(t18,t17),Adj(t18,t19),Adj(t19,t14),Adj(t19,t24),Adj(t19,t18),Adj(t20,t15),Adj(t20,t21),Adj(t21,t16),Adj(t21,t20),Adj(t21,t22),Adj(t22,t17),Adj(t22,t21),Adj(t22,t23),Adj(t23,t18),Adj(t23,t22),Adj(t23,t24),Adj(t24,t19),Adj(t24,t23)'
    # arg = 'Blue(t02),At(t03),Blue(t04),Adj(t00,t05),Adj(t00,t01),Adj(t01,t06),Adj(t01,t00),Adj(t01,t02),Adj(t02,t07),Adj(t02,t01),Adj(t02,t03),Adj(t03,t08),Adj(t03,t02),Adj(t03,t04),Adj(t04,t09),Adj(t04,t03),Adj(t05,t00),Adj(t05,t10),Adj(t05,t06),Adj(t06,t01),Adj(t06,t11),Adj(t06,t05),Adj(t06,t07),Adj(t07,t02),Adj(t07,t12),Adj(t07,t06),Adj(t07,t08),Adj(t08,t03),Adj(t08,t13),Adj(t08,t07),Adj(t08,t09),Adj(t09,t04),Adj(t09,t14),Adj(t09,t08),Adj(t10,t05),Adj(t10,t15),Adj(t10,t11),Adj(t11,t06),Adj(t11,t16),Adj(t11,t10),Adj(t11,t12),Adj(t12,t07),Adj(t12,t17),Adj(t12,t11),Adj(t12,t13),Adj(t13,t08),Adj(t13,t18),Adj(t13,t12),Adj(t13,t14),Adj(t14,t09),Adj(t14,t19),Adj(t14,t13),Adj(t15,t10),Adj(t15,t20),Adj(t15,t16),Adj(t16,t11),Adj(t16,t21),Adj(t16,t15),Adj(t16,t17),Adj(t17,t12),Adj(t17,t22),Adj(t17,t16),Adj(t17,t18),Adj(t18,t13),Adj(t18,t23),Adj(t18,t17),Adj(t18,t19),Adj(t19,t14),Adj(t19,t24),Adj(t19,t18),Adj(t20,t15),Adj(t20,t21),Adj(t21,t16),Adj(t21,t20),Adj(t21,t22),Adj(t22,t17),Adj(t22,t21),Adj(t22,t23),Adj(t23,t18),Adj(t23,t22),Adj(t23,t24),Adj(t24,t19),Adj(t24,t23)'
    main(arg)