import unittest
import mcycle as mc
import CoolProp as CP


class TestHxUnitPlateCorrChevron(unittest.TestCase):
    hxUnit = mc.HxUnitPlate(
        flowConfig=mc.HxFlowConfig("counter", "1", True, True),
        NPlate=23,
        RfWf=0,
        RfSf=0,
        plate=mc.library.materials.stainlessSteel_316(573.15),
        tPlate=0.424e-3,
        geomWf=mc.GeomHxPlateCorrugatedChevron(1.096e-3, 60, 10e-3, 1.117),
        geomSf=mc.GeomHxPlateCorrugatedChevron(1.096e-3, 60, 10e-3, 1.117),
        L=269e-3,
        W=95e-3,
        ARatioWf=1,
        ARatioSf=1,
        ARatioPlate=1,
        effThermal=1.0,
        config=mc.Config())
    hxUnit.config.set_method("savostinTikhonov_sp",
                             ["GeomHxPlateCorrugatedChevron"], ["all"],
                             ["all"], ["sf"])

    def test_size_liq(self):
        flowInWf = mc.FlowState("R123", -1, 0.34307814292524513, CP.PT_INPUTS,
                                1000000., 300.57890653991495)
        flowOutWf = mc.FlowState("R123", -1, 0.34307814292524513, CP.PT_INPUTS,
                                 1000000., 305.79345550292123)
        flowInSf = mc.FlowState("Air", -1, 0.09, CP.PT_INPUTS, 111600.,
                                330.77794902610714)
        flowOutSf = mc.FlowState("Air", -1, 0.09, CP.PT_INPUTS, 111600.,
                                 310.57890653991586)
        self.hxUnit.update({
            'flowInWf': flowInWf,
            'flowInSf': flowInSf,
            'flowOutWf': flowOutWf,
            'flowOutSf': flowOutSf
        })

        self.hxUnit.update({'sizeAttr': 'L', 'sizeBounds': [0.005, 0.5]})
        self.hxUnit.sizeUnits('', [])
        self.assertAlmostEqual(
            abs(self.hxUnit.L - 0.0636564105282744) / 0.0636564105282744, 0, 4)
        self.hxUnit.update({'sizeAttr': 'W', 'sizeBounds': [50e-3, 500e-3]})
        self.hxUnit.sizeUnits('', [])
        self.assertAlmostEqual(self.hxUnit.W, 95e-3, 7)
        self.hxUnit.update({
            'sizeAttr': 'geomWf.b',
            'sizeBounds': [0.1e-3, 10e-3]
        })
        self.hxUnit.sizeUnits('', [])
        self.assertAlmostEqual(
            abs(self.hxUnit.geomWf.b - 1.096e-3) / 1.096e-3, 0, 2)
        #
        self.assertAlmostEqual(
            abs(self.hxUnit._dpFWf() - 7200.2135758720115) /
            7200.2135758720115, 0, 2)

    def test_size_tp(self):
        flowInWf = mc.FlowState("R123", -1, 0.34307814292524513, CP.PQ_INPUTS,
                                1000000., 0.4)
        flowOutWf = mc.FlowState("R123", -1, 0.34307814292524513, CP.PQ_INPUTS,
                                 1000000., 0.5)
        flowInSf = mc.FlowState("Air", -1, 0.09, CP.PT_INPUTS, 111600.,
                                868.7758979999346)
        flowOutSf = mc.FlowState("Air", -1, 0.09, CP.PT_INPUTS, 111600.,
                                 825.2114243937383)
        self.hxUnit.update({
            'flowInWf': flowInWf,
            'flowInSf': flowInSf,
            'flowOutWf': flowOutWf,
            'flowOutSf': flowOutSf
        })
        #
        self.hxUnit.update({'sizeAttr': 'L', 'sizeBounds': [0.001, 0.5]})
        self.hxUnit.sizeUnits('', [])
        self.assertAlmostEqual(
            abs(self.hxUnit.L - 0.003778819723856917) / 0.003778819723856917,
            0, 4)
        #
        self.assertAlmostEqual(
            abs(self.hxUnit._dpFWf() - 722.9638885277705) / 722.9638885277705,
            0, 2)

    def test_size_vap(self):
        flowInWf = mc.FlowState("R123", -1, 0.34307814292524513, CP.PT_INPUTS,
                                1000000., 409.2350351214396)
        flowOutWf = mc.FlowState("R123", -1, 0.34307814292524513, CP.PT_INPUTS,
                                 1000000., 414.3019814953263)
        flowInSf = mc.FlowState("Air", -1, 0.09, CP.PT_INPUTS, 111600., 1170.)
        flowOutSf = mc.FlowState("Air", -1, 0.09, CP.PT_INPUTS, 111600.,
                                 1155.3292007981324)
        self.hxUnit.update({
            'flowInWf': flowInWf,
            'flowInSf': flowInSf,
            'flowOutWf': flowOutWf,
            'flowOutSf': flowOutSf
        })
        #
        self.hxUnit.update({'sizeAttr': 'L', 'sizeBounds': [0.0001, 0.5]})
        self.hxUnit.sizeUnits('', [])
        self.assertAlmostEqual(
            abs(self.hxUnit.L - 0.0009979724829425561) / 0.0009979724829425561,
            0, 4)
        #
        self.assertAlmostEqual(
            abs(self.hxUnit._dpFWf() - 1363.6424738901792) /
            1363.6424738901792, 0, 2)


if __name__ == "__main__":
    unittest.main()
