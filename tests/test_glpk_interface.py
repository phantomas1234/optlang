# Copyright (c) 2013 Novo Nordisk Foundation Center for Biosustainability, DTU.
# See LICENSE for details.
import copy

import unittest
import random
import pickle

import os
import nose
from swiglpk import *
import sys
import six

import optlang
from optlang import glpk_interface

from optlang.glpk_interface import Variable, Constraint, Model, Objective
from optlang.util import glpk_read_cplex


random.seed(666)
TESTMODELPATH = os.path.join(os.path.dirname(__file__), 'data/model.lp')
TESTMILPMODELPATH = os.path.join(os.path.dirname(__file__), 'data/simple_milp.lp')

class VariableTestCase(unittest.TestCase):
    def setUp(self):
        self.var = Variable('test')

    def test_variable_without_problem_returns_None_index(self):
        self.assertEqual(self.var.index, None)

    def test_set_wrong_type_raises(self):
        self.assertRaises(Exception, setattr, self.var, 'type', 'ketchup')

    def test_get_primal(self):
        self.assertEqual(self.var.primal, None)
        model = Model(problem=glpk_read_cplex(TESTMODELPATH))
        model.optimize()
        for i, j in zip([var.primal for var in model.variables], [0.8739215069684306, -16.023526143167608, 16.023526143167604, -14.71613956874283, 14.71613956874283, 4.959984944574658, 4.959984944574657, 4.959984944574658, 3.1162689467973905e-29, 2.926716099010601e-29, 0.0, 0.0, -6.112235045340358e-30, -5.6659435396316186e-30, 0.0, -4.922925402711085e-29, 0.0, 9.282532599166613, 0.0, 6.00724957535033, 6.007249575350331, 6.00724957535033, -5.064375661482091, 1.7581774441067828, 0.0, 7.477381962160285, 0.0, 0.22346172933182767, 45.514009774517454, 8.39, 0.0, 6.007249575350331, 0.0, -4.541857463865631, 0.0, 5.064375661482091, 0.0, 0.0, 2.504309470368734, 0.0, 0.0, -22.809833310204958, 22.809833310204958, 7.477381962160285, 7.477381962160285, 1.1814980932459636, 1.496983757261567, -0.0, 0.0, 4.860861146496815, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 5.064375661482091, 0.0, 5.064375661482091, 0.0, 0.0, 1.496983757261567, 10.000000000000002, -10.0, 0.0, 0.0, 0.0, 0.0, 0.0, -29.175827135565804, 43.598985311997524, 29.175827135565804, 0.0, 0.0, 0.0, -1.2332237321082153e-29, 3.2148950476847613, 38.53460965051542, 5.064375661482091, 0.0, -1.2812714099825612e-29, -1.1331887079263237e-29, 17.530865429786694, 0.0, 0.0, 0.0, 4.765319193197458, -4.765319193197457, 21.79949265599876, -21.79949265599876, -3.2148950476847613, 0.0, -2.281503094067127, 2.6784818505075303, 0.0]):
            self.assertAlmostEqual(i, j)

    @unittest.skip
    def test_get_dual(self):
        self.assertEqual(self.var.dual, None)
        model = Model(problem=glpk_read_cplex(TESTMODELPATH))
        model.optimize()
        for i, j in zip([var.dual for var in model.variables], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.022916186593776235, 0.0, 0.0, 0.0, -0.03437427989066435, 0.0, -0.007638728864592075, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.005092485909728057, 0.0, 0.0, 0.0, 0.0, -0.005092485909728046, 0.0, 0.0, -0.005092485909728045, 0.0, 0.0, 0.0, -0.0611098309167366, -0.005092485909728045, 0.0, -0.003819364432296033, -0.00509248590972805, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.03946676580039239, 0.0, 0.0, -0.005092485909728042, -0.0, -0.0012731214774320113, 0.0, -0.0916647463751049, 0.0, 0.0, 0.0, -0.0, -0.04583237318755246, 0.0, 0.0, -0.0916647463751049, -0.005092485909728045, -0.07002168125876067, 0.0, -0.06874855978132867, -0.0012731214774320113, 0.0, 0.0, 0.0, -0.001273121477432006, -0.0038193644322960392, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.040739887277824405, -0.04583237318755245, -0.0012731214774320163, 0.0, 0.0, 0.0, 0.0, 0.0, -0.03437427989066435, 0.0, 0.0, -0.04837861614241648]):
            self.assertAlmostEqual(i, j)

    def test_setting_lower_bound_higher_than_upper_bound_raises(self):
        model = Model(problem=glpk_read_cplex(TESTMODELPATH))
        self.assertRaises(ValueError, setattr, model.variables[0], 'lb', 10000000000.)

    def test_setting_nonnumerical_bounds_raises(self):
        model = Model(problem=glpk_read_cplex(TESTMODELPATH))
        self.assertRaises(Exception, setattr, model.variables[0], 'lb', 'Chicken soup')

    def test_changing_variable_names_is_reflected_in_the_solver(self):
        model = Model(problem=glpk_read_cplex(TESTMODELPATH))
        for i, variable in enumerate(model.variables):
            variable.name = "var"+str(i)
            self.assertEqual(variable.name, "var"+str(i))
            self.assertEqual(glp_get_col_name(model.problem, variable.index), "var"+str(i))

    def test_setting_bounds(self):
        model = Model(problem=glpk_read_cplex(TESTMODELPATH))
        var = model.variables[0]
        var.lb = 1
        self.assertEqual(var.lb, 1)
        self.assertEqual(glpk_interface.glp_get_col_lb(model.problem, var.index), 1)
        var.ub = 2
        self.assertEqual(var.ub, 2)
        self.assertEqual(glpk_interface.glp_get_col_ub(model.problem, var.index), 2)


class ConstraintTestCase(unittest.TestCase):
    def setUp(self):
        self.model = Model(problem=glpk_read_cplex(TESTMODELPATH))
        self.constraint = Constraint(Variable('chip') + Variable('chap'), name='woodchips', lb=100)

    def test_indicator_constraint_raises(self):
        self.assertRaises(optlang.exceptions.IndicatorConstraintsNotSupported, Constraint, Variable('chip') + Variable('chap'), indicator_variable=Variable('indicator', type='binary'))

    def test_constraint_index(self):
        constraint = self.model.constraints.M_atp_c
        self.assertEqual(constraint.index, 17)
        self.model.remove(constraint)
        self.model.update()
        self.assertEqual(constraint.index, None)

    def test_get_primal(self):
        self.assertEqual(self.constraint.primal, None)
        self.model.optimize()
        print([constraint.primal for constraint in self.model.constraints])
        for i, j in zip([constraint.primal for constraint in self.model.constraints], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 4.048900234729145e-15, 0.0, 0.0, 0.0, -3.55971196577979e-16, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.5546369406238147e-17, 0.0, -5.080374405378186e-29, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]):
            self.assertAlmostEqual(i, j)

    @unittest.skip
    def test_get_dual(self):
        self.assertEqual(self.constraint.dual, None)
        self.model.optimize()
        for i, j in zip([constraint.dual for constraint in self.model.constraints], [-0.047105494664984454, -0.042013008755256424, -0.04201300875525642, -0.09166474637510488, -0.09039162489767284, -0.024189308071208247, -0.022916186593776238, -0.03437427989066435, -0.03437427989066435, -0.028008672503504285, -0.07129480273619271, -0.029281793980936298, 0.005092485909728047, -0.06238295239416862, -0.06110983091673661, 0.010184971819456094, 0.0, -0.07129480273619271, -5.140926862910144e-32, -6.0634800261074814e-33, 0.0, -0.052197980574712505, -0.06747543830389666, -0.040739887277824405, -0.03946676580039239, -0.09803035376226496, -0.10439596114942501, 0.0, 0.0, -0.0916647463751049, -0.04837861614241648, -0.04583237318755246, -0.052197980574712505, -0.09803035376226495, -0.0916647463751049, -0.07511416716848872, -0.07002168125876067, -0.07002168125876068, -0.06874855978132868, -0.019096822161480186, -1.5662469903861418e-32, -0.0, 0.0012731214774320113, -0.0, -0.07129480273619271, -0.04201300875525642, -0.04073988727782441, -0.048378616142416474, -0.04583237318755245, 0.0, -0.00763872886459207, 0.0, -0.008911850342024085, -0.0, -0.0, -0.0, -0.0, -0.042013008755256424, -0.042013008755256424, -0.0012731214774320118, -0.0, -0.035647401368096354, -0.03437427989066435, 0.002546242954864023, 0.0, -0.08275289603308078, -0.0827528960330808, -0.11330781149144908, -0.050924859097280506, -0.04837861614241648, -0.05474422352957655, -0.08275289603308081]):
            self.assertAlmostEqual(i, j)

    def test_change_constraint_name(self):
        constraint = copy.copy(self.constraint)
        self.assertEqual(constraint.name, 'woodchips')
        constraint.name = 'ketchup'
        self.assertEqual(constraint.name, 'ketchup')
        self.assertEqual([constraint.name for constraint in self.model.constraints], ['M_13dpg_c', 'M_2pg_c', 'M_3pg_c', 'M_6pgc_c', 'M_6pgl_c', 'M_ac_c', 'M_ac_e', 'M_acald_c', 'M_acald_e', 'M_accoa_c', 'M_acon_C_c', 'M_actp_c', 'M_adp_c', 'M_akg_c', 'M_akg_e', 'M_amp_c', 'M_atp_c', 'M_cit_c', 'M_co2_c', 'M_co2_e', 'M_coa_c', 'M_dhap_c', 'M_e4p_c', 'M_etoh_c', 'M_etoh_e', 'M_f6p_c', 'M_fdp_c', 'M_for_c', 'M_for_e', 'M_fru_e', 'M_fum_c', 'M_fum_e', 'M_g3p_c', 'M_g6p_c', 'M_glc_D_e', 'M_gln_L_c', 'M_gln_L_e', 'M_glu_L_c', 'M_glu_L_e', 'M_glx_c', 'M_h2o_c', 'M_h2o_e', 'M_h_c', 'M_h_e', 'M_icit_c', 'M_lac_D_c', 'M_lac_D_e', 'M_mal_L_c', 'M_mal_L_e', 'M_nad_c', 'M_nadh_c', 'M_nadp_c', 'M_nadph_c', 'M_nh4_c', 'M_nh4_e', 'M_o2_c', 'M_o2_e', 'M_oaa_c', 'M_pep_c', 'M_pi_c', 'M_pi_e', 'M_pyr_c', 'M_pyr_e', 'M_q8_c', 'M_q8h2_c', 'M_r5p_c', 'M_ru5p_D_c', 'M_s7p_c', 'M_succ_c', 'M_succ_e', 'M_succoa_c', 'M_xu5p_D_c']
)
        for i, constraint in enumerate(self.model.constraints):
            constraint.name = 'c'+ str(i)
        self.assertEqual([constraint.name for constraint in self.model.constraints], ['c' + str(i) for i in range(0, len(self.model.constraints))])

    def test_setting_lower_bound_higher_than_upper_bound_raises(self):
        model = Model(problem=glpk_read_cplex(TESTMODELPATH))
        self.assertRaises(ValueError, setattr, model.constraints[0], 'lb', 10000000000.)

    def test_setting_nonnumerical_bounds_raises(self):
        model = Model(problem=glpk_read_cplex(TESTMODELPATH))
        self.assertRaises(Exception, setattr, model.constraints[0], 'lb', 'Chicken soup')


class ObjectiveTestCase(unittest.TestCase):
    def setUp(self):
        self.model = Model(problem=glpk_read_cplex(TESTMODELPATH))
        self.obj = self.model.objective

    def test_change_direction(self):
        self.obj.direction = "min"
        self.assertEqual(self.obj.direction, "min")
        self.assertEqual(glpk_interface.glp_get_obj_dir(self.model.problem), glpk_interface.GLP_MIN)

        self.obj.direction = "max"
        self.assertEqual(self.obj.direction, "max")
        self.assertEqual(glpk_interface.glp_get_obj_dir(self.model.problem), glpk_interface.GLP_MAX)


class SolverTestCase(unittest.TestCase):
    def setUp(self):
        problem = glpk_read_cplex(TESTMODELPATH)
        self.model = Model(problem=problem)

    def test_create_empty_model(self):
        model = Model()
        self.assertEqual(glp_get_num_cols(model.problem), 0)
        self.assertEqual(glp_get_num_rows(model.problem), 0)
        self.assertEqual(model.name, None)
        self.assertEqual(glp_get_prob_name(model.problem), None)
        model = Model(name="empty_problem")
        self.assertEqual(glp_get_prob_name(model.problem), "empty_problem")

    def test_pickle_ability(self):
        self.model.optimize()
        value = self.model.objective.value
        pickle_string = pickle.dumps(self.model)
        from_pickle = pickle.loads(pickle_string)
        from_pickle.optimize()
        self.assertAlmostEqual(value, from_pickle.objective.value)
        self.assertEqual([(var.lb, var.ub, var.name, var.type) for var in from_pickle.variables.values()],
                         [(var.lb, var.ub, var.name, var.type) for var in self.model.variables.values()])
        self.assertEqual([(constr.lb, constr.ub, constr.name) for constr in from_pickle.constraints],
                         [(constr.lb, constr.ub, constr.name) for constr in self.model.constraints])

    # def test_copy(self):
    #     model_copy = copy.copy(self.model)
    #     self.assertNotEqual(id(self.model), id(model_copy))
    #     self.assertEqual(id(self.model.problem), id(model_copy.problem))
    #
    # def test_deepcopy(self):
    #     model_copy = copy.deepcopy(self.model)
    #     self.assertNotEqual(id(self.model), id(model_copy))
    #     self.assertNotEqual(id(self.model.problem), id(model_copy.problem))

    def test_config_gets_copied_too(self):
        self.assertEquals(self.model.configuration.verbosity, 0)
        self.model.configuration.verbosity = 3
        model_copy = copy.copy(self.model)
        self.assertEquals(model_copy.configuration.verbosity, 3)

    def test_init_from_existing_problem(self):
        inner_prob = self.model.problem
        self.assertEqual(len(self.model.variables), glp_get_num_cols(inner_prob))
        self.assertEqual(len(self.model.constraints), glp_get_num_rows(inner_prob))
        self.assertEqual(self.model.variables.keys(),
                         [glp_get_col_name(inner_prob, i) for i in range(1, glp_get_num_cols(inner_prob) + 1)])
        self.assertEqual(self.model.constraints.keys(),
                         [glp_get_row_name(inner_prob, j) for j in range(1, glp_get_num_rows(inner_prob) + 1)])

    def test_add_variable(self):
        var = Variable('x')
        self.assertEqual(var.index, None)
        self.model.add(var)
        self.assertTrue(var in self.model.variables.values())
        self.assertEqual(self.model.variables.values().count(var), 1)
        self.assertEqual(var.index, glp_get_num_cols(self.model.problem))
        self.assertEqual(var.name, glp_get_col_name(self.model.problem, var.index))
        self.assertEqual(self.model.variables['x'].problem, var.problem)
        self.assertEqual(glp_get_col_kind(self.model.problem, var.index), GLP_CV)
        var = Variable('y', lb=-13)
        self.model.add(var)
        self.assertTrue(var in self.model.variables.values())
        self.assertEqual(var.name, glp_get_col_name(self.model.problem, var.index))
        self.assertEqual(glp_get_col_kind(self.model.problem, var.index), GLP_CV)
        self.assertEqual(self.model.variables['x'].lb, None)
        self.assertEqual(self.model.variables['x'].ub, None)
        self.assertEqual(self.model.variables['y'].lb, -13)
        self.assertEqual(self.model.variables['x'].ub, None)
        var = Variable('x_with_ridiculously_long_variable_name_asdffffffffasdfasdfasdfasdfasdfasdfasdf')
        self.model.add(var)
        self.assertTrue(var in self.model.variables.values())
        self.assertEqual(self.model.variables.values().count(var), 1)
        var = Variable('x_with_ridiculously_long_variable_name_asdffffffffasdfasdfasdfasdfasdfasdfasdf')
        self.model.add(var)
        # TODO: the following tests fail because transactions are not safe yet
        # self.assertRaises(Exception, self.model.update, var)
        # self.assertEqual(len(self.model.variables), glp_get_num_cols(self.model.problem))

    def test_add_integer_var(self):
        var = Variable('int_var', lb=-13, ub=500, type='integer')
        self.model.add(var)
        self.model.update()
        print(var.index, 1)
        self.assertEqual(self.model.variables['int_var'].type, 'integer')
        self.assertEqual(glp_get_col_kind(self.model.problem, var.index), GLP_IV)
        self.assertEqual(self.model.variables['int_var'].ub, 500)
        self.assertEqual(self.model.variables['int_var'].lb, -13)

    def test_add_non_cplex_conform_variable(self):
        var = Variable('12x!!@#5_3', lb=-666, ub=666)
        self.assertEqual(var.index, None)
        self.model.add(var)
        self.assertTrue(var in self.model.variables.values())
        self.assertEqual(var.name, glp_get_col_name(self.model.problem, var.index))
        self.assertEqual(self.model.variables['12x!!@#5_3'].lb, -666)
        self.assertEqual(self.model.variables['12x!!@#5_3'].ub, 666)
        repickled = pickle.loads(pickle.dumps(self.model))
        var_from_pickle = repickled.variables['12x!!@#5_3']
        self.assertEqual(var_from_pickle.name, glp_get_col_name(repickled.problem, var_from_pickle.index))

    def test_remove_variable(self):
        var = self.model.variables.values()[0]
        self.assertEqual(self.model.constraints['M_atp_c'].__str__(),
                         'M_atp_c: 0.0 <= -1.0*R_ACKr - 1.0*R_ADK1 + 1.0*R_ATPS4r - 1.0*R_PGK - 1.0*R_SUCOAS - 59.81*R_Biomass_Ecoli_core_w_GAM - 1.0*R_GLNS - 1.0*R_GLNabc - 1.0*R_PFK - 1.0*R_PPCK - 1.0*R_PPS + 1.0*R_PYK - 1.0*R_ATPM <= 0.0')
        self.assertEqual(var.problem, self.model)
        self.model.remove(var)
        self.model.update()
        self.assertEqual(self.model.constraints['M_atp_c'].__str__(),
                         'M_atp_c: 0.0 <= -1.0*R_ACKr - 1.0*R_ADK1 + 1.0*R_ATPS4r - 1.0*R_PGK - 1.0*R_SUCOAS - 1.0*R_GLNS - 1.0*R_GLNabc - 1.0*R_PFK - 1.0*R_PPCK - 1.0*R_PPS + 1.0*R_PYK - 1.0*R_ATPM <= 0.0')
        self.assertNotIn(var, self.model.variables.values())
        self.assertEqual(glp_find_col(self.model.problem, var.name), 0)
        self.assertEqual(var.problem, None)

    def test_remove_variable_str(self):
        var = self.model.variables.values()[0]
        self.model.remove(var.name)
        self.assertNotIn(var, self.model.variables.values())
        self.assertEqual(glp_find_col(self.model.problem, var.name), 0)
        self.assertEqual(var.problem, None)

    def test_add_constraints(self):
        x = Variable('x', lb=0, ub=1, type='binary')
        y = Variable('y', lb=-181133.3, ub=12000., type='continuous')
        z = Variable('z', lb=0., ub=10., type='integer')
        constr1 = Constraint(0.3 * x + 0.4 * y + 66. * z, lb=-100, ub=0., name='test')
        constr2 = Constraint(2.333 * x + y + 3.333, ub=100.33, name='test2')
        constr3 = Constraint(2.333 * x + y + z, lb=-300)
        constr4 = Constraint(x, lb=-300, ub=-300)
        constr5 = Constraint(3*x)
        self.model.add(constr1)
        self.model.add(constr2)
        self.model.add(constr3)
        self.model.add([constr4, constr5])
        self.assertIn(constr1.name, self.model.constraints)
        self.assertIn(constr2.name, self.model.constraints)
        self.assertIn(constr3.name, self.model.constraints)
        self.assertIn(constr4.name, self.model.constraints)
        self.assertIn(constr5.name, self.model.constraints)
        # constr1
        ia = intArray(glp_get_num_rows(self.model.problem) + 1)
        da = doubleArray(glp_get_num_rows(self.model.problem) + 1)
        nnz = glp_get_mat_row(self.model.problem, constr1.index, ia, da)
        coeff_dict = dict()
        for i in range(1, nnz+1):
            coeff_dict[glp_get_col_name(self.model.problem, ia[i])] = da[i]
        self.assertDictEqual(coeff_dict, {'x': 0.3, 'y': 0.4, 'z': 66.})
        self.assertEqual(glp_get_row_type(self.model.problem, constr1.index), GLP_DB)
        self.assertEqual(glp_get_row_lb(self.model.problem, constr1.index), -100)
        self.assertEqual(glp_get_row_ub(self.model.problem, constr1.index), 0)
        # constr2
        ia = intArray(glp_get_num_rows(self.model.problem) + 1)
        da = doubleArray(glp_get_num_rows(self.model.problem) + 1)
        nnz = glp_get_mat_row(self.model.problem, constr2.index, ia, da)
        coeff_dict = dict()
        for i in range(1, nnz+1):
            coeff_dict[glp_get_col_name(self.model.problem, ia[i])] = da[i]
        self.assertDictEqual(coeff_dict, {'x': 2.333, 'y': 1.})
        self.assertEqual(glp_get_row_type(self.model.problem, constr2.index), GLP_UP)
        self.assertEqual(glp_get_row_lb(self.model.problem, constr2.index), -1.7976931348623157e+308)
        self.assertEqual(glp_get_row_ub(self.model.problem, constr2.index), 96.997)
        # constr3
        ia = intArray(glp_get_num_rows(self.model.problem) + 1)
        da = doubleArray(glp_get_num_rows(self.model.problem) + 1)
        nnz = glp_get_mat_row(self.model.problem, constr3.index, ia, da)
        coeff_dict = dict()
        for i in range(1, nnz+1):
            coeff_dict[glp_get_col_name(self.model.problem, ia[i])] = da[i]
        self.assertDictEqual(coeff_dict, {'x': 2.333, 'y': 1., 'z': 1.})
        self.assertEqual(glp_get_row_type(self.model.problem, constr3.index), GLP_LO)
        self.assertEqual(glp_get_row_lb(self.model.problem, constr3.index), -300)
        self.assertEqual(glp_get_row_ub(self.model.problem, constr3.index), 1.7976931348623157e+308)
        # constr4
        ia = intArray(glp_get_num_rows(self.model.problem) + 1)
        da = doubleArray(glp_get_num_rows(self.model.problem) + 1)
        nnz = glp_get_mat_row(self.model.problem, constr4.index, ia, da)
        coeff_dict = dict()
        for i in range(1, nnz+1):
            coeff_dict[glp_get_col_name(self.model.problem, ia[i])] = da[i]
        self.assertDictEqual(coeff_dict, {'x': 1})
        self.assertEqual(glp_get_row_type(self.model.problem, constr4.index), GLP_FX)
        self.assertEqual(glp_get_row_lb(self.model.problem, constr4.index), -300)
        self.assertEqual(glp_get_row_ub(self.model.problem, constr4.index), -300)

        # constr5
        ia = intArray(glp_get_num_rows(self.model.problem) + 1)
        da = doubleArray(glp_get_num_rows(self.model.problem) + 1)
        nnz = glp_get_mat_row(self.model.problem, constr5.index, ia, da)
        coeff_dict = dict()
        for i in range(1, nnz+1):
            coeff_dict[glp_get_col_name(self.model.problem, ia[i])] = da[i]
        self.assertDictEqual(coeff_dict, {'x': 3})
        self.assertEqual(glp_get_row_type(self.model.problem, constr5.index), GLP_FR)
        self.assertLess(glp_get_row_lb(self.model.problem, constr5.index), -1e30)
        self.assertGreater(glp_get_row_ub(self.model.problem, constr5.index), 1e30)

    def test_remove_constraints(self):
        x = Variable('x', type='binary')
        y = Variable('y', lb=-181133.3, ub=12000., type='continuous')
        z = Variable('z', lb=3, ub=3, type='integer')
        constr1 = Constraint(0.3 * x + 0.4 * y + 66. * z, lb=-100, ub=0., name='test')
        self.assertEqual(constr1.problem, None)
        self.model.add(constr1)
        self.model.update()
        self.assertEqual(constr1.problem, self.model)
        self.assertIn(constr1.name, self.model.constraints)
        print(constr1.index)
        self.model.remove(constr1.name)
        self.model.update()
        self.assertEqual(constr1.problem, None)
        self.assertNotIn(constr1, self.model.constraints)

    def test_add_nonlinear_constraint_raises(self):
        x = Variable('x', type='binary')
        y = Variable('y', lb=-181133.3, ub=12000., type='continuous')
        z = Variable('z', lb=10, type='integer')
        self.assertRaises(ValueError, Constraint, 0.3 * x + 0.4 * y ** 2 + 66. * z, lb=-100, ub=0., name='test')

    def test_change_of_constraint_is_reflected_in_low_level_solver(self):
        x = Variable('x', lb=-83.3, ub=1324422.)
        y = Variable('y', lb=-181133.3, ub=12000.)
        constraint = Constraint(0.3 * x + 0.4 * y, lb=-100, name='test')
        self.assertEqual(constraint.index, None)
        self.model.add(constraint)
        self.assertEqual(self.model.constraints['test'].__str__(), 'test: -100 <= 0.4*y + 0.3*x')
        self.assertEqual(constraint.index, 73)
        z = Variable('z', lb=3, ub=10, type='integer')
        self.assertEqual(z.index, None)
        constraint += 77. * z
        self.assertEqual(z.index, 98)
        self.assertEqual(self.model.constraints['test'].__str__(), 'test: -100 <= 0.4*y + 0.3*x + 77.0*z')
        print(self.model)
        self.assertEqual(constraint.index, 73)

    def test_change_of_objective_is_reflected_in_low_level_solver(self):
        x = Variable('x', lb=-83.3, ub=1324422.)
        y = Variable('y', lb=-181133.3, ub=12000.)
        objective = Objective(0.3 * x + 0.4 * y, name='test', direction='max')
        self.model.objective = objective
        self.assertEqual(self.model.objective.__str__(), 'Maximize\n0.4*y + 0.3*x')
        self.assertEqual(glp_get_obj_coef(self.model.problem, x.index), 0.3)
        self.assertEqual(glp_get_obj_coef(self.model.problem, y.index), 0.4)
        for i in range(1, glp_get_num_cols(self.model.problem) + 1):
            if i != x.index and i != y.index:
                self.assertEqual(glp_get_obj_coef(self.model.problem, i), 0)
        z = Variable('z', lb=4, ub=4, type='integer')
        self.model.objective += 77. * z
        self.assertEqual(self.model.objective.__str__(), 'Maximize\n0.4*y + 0.3*x + 77.0*z')
        self.assertEqual(glp_get_obj_coef(self.model.problem, x.index), 0.3)
        self.assertEqual(glp_get_obj_coef(self.model.problem, y.index), 0.4)
        self.assertEqual(glp_get_obj_coef(self.model.problem, z.index), 77.)
        for i in range(1, glp_get_num_cols(self.model.problem) + 1):
            if i != x.index and i != y.index and i != z.index:
                self.assertEqual(glp_get_obj_coef(self.model.problem, i), 0)

    @unittest.skip('Skipping for now')
    def test_absolute_value_objective(self):
        # TODO: implement hack mentioned in http://www.aimms.com/aimms/download/manuals/aimms3om_linearprogrammingtricks.pdf

        objective = Objective(sum(abs(variable) for variable in six.itervalues(self.model.variables)), name='test',
                              direction='max')
        print(objective)
        self.assertTrue(False)

    def test_change_variable_bounds(self):
        inner_prob = self.model.problem
        inner_problem_bounds = [(glp_get_col_lb(inner_prob, i), glp_get_col_ub(inner_prob, i)) for i in
                                range(1, glp_get_num_cols(inner_prob) + 1)]
        bounds = [(var.lb, var.ub) for var in self.model.variables.values()]
        self.assertEqual(bounds, inner_problem_bounds)
        for var in self.model.variables.values():
            var.lb = random.uniform(-1000, 1000)
            var.ub = random.uniform(var.lb, 1000)
        inner_problem_bounds_new = [(glp_get_col_lb(inner_prob, i), glp_get_col_ub(inner_prob, i)) for i in
                                    range(1, glp_get_num_cols(inner_prob) + 1)]
        bounds_new = [(var.lb, var.ub) for var in self.model.variables.values()]
        self.assertNotEqual(bounds, bounds_new)
        self.assertNotEqual(inner_problem_bounds, inner_problem_bounds_new)
        self.assertEqual(bounds_new, inner_problem_bounds_new)

    def test_change_variable_type(self):
        for variable in self.model.variables:
            variable.type = 'integer'
        for i in range(1, glp_get_num_cols(self.model.problem) + 1):
            self.assertEqual(glp_get_col_kind(self.model.problem, i), GLP_IV)

    def test_change_constraint_bounds(self):
        inner_prob = self.model.problem
        inner_problem_bounds = [(glp_get_row_lb(inner_prob, i), glp_get_row_ub(inner_prob, i)) for i in
                                range(1, glp_get_num_rows(inner_prob) + 1)]
        bounds = [(constr.lb, constr.ub) for constr in self.model.constraints]
        self.assertEqual(bounds, inner_problem_bounds)
        for constr in self.model.constraints:
            constr.lb = random.uniform(-1000, constr.ub)
            constr.ub = random.uniform(constr.lb, 1000)
        inner_problem_bounds_new = [(glp_get_row_lb(inner_prob, i), glp_get_row_ub(inner_prob, i)) for i in
                                    range(1, glp_get_num_rows(inner_prob) + 1)]
        bounds_new = [(constr.lb, constr.ub) for constr in self.model.constraints]
        self.assertNotEqual(bounds, bounds_new)
        self.assertNotEqual(inner_problem_bounds, inner_problem_bounds_new)
        self.assertEqual(bounds_new, inner_problem_bounds_new)

    def test_initial_objective(self):
        self.assertEqual(self.model.objective.expression.__str__(), '1.0*R_Biomass_Ecoli_core_w_GAM')

    def test_optimize(self):
        self.model.optimize()
        self.assertEqual(self.model.status, 'optimal')
        self.assertAlmostEqual(self.model.objective.value, 0.8739215069684303)

    def test_optimize_milp(self):
        problem = glpk_read_cplex(TESTMILPMODELPATH)
        milp_model = Model(problem=problem)
        milp_model.optimize()
        self.assertEqual(milp_model.status, 'optimal')
        self.assertAlmostEqual(milp_model.objective.value, 122.5)
        for variable in milp_model.variables:
            if variable.type == 'integer':
                self.assertEqual(variable.primal % 1, 0)

    def test_change_objective(self):
        """Test that all different kinds of linear objective specification work."""
        print(self.model.variables.values()[0:2])
        v1, v2 = self.model.variables.values()[0:2]
        self.model.objective = Objective(1. * v1 + 1. * v2)
        self.assertEqual(self.model.objective.__str__(), 'Maximize\n1.0*R_PGK + 1.0*R_Biomass_Ecoli_core_w_GAM')
        self.model.objective = Objective(v1 + v2)
        self.assertEqual(self.model.objective.__str__(), 'Maximize\n1.0*R_PGK + 1.0*R_Biomass_Ecoli_core_w_GAM')

    def test_number_objective(self):
        self.model.objective = Objective(0.)
        self.assertEqual(self.model.objective.__str__(), 'Maximize\n0')
        obj_coeff = list()
        for i in range(1, glp_get_num_cols(self.model.problem) + 1):
            obj_coeff.append(glp_get_obj_coef(self.model.problem, i))
        self.assertEqual(set(obj_coeff), {0.})

    def test_raise_on_non_linear_objective(self):
        """Test that an exception is raised when a non-linear objective is added to the model."""
        v1, v2 = self.model.variables.values()[0:2]
        self.assertRaises(ValueError, Objective, v1*v2)

    def test_iadd_objective(self):
        v2, v3 = self.model.variables.values()[1:3]
        self.model.objective += 2. * v2 - 3. * v3
        obj_coeff = list()
        for i in range(len(self.model.variables)):
            obj_coeff.append(glp_get_obj_coef(self.model.problem, i))
        self.assertEqual(obj_coeff,
                         [0.0, 1.0, 2.0, -3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                          0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                          0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                          0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                          0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                          0.0]
        )

    def test_imul_objective(self):
        self.model.objective *= 2.
        obj_coeff = list()
        for i in range(len(self.model.variables)):
            obj_coeff.append(glp_get_obj_coef(self.model.problem, i))
        self.assertEqual(obj_coeff,
                         [0.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                          0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                          0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                          0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                          0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                          0.0]
        )

    def test_set_copied_objective(self):
        obj_copy = copy.copy(self.model.objective)
        self.model.objective = obj_copy
        self.assertEqual(self.model.objective.__str__(), 'Maximize\n1.0*R_Biomass_Ecoli_core_w_GAM')

    def test_timeout(self):
        self.model.configuration.timeout = 0
        status = self.model.optimize()
        self.assertEqual(status, 'time_limit')

    def test_set_linear_objective_term(self):
        self.model._set_linear_objective_term(self.model.variables.R_TPI, 666.)
        self.assertEqual(glp_get_obj_coef(self.model.problem, self.model.variables.R_TPI.index), 666.)

    def test_instantiating_model_with_non_glpk_problem_raises(self):
        self.assertRaises(TypeError, Model, problem='Chicken soup')

    def test__set_coefficients_low_level(self):
        constraint = self.model.constraints.M_atp_c
        constraint._set_coefficients_low_level({self.model.variables.R_Biomass_Ecoli_core_w_GAM: 666.})
        num_cols = glp_get_num_cols(self.model.problem)
        ia = intArray(num_cols + 1)
        da = doubleArray(num_cols + 1)
        index = constraint.index
        num = glp_get_mat_row(self.model.problem, index, ia, da)
        for i in range(1, num +1):
            col_name = glp_get_col_name(self.model.problem, ia[i])
            if col_name == 'R_Biomass_Ecoli_core_w_GAM':
                self.assertEqual(da[i], 666.)

    def test_primal_values(self):
            self.model.optimize()
            for k, v in self.model.primal_values.items():
                self.assertEquals(v, self.model.variables[k].primal)

    def test_reduced_costs(self):
        self.model.optimize()
        for k, v in self.model.reduced_costs.items():
            self.assertEquals(v, self.model.variables[k].dual)

    def test_dual_values(self):
        self.model.optimize()
        for k, v in self.model.dual_values.items():
            self.assertEquals(v, self.model.constraints[k].primal)

    def test_shadow_prices(self):
        self.model.optimize()
        for k, v in self.model.shadow_prices.items():
            self.assertEquals(v, self.model.constraints[k].dual)

    def test_clone_solver(self):
        self.assertEquals(self.model.configuration.verbosity, 0)
        self.model.configuration.verbosity = 3
        cloned_model = Model.clone(self.model)
        self.assertEquals(cloned_model.configuration.verbosity, 3)
        self.assertEquals(len(cloned_model.variables), len(self.model.variables))
        self.assertEquals(len(cloned_model.constraints), len(self.model.constraints))


if __name__ == '__main__':
    nose.runmodule()
